package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * The Digital World (dimension cobbleeffort_digital:digital_world: File Island's wireframe plains and voxel forests,
 * the Server Continent's circuit flats and plug-in socket cliffs, the Dark Area). The way in: an Ancient Terminal used
 * with a Digivice (they stand in Abandoned Server Terminals, or craft one), or a Digital Rift, a tear that opens near
 * players now and then for a few minutes (walk into it). Into the Digital World: the same x/z on the surface, on a
 * small pad with a terminal for the way home (built once); home: where you left from. Its data streams (any water
 * there) refill a Digivice's Tamer Energy and heal your sent-out Pokémon.
 */
public final class DigitalWorld {
    public static final ResourceKey<Level> DIMENSION =
            ResourceKey.create(Registries.DIMENSION, ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "digital_world"));
    /** A rift opens near a random player about once in this many ticks (on average): 40 minutes. */
    static final int RIFT_CHANCE = 48000;
    static final int RIFT_TICKS = 20 * 180;
    static final DustParticleOptions CYAN = new DustParticleOptions(new Vector3f(0.25F, 0.9F, 1F), 1.4F);

    record Rift(ResourceKey<Level> level, Vec3 at, long until) {
    }

    static final List<Rift> RIFTS = new ArrayList<>();

    private DigitalWorld() {
    }

    public static boolean inDigitalWorld(Level level) {
        return level.dimension() == DIMENSION;
    }

    // --- travel -----------------------------------------------------------------------------------------------------

    public static void travel(ServerPlayer player) {
        try {
            MinecraftServer server = player.server;
            if (player.level().dimension() == DIMENSION) {
                Returns returns = returns(server);
                CompoundTag back = returns.positions.getCompound(player.getStringUUID());
                ServerLevel to = back.contains("dim") ? levelOf(server, back.getString("dim")) : null;
                if (to == null || to == player.level()) to = server.overworld();
                BlockPos pos = back.contains("x") && to.dimension().location().toString().equals(back.getString("dim"))
                        ? new BlockPos(back.getInt("x"), back.getInt("y"), back.getInt("z")) : to.getSharedSpawnPos();
                effects(player);
                player.teleportTo(to, pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, player.getYRot(), player.getXRot());
                effects(player);
                return;
            }
            ServerLevel dest = server.getLevel(DIMENSION);
            if (dest == null) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".world.missing"), true);
                return;
            }
            CompoundTag here = new CompoundTag();
            here.putString("dim", player.level().dimension().location().toString());
            here.putInt("x", player.getBlockX());
            here.putInt("y", player.getBlockY());
            here.putInt("z", player.getBlockZ());
            Returns returns = returns(server);
            returns.positions.put(player.getStringUUID(), here);
            returns.setDirty();
            int x = player.getBlockX(), z = player.getBlockZ();
            dest.getChunk(x >> 4, z >> 4);
            int y = Math.max(dest.getMinBuildHeight() + 2, dest.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z));
            if (!dest.getFluidState(new BlockPos(x, y - 1, z)).isEmpty()) y += 1;
            BlockPos arrival = new BlockPos(x, y, z);
            arrivalPad(dest, arrival);
            effects(player);
            player.teleportTo(dest, x + 0.5, y, z + 0.5, player.getYRot(), player.getXRot());
            effects(player);
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".world.arrived").withStyle(ChatFormatting.AQUA), true);
        } catch (Throwable t) {
            Digital.LOG.error("Travelling to the Digital World failed", t);
        }
    }

    private static ServerLevel levelOf(MinecraftServer server, String dim) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dim)) return level;
        }
        return null;
    }

    /** A 5x5 circuit pad, room to stand, and an Ancient Terminal two blocks north (unless one is already near). */
    private static void arrivalPad(ServerLevel level, BlockPos at) {
        for (BlockPos p : BlockPos.betweenClosed(at.offset(-6, -3, -6), at.offset(6, 3, 6))) {
            if (level.getBlockState(p).is(Digital.TERMINAL.get())) return;
        }
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                boolean edge = Math.abs(dx) == 2 || Math.abs(dz) == 2;
                level.setBlock(at.offset(dx, -1, dz), edge ? Digital.SERVER_CASING.get().defaultBlockState()
                        : Digital.CIRCUIT_BLOCK.get().defaultBlockState(), 3);
                for (int dy = 0; dy < 4; dy++) level.setBlock(at.offset(dx, dy, dz), Blocks.AIR.defaultBlockState(), 3);
            }
        }
        level.setBlock(at.offset(0, 0, -2), Digital.TERMINAL.get().defaultBlockState(), 3);
    }

    static void effects(ServerPlayer player) {
        if (player.level() instanceof ServerLevel level) {
            level.sendParticles(CYAN, player.getX(), player.getY() + 1, player.getZ(), 80, 0.4, 0.9, 0.4, 0.02);
            level.sendParticles(ParticleTypes.ELECTRIC_SPARK, player.getX(), player.getY() + 1, player.getZ(), 30, 0.4, 0.9, 0.4, 0.2);
            level.playSound(null, player.blockPosition(), SoundEvents.BEACON_POWER_SELECT, SoundSource.PLAYERS, 0.6F, 1.8F);
        }
    }

    // --- rifts and data streams ---------------------------------------------------------------------------------------

    /** Opens a rift a little way from the player (also used by raids and /digital rift). */
    static Vec3 openRift(ServerPlayer player) {
        ServerLevel level = player.serverLevel();
        RandomSource r = level.getRandom();
        double a = r.nextDouble() * Math.PI * 2, d = 8 + r.nextDouble() * 8;
        int x = (int) (player.getX() + Math.cos(a) * d), z = (int) (player.getZ() + Math.sin(a) * d);
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        Vec3 at = new Vec3(x + 0.5, y + 1.2, z + 0.5);
        synchronized (RIFTS) {
            RIFTS.add(new Rift(level.dimension(), at, level.getGameTime() + RIFT_TICKS));
        }
        level.playSound(null, BlockPos.containing(at), SoundEvents.END_PORTAL_SPAWN, SoundSource.AMBIENT, 0.5F, 1.6F);
        player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".world.rift_opened").withStyle(ChatFormatting.AQUA), true);
        return at;
    }

    /** Keeps (or opens) a rift at a spot until a time: raids hold theirs open. */
    static void keepRift(ServerLevel level, Vec3 at, long until) {
        synchronized (RIFTS) {
            RIFTS.removeIf(r -> r.level() == level.dimension() && r.at().distanceToSqr(at) < 1);
            RIFTS.add(new Rift(level.dimension(), at, until));
        }
    }

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            long now = server.overworld().getGameTime();
            // rifts: particles, walk-in travel, expiry; and now and then a new one near a random player
            synchronized (RIFTS) {
                Iterator<Rift> it = RIFTS.iterator();
                while (it.hasNext()) {
                    Rift rift = it.next();
                    ServerLevel level = server.getLevel(rift.level());
                    if (level == null || level.getGameTime() > rift.until()) {
                        it.remove();
                        continue;
                    }
                    if (now % 4 == 0) {
                        for (int i = 0; i < 6; i++) {
                            double t = (now / 4.0 + i) * 0.9;
                            level.sendParticles(CYAN, rift.at().x + Math.cos(t) * 0.8, rift.at().y + Math.sin(t * 0.7) * 1.2,
                                    rift.at().z + Math.sin(t) * 0.8, 1, 0, 0, 0, 0);
                        }
                        level.sendParticles(ParticleTypes.REVERSE_PORTAL, rift.at().x, rift.at().y, rift.at().z, 3, 0.3, 0.7, 0.3, 0.02);
                    }
                    for (ServerPlayer p : level.players()) {
                        if (p.position().add(0, 1, 0).distanceToSqr(rift.at()) < 1.7 && !p.isSpectator()) {
                            Scheduler.later(server, 1, () -> travel(p));
                        }
                    }
                }
            }
            if (now % 20 == 0) {
                List<ServerPlayer> players = new ArrayList<>(server.getPlayerList().getPlayers());
                if (!players.isEmpty() && server.overworld().getRandom().nextInt(RIFT_CHANCE / 20) == 0) {
                    ServerPlayer p = players.get(server.overworld().getRandom().nextInt(players.size()));
                    if (p.level().dimension() == Level.OVERWORLD && !p.isSpectator()) openRift(p);
                }
                for (ServerPlayer p : players) {
                    if (p.level().dimension() == DIMENSION && p.isInWater()) dataStream(p);
                }
            }
        });
    }

    /** In a data stream: +3 Tamer Energy a second, and sent-out Pokémon nearby heal a little. */
    static void dataStream(ServerPlayer player) {
        ItemStack dv = Digivice.find(player);
        if (!dv.isEmpty() && Digivice.energy(dv) < Digivice.MAX_ENERGY) {
            Digivice.setEnergy(dv, Digivice.energy(dv) + 3);
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".world.data_stream", Digivice.energy(dv), Digivice.MAX_ENERGY)
                    .withStyle(ChatFormatting.AQUA), true);
        }
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            PokemonEntity e = p.getEntity();
            if (e != null && !e.isBattling() && e.distanceToSqr(player) < 256 && p.getCurrentHealth() < p.getMaxHealth() && !p.isFainted()) {
                p.setCurrentHealth(Math.min(p.getMaxHealth(), p.getCurrentHealth() + Math.max(1, p.getMaxHealth() / 20)));
            }
        }
        player.serverLevel().sendParticles(ParticleTypes.GLOW, player.getX(), player.getY() + 0.5, player.getZ(), 3, 0.4, 0.4, 0.4, 0.01);
    }

    // --- where each player came from (saved with the overworld) -------------------------------------------------------

    private static Returns returns(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(Returns::new, Returns::load, null), Digital.MOD_ID + "_returns");
    }

    static final class Returns extends SavedData {
        final CompoundTag positions;

        Returns() {
            this(new CompoundTag());
        }

        Returns(CompoundTag positions) {
            this.positions = positions;
        }

        static Returns load(CompoundTag tag, HolderLookup.Provider registries) {
            return new Returns(tag.getCompound("positions"));
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("positions", positions);
            return tag;
        }
    }
}
