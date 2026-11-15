package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.item.PokeBallItem;
import com.cobblemon.mod.common.pokeball.PokeBall;
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
 * CobbleEffort: Digital. A Digimon crossover for Cobblemon: the Digimon themselves are species in CobbleEffort (label
 * "digimon"; they spawn, battle and evolve like any Pokémon); this add-on brings what needs code: the Digiball (a real
 * Cobblemon Poké Ball, three times as good on Digimon) and Digitama, Digi-Eggs that warm up in your inventory and
 * hatch a baby Digimon.
 */
public final class Digital {
    public static final String MOD_ID = "cobbleeffort_digital";
    public static final org.slf4j.Logger LOG = org.slf4j.LoggerFactory.getLogger("CobbleEffort Digital");

    /** The Digiball, in Cobblemon's own Poké Ball registry before any item is made (see DigiBall). */
    public static final PokeBall DIGIBALL_BALL = DigiBall.register();

    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(MOD_ID, Registries.ITEM);

    public static final RegistrySupplier<Item> DIGIBALL = ITEMS.register("digiball", () -> {
        PokeBallItem item = new PokeBallItem(DIGIBALL_BALL);
        DIGIBALL_BALL.item = item;
        return item;
    });
    public static final RegistrySupplier<Item> DIGITAMA = ITEMS.register("digitama", () ->
            new DigitamaItem(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON).arch$tab(Digital.TAB)));

    public static final RegistrySupplier<CreativeModeTab> TAB = TABS.register("digital", () ->
            CreativeTabRegistry.create(Component.translatable("itemGroup." + MOD_ID), () -> new ItemStack(Digital.DIGIBALL.get())));

    private Digital() {
    }

    public static void init() {
        TABS.register();
        ITEMS.register();
        CreativeTabRegistry.append(TAB, DIGIBALL);
        DigitalEvents.init();
    }
}
