package io.github.cobbleeffort.kanto;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.saveddata.SavedData;

/**
 * Going to Kanto and back through a lit glitchy PC. Into Kanto: the same x/z, on the surface, on a little platform of
 * Gen 1 Bricks with a lit PC for the way home (built once, if there's no PC nearby). Back: to where you left from.
 */
public final class KantoTravel {
    private KantoTravel() {
    }

    public static void travel(ServerPlayer player) {
        try {
            MinecraftServer server = player.server;
            if (player.level().dimension() == Kanto.KANTO) {
                Returns returns = returns(server);
                CompoundTag back = returns.positions.getCompound(player.getStringUUID());
                ServerLevel to = back.contains("dim") ? levelOf(server, back.getString("dim")) : null;
                if (to == null) to = server.overworld();
                BlockPos pos = back.contains("x") ? new BlockPos(back.getInt("x"), back.getInt("y"), back.getInt("z"))
                        : to.getSharedSpawnPos();
                effects(player);
                player.teleportTo(to, pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, player.getYRot(), player.getXRot());
                effects(player);
                return;
            }
            ServerLevel kanto = server.getLevel(Kanto.KANTO);
            if (kanto == null) {
                player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".pc.no_kanto"), true);
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
            kanto.getChunk(x >> 4, z >> 4);
            int y = Math.max(kanto.getMinBuildHeight() + 2, kanto.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z));
            BlockPos arrival = new BlockPos(x, y, z);
            arrivalPad(kanto, arrival);
            effects(player);
            player.teleportTo(kanto, x + 0.5, y, z + 0.5, player.getYRot(), player.getXRot());
            effects(player);
            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".pc.arrived"), true);
        } catch (Throwable t) {
            Kanto.LOG.error("Travelling through the glitchy PC failed", t);
        }
    }

    private static ServerLevel levelOf(MinecraftServer server, String dim) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dim)) return level;
        }
        return null;
    }

    /** A 5x5 floor of Gen 1 Bricks, room to stand, and a lit PC two blocks north (unless a PC is already near). */
    private static void arrivalPad(ServerLevel kanto, BlockPos at) {
        for (BlockPos p : BlockPos.betweenClosed(at.offset(-6, -3, -6), at.offset(6, 3, 6))) {
            if (kanto.getBlockState(p).is(Kanto.PC.get())) return;
        }
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                boolean edge = Math.abs(dx) == 2 || Math.abs(dz) == 2;
                kanto.setBlock(at.offset(dx, -1, dz), (edge ? Kanto.BRICKS_BLACK : Kanto.BRICKS_GREY).get().defaultBlockState(), 3);
                for (int dy = 0; dy < 3; dy++) kanto.setBlock(at.offset(dx, dy, dz), Blocks.AIR.defaultBlockState(), 3);
            }
        }
        kanto.setBlock(at.offset(0, 0, -2), Kanto.PC.get().defaultBlockState().setValue(KantoPcBlock.FACING, Direction.SOUTH)
                .setValue(KantoPcBlock.LIT, true), 3);
    }

    private static void effects(ServerPlayer player) {
        if (player.level() instanceof ServerLevel level) {
            level.sendParticles(ParticleTypes.REVERSE_PORTAL, player.getX(), player.getY() + 1, player.getZ(), 80, 0.4, 0.8, 0.4, 0.05);
            level.playSound(null, player.blockPosition(), SoundEvents.PORTAL_TRAVEL, SoundSource.PLAYERS, 0.25F, 1.6F);
        }
    }

    // --- where each player came from (saved with the overworld) ----------------------------------------------------
    private static Returns returns(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(Returns::new, Returns::load, null), Kanto.MOD_ID + "_returns");
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
