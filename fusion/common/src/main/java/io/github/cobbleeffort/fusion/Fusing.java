package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.abilities.Abilities;
import com.cobblemon.mod.common.api.abilities.AbilityTemplate;
import com.cobblemon.mod.common.api.moves.BenchedMove;
import com.cobblemon.mod.common.api.moves.Move;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.api.storage.pc.PCStore;
import com.cobblemon.mod.common.pokemon.Pokemon;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.HoverEvent;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;

/**
 * Fusing, unfusing and reversing (swapping head and body), Infinite Fusion's way.
 *
 * The fused Pokémon is the BODY's Pokémon object (its party slot, identity, nature, IVs, EVs); the HEAD leaves the
 * party and is saved whole in the body's persistent data under "cobbleeffort_fusion", together with what the body
 * had before (its nickname and ability), so unfusing gives both Pokémon back.
 * Level: DNA Splicers and Infinite Splicers take the average of the two levels, Super Splicers the higher one; on
 * unfusing both Pokémon come back at the fusion's level. Ability: the body's to start with; the player can switch to
 * the head's (a clickable choice in chat, /fusion ability). Moves: the fusion keeps the body's moves, and the head's
 * moves are added to the moves it can relearn (Cobblemon's benched moves), so either set can be used.
 */
public final class Fusing {
    public static final String KEY = "cobbleeffort_fusion";

    private Fusing() {
    }

    public enum LevelRule { AVERAGE, HIGHER }

    public static CompoundTag data(Pokemon pokemon) {
        return pokemon.getPersistentData().getCompound(KEY);
    }

    /** Fuse: head leaves the party and becomes part of body. Returns an error message, or null when it worked. */
    public static Component fuse(ServerPlayer player, Pokemon head, Pokemon body, LevelRule rule) {
        return fuse(Cobblemon.INSTANCE.getStorage().getParty(player), player.registryAccess(), player, head, body, rule);
    }

    public static Component fuse(PlayerPartyStore party, net.minecraft.core.RegistryAccess access, ServerPlayer player,
                                 Pokemon head, Pokemon body, LevelRule rule) {
        if (head == body) return Component.translatable("cobbleeffort_fusion.error.same");
        if (FusionRules.isFused(head) || FusionRules.isFused(body)) return Component.translatable("cobbleeffort_fusion.error.already");
        int fusedLevel = rule == LevelRule.HIGHER ? Math.max(head.getLevel(), body.getLevel())
                : Math.max(1, (head.getLevel() + body.getLevel()) / 2);
        double hpFraction = body.getMaxHealth() > 0 ? body.getCurrentHealth() / (double) body.getMaxHealth() : 1.0;

        CompoundTag data = new CompoundTag();
        data.put("head", head.saveToNBT(access, new CompoundTag()));
        data.putString("body_ability", body.getAbility().getName());
        data.putString("head_ability", head.getAbility().getName());
        if (body.getNickname() != null) data.putString("body_nickname", Component.Serializer.toJson(body.getNickname(), access));
        if (!party.remove(head)) return Component.translatable("cobbleeffort_fusion.error.party");

        body.getPersistentData().put(KEY, data);
        Set<String> aspects = new HashSet<>(FusionRules.withoutFusion(body.getForcedAspects()));
        aspects.addAll(FusionRules.aspectsFor(head));
        body.setForcedAspects(aspects);
        body.updateAspects();
        body.setLevel(fusedLevel);
        for (Move move : head.getMoveSet().getMoves()) {
            body.getBenchedMoves().add(new BenchedMove(move.getTemplate(), move.getRaisedPpStages()));
        }
        if (body.getNickname() == null) body.setNickname(Component.literal(fusionName(head, body)));
        body.setCurrentHealth(Math.max(1, (int) Math.round(hpFraction * body.getMaxHealth())));
        FusionEngine.register(body);
        if (player != null) offerAbilityChoice(player, body);
        return null;
    }

    /** Unfuse: the head comes back (to the party, or the PC when the party is full). */
    public static Component unfuse(ServerPlayer player, Pokemon fused) {
        return unfuse(Cobblemon.INSTANCE.getStorage().getParty(player), Cobblemon.INSTANCE.getStorage().getPC(player),
                player.registryAccess(), player, fused);
    }

    public static Component unfuse(PlayerPartyStore party, PCStore pc, net.minecraft.core.RegistryAccess access, ServerPlayer player,
                                   Pokemon fused) {
        if (!FusionRules.isFused(fused)) return Component.translatable("cobbleeffort_fusion.error.not_fused");
        CompoundTag data = data(fused);
        if (!data.contains("head")) return Component.translatable("cobbleeffort_fusion.error.no_head");
        Pokemon head;
        try {
            head = Pokemon.Companion.loadFromNBT(access, data.getCompound("head"));
        } catch (Exception e) {
            Fusion.LOG.error("Couldn't load the head of {}", fused.getUuid(), e);
            return Component.translatable("cobbleeffort_fusion.error.no_head");
        }
        int level = fused.getLevel();
        restoreBody(access, fused, data);
        head.setLevel(level);
        head.heal();
        if (!party.add(head)) {
            pc.add(head);
            if (player != null) player.sendSystemMessage(Component.translatable("cobbleeffort_fusion.unfused_pc", head.getDisplayName(false)));
        }
        return null;
    }

    /** Reverse: swap head and body (same two Pokémon, the other way round), keeping the fusion's level and moves. */
    public static Component reverse(ServerPlayer player, Pokemon fused) {
        return reverse(Cobblemon.INSTANCE.getStorage().getParty(player), player.registryAccess(), player, fused);
    }

    public static Component reverse(PlayerPartyStore party, net.minecraft.core.RegistryAccess access, ServerPlayer player, Pokemon fused) {
        if (!FusionRules.isFused(fused)) return Component.translatable("cobbleeffort_fusion.error.not_fused");
        CompoundTag data = data(fused);
        Pokemon head;
        try {
            head = Pokemon.Companion.loadFromNBT(access, data.getCompound("head"));
        } catch (Exception e) {
            return Component.translatable("cobbleeffort_fusion.error.no_head");
        }
        int slot = -1;
        for (int i = 0; i < 6; i++) if (party.get(i) == fused) slot = i;
        if (slot < 0) return Component.translatable("cobbleeffort_fusion.error.party");
        int level = fused.getLevel();
        double hpFraction = fused.getMaxHealth() > 0 ? fused.getCurrentHealth() / (double) fused.getMaxHealth() : 1.0;
        boolean autoName = isAutoName(fused);
        java.util.List<Move> moves = new java.util.ArrayList<>(fused.getMoveSet().getMoves());
        restoreBody(access, fused, data);
        fused.setLevel(level);

        // the old head is the new body: put it in the old body's place, then fuse the old body onto it as the head
        party.set(slot, head);
        head.setLevel(level);
        CompoundTag newData = new CompoundTag();
        newData.put("head", fused.saveToNBT(access, new CompoundTag()));
        newData.putString("body_ability", head.getAbility().getName());
        newData.putString("head_ability", fused.getAbility().getName());
        if (head.getNickname() != null) newData.putString("body_nickname", Component.Serializer.toJson(head.getNickname(), access));
        head.getPersistentData().put(KEY, newData);
        Set<String> aspects = new HashSet<>(FusionRules.withoutFusion(head.getForcedAspects()));
        aspects.addAll(FusionRules.aspectsFor(fused));
        head.setForcedAspects(aspects);
        head.updateAspects();
        head.getMoveSet().clear();
        for (int i = 0; i < moves.size() && i < 4; i++) head.getMoveSet().setMove(i, moves.get(i));
        for (Move move : fused.getMoveSet().getMoves()) {
            head.getBenchedMoves().add(new BenchedMove(move.getTemplate(), move.getRaisedPpStages()));
        }
        if (head.getNickname() == null || autoName) head.setNickname(Component.literal(fusionName(fused, head)));
        head.setCurrentHealth(Math.max(1, (int) Math.round(hpFraction * head.getMaxHealth())));
        FusionEngine.unregister(fused);
        FusionEngine.register(head);
        if (player != null) offerAbilityChoice(player, head);
        return null;
    }

    /** Put the body back the way it was before fusing (aspects, ability, nickname) and drop the stored head. */
    private static void restoreBody(net.minecraft.core.RegistryAccess access, Pokemon body, CompoundTag data) {
        boolean autoName = isAutoName(body);
        double hpFraction = body.getMaxHealth() > 0 ? body.getCurrentHealth() / (double) body.getMaxHealth() : 1.0;
        body.setForcedAspects(FusionRules.withoutFusion(body.getForcedAspects()));
        body.updateAspects();
        body.getPersistentData().remove(KEY);
        setAbility(body, data.getString("body_ability"));
        if (data.contains("body_nickname")) {
            body.setNickname(Component.Serializer.fromJson(data.getString("body_nickname"), access));
        } else if (autoName) {
            body.setNickname(null);
        }
        FusionEngine.unregister(body);
        body.setCurrentHealth(Math.max(body.getCurrentHealth() > 0 ? 1 : 0, (int) Math.round(hpFraction * body.getMaxHealth())));
    }

    /** The fusion's name: Infinite Fusion style (head's first part + body's last part). */
    public static String fusionName(Pokemon head, Pokemon body) {
        return FusionRules.fusedName(head.getSpecies().getTranslatedName().getString(), body.getSpecies().getTranslatedName().getString());
    }

    /** Whether the fusion still has the name we gave it (not one the player chose). */
    private static boolean isAutoName(Pokemon fused) {
        CompoundTag data = data(fused);
        if (data.contains("body_nickname")) return false;
        return fused.getNickname() != null;
    }

    public static boolean setAbility(Pokemon pokemon, String name) {
        if (name == null || name.isEmpty()) return false;
        AbilityTemplate template = Abilities.INSTANCE.get(name);
        if (template == null) return false;
        pokemon.updateAbility(template.create(true, com.cobblemon.mod.common.api.Priority.LOWEST));
        return true;
    }

    /** A clickable chat line to keep the body's ability or take the head's. */
    public static void offerAbilityChoice(ServerPlayer player, Pokemon fused) {
        CompoundTag data = data(fused);
        String body = data.getString("body_ability");
        String head = data.getString("head_ability");
        MutableComponent line = Component.translatable("cobbleeffort_fusion.fused", fused.getDisplayName(false)).withStyle(ChatFormatting.LIGHT_PURPLE);
        player.sendSystemMessage(line);
        if (head.isEmpty() || head.equals(body)) return;
        player.sendSystemMessage(Component.translatable("cobbleeffort_fusion.ability_choice")
                .append(button(abilityName(body), fused, "body"))
                .append(Component.literal(" "))
                .append(button(abilityName(head), fused, "head")));
    }

    private static Component abilityName(String id) {
        AbilityTemplate t = Abilities.INSTANCE.get(id);
        return t == null ? Component.literal(id) : Component.translatable(t.getDisplayName());
    }

    private static MutableComponent button(Component label, Pokemon fused, String which) {
        String cmd = "/fusion ability " + fused.getUuid() + " " + which;
        return Component.literal("[").append(label).append("]").withStyle(s -> s.withColor(ChatFormatting.AQUA)
                .withClickEvent(new ClickEvent(ClickEvent.Action.RUN_COMMAND, cmd))
                .withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, Component.translatable("cobbleeffort_fusion.ability_" + which))));
    }
}
