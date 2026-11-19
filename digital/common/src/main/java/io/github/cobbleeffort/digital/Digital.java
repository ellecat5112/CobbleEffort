package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.item.PokeBallItem;
import com.cobblemon.mod.common.pokeball.PokeBall;
import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.level.biome.BiomeModifications;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.BiomeTags;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;

/**
 * CobbleEffort: Digital. A Digimon crossover for Cobblemon: the Digimon themselves are species in CobbleEffort (label
 * "digimon"; they spawn, battle and evolve like any Pokémon); this add-on brings what needs code: the Digiballs (the
 * Digiball and its stage tiers), Digitama that hatch baby Digimon, attribute data (the Vaccine/Data/Virus triangle in
 * battle, fragments and chips that rewrite a Digimon's attribute), Digi-Meat farming, the training gym and Chrome
 * Digizoid.
 */
public final class Digital {
    public static final String MOD_ID = "cobbleeffort_digital";
    public static final org.slf4j.Logger LOG = org.slf4j.LoggerFactory.getLogger("CobbleEffort Digital");

    /** The balls, in Cobblemon's own Poké Ball registry before any item is made (see DigiBall). */
    public static final PokeBall DIGIBALL_BALL = DigiBall.digiball();
    public static final PokeBall WIREFRAME_BALL = DigiBall.wireframe();
    public static final PokeBall DATA_NET_BALL = DigiBall.dataNet();
    public static final PokeBall CHROME_BALL = DigiBall.chrome();

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(MOD_ID, Registries.BLOCK);
    /** Everything for the creative tab, in order. */
    static final List<RegistrySupplier<Item>> TAB_ITEMS = new ArrayList<>();

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("digital", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Digital.DIGIBALL.get())));

    private static RegistrySupplier<Item> item(String name, Supplier<Item> item) {
        RegistrySupplier<Item> r = ITEMS.register(name, item);
        TAB_ITEMS.add(r);
        return r;
    }

    private static RegistrySupplier<Item> ball(String name, PokeBall ball) {
        return item(name, () -> {
            PokeBallItem item = new PokeBallItem(ball);
            ball.item = item;
            return item;
        });
    }

    private static Item.Properties props() {
        return new Item.Properties();
    }

    // --- balls ------------------------------------------------------------------------------------------------------
    public static final RegistrySupplier<Item> DIGIBALL = ball("digiball", DIGIBALL_BALL);
    public static final RegistrySupplier<Item> WIREFRAME_BALL_ITEM = ball("wireframe_ball", WIREFRAME_BALL);
    public static final RegistrySupplier<Item> DATA_NET_BALL_ITEM = ball("data_net_ball", DATA_NET_BALL);
    public static final RegistrySupplier<Item> CHROME_BALL_ITEM = ball("chrome_digizoid_ball", CHROME_BALL);

    public static final RegistrySupplier<Item> DIGITAMA = item("digitama", () ->
            new DigitamaItem(props().stacksTo(1).rarity(Rarity.UNCOMMON)));

    // --- attribute data -----------------------------------------------------------------------------------------------
    public static final Map<Attribute, RegistrySupplier<Item>> FRAGMENTS = new EnumMap<>(Attribute.class);
    public static final Map<Attribute, RegistrySupplier<Item>> CHIPS = new EnumMap<>(Attribute.class);

    static {
        for (Attribute a : new Attribute[]{Attribute.VACCINE, Attribute.DATA, Attribute.VIRUS}) {
            FRAGMENTS.put(a, item(a.id() + "_fragment", () -> new AttributeItem(props(), a, false)));
        }
        for (Attribute a : new Attribute[]{Attribute.VACCINE, Attribute.DATA, Attribute.VIRUS}) {
            CHIPS.put(a, item(a.id() + "_chip", () -> new AttributeItem(props().stacksTo(16).rarity(Rarity.UNCOMMON), a, true)));
        }
    }

    // --- Digi-Meat farm ----------------------------------------------------------------------------------------------
    public static final DigiFood.Effect MEAT = DigiFood.Effect.of(1, 2);
    public static final DigiFood.Effect SIRLOIN_FEED = DigiFood.Effect.of(2, 8, Stats.HP, 10, Stats.ATTACK, 10);
    public static final DigiFood.Effect CARROT_FEED = DigiFood.Effect.of(1, 5, Stats.SPEED, 10, Stats.SPECIAL_DEFENCE, 10);

    public static final RegistrySupplier<Block> DIGIMEAT_CROP = BLOCKS.register("digimeat_crop", () ->
            new DigiCropBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.CARROTS), () -> Digital.DIGIMEAT.get()));
    public static final RegistrySupplier<Block> SUPER_CARROT_CROP = BLOCKS.register("super_carrot_crop", () ->
            new DigiCropBlock(BlockBehaviour.Properties.ofFullCopy(Blocks.CARROTS), () -> Digital.SUPER_CARROT.get()));
    public static final RegistrySupplier<Item> DIGIMEAT = item("digimeat", () -> new DigiFood.Plantable(DIGIMEAT_CROP.get(),
            props().food(new FoodProperties.Builder().nutrition(6).saturationModifier(0.6F).build()), MEAT));
    public static final RegistrySupplier<Item> SIRLOIN = item("sirloin", () -> new DigiFood.Plain(
            props().rarity(Rarity.UNCOMMON).food(new FoodProperties.Builder().nutrition(10).saturationModifier(0.9F).build()), SIRLOIN_FEED));
    public static final RegistrySupplier<Item> SUPER_CARROT = item("super_carrot", () -> new DigiFood.Plantable(SUPER_CARROT_CROP.get(),
            props().rarity(Rarity.UNCOMMON).food(new FoodProperties.Builder().nutrition(5).saturationModifier(1.0F).build()), CARROT_FEED));

    // --- training gym --------------------------------------------------------------------------------------------------
    public static final Map<Training.Kind, RegistrySupplier<Block>> TRAINING = new EnumMap<>(Training.Kind.class);

    static {
        for (Training.Kind k : Training.Kind.values()) {
            VoxelShape shape = switch (k) {
                case PUNCHING_BAG -> Shapes.or(Block.box(4, 0, 4, 12, 15, 12), Block.box(7, 15, 7, 9, 16, 9));
                case TREADMILL -> Shapes.or(Block.box(0, 0, 1, 16, 4, 15), Block.box(1, 4, 1, 15, 14, 3));
                case WATERFALL -> Shapes.block();
                case MEDITATION_MAT -> Block.box(0, 0, 0, 16, 1, 16);
                case TARGET_DUMMY -> Shapes.or(Block.box(7, 0, 7, 9, 8, 9), Block.box(2, 6, 6, 14, 16, 10));
            };
            BlockBehaviour.Properties p = switch (k) {
                case WATERFALL -> BlockBehaviour.Properties.of().mapColor(MapColor.STONE).strength(1.5F, 6F).sound(SoundType.STONE);
                case MEDITATION_MAT -> BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(0.2F).sound(SoundType.WOOL)
                        .noOcclusion().pushReaction(PushReaction.DESTROY);
                case TREADMILL -> BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(2F, 6F).sound(SoundType.METAL).noOcclusion();
                default -> BlockBehaviour.Properties.of().mapColor(MapColor.WOOD).strength(1F).sound(SoundType.WOOL).noOcclusion();
            };
            RegistrySupplier<Block> b = BLOCKS.register(k.id(), () -> new TrainingBlock(p, k, shape));
            TRAINING.put(k, b);
            item(k.id(), () -> new BlockItem(b.get(), props()));
        }
    }

    // --- the Tamer's Digivice and Digi-Modify cards ----------------------------------------------------------------------
    public static final RegistrySupplier<Item> DIGIVICE = item("digivice", () -> new Digivice(props().stacksTo(1).rarity(Rarity.RARE)));
    public static final List<String> CARDS = List.of("high_speed_plugin", "metal_armor", "giga_destroyer", "recovery_disk",
            "dot_virus", "bug_card");
    /** Digi-Eggs (Digimentals): used on a Child they armor-digivolve it (item_interact evolutions in the species data). */
    public static final RegistrySupplier<Item> DIGIEGG_COURAGE = item("digiegg_of_courage", () -> new TooltipItem(props().stacksTo(16).rarity(Rarity.RARE)));
    public static final RegistrySupplier<Item> DIGIEGG_FRIENDSHIP = item("digiegg_of_friendship", () -> new TooltipItem(props().stacksTo(16).rarity(Rarity.RARE)));
    public static final Map<String, RegistrySupplier<Item>> CARD_ITEMS = new java.util.LinkedHashMap<>();

    static {
        for (String c : CARDS) CARD_ITEMS.put(c, item(c, () -> new DigiModifyCard(props().stacksTo(16).rarity(Rarity.UNCOMMON), c)));
    }

    // --- the Digital World ---------------------------------------------------------------------------------------------
    public static final DeferredRegister<net.minecraft.world.level.block.entity.BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(MOD_ID, Registries.BLOCK_ENTITY_TYPE);

    private static RegistrySupplier<Block> block(String name, Supplier<Block> block, Rarity rarity) {
        RegistrySupplier<Block> b = BLOCKS.register(name, block);
        item(name, () -> new BlockItem(b.get(), props().rarity(rarity)));
        return b;
    }

    private static BlockBehaviour.Properties stoneLike(MapColor colour) {
        return BlockBehaviour.Properties.of().mapColor(colour).strength(1.5F, 6F).requiresCorrectToolForDrops().sound(SoundType.METAL);
    }

    public static final RegistrySupplier<Block> CIRCUIT_BLOCK = block("circuit_block", () -> new Block(stoneLike(MapColor.COLOR_GREEN)), Rarity.COMMON);
    public static final RegistrySupplier<Block> SERVER_CASING = block("server_casing", () -> new Block(stoneLike(MapColor.METAL)), Rarity.COMMON);
    public static final RegistrySupplier<Block> SOCKET_BLOCK = block("socket_block", () -> new Block(stoneLike(MapColor.METAL)), Rarity.COMMON);
    public static final RegistrySupplier<Block> WIREFRAME_BLOCK = block("wireframe_block", () -> new net.minecraft.world.level.block.TransparentBlock(
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_CYAN).strength(0.6F).sound(SoundType.GLASS).noOcclusion()
                    .lightLevel(s -> 9).isViewBlocking((s, l, p) -> false).isSuffocating((s, l, p) -> false)), Rarity.COMMON);
    public static final RegistrySupplier<Block> VOXEL_LOG = block("voxel_log", () -> new net.minecraft.world.level.block.RotatedPillarBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.OAK_LOG).mapColor(MapColor.WOOD)), Rarity.COMMON);
    public static final RegistrySupplier<Block> VOXEL_LEAVES = block("voxel_leaves", () -> new net.minecraft.world.level.block.LeavesBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.OAK_LEAVES).mapColor(MapColor.COLOR_LIGHT_GREEN)), Rarity.COMMON);
    public static final RegistrySupplier<Block> CORRUPTED_DATA = block("corrupted_data", () -> new Block(
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(1.2F, 4F).requiresCorrectToolForDrops().lightLevel(s -> 2)), Rarity.COMMON);
    public static final RegistrySupplier<Block> TOWER_CORE = block("dark_tower_core", () -> new DarkTower.CoreBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.OBSIDIAN).lightLevel(s -> 7).strength(30F, 1200F)), Rarity.EPIC);
    @SuppressWarnings("DataFlowIssue")
    public static final RegistrySupplier<net.minecraft.world.level.block.entity.BlockEntityType<DarkTower.CoreEntity>> TOWER_CORE_ENTITY =
            BLOCK_ENTITIES.register("dark_tower_core", () -> net.minecraft.world.level.block.entity.BlockEntityType.Builder
                    .of(DarkTower.CoreEntity::new, TOWER_CORE.get()).build(null));
    public static final RegistrySupplier<Block> TERMINAL = block("ancient_terminal", () -> new WorldBlocks.Terminal(
            BlockBehaviour.Properties.of().mapColor(MapColor.STONE).strength(3F, 9F).sound(SoundType.STONE).lightLevel(s -> 8)), Rarity.RARE);
    public static final RegistrySupplier<Block> CRADLE = block("digitama_cradle", () -> new WorldBlocks.Cradle(
            BlockBehaviour.Properties.of().mapColor(MapColor.WOOD).strength(1F).sound(SoundType.WOOD).noOcclusion(), false), Rarity.UNCOMMON);
    public static final RegistrySupplier<Block> WILD_CRADLE = block("wild_digitama_cradle", () -> new WorldBlocks.Cradle(
            BlockBehaviour.Properties.of().mapColor(MapColor.WOOD).strength(1F).sound(SoundType.WOOD).noOcclusion(), true), Rarity.UNCOMMON);
    public static final RegistrySupplier<Item> DARK_SPORE = item("dark_spore", () -> new DarkSporeItem(props().stacksTo(16).rarity(Rarity.EPIC)));
    public static final RegistrySupplier<Item> DIGI_CORE = item("digi_core", () -> new TooltipItem(props().rarity(Rarity.RARE)));

    // --- Crests and the Tag --------------------------------------------------------------------------------------------
    public static final RegistrySupplier<Item> TAG = item("digimon_tag", () -> new Crests.TagItem(props().stacksTo(1).rarity(Rarity.RARE)));
    public static final Map<String, RegistrySupplier<Item>> CRESTS = new java.util.LinkedHashMap<>();

    static {
        for (String c : Crests.CRESTS) CRESTS.put(c, item("crest_of_" + c, () -> new Crests.CrestItem(props().stacksTo(1).rarity(Rarity.EPIC), c)));
    }

    // --- Tamer life (0.16.0): Digizoid gear, the Digi-Farm, harnesses ---------------------------------------------------
    static {
        DigizoidGear.register(Digital::item);
    }

    public static final RegistrySupplier<Block> FARM_TERMINAL = block("digi_farm_terminal", () -> new DigiFarm.TerminalBlock(
            BlockBehaviour.Properties.of().mapColor(MapColor.METAL).strength(3F, 6F).sound(SoundType.METAL).lightLevel(s -> 6)), Rarity.RARE);
    @SuppressWarnings("DataFlowIssue")
    public static final RegistrySupplier<net.minecraft.world.level.block.entity.BlockEntityType<DigiFarm.TerminalEntity>> FARM_ENTITY =
            BLOCK_ENTITIES.register("digi_farm_terminal", () -> net.minecraft.world.level.block.entity.BlockEntityType.Builder
                    .of(DigiFarm.TerminalEntity::new, FARM_TERMINAL.get()).build(null));
    public static final RegistrySupplier<Item> HARNESS = item("chest_harness", () -> new PartnerUtility.HarnessItem(props().stacksTo(1)));

    // --- Spirit Evolution and Bio-Merge (0.17.0) ---------------------------------------------------------------------------
    public static final Map<String, RegistrySupplier<Item>> SPIRIT_ITEMS = new java.util.LinkedHashMap<>();

    static {
        for (String e : SpiritEvolution.ELEMENTS) {
            SPIRIT_ITEMS.put(e + "_human", item("human_spirit_of_" + e, () ->
                    new SpiritEvolution.SpiritItem(props().stacksTo(1).rarity(Rarity.EPIC), e, false)));
            SPIRIT_ITEMS.put(e + "_beast", item("beast_spirit_of_" + e, () ->
                    new SpiritEvolution.SpiritItem(props().stacksTo(1).rarity(Rarity.EPIC), e, true)));
        }
    }

    /** The spirit's hotbar items (not in the creative tab: they only exist while a spirit is active). */
    public static final RegistrySupplier<Item> SPIRIT_ATTACK = ITEMS.register("spirit_attack", () ->
            new SpiritEvolution.SpiritAttack(props().stacksTo(1).rarity(Rarity.EPIC)));

    // --- Chrome Digizoid ------------------------------------------------------------------------------------------------
    public static final RegistrySupplier<Block> CHROME_ORE = BLOCKS.register("chrome_digizoid_ore", () ->
            new DropExperienceBlock(UniformInt.of(3, 7), BlockBehaviour.Properties.ofFullCopy(Blocks.DIAMOND_ORE)));
    public static final RegistrySupplier<Block> DEEPSLATE_CHROME_ORE = BLOCKS.register("deepslate_chrome_digizoid_ore", () ->
            new DropExperienceBlock(UniformInt.of(3, 7), BlockBehaviour.Properties.ofFullCopy(Blocks.DEEPSLATE_DIAMOND_ORE)));
    public static final RegistrySupplier<Block> CHROME_BLOCK = BLOCKS.register("chrome_digizoid_block", () ->
            new Block(BlockBehaviour.Properties.ofFullCopy(Blocks.NETHERITE_BLOCK).mapColor(MapColor.COLOR_LIGHT_GRAY)));
    public static final RegistrySupplier<Item> CHROME_ORE_ITEM = item("chrome_digizoid_ore", () -> new BlockItem(CHROME_ORE.get(), props()));
    public static final RegistrySupplier<Item> DEEPSLATE_CHROME_ORE_ITEM = item("deepslate_chrome_digizoid_ore", () ->
            new BlockItem(DEEPSLATE_CHROME_ORE.get(), props()));
    public static final RegistrySupplier<Item> RAW_CHROME = item("raw_chrome_digizoid", () -> new Item(props()));
    public static final RegistrySupplier<Item> CHROME_INGOT = item("chrome_digizoid_ingot", () -> new Item(props().rarity(Rarity.RARE)));
    public static final RegistrySupplier<Item> CHROME_BLOCK_ITEM = item("chrome_digizoid_block", () ->
            new BlockItem(CHROME_BLOCK.get(), props().rarity(Rarity.RARE)));
    public static final ResourceKey<PlacedFeature> CHROME_ORE_PLACED =
            ResourceKey.create(Registries.PLACED_FEATURE, ResourceLocation.fromNamespaceAndPath(MOD_ID, "chrome_digizoid_ore"));

    private static boolean bagItemsAdded;
    private static net.minecraft.server.MinecraftServer server;

    /** The running server (null on a client between worlds). */
    public static net.minecraft.server.MinecraftServer server() {
        return server;
    }

    private Digital() {
    }

    public static void init() {
        TABS.register();
        BLOCKS.register();
        ITEMS.register();
        BLOCK_ENTITIES.register();
        for (RegistrySupplier<Item> i : TAB_ITEMS) CreativeTabRegistry.append(TAB, i);
        // battle bag items (used on your battling Digimon): Cobblemon only lists the items it registers itself
        dev.architectury.event.events.common.LifecycleEvent.SERVER_STARTING.register(server -> {
            if (bagItemsAdded) return;
            bagItemsAdded = true;
            var bag = com.cobblemon.mod.common.battles.BagItems.INSTANCE.getBagItems();
            bag.add(com.cobblemon.mod.common.api.Priority.NORMAL, (Digivice) DIGIVICE.get());
            for (RegistrySupplier<Item> c : CARD_ITEMS.values()) bag.add(com.cobblemon.mod.common.api.Priority.NORMAL, (DigiModifyCard) c.get());
        });
        BiomeModifications.addProperties(ctx -> ctx.hasTag(BiomeTags.IS_OVERWORLD),
                (ctx, props) -> props.getGenerationProperties().addFeature(GenerationStep.Decoration.UNDERGROUND_ORES, CHROME_ORE_PLACED));
        DigitalRules.init();
        DigitalEvents.init();
        Training.init();
        CatchRules.init();
        DarkAura.init();
        GlitchLook.init();
        Scheduler.init();
        DarkTower.init();
        DigitalWorld.init();
        BlackMarket.init();
        Crests.init();
        Raids.init();
        DigitalCommand.init();
        DigizoidGear.init();
        PartnerUtility.init();
        Tamers.init();
        SpiritEvolution.init();
        dev.architectury.event.events.common.LifecycleEvent.SERVER_STARTING.register(s -> server = s);
        dev.architectury.event.events.common.LifecycleEvent.SERVER_STOPPED.register(s -> server = null);
        // the gamerules (registered on class load)
        Digital.LOG.debug("gamerules {} {}", Raids.DIGITIZATION, MoveEffects.GRIEFING);
        if (dev.architectury.platform.Platform.getEnvironment() == dev.architectury.utils.Env.CLIENT) DigitalClient.init();
        dev.architectury.event.events.common.LifecycleEvent.SERVER_STARTED.register(server -> DigitalEngine.installNow());
    }
}
