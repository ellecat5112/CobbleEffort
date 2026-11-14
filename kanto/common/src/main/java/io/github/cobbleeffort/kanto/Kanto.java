package io.github.cobbleeffort.kanto;

import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.level.biome.BiomeModifications;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BiomeTags;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.minecraft.world.level.levelgen.placement.PlacementModifierType;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * CobbleEffort: Kanto. Gen 1 Bricks, a Gen 1-styled lab in villages with a glitchy PC, and the Kanto dimension (only
 * Gen 1 Pokémon) reached through that PC once a Kantonian Orb has woken it. See the add-on's README.
 */
public final class Kanto {
    public static final String MOD_ID = "cobbleeffort_kanto";
    public static final Logger LOG = LoggerFactory.getLogger("CobbleEffort Kanto");
    public static final ResourceKey<Level> KANTO = ResourceKey.create(Registries.DIMENSION, id("kanto"));

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(MOD_ID, Registries.BLOCK);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);
    public static final DeferredRegister<PlacementModifierType<?>> PLACEMENTS = DeferredRegister.create(MOD_ID, Registries.PLACEMENT_MODIFIER_TYPE);

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("kanto", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Kanto.ORB.get())));

    public static final RegistrySupplier<Block> BRICKS_BLACK = bricks("gen1_bricks_black");
    public static final RegistrySupplier<Block> BRICKS_WHITE = bricks("gen1_bricks_white");
    public static final RegistrySupplier<Block> BRICKS_GREY = bricks("gen1_bricks_grey");
    /** The lab's glitchy PC: a Kantonian Orb wakes it, then it takes you to Kanto (and back). */
    public static final RegistrySupplier<Block> PC = BLOCKS.register("glitchy_pc", () -> new KantoPcBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_BLOCK).strength(3F, 1200F).noOcclusion()
                    .lightLevel(s -> s.getValue(KantoPcBlock.LIT) ? 12 : 3)));
    public static final RegistrySupplier<Item> PC_ITEM = ITEMS.register("glitchy_pc", () ->
            new BlockItem(PC.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(TAB)));
    /** The portal igniter: a Distortion Crystal and Essence of Olde. */
    public static final RegistrySupplier<Item> ORB = ITEMS.register("kantonian_orb", () ->
            new Item(new Item.Properties().durability(16).rarity(Rarity.EPIC).arch$tab(TAB)));
    /** A rare drop from Gen 1 Pokémon defeated in battle. */
    public static final RegistrySupplier<Item> ESSENCE = ITEMS.register("essence_of_olde", () ->
            new Item(new Item.Properties().rarity(Rarity.RARE).arch$tab(TAB)));

    // --- stage 2: gym badges and the Champion Ribbon -----------------------------------------------------------------
    public static final String[] BADGES = {"rock", "water", "electric", "grass", "poison", "psychic", "fire", "ground"};
    static {
        for (String type : BADGES) ITEMS.register(type + "_badge", () ->
                new Item(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON).arch$tab(TAB)));
    }
    public static final RegistrySupplier<Item> RIBBON = ITEMS.register("champion_ribbon", () ->
            new Item(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).arch$tab(TAB)));

    // --- stage 3: Kantonian ore (Kanto only), raw Kantonian, ingots, armor ------------------------------------------
    public static final RegistrySupplier<Block> ORE = BLOCKS.register("kantonian_ore", () ->
            new DropExperienceBlock(UniformInt.of(0, 0), BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_ORE)));
    public static final RegistrySupplier<Block> DEEPSLATE_ORE = BLOCKS.register("deepslate_kantonian_ore", () ->
            new DropExperienceBlock(UniformInt.of(0, 0), BlockBehaviour.Properties.ofFullCopy(Blocks.DEEPSLATE_IRON_ORE)));
    public static final RegistrySupplier<Item> ORE_ITEM = ITEMS.register("kantonian_ore", () ->
            new BlockItem(ORE.get(), new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<Item> DEEPSLATE_ORE_ITEM = ITEMS.register("deepslate_kantonian_ore", () ->
            new BlockItem(DEEPSLATE_ORE.get(), new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<Item> RAW = ITEMS.register("raw_kantonian", () -> new Item(new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<Item> INGOT = ITEMS.register("kantonian_ingot", () -> new Item(new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<Block> BLOCK = BLOCKS.register("kantonian_block", () ->
            new Block(BlockBehaviour.Properties.ofFullCopy(Blocks.IRON_BLOCK)));
    public static final RegistrySupplier<Item> BLOCK_ITEM = ITEMS.register("kantonian_block", () ->
            new BlockItem(BLOCK.get(), new Item.Properties().arch$tab(TAB)));
    public static final RegistrySupplier<PlacementModifierType<?>> IN_KANTO = PLACEMENTS.register("in_kanto",
            () -> (PlacementModifierType<KantoOnly>) () -> KantoOnly.CODEC);
    static final String[] ORE_FEATURES = {"kantonian_ore_upper", "kantonian_ore_middle", "kantonian_ore_small"};
    static {
        KantoArmor.setup();
        Regions.register();
        // the other regions' badges and Champion Ribbons (tools/make_leagues.py lists them)
        try (java.io.InputStream in = Kanto.class.getResourceAsStream("/data/" + MOD_ID + "/kanto/league_items.json")) {
            if (in != null) {
                for (com.google.gson.JsonElement e : com.google.gson.JsonParser.parseReader(
                        new java.io.InputStreamReader(in, java.nio.charset.StandardCharsets.UTF_8)).getAsJsonArray()) {
                    String name = e.getAsString();
                    boolean ribbon = name.endsWith("_champion_ribbon");
                    ITEMS.register(name, () -> new Item(new Item.Properties().stacksTo(1)
                            .rarity(ribbon ? Rarity.EPIC : Rarity.UNCOMMON).arch$tab(TAB)));
                }
            }
        } catch (Exception ex) {
            LOG.error("Couldn't read the league items", ex);
        }
    }

    private Kanto() {
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
    }

    private static RegistrySupplier<Block> bricks(String name) {
        RegistrySupplier<Block> block = BLOCKS.register(name, () -> new Block(BlockBehaviour.Properties.ofFullCopy(Blocks.STONE_BRICKS)));
        ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties().arch$tab(TAB)));
        return block;
    }

    public static void init() {
        TABS.register();
        Tar.register();                                     // the tar fluid (its block and bucket register below)
        Ashtray.register();                                 // the Ashtray Wastes: blocks, features, biome patches
        BLOCKS.register();
        KantoArmor.MATERIALS.register();
        ITEMS.register();
        PLACEMENTS.register();
        for (String feature : ORE_FEATURES) {
            ResourceKey<PlacedFeature> key = ResourceKey.create(Registries.PLACED_FEATURE, id(feature));
            BiomeModifications.addProperties(ctx -> ctx.hasTag(BiomeTags.IS_OVERWORLD),
                    (ctx, props) -> props.getGenerationProperties().addFeature(GenerationStep.Decoration.UNDERGROUND_ORES, key));
        }
        Tar.worldgen();
        KantoEvents.init();
        KantoGyms.init();
        KantoCommand.init();
    }
}
