package io.github.cobbleeffort.kanto;

import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraft.world.phys.Vec3;

/**
 * A cigarette stuck in the ground at an odd angle: an orange filter end buried in the dirt, a gold ring, a long white
 * paper body and, at the top, a smouldering ember ringed with ash (or an ashy stub where it was put out). Giant ones
 * are 3 to 5 blocks thick and 16 to 30 long; butts are one block thick and mostly filter.
 */
public final class GiantCigaretteFeature extends Feature<NoneFeatureConfiguration> {
    private static final double MAX_REACH = 12.0;                  // stays inside the chunks a feature may write to
    private final boolean giant;

    public GiantCigaretteFeature(Codec<NoneFeatureConfiguration> codec, boolean giant) {
        super(codec);
        this.giant = giant;
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> ctx) {
        WorldGenLevel level = ctx.level();
        RandomSource random = ctx.random();
        BlockPos origin = ctx.origin();
        if (!level.getBiome(origin).is(Ashtray.KEY)) return false;
        double r = giant ? 1.3 + random.nextDouble() * 1.1 : 0.4;
        double len = giant ? 16 + random.nextInt(15) : 5 + random.nextInt(4);
        double tilt = Math.toRadians(12 + random.nextInt(66));
        if (len * Math.sin(tilt) > MAX_REACH) tilt = Math.asin(MAX_REACH / len);
        double yaw = random.nextDouble() * Math.PI * 2;
        Vec3 dir = new Vec3(Math.sin(tilt) * Math.cos(yaw), Math.cos(tilt), Math.sin(tilt) * Math.sin(yaw));
        Vec3 u = dir.cross(new Vec3(0, 1, 0));
        u = u.lengthSqr() < 1e-6 ? new Vec3(1, 0, 0) : u.normalize();
        Vec3 v = dir.cross(u).normalize();
        double buried = giant ? 4 + random.nextInt(3) : 2;
        Vec3 start = Vec3.atBottomCenterOf(origin).subtract(dir.scale(buried));
        boolean lit = random.nextFloat() < 0.65F;
        double filterEnd = len * (giant ? 0.27 : 0.6);
        BlockState filter = Ashtray.FILTER.get().defaultBlockState();
        BlockState paper = Ashtray.PAPER.get().defaultBlockState();
        BlockState ash = Ashtray.ASH.get().defaultBlockState();
        BlockState ember = Ashtray.EMBER.get().defaultBlockState();
        BlockState ring = Blocks.YELLOW_TERRACOTTA.defaultBlockState();
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (double t = 0; t <= len; t += 0.4) {
            for (double a = -r; a <= r; a += 0.4) {
                for (double b = -r; b <= r; b += 0.4) {
                    double d2 = a * a + b * b;
                    if (d2 > r * r) continue;
                    Vec3 q = start.add(dir.scale(t)).add(u.scale(a)).add(v.scale(b));
                    p.set(Math.floor(q.x), Math.floor(q.y), Math.floor(q.z));
                    if (level.getBlockState(p).is(Blocks.BEDROCK) || level.isOutsideBuildHeight(p)) continue;
                    BlockState s;
                    if (t > len - 1.2) {
                        s = lit && d2 < (r * 0.65) * (r * 0.65) ? ember : ash;        // the tip
                    } else if (t < filterEnd) {
                        s = filter;
                    } else if (giant && t < filterEnd + 0.8) {
                        s = ring;                                                   // the gold ring
                    } else {
                        s = paper;
                    }
                    level.setBlock(p, s, 2);
                }
            }
        }
        return true;
    }
}
