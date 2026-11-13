package io.github.cobbleeffort.fusion;

import dev.architectury.platform.Platform;
import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import dev.architectury.utils.Env;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;

/**
 * CobbleEffort: Fusion. Pokémon Infinite Fusion's DNA Splicers for Cobblemon: fuse two party Pokémon into one, HEAD
 * and BODY (FusionRules), unfuse them again (Fusing), battle as the fusion (FusionEngine) and see the head on the
 * body (client/FusionRender: the head species' head bones drawn on the body's head joint, automatically, for any
 * pair).
 */
public final class Fusion {
    public static final String MOD_ID = "cobbleeffort_fusion";
    public static final org.slf4j.Logger LOG = org.slf4j.LoggerFactory.getLogger("CobbleEffort Fusion");

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);

    public static final RegistrySupplier<Item> SPLICERS = ITEMS.register("dna_splicers", () ->
            new SplicerItem(SplicerItem.Kind.SPLICERS, new Item.Properties().stacksTo(16).arch$tab(Fusion.TAB)));
    public static final RegistrySupplier<Item> SUPER = ITEMS.register("super_splicers", () ->
            new SplicerItem(SplicerItem.Kind.SUPER, new Item.Properties().stacksTo(16).rarity(Rarity.RARE).arch$tab(Fusion.TAB)));
    public static final RegistrySupplier<Item> INFINITE = ITEMS.register("infinite_splicers", () ->
            new SplicerItem(SplicerItem.Kind.INFINITE, new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).arch$tab(Fusion.TAB)));
    public static final RegistrySupplier<Item> REVERSERS = ITEMS.register("dna_reversers", () ->
            new SplicerItem(SplicerItem.Kind.REVERSERS, new Item.Properties().stacksTo(16).arch$tab(Fusion.TAB)));

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("fusion", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Fusion.SPLICERS.get())));

    private Fusion() {
    }

    public static void init() {
        TABS.register();
        ITEMS.register();
        FusionCommand.init();
        FusionDesigns.preload();
        if (Platform.getEnvironment() == Env.CLIENT) {
            io.github.cobbleeffort.fusion.client.FusionRender.init();
        }
    }
}
