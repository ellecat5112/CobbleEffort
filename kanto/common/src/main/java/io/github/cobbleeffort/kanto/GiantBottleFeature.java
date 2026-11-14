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

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * A bottle stuck in the ground at an odd angle (the Liquor Meadows' trees): a one-block glass shell (body, shoulders,
 * neck, a lip ring and a cork or cap), a paper label band with a coloured stripe, and the drink inside filled up to a
 * level in WORLD height, so it lies flat however the bottle leans. Giant ones are 3 to 7 blocks wide and 18 to 34
 * long; fallen ones are little empties lying in the grass. Kinds: wine, champagne, beer, whisky, vodka and sake.
 */
public final class GiantBottleFeature extends Feature<NoneFeatureConfiguration> {
    private static final double MAX_REACH = 11.0;                  // stays inside the chunks a feature may write to
    private final boolean giant;

    private record Kind(Supplier<BlockState> shell, Supplier<BlockState> liquid, Supplier<BlockState> label,
                        Supplier<BlockState> stripe, Supplier<BlockState> top, Supplier<BlockState> foil,
                        double body, double shoulder, double neck, boolean bulb, int weight) {}

    private static Supplier<BlockState> b(net.minecraft.world.level.block.Block block) {
        return block::defaultBlockState;
    }

    private static final Supplier<BlockState> PAPER = () -> Liquor.LABEL.get().defaultBlockState();
    private static final Supplier<BlockState> CORK = () -> Liquor.CORK.get().defaultBlockState();
    private static final Supplier<BlockState> CAP = () -> Liquor.CAP.get().defaultBlockState();

    //                       shell                          liquid                          label                    stripe                         top             foil                 body  shoulder neck bulb weight
    private static final Kind[] KINDS = {
        new Kind(b(Blocks.GREEN_STAINED_GLASS), b(Blocks.RED_STAINED_GLASS), PAPER, b(Blocks.RED_TERRACOTTA), CORK, null, 0.55, 0.14, 0.31, false, 4),   // wine
        new Kind(b(Blocks.GREEN_STAINED_GLASS), b(Blocks.YELLOW_STAINED_GLASS), b(Blocks.BLACK_CONCRETE), b(Blocks.GOLD_BLOCK), CORK, b(Blocks.GOLD_BLOCK), 0.55, 0.15, 0.30, false, 2),   // champagne
        new Kind(b(Blocks.BROWN_STAINED_GLASS), b(Blocks.ORANGE_STAINED_GLASS), PAPER, b(Blocks.BLUE_CONCRETE), CAP, null, 0.60, 0.16, 0.24, false, 4),    // beer
        new Kind(b(Blocks.GLASS), b(Blocks.ORANGE_STAINED_GLASS), b(Blocks.BLACK_CONCRETE), b(Blocks.GOLD_BLOCK), CORK, null, 0.68, 0.10, 0.22, false, 4),   // whisky
        new Kind(b(Blocks.GLASS), b(Blocks.WHITE_STAINED_GLASS), PAPER, b(Blocks.RED_CONCRETE), b(Blocks.IRON_BLOCK), null, 0.60, 0.12, 0.28, false, 3),   // vodka
        new Kind(b(Blocks.WHITE_TERRACOTTA), null, b(Blocks.BLUE_TERRACOTTA), b(Blocks.WHITE_TERRACOTTA), null, null, 0.62, 0.18, 0.20, true, 2),          // sake (a ceramic tokkuri)
    };

    public GiantBottleFeature(Codec<NoneFeatureConfiguration> codec, boolean giant) {
        super(codec);
        this.giant = giant;
    }

    private static Kind pick(RandomSource random) {
        int total = 0;
        for (Kind k : KINDS) total += k.weight;
        int n = random.nextInt(total);
        for (Kind k : KINDS) if ((n -= k.weight) < 0) return k;
        return KINDS[0];
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> ctx) {
        WorldGenLevel level = ctx.level();
        RandomSource random = ctx.random();
        BlockPos origin = ctx.origin();
        if (!level.getBiome(origin).is(Liquor.KEY)) return false;
        Kind kind = pick(random);
        double r = giant ? 1.6 + random.nextDouble() * 1.8 : 0.9 + random.nextDouble() * 0.5;
        double len = giant ? 18 + random.nextInt(17) : 5 + random.nextInt(4);
        double tilt = Math.toRadians(giant ? 8 + random.nextInt(55) : 72 + random.nextInt(16));
        if (len * Math.sin(tilt) > MAX_REACH) tilt = Math.asin(MAX_REACH / len);
        double yaw = random.nextDouble() * Math.PI * 2;
        Vec3 dir = new Vec3(Math.sin(tilt) * Math.cos(yaw), Math.cos(tilt), Math.sin(tilt) * Math.sin(yaw));
        Vec3 u = dir.cross(new Vec3(0, 1, 0));
        u = u.lengthSqr() < 1e-6 ? new Vec3(1, 0, 0) : u.normalize();
        Vec3 v = dir.cross(u).normalize();
        double buried = giant ? 3 + random.nextInt(3) : 0.6;
        Vec3 start = Vec3.atBottomCenterOf(origin).subtract(dir.scale(buried));
        double bodyEnd = len * kind.body, shoulderEnd = len * (kind.body + kind.shoulder), topLen = giant ? 1.6 : 0.8;
        double neckR = Math.max(giant ? 1.05 : 0.5, r * 0.4);
        // the drink's surface, in world height: somewhere up the body (a giant's never quite full, an empty's dry)
        double liquidY = giant ? start.y + dir.y * bodyEnd * (0.35 + random.nextDouble() * 0.6) : -1e9;

        Map<BlockPos, BlockState> out = new HashMap<>();
        Map<BlockPos, Integer> rank = new HashMap<>();
        double step = 0.35;
        for (double t = 0; t <= len; t += step) {
            double R;
            if (t < bodyEnd) {
                R = kind.bulb ? r * (0.72 + 0.28 * Math.sin(Math.PI * Math.min(1.0, t / bodyEnd * 0.85 + 0.15))) : r;
            } else if (t < shoulderEnd) {
                double s = (t - bodyEnd) / Math.max(0.1, shoulderEnd - bodyEnd);
                s = s * s * (3 - 2 * s);
                R = r + (neckR - r) * s;
            } else {
                R = neckR;
            }
            boolean lip = t > len - topLen - 0.9 && t <= len - topLen;
            boolean topPart = t > len - topLen;
            if (lip) R += kind.bulb ? 0.9 : 0.4;                                             // the lip ring (sake: a flared rim)
            boolean label = t > bodyEnd * 0.32 && t < bodyEnd * 0.78;
            boolean stripe = t > bodyEnd * 0.5 && t < bodyEnd * 0.6;
            boolean foil = kind.foil != null && t > shoulderEnd - 0.5 && !topPart;
            for (double a = -R; a <= R; a += step) {
                for (double c = -R; c <= R; c += step) {
                    double d = Math.sqrt(a * a + c * c);
                    if (d > R) continue;
                    Vec3 q = start.add(dir.scale(t)).add(u.scale(a)).add(v.scale(c));
                    BlockPos p = BlockPos.containing(q);
                    BlockState s;
                    int pri;
                    if (topPart) {
                        if (kind.top == null) {                                              // an open neck
                            if (d < R - 1.0) continue;
                            s = kind.shell.get();
                        } else {
                            s = kind.top.get();
                        }
                        pri = 3;
                    } else if (d > R - 1.0 || t < 0.8) {                                    // the shell (and its base)
                        s = foil ? kind.foil.get() : label && kind.label != null ? (stripe ? kind.stripe.get() : kind.label.get())
                                : kind.shell.get();
                        pri = 2;
                    } else {                                                                 // inside: drink below its level
                        s = kind.liquid != null && q.y < liquidY ? kind.liquid.get() : Blocks.AIR.defaultBlockState();
                        pri = 1;
                    }
                    Integer old = rank.get(p);
                    if (old != null && old >= pri) continue;
                    rank.put(p, pri);
                    out.put(p.immutable(), s);
                }
            }
        }
        for (Map.Entry<BlockPos, BlockState> e : out.entrySet()) {
            BlockPos p = e.getKey();
            if (level.isOutsideBuildHeight(p) || level.getBlockState(p).is(Blocks.BEDROCK)) continue;
            level.setBlock(p, e.getValue(), 2);
        }
        return true;
    }
}
