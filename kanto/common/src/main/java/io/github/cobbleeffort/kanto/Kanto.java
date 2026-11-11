package io.github.cobbleeffort.kanto;

import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
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
        BLOCKS.register();
        ITEMS.register();
        KantoEvents.init();
    }
}
