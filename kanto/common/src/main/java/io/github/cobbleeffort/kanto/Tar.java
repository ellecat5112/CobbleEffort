package io.github.cobbleeffort.kanto;

import dev.architectury.core.block.ArchitecturyLiquidBlock;
import dev.architectury.core.fluid.ArchitecturyFlowingFluid;
import dev.architectury.core.fluid.ArchitecturyFluidAttributes;
import dev.architectury.core.fluid.SimpleArchitecturyFluidAttributes;
import dev.architectury.core.item.ArchitecturyBucketItem;
import dev.architectury.registry.level.biome.BiomeModifications;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BiomeTags;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.minecraft.world.level.material.FlowingFluid;
import net.minecraft.world.level.material.Fluid;
import net.minecraft.world.phys.Vec3;

/**
 * Tar: a thick black fluid of the overworld (the user's design for CobbleEffort's fossil Pokémon). It pools in tar
 * lakes in badlands, deserts, savannas and swamps and underground, flows slowly like lava but is cold, and is sticky:
 * anything wading through it is slowed. Collect it with a bucket: a Bucket of Tar is the fossil Petroleodd is revived
 * from at a Fossil Analyzer (its Cobblemon fossil entry and the tar lakes are data, written by tools/make_tar.py).
 */
public final class Tar {
    public static final DeferredRegister<Fluid> FLUIDS = DeferredRegister.create(Kanto.MOD_ID, Registries.FLUID);

    public static final ArchitecturyFluidAttributes ATTRIBUTES = SimpleArchitecturyFluidAttributes
            .ofSupplier(() -> Tar.FLOWING, () -> Tar.SOURCE)
            .convertToSource(false)
            .slopeFindDistance(2).dropOff(2).tickDelay(30)
            .explosionResistance(100F)
            .density(3000).viscosity(6000).temperature(300)
            .sourceTexture(Kanto.id("block/tar_still")).flowingTexture(Kanto.id("block/tar_flow"))
            .color(0xFFFFFFFF)
            .fillSound(SoundEvents.BUCKET_FILL_LAVA).emptySound(SoundEvents.BUCKET_EMPTY_LAVA)
            .blockSupplier(() -> Tar.BLOCK).bucketItemSupplier(() -> Tar.BUCKET);

    public static final RegistrySupplier<FlowingFluid> SOURCE = FLUIDS.register("tar", () -> new ArchitecturyFlowingFluid.Source(ATTRIBUTES));
    public static final RegistrySupplier<FlowingFluid> FLOWING = FLUIDS.register("flowing_tar", () -> new ArchitecturyFlowingFluid.Flowing(ATTRIBUTES));
    public static final RegistrySupplier<LiquidBlock> BLOCK = Kanto.BLOCKS.register("tar", () -> new TarBlock(SOURCE,
            BlockBehaviour.Properties.ofFullCopy(Blocks.LAVA).lightLevel(s -> 0)));
    public static final RegistrySupplier<Item> BUCKET = Kanto.ITEMS.register("tar_bucket", () -> new ArchitecturyBucketItem(SOURCE,
            new Item.Properties().craftRemainder(Items.BUCKET).stacksTo(1).arch$tab(Kanto.TAB)));

    /** The liquid block: sticky, so anything inside it moves slowly (like wading through cobwebs, but less). */
    static final class TarBlock extends ArchitecturyLiquidBlock {
        TarBlock(java.util.function.Supplier<? extends FlowingFluid> fluid, BlockBehaviour.Properties props) {
            super(fluid, props);
        }

        @Override
        protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
            entity.makeStuckInBlock(state, new Vec3(0.55, 0.4, 0.55));
        }
    }

    private Tar() {}

    static void register() {
        FLUIDS.register();
    }

    /** Tar lakes: on the surface of dry and swampy biomes, and underground everywhere in the overworld. */
    static void worldgen() {
        ResourceKey<PlacedFeature> surface = ResourceKey.create(Registries.PLACED_FEATURE, Kanto.id("tar_lake_surface"));
        ResourceKey<PlacedFeature> underground = ResourceKey.create(Registries.PLACED_FEATURE, Kanto.id("tar_lake_underground"));
        BiomeModifications.addProperties(ctx -> ctx.hasTag(BiomeTags.IS_BADLANDS) || ctx.hasTag(BiomeTags.IS_SAVANNA)
                        || ctx.getKey().filter(k -> k.equals(Biomes.DESERT.location()) || k.equals(Biomes.SWAMP.location())
                        || k.equals(Biomes.MANGROVE_SWAMP.location())).isPresent(),
                (ctx, props) -> props.getGenerationProperties().addFeature(GenerationStep.Decoration.LAKES, surface));
        BiomeModifications.addProperties(ctx -> ctx.hasTag(BiomeTags.IS_OVERWORLD),
                (ctx, props) -> props.getGenerationProperties().addFeature(GenerationStep.Decoration.LAKES, underground));
    }
}
