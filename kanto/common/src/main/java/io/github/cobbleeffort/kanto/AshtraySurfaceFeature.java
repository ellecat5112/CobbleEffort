package io.github.cobbleeffort.kanto;

import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;

/**
 * Runs once per chunk, last: in every column of the Ashtray Wastes it turns the top of the ground to ash, its water to
 * tar (lakes and rivers alike) and clears plants away (dead bushes stay), leaving the giant cigarettes untouched.
 */
public final class AshtraySurfaceFeature extends Feature<NoneFeatureConfiguration> {
    private static final int ASH_DEPTH = 3;

    public AshtraySurfaceFeature(Codec<NoneFeatureConfiguration> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> ctx) {
        WorldGenLevel level = ctx.level();
        int x0 = ctx.origin().getX() & ~15, z0 = ctx.origin().getZ() & ~15;
        BlockState ash = Ashtray.ASH.get().defaultBlockState();
        BlockState tar = Tar.BLOCK.get().defaultBlockState();
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        boolean changed = false;
        for (int dx = 0; dx < 16; dx++) {
            for (int dz = 0; dz < 16; dz++) {
                int x = x0 + dx, z = z0 + dz;
                int top = level.getHeight(Heightmap.Types.MOTION_BLOCKING, x, z);
                p.set(x, top, z);
                if (!level.getBiome(p).is(Ashtray.KEY)) continue;
                int ashed = 0;
                for (int y = top + 1; y > top - 48 && y > level.getMinBuildHeight(); y--) {
                    p.setY(y);
                    BlockState s = level.getBlockState(p);
                    if (s.isAir()) continue;
                    if (s.getFluidState().is(FluidTags.WATER) || s.is(Blocks.ICE) || s.is(Blocks.PACKED_ICE)) {
                        level.setBlock(p, tar, 2);                  // its water is tar
                        changed = true;
                        continue;
                    }
                    if (s.is(Blocks.DEAD_BUSH)) continue;
                    if (s.is(BlockTags.REPLACEABLE) || s.is(BlockTags.FLOWERS) || s.is(BlockTags.SAPLINGS)
                            || s.is(Blocks.CACTUS) || s.is(Blocks.SUGAR_CANE) || s.is(Blocks.SNOW)) {
                        level.setBlock(p, Blocks.AIR.defaultBlockState(), 2);
                        changed = true;
                        continue;
                    }
                    if (ground(s)) {
                        level.setBlock(p, ash, 2);
                        changed = true;
                        if (++ashed >= ASH_DEPTH) break;
                        continue;
                    }
                    break;                                          // a cigarette, a structure: leave it be
                }
            }
        }
        return changed;
    }

    private static boolean ground(BlockState s) {
        return s.is(BlockTags.DIRT) || s.is(BlockTags.SAND) || s.is(BlockTags.TERRACOTTA) || s.is(Blocks.GRAVEL)
                || s.is(Blocks.SANDSTONE) || s.is(Blocks.RED_SANDSTONE) || s.is(Blocks.CLAY) || s.is(Blocks.STONE)
                || s.is(Blocks.GRANITE) || s.is(Blocks.DIORITE) || s.is(Blocks.ANDESITE) || s.is(Blocks.GRASS_BLOCK)
                || s.is(Blocks.MUD) || s.is(Blocks.COARSE_DIRT);
    }
}
