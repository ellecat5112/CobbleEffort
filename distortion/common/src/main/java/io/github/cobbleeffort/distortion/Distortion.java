package io.github.cobbleeffort.distortion;

import dev.architectury.networking.NetworkManager;
import dev.architectury.platform.Platform;
import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.level.biome.BiomeModifications;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BiomeTags;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import dev.architectury.utils.Env;
import io.github.cobbleeffort.distortion.client.DistortWheelOption;
import io.github.cobbleeffort.distortion.client.DnaMachineClient;
import io.github.cobbleeffort.distortion.dna.DnaInsertPacket;
import io.github.cobbleeffort.distortion.dna.DnaMachineBlock;
import io.github.cobbleeffort.distortion.dna.DnaMachineBlockEntity;
import io.github.cobbleeffort.distortion.dna.MewDna;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Rarity;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * CobbleEffort: Distortion. A battle gimmick: a Pokémon holding the Distortion Crystal, with its trainer
 * wearing the Distortion Band (in its own accessory slot), distorts: its types turn into their weaknesses, its ability
 * and moves follow, and its colours invert. See docs/distortion_design.md in the CobbleEffort repository.
 */
public final class Distortion {
    public static final String MOD_ID = "cobbleeffort_distortion";

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final Logger LOG = LoggerFactory.getLogger("CobbleEffort Distortion");
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(MOD_ID, Registries.BLOCK);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(MOD_ID, Registries.BLOCK_ENTITY_TYPE);

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("distortion", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Distortion.BAND.get())));

    /** Worn in the "distortion_slot" accessory slot. */
    public static final RegistrySupplier<Item> BAND = ITEMS.register("distortion_band", () ->
            new Item(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).arch$tab(TAB)));

    /** Held by the Pokémon: one crystal works for every distortable Pokémon. */
    public static final RegistrySupplier<Item> CRYSTAL = ITEMS.register("distortion_crystal", () ->
            new Item(new Item.Properties().stacksTo(1).rarity(Rarity.RARE).arch$tab(TAB)));

    /** Distortion Crystal ore (stone and deepslate), a little rarer than coal at coal's heights: 2-4 shards, stone pickaxe. */
    public static final RegistrySupplier<Block> DISTORTION_ORE = BLOCKS.register("distortion_crystal_ore", () ->
            new DropExperienceBlock(UniformInt.of(1, 4), BlockBehaviour.Properties.ofFullCopy(Blocks.COAL_ORE).lightLevel(s -> 3)));
    public static final RegistrySupplier<Block> DEEPSLATE_DISTORTION_ORE = BLOCKS.register("deepslate_distortion_crystal_ore", () ->
            new DropExperienceBlock(UniformInt.of(1, 4), BlockBehaviour.Properties.ofFullCopy(Blocks.DEEPSLATE_COAL_ORE).lightLevel(s -> 3)));
    public static final RegistrySupplier<Item> DISTORTION_ORE_ITEM = ITEMS.register("distortion_crystal_ore", () ->
            new BlockItem(DISTORTION_ORE.get(), new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<Item> DEEPSLATE_DISTORTION_ORE_ITEM = ITEMS.register("deepslate_distortion_crystal_ore", () ->
            new BlockItem(DEEPSLATE_DISTORTION_ORE.get(), new Item.Properties().arch$tab(TAB)));
    /** What the ore drops: crafted into the Distortion Crystal and the Distortion Band. */
    public static final RegistrySupplier<Item> SHARD = ITEMS.register("distortion_shard", () ->
            new Item(new Item.Properties().arch$tab(TAB)));
    public static final ResourceKey<PlacedFeature> ORE_PLACED =
            ResourceKey.create(Registries.PLACED_FEATURE, ResourceLocation.fromNamespaceAndPath(MOD_ID, "distortion_crystal_ore"));

    /** The cloning tank Mewtwo comes from: Mew DNA + Mew -> Mewtwo in five minutes. */
    public static final RegistrySupplier<Block> DNA_MACHINE = BLOCKS.register("dna_machine", () -> new DnaMachineBlock(
            BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(3.5F, 6F).sound(SoundType.METAL).noOcclusion()
                    .lightLevel(s -> 6).pushReaction(PushReaction.BLOCK)));
    public static final RegistrySupplier<Item> DNA_MACHINE_ITEM = ITEMS.register("dna_machine", () ->
            new BlockItem(DNA_MACHINE.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(TAB)));
    @SuppressWarnings("DataFlowIssue")
    public static final RegistrySupplier<BlockEntityType<DnaMachineBlockEntity>> DNA_MACHINE_ENTITY = BLOCK_ENTITIES.register("dna_machine",
            () -> BlockEntityType.Builder.of(DnaMachineBlockEntity::new, DNA_MACHINE.get()).build(null));
    /** Dropped (3-8) when a Pokémon is defeated by a trainer with Mew in their party: the DNA machine's fuel. */
    public static final RegistrySupplier<Item> MEW_DNA = ITEMS.register("mew_dna", () ->
            new Item(new Item.Properties().rarity(Rarity.RARE).arch$tab(TAB)));

    private Distortion() {
    }

    public static void init() {
        TABS.register();
        BLOCKS.register();
        ITEMS.register();
        BLOCK_ENTITIES.register();
        NetworkManager.registerReceiver(NetworkManager.Side.C2S, DnaInsertPacket.TYPE, DnaInsertPacket.STREAM_CODEC,
                (packet, context) -> context.queue(() -> {
                    try {
                        if (context.getPlayer() instanceof ServerPlayer player
                                && player.level().getBlockEntity(packet.pos()) instanceof DnaMachineBlockEntity machine) {
                            machine.insert(player, packet.pokemonId());
                        }
                    } catch (Throwable t) {
                        LOG.error("Putting a Pokémon in the DNA machine failed", t);
                    }
                }));
        MewDna.init();
        // the ore in every overworld biome, with the other underground ores
        BiomeModifications.addProperties(ctx -> ctx.hasTag(BiomeTags.IS_OVERWORLD),
                (ctx, props) -> props.getGenerationProperties().addFeature(GenerationStep.Decoration.UNDERGROUND_ORES, ORE_PLACED));
        DistortionBattle.init();
        DistortionWheel.init();
        if (Platform.getEnvironment() == Env.CLIENT) {
            DistortWheelOption.init();
            DnaMachineClient.init();
        }
    }
}
