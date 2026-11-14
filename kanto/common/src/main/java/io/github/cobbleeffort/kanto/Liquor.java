package io.github.cobbleeffort.kanto;

import dev.architectury.event.events.common.LifecycleEvent;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraft.world.level.material.MapColor;

import java.util.Set;

/**
 * The Liquor Meadows (the user's design): a tipsy overworld biome of extra-vibrant grass under clear skies, whose
 * water runs the colour of whisky and where, instead of trees, giant bottles (wine, champagne, beer, whisky, vodka and
 * sake) stick out of the ground at odd angles, half full; small empties lie about in the grass. It takes over patches
 * of forests, flower and birch forests, plains and meadows ({@link #swap}, called by the biome source mixin, like
 * the Ashtray Wastes; rivers stay rivers, so its whisky water is in its own ponds and lakes). Its data (biome, features, textures) is written by
 * tools/make_liquor.py.
 */
public final class Liquor {
    public static final ResourceKey<Biome> KEY = ResourceKey.create(Registries.BIOME, Kanto.id("liquor_meadows"));
    /** The biomes it takes patches of (plains are shared with the Ashtray Wastes, which are asked first). */
    private static final Set<ResourceKey<Biome>> HOSTS = Set.of(Biomes.FOREST, Biomes.FLOWER_FOREST, Biomes.BIRCH_FOREST,
            Biomes.OLD_GROWTH_BIRCH_FOREST, Biomes.SUNFLOWER_PLAINS, Biomes.PLAINS, Biomes.MEADOW);
    private static final int CELL = 64;
    private static final double THRESHOLD = 0.66;
    private static final long SALT = 0x2545F4914F6CDD1DL;

    public static final DeferredRegister<Feature<?>> FEATURES = DeferredRegister.create(Kanto.MOD_ID, Registries.FEATURE);

    public static final RegistrySupplier<Block> CORK = block("cork", () -> new Block(
            BlockBehaviour.Properties.ofFullCopy(Blocks.STRIPPED_OAK_WOOD).mapColor(MapColor.TERRACOTTA_ORANGE).strength(1.0F)));
    public static final RegistrySupplier<Block> CAP = block("bottle_cap", () -> new Block(
            BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_BLOCK).mapColor(MapColor.GOLD).strength(2.0F)));
    public static final RegistrySupplier<Block> LABEL = block("bottle_label", () -> new Block(
            BlockBehaviour.Properties.ofFullCopy(Blocks.WHITE_WOOL).mapColor(MapColor.SAND).strength(0.8F)));

    public static final RegistrySupplier<Feature<?>> GIANT_BOTTLE = FEATURES.register("giant_bottle",
            () -> new GiantBottleFeature(NoneFeatureConfiguration.CODEC, true));
    public static final RegistrySupplier<Feature<?>> FALLEN_BOTTLE = FEATURES.register("fallen_bottle",
            () -> new GiantBottleFeature(NoneFeatureConfiguration.CODEC, false));

    private static volatile Holder<Biome> holder;

    private Liquor() {}

    private static RegistrySupplier<Block> block(String name, java.util.function.Supplier<Block> make) {
        RegistrySupplier<Block> b = Kanto.BLOCKS.register(name, make);
        Kanto.ITEMS.register(name, () -> new BlockItem(b.get(), new Item.Properties().arch$tab(Kanto.TAB)));
        return b;
    }

    static void register() {
        FEATURES.register();
        LifecycleEvent.SERVER_BEFORE_START.register(server -> {
            holder = server.registryAccess().registryOrThrow(Registries.BIOME).getHolder(KEY).orElse(null);
            if (holder == null) Kanto.LOG.warn("The Liquor Meadows biome is missing from the biome registry");
        });
        LifecycleEvent.SERVER_STOPPED.register(server -> holder = null);
    }

    /** The biome, once the server has started (null before, or if its data is missing). */
    public static Holder<Biome> holder() {
        return holder;
    }

    /** Called by the overworld biome source: the Liquor Meadows in place of a host biome inside its patches. */
    public static Holder<Biome> swap(Holder<Biome> biome, int qx, int qz) {
        Holder<Biome> ours = holder;
        if (ours == null || biome == null) return null;
        for (ResourceKey<Biome> host : HOSTS) {
            if (biome.is(host)) return Ashtray.noise(qx, qz, CELL, Ashtray.seed() ^ SALT) > THRESHOLD ? ours : null;
        }
        return null;
    }
}
