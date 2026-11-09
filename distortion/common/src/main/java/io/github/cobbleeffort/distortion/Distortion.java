package io.github.cobbleeffort.distortion;

import dev.architectury.registry.CreativeTabRegistry;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;

/**
 * CobbleEffort: Distortion. A battle gimmick: a Pokémon holding the Distortion Crystal, with its trainer
 * wearing the Distortion Band (in its own accessory slot), distorts: its types turn into their weaknesses, its ability
 * and moves follow, and its colours invert. See docs/distortion_design.md in the CobbleEffort repository.
 */
public final class Distortion {
    public static final String MOD_ID = "cobbleeffort_distortion";

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("distortion", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Distortion.BAND.get())));

    /** Worn in the "distortion_slot" accessory slot. */
    public static final RegistrySupplier<Item> BAND = ITEMS.register("distortion_band", () ->
            new Item(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).arch$tab(TAB)));

    /** Held by the Pokémon: one crystal works for every distortable Pokémon. */
    public static final RegistrySupplier<Item> CRYSTAL = ITEMS.register("distortion_crystal", () ->
            new Item(new Item.Properties().stacksTo(1).rarity(Rarity.RARE).arch$tab(TAB)));

    private Distortion() {
    }

    public static void init() {
        TABS.register();
        ITEMS.register();
        DistortionBattle.init();
    }
}
