package io.github.cobbleeffort.kanto;

import dev.architectury.event.events.common.LifecycleEvent;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.ColorRGBA;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ColoredFallingBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraft.world.level.material.MapColor;

import java.util.Set;

/**
 * The Ashtray Wastes (the user's design): a nicotine-blighted overworld biome. Its ground is ash, its water is tar,
 * nothing grows there but dead bushes, and giant cigarettes (filter, paper, and a smouldering or stubbed-out tip) stick
 * out of the ground at odd angles. It takes over patches of deserts, savannas, plains and badlands (see
 * {@link #swap}; the biome source mixin calls it), so it needs no change to the overworld's biome list. Its blocks,
 * features and the biome itself are here; its data (biome, features, textures) is written by tools/make_ashtray.py.
 */
public final class Ashtray {
    public static final ResourceKey<Biome> KEY = ResourceKey.create(Registries.BIOME, Kanto.id("ashtray"));
    /** The biomes it takes patches of. */
    private static final Set<ResourceKey<Biome>> HOSTS = Set.of(Biomes.DESERT, Biomes.SAVANNA, Biomes.PLAINS,
            Biomes.BADLANDS, Biomes.SAVANNA_PLATEAU);
    /** Patch size (in quarts, 4 blocks) and how much of a host biome becomes Ashtray Wastes. */
    private static final int CELL = 64;
    private static final double THRESHOLD = 0.68;

    public static final DeferredRegister<Feature<?>> FEATURES = DeferredRegister.create(Kanto.MOD_ID, Registries.FEATURE);

    public static final RegistrySupplier<Block> ASH = block("ash", () -> new ColoredFallingBlock(new ColorRGBA(0xFF8A8580),
            BlockBehaviour.Properties.ofFullCopy(Blocks.SAND).mapColor(MapColor.COLOR_GRAY).sound(SoundType.SAND)));
    public static final RegistrySupplier<Block> PAPER = block("cigarette_paper", () -> new Block(
            BlockBehaviour.Properties.ofFullCopy(Blocks.WHITE_WOOL).mapColor(MapColor.SNOW).strength(0.8F)));
    public static final RegistrySupplier<Block> FILTER = block("cigarette_filter", () -> new Block(
            BlockBehaviour.Properties.ofFullCopy(Blocks.ORANGE_WOOL).mapColor(MapColor.COLOR_ORANGE).strength(0.8F)));
    public static final RegistrySupplier<Block> EMBER = block("cigarette_ember", () -> new EmberBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.MAGMA_BLOCK).mapColor(MapColor.FIRE).lightLevel(s -> 12)));

    public static final RegistrySupplier<Feature<?>> SURFACE = FEATURES.register("ashtray_surface",
            () -> new AshtraySurfaceFeature(NoneFeatureConfiguration.CODEC));
    public static final RegistrySupplier<Feature<?>> GIANT_CIGARETTE = FEATURES.register("giant_cigarette",
            () -> new GiantCigaretteFeature(NoneFeatureConfiguration.CODEC, true));
    public static final RegistrySupplier<Feature<?>> CIGARETTE_BUTT = FEATURES.register("cigarette_butt",
            () -> new GiantCigaretteFeature(NoneFeatureConfiguration.CODEC, false));

    private static volatile Holder<Biome> holder;
    private static volatile long seed;

    private Ashtray() {}

    private static RegistrySupplier<Block> block(String name, java.util.function.Supplier<Block> make) {
        RegistrySupplier<Block> b = Kanto.BLOCKS.register(name, make);
        Kanto.ITEMS.register(name, () -> new BlockItem(b.get(), new Item.Properties().arch$tab(Kanto.TAB)));
        return b;
    }

    static void register() {
        FEATURES.register();
        LifecycleEvent.SERVER_BEFORE_START.register(server -> {
            seed = server.getWorldData().worldGenOptions().seed();
            holder = server.registryAccess().registryOrThrow(Registries.BIOME).getHolder(KEY).orElse(null);
            if (holder == null) Kanto.LOG.warn("The Ashtray Wastes biome is missing from the biome registry");
        });
        LifecycleEvent.SERVER_STOPPED.register(server -> holder = null);
    }

    /** The biome, once the server has started (null before, or if its data is missing). */
    public static Holder<Biome> holder() {
        return holder;
    }

    /** Called by the overworld biome source: the Ashtray Wastes in place of a host biome inside its patches. */
    public static Holder<Biome> swap(Holder<Biome> biome, int qx, int qz) {
        Holder<Biome> ours = holder;
        if (ours == null || biome == null) return null;
        for (ResourceKey<Biome> host : HOSTS) {
            if (biome.is(host)) return noise(qx, qz) > THRESHOLD ? ours : null;
        }
        return null;
    }

    /** Smooth value noise in [0, 1] over quart coordinates: two octaves of seeded lattice values. */
    static double noise(int qx, int qz) {
        return noise(qx, qz, CELL, seed);
    }

    /** The same noise for any patch size and seed (other patch biomes salt the world seed so patches don't line up). */
    static double noise(int qx, int qz, int cell, long s) {
        return 0.7 * octave(qx, qz, cell, s) + 0.3 * octave(qx, qz, cell / 3, s ^ 0x5DEECE66DL);
    }

    /** The world seed, once the server has started. */
    static long seed() {
        return seed;
    }

    private static double octave(int qx, int qz, int cell, long s) {
        double fx = Math.floorDiv(qx, cell), fz = Math.floorDiv(qz, cell);
        double tx = (qx - fx * cell) / cell, tz = (qz - fz * cell) / cell;
        tx = tx * tx * (3 - 2 * tx);
        tz = tz * tz * (3 - 2 * tz);
        long ix = (long) fx, iz = (long) fz;
        double a = lattice(ix, iz, s), b = lattice(ix + 1, iz, s), c = lattice(ix, iz + 1, s), d = lattice(ix + 1, iz + 1, s);
        return (a * (1 - tx) + b * tx) * (1 - tz) + (c * (1 - tx) + d * tx) * tz;
    }

    private static double lattice(long x, long z, long s) {
        long h = s ^ (x * 0x9E3779B97F4A7C15L) ^ (z * 0xC2B2AE3D27D4EB4FL);
        h ^= h >>> 33;
        h *= 0xFF51AFD7ED558CCDL;
        h ^= h >>> 33;
        h *= 0xC4CEB9FE1A85EC53L;
        h ^= h >>> 33;
        return (h >>> 11) * 0x1.0p-53;
    }

    /** The smouldering tip of a lit cigarette: it glows, smokes, and burns what stands on it. */
    public static final class EmberBlock extends Block {
        public EmberBlock(BlockBehaviour.Properties props) {
            super(props);
        }

        @Override
        public void stepOn(Level level, BlockPos pos, BlockState state, Entity entity) {
            if (!entity.isSteppingCarefully() && entity instanceof LivingEntity) {
                entity.hurt(level.damageSources().hotFloor(), 1.0F);
            }
            super.stepOn(level, pos, state, entity);
        }

        @Override
        public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
            if (!level.getBlockState(pos.above()).isAir()) return;
            double x = pos.getX() + random.nextDouble(), z = pos.getZ() + random.nextDouble();
            level.addParticle(ParticleTypes.SMOKE, x, pos.getY() + 1.05, z, 0.0, 0.04, 0.0);
            if (random.nextInt(4) == 0) {
                level.addAlwaysVisibleParticle(ParticleTypes.CAMPFIRE_COSY_SMOKE, true, pos.getX() + 0.5, pos.getY() + 1.1,
                        pos.getZ() + 0.5, 0.0, 0.05, 0.0);
            }
            if (random.nextInt(12) == 0) level.addParticle(ParticleTypes.LAVA, x, pos.getY() + 1.0, z, 0.0, 0.0, 0.0);
        }
    }
}
