package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.StringArgumentType;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;

/**
 * /fusion ability <pokemon uuid> head|body   pick the fusion's ability (the clickable choice after fusing runs this)
 * /fusion info                               the fusions in your party: head, body, base stats, types
 * /fusion selftest                           (ops) fuse, reverse and unfuse a Bulbasaur and a Charmander in a scratch
 *                                            party and report what came out (for testing a server install)
 */
public final class FusionCommand {
    private FusionCommand() {
    }

    static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> register(dispatcher));
    }

    private static Pokemon find(ServerPlayer player, String uuid) {
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        UUID id;
        try {
            id = UUID.fromString(uuid);
        } catch (IllegalArgumentException e) {
            return null;
        }
        for (int i = 0; i < 6; i++) {
            Pokemon p = party.get(i);
            if (p != null && p.getUuid().equals(id)) return p;
        }
        return null;
    }

    private static int ability(CommandSourceStack src, String uuid, String which) {
        ServerPlayer player = src.getPlayer();
        if (player == null) return 0;
        Pokemon fused = find(player, uuid);
        if (fused == null || !FusionRules.isFused(fused)) {
            src.sendFailure(Component.translatable("cobbleeffort_fusion.error.not_fused"));
            return 0;
        }
        CompoundTag data = Fusing.data(fused);
        String name = data.getString(which.equals("head") ? "head_ability" : "body_ability");
        if (!Fusing.setAbility(fused, name)) {
            src.sendFailure(Component.translatable("cobbleeffort_fusion.error.ability"));
            return 0;
        }
        src.sendSuccess(() -> Component.translatable("cobbleeffort_fusion.ability_set", fused.getDisplayName(false),
                Component.translatable(fused.getAbility().getDisplayName())), false);
        return 1;
    }

    private static int info(CommandSourceStack src) {
        ServerPlayer player = src.getPlayer();
        if (player == null) return 0;
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        int n = 0;
        for (int i = 0; i < 6; i++) {
            Pokemon p = party.get(i);
            if (p == null || !FusionRules.isFused(p)) continue;
            FormData head = FusionRules.headForm(p);
            if (head == null) continue;
            Map<Stats, Integer> base = FusionRules.fusedBaseStats(head, p.getForm());
            MutableComponent types = Component.empty();
            for (ElementalType t : FusionRules.fusedTypes(head, p.getForm())) {
                if (!types.getSiblings().isEmpty()) types.append("/");
                types.append(t.getDisplayName());
            }
            MutableComponent line = Component.translatable("cobbleeffort_fusion.info", p.getDisplayName(false),
                    head.getSpecies().getTranslatedName(), p.getSpecies().getTranslatedName(), types,
                    base.get(Stats.HP) + "/" + base.get(Stats.ATTACK) + "/" + base.get(Stats.DEFENCE) + "/"
                            + base.get(Stats.SPECIAL_ATTACK) + "/" + base.get(Stats.SPECIAL_DEFENCE) + "/" + base.get(Stats.SPEED));
            src.sendSuccess(() -> line.withStyle(ChatFormatting.LIGHT_PURPLE), false);
            n++;
        }
        if (n == 0) src.sendSuccess(() -> Component.translatable("cobbleeffort_fusion.info.none"), false);
        return n;
    }

    private static String describe(Pokemon p) {
        StringBuilder types = new StringBuilder();
        for (ElementalType t : p.getTypes()) types.append(types.length() == 0 ? "" : "/").append(t.getName());
        return p.getSpecies().getName() + " \"" + p.getDisplayName(false).getString() + "\" lv" + p.getLevel() + " " + types
                + " hp " + p.getCurrentHealth() + "/" + p.getMaxHealth() + " atk " + p.getStat(Stats.ATTACK) + " spa "
                + p.getStat(Stats.SPECIAL_ATTACK) + " spe " + p.getStat(Stats.SPEED) + " ability " + p.getAbility().getName()
                + " aspects " + p.getAspects();
    }

    private static int selftest(CommandSourceStack src) {
        java.util.function.Consumer<String> say = msg -> {
            Fusion.LOG.info("[selftest] {}", msg);
            src.sendSuccess(() -> Component.literal(msg), false);
        };
        try {
            UUID owner = UUID.randomUUID();
            PlayerPartyStore party = new PlayerPartyStore(owner);
            com.cobblemon.mod.common.api.storage.pc.PCStore pc = new com.cobblemon.mod.common.api.storage.pc.PCStore(owner);
            Pokemon bulbasaur = com.cobblemon.mod.common.api.pokemon.PokemonProperties.Companion.parse("bulbasaur level=20").create();
            Pokemon charmander = com.cobblemon.mod.common.api.pokemon.PokemonProperties.Companion.parse("charmander level=30").create();
            party.add(bulbasaur);
            party.add(charmander);
            say.accept("before: " + describe(bulbasaur) + " | " + describe(charmander));
            Component err = Fusing.fuse(party, src.registryAccess(), null, bulbasaur, charmander, Fusing.LevelRule.AVERAGE);
            if (err != null) throw new IllegalStateException("fuse: " + err.getString());
            say.accept("fused (head Bulbasaur, body Charmander): " + describe(charmander) + " party " + party.occupied());
            FusionEngine.probe(msg -> Fusion.LOG.info("[selftest] {}", msg));
            err = Fusing.reverse(party, src.registryAccess(), null, charmander);
            if (err != null) throw new IllegalStateException("reverse: " + err.getString());
            Pokemon reversed = null;
            for (int i = 0; i < 6 && reversed == null; i++) reversed = party.get(i);
            say.accept("reversed: " + describe(reversed) + " party " + party.occupied());
            err = Fusing.unfuse(party, pc, src.registryAccess(), null, reversed);
            if (err != null) throw new IllegalStateException("unfuse: " + err.getString());
            StringBuilder out = new StringBuilder("unfused:");
            for (int i = 0; i < 6; i++) if (party.get(i) != null) out.append(" | ").append(describe(party.get(i)));
            say.accept(out.toString());
            say.accept("selftest OK");
            return 1;
        } catch (Throwable t) {
            Fusion.LOG.error("[selftest] failed", t);
            src.sendFailure(Component.literal("selftest FAILED: " + t));
            return 0;
        }
    }

    private static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(Commands.literal("fusion")
                .then(Commands.literal("selftest").requires(s -> s.hasPermission(2)).executes(ctx -> selftest(ctx.getSource())))
                .then(Commands.literal("info").executes(ctx -> info(ctx.getSource())))
                .then(Commands.literal("ability").then(Commands.argument("pokemon", StringArgumentType.word())
                        .then(Commands.literal("head").executes(ctx -> ability(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon"), "head")))
                        .then(Commands.literal("body").executes(ctx -> ability(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon"), "body"))))));
    }
}
