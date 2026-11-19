package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.stats.SidemodEvSource;
import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.phys.AABB;

import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * The training gym's timing game. Using a training block starts it: a marker sweeps back and forth along a bar on the
 * action bar; use the block again while the marker is in the green zone. The partner trained is your sent-out Pokémon
 * nearest the block, else the first healthy one in your party. Perfect (the zone's middle) = 8 EVs, good = 4, a miss = 1.
 */
public final class Training {
    /** One kind of training block: the stat it trains, the sweep period (ticks) and the zone's width (share of the bar). */
    public enum Kind {
        PUNCHING_BAG(Stats.ATTACK, 34, 0.22F, SoundEvents.PLAYER_ATTACK_STRONG),
        TREADMILL(Stats.SPEED, 22, 0.26F, SoundEvents.ARMOR_EQUIP_LEATHER.value()),
        WATERFALL(Stats.DEFENCE, 40, 0.22F, SoundEvents.GENERIC_SPLASH),
        MEDITATION_MAT(Stats.SPECIAL_DEFENCE, 52, 0.16F, SoundEvents.AMETHYST_BLOCK_RESONATE),
        TARGET_DUMMY(Stats.SPECIAL_ATTACK, 30, 0.18F, SoundEvents.ARROW_HIT_PLAYER);

        final Stat stat;
        final int period;
        final float zone;
        final SoundEvent sound;

        Kind(Stat stat, int period, float zone, SoundEvent sound) {
            this.stat = stat;
            this.period = period;
            this.zone = zone;
            this.sound = sound;
        }

        public String id() {
            return name().toLowerCase(java.util.Locale.ROOT);
        }
    }

    static final int PERFECT_EVS = 8, GOOD_EVS = 4, MISS_EVS = 1;
    static final int BAR = 25;
    /** Sweeps before a round times out. */
    static final int SWEEPS = 3;

    private record Session(BlockPos pos, Kind kind, long start, float centre, UUID partner) {
    }

    private static final Map<UUID, Session> SESSIONS = new HashMap<>();
    private static final Map<UUID, Long> COOLDOWN = new HashMap<>();

    private Training() {
    }

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            if (SESSIONS.isEmpty()) return;
            long now = server.overworld().getGameTime();
            SESSIONS.entrySet().removeIf(e -> {
                ServerPlayer p = server.getPlayerList().getPlayer(e.getKey());
                Session s = e.getValue();
                if (p == null || p.blockPosition().distSqr(s.pos()) > 64) return true;
                long t = now - s.start();
                if (t > (long) s.kind().period * SWEEPS) {
                    p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".training.timeout").withStyle(ChatFormatting.GRAY), true);
                    return true;
                }
                if (t % 2 == 0) p.displayClientMessage(bar(s, marker(s, t)), true);
                return false;
            });
        });
    }

    /** Marker position 0..1 at t ticks into the round (ping-pong). */
    static float marker(Session s, long t) {
        float u = (t % s.kind().period) / (float) s.kind().period;
        return u < 0.5F ? u * 2 : 2 - u * 2;
    }

    static MutableComponent bar(Session s, float m) {
        MutableComponent c = Component.literal("[").withStyle(ChatFormatting.DARK_GRAY);
        int at = Math.round(m * (BAR - 1));
        for (int i = 0; i < BAR; i++) {
            float x = i / (float) (BAR - 1);
            float d = Math.abs(x - s.centre());
            boolean zone = d <= s.kind().zone / 2, perfect = d <= s.kind().zone / 6;
            ChatFormatting colour = i == at ? ChatFormatting.WHITE : perfect ? ChatFormatting.GOLD : zone ? ChatFormatting.GREEN : ChatFormatting.DARK_GRAY;
            c.append(Component.literal(i == at ? "◆" : "|").withStyle(colour));
        }
        return c.append(Component.literal("]").withStyle(ChatFormatting.DARK_GRAY));
    }

    static void press(ServerPlayer player, BlockPos pos, Kind kind) {
        long now = player.serverLevel().getServer().overworld().getGameTime();
        Session s = SESSIONS.get(player.getUUID());
        if (s != null && s.pos().equals(pos)) {
            SESSIONS.remove(player.getUUID());
            finish(player, s, marker(s, now - s.start()));
            COOLDOWN.put(player.getUUID(), now + 10);
            return;
        }
        Long cd = COOLDOWN.get(player.getUUID());
        if (cd != null && now < cd) return;
        if (BattleRegistry.getBattleByParticipatingPlayer(player) != null) return;
        Pokemon partner = partner(player, pos);
        if (partner == null) {
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".training.no_partner"), true);
            return;
        }
        float centre = kind.zone / 2 + 0.05F + player.getRandom().nextFloat() * (0.9F - kind.zone);
        SESSIONS.put(player.getUUID(), new Session(pos, kind, now, centre, partner.getUuid()));
        player.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".training.start", partner.getDisplayName(false),
                Component.translatable(Digital.MOD_ID + ".training." + kind.id()), kind.stat.getDisplayName()).withStyle(ChatFormatting.YELLOW));
    }

    private static void finish(ServerPlayer player, Session s, float m) {
        Pokemon partner = null;
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            if (p.getUuid().equals(s.partner())) partner = p;
        }
        if (partner == null) return;
        float d = Math.abs(m - s.centre());
        String grade = d <= s.kind().zone / 6 ? "perfect" : d <= s.kind().zone / 2 ? "good" : "miss";
        int evs = switch (grade) {
            case "perfect" -> PERFECT_EVS;
            case "good" -> GOOD_EVS;
            default -> MISS_EVS;
        };
        int got = partner.getEvs().add(s.kind().stat, evs, new SidemodEvSource(Digital.MOD_ID, partner));
        if (!"miss".equals(grade)) {
            partner.incrementFriendship(1, true);
            Crests.trained(player);
        }
        ServerLevel level = player.serverLevel();
        level.playSound(null, s.pos(), s.kind().sound, SoundSource.BLOCKS, 0.8F, "perfect".equals(grade) ? 1.4F : 1F);
        if (!"miss".equals(grade)) {
            level.sendParticles("perfect".equals(grade) ? ParticleTypes.TOTEM_OF_UNDYING : ParticleTypes.CRIT,
                    s.pos().getX() + 0.5, s.pos().getY() + 1.1, s.pos().getZ() + 0.5, 14, 0.3, 0.3, 0.3, 0.1);
        }
        ChatFormatting colour = "perfect".equals(grade) ? ChatFormatting.GOLD : "good".equals(grade) ? ChatFormatting.GREEN : ChatFormatting.RED;
        Component msg = got > 0
                ? Component.translatable(Digital.MOD_ID + ".training." + grade, partner.getDisplayName(false), got, s.kind().stat.getDisplayName())
                : Component.translatable(Digital.MOD_ID + ".training.maxed", partner.getDisplayName(false), s.kind().stat.getDisplayName());
        player.displayClientMessage(msg.copy().withStyle(colour), true);
    }

    /** Your sent-out Pokémon nearest the block (16 blocks), else the first healthy one in the party. */
    static Pokemon partner(ServerPlayer player, BlockPos pos) {
        List<PokemonEntity> near = player.serverLevel().getEntitiesOfClass(PokemonEntity.class, new AABB(pos).inflate(16),
                e -> player.getUUID().equals(e.getPokemon().getOwnerUUID()) && !e.isBattling());
        if (!near.isEmpty()) {
            return near.stream().min(Comparator.comparingDouble(e -> e.distanceToSqr(pos.getCenter()))).get().getPokemon();
        }
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            if (!p.isFainted()) return p;
        }
        return null;
    }
}
