package io.github.cobbleeffort.kanto;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;
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
        travel(player, Region.KANTO);
    }

    /**
     * Through a region's portal: from inside that region's dimension, home (where you left from); from anywhere else,
     * into the region at the same x/z, on the surface, on a small pad with a return portal (built once).
     */
    public static void travel(ServerPlayer player, Region region) {
        try {
            MinecraftServer server = player.server;
            if (player.level().dimension() == region.dimension) {
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
            ServerLevel dest = server.getLevel(region.dimension);
            if (dest == null) {
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
            dest.getChunk(x >> 4, z >> 4);
            int y = Math.max(dest.getMinBuildHeight() + 2, dest.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z));
            if (!dest.getFluidState(new BlockPos(x, y - 1, z)).isEmpty()) y += 1;   // a pad on the water, not under it
            BlockPos arrival = new BlockPos(x, y, z);
            arrivalPad(dest, arrival, region);
            effects(player);
            player.teleportTo(dest, x + 0.5, y, z + 0.5, player.getYRot(), player.getXRot());
            effects(player);
            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".arrived." + region.id), true);
            if (region == Region.KANTO) KantoGyms.arrived(player, dest);
        } catch (Throwable t) {
            Kanto.LOG.error("Travelling to {} failed", region.id, t);
        }
    }

    private static ServerLevel levelOf(MinecraftServer server, String dim) {
        for (ServerLevel level : server.getAllLevels()) {
            if (level.dimension().location().toString().equals(dim)) return level;
        }
        return null;
    }

    private static BlockState block(String id) {
        return BuiltInRegistries.BLOCK.get(ResourceLocation.parse(id)).defaultBlockState();
    }

    /** A 5x5 floor in the region's style, room to stand, and the way home two blocks north (unless one is already near). */
    private static void arrivalPad(ServerLevel level, BlockPos at, Region region) {
        Block portal = region == Region.KANTO ? Kanto.PC.get() : Regions.PORTALS.get(region).get();
        for (BlockPos p : BlockPos.betweenClosed(at.offset(-6, -3, -6), at.offset(6, 3, 6))) {
            if (level.getBlockState(p).is(portal)) return;
        }
        String[] floor = switch (region) {
            case KANTO -> new String[]{"cobbleeffort_kanto:gen1_bricks_black", "cobbleeffort_kanto:gen1_bricks_grey"};
            case JOHTO -> new String[]{"minecraft:stripped_dark_oak_wood", "minecraft:spruce_planks"};
            case HOENN -> new String[]{"minecraft:polished_granite", "minecraft:granite"};
            case SINNOH -> new String[]{"minecraft:polished_deepslate", "minecraft:dark_oak_planks"};
            case UNOVA -> new String[]{"minecraft:gold_block", "minecraft:quartz_bricks"};
            case KALOS -> new String[]{"minecraft:red_concrete", "minecraft:white_concrete"};
            case ALOLA -> new String[]{"minecraft:cut_sandstone", "minecraft:smooth_sandstone"};
            case GALAR -> new String[]{"minecraft:stone_bricks", "minecraft:polished_andesite"};
            case PALDEA -> new String[]{"minecraft:orange_terracotta", "minecraft:smooth_quartz"};
        };
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                boolean edge = Math.abs(dx) == 2 || Math.abs(dz) == 2;
                level.setBlock(at.offset(dx, -1, dz), block(edge ? floor[0] : floor[1]), 3);
                for (int dy = 0; dy < 4; dy++) level.setBlock(at.offset(dx, dy, dz), Blocks.AIR.defaultBlockState(), 3);
            }
        }
        BlockPos p = at.offset(0, 0, -2);
        BlockState facing = portal.defaultBlockState().hasProperty(HorizontalDirectionalBlock.FACING)
                ? portal.defaultBlockState().setValue(HorizontalDirectionalBlock.FACING, Direction.SOUTH) : portal.defaultBlockState();
        switch (region) {
            case KANTO -> level.setBlock(p, facing.setValue(KantoPcBlock.LIT, true), 3);
            case JOHTO -> {                                   // the bell hangs from a little gantry
                for (int dy = 0; dy < 3; dy++) {
                    level.setBlock(p.offset(-1, dy, 0), block("minecraft:dark_oak_fence"), 3);
                    level.setBlock(p.offset(1, dy, 0), block("minecraft:dark_oak_fence"), 3);
                }
                for (int dx = -1; dx <= 1; dx++) level.setBlock(p.offset(dx, 3, 0), block("minecraft:dark_oak_planks"), 3);
                level.setBlock(p.above(2), portal.defaultBlockState(), 3);
            }
            case HOENN -> {
                level.setBlock(p, portal.defaultBlockState(), 3);
                level.setBlock(p.above(), portal.defaultBlockState(), 3);
            }
            case SINNOH, UNOVA -> {
                level.setBlock(p, facing.setValue(RegionPortalBlock.Tall.HALF, DoubleBlockHalf.LOWER), 2);
                level.setBlock(p.above(), facing.setValue(RegionPortalBlock.Tall.HALF, DoubleBlockHalf.UPPER), 2);
                if (region == Region.SINNOH) {
                    for (int dy = 0; dy < 3; dy++) {
                        level.setBlock(p.offset(-1, dy, 0), block("minecraft:dark_oak_log"), 3);
                        level.setBlock(p.offset(1, dy, 0), block("minecraft:dark_oak_log"), 3);
                    }
                    level.setBlock(p.above(2), block("minecraft:dark_oak_log"), 3);
                }
            }
            case KALOS -> level.setBlock(p, portal.defaultBlockState().setValue(RegionPortalBlock.Parts.PART, RegionPortalBlock.Part.BUTTON), 3);
            case ALOLA -> {
                level.setBlock(p, block("minecraft:iron_block"), 3);
                level.setBlock(p.above(), portal.defaultBlockState(), 3);
            }
            case GALAR -> {
                level.setBlock(p, block("minecraft:dark_oak_log"), 3);
                level.setBlock(p.above(), facing, 3);
                level.setBlock(p.above(2), block("minecraft:dark_oak_log"), 3);
            }
            case PALDEA -> {
                level.setBlock(p, block("minecraft:quartz_block"), 3);
                level.setBlock(p.above(), facing, 3);
            }
        }
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
