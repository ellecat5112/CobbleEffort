package io.github.cobbleeffort.kanto;

import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.Util;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;

/**
 * Kantonian armor: a plain set from Kantonian ingots, and outfits, each crafted with a dye or wool of its colour in the
 * armor shape's gap (see the add-on's recipes). Every outfit is its own armor material (same stats, its own look).
 * Stats sit between iron and diamond.
 */
public final class KantoArmor {
    /** The outfits, by id (the colour is only used by the recipes and textures, in tools/make_assets.py). */
    public static final String[] OUTFITS = {"trainer", "ace", "professor", "hiker", "swimmer", "biker", "bug_catcher", "engineer", "psychic"};
    public static final DeferredRegister<ArmorMaterial> MATERIALS = DeferredRegister.create(Kanto.MOD_ID, Registries.ARMOR_MATERIAL);
    public static final List<RegistrySupplier<Item>> PIECES = new ArrayList<>();
    private static final int DURABILITY = 20;      // iron 15, diamond 33

    private KantoArmor() {
    }

    private static RegistrySupplier<ArmorMaterial> material(String id) {
        return MATERIALS.register(id, () -> new ArmorMaterial(
                Util.make(new EnumMap<>(ArmorItem.Type.class), m -> {
                    m.put(ArmorItem.Type.BOOTS, 2);
                    m.put(ArmorItem.Type.LEGGINGS, 6);
                    m.put(ArmorItem.Type.CHESTPLATE, 7);
                    m.put(ArmorItem.Type.HELMET, 2);
                    m.put(ArmorItem.Type.BODY, 6);
                }),
                12, SoundEvents.ARMOR_EQUIP_IRON, () -> Ingredient.of(Kanto.INGOT.get()),
                List.of(new ArmorMaterial.Layer(Kanto.id(id))), 1.0F, 0.0F));
    }

    private static void set(String id) {
        RegistrySupplier<ArmorMaterial> material = material(id);
        for (ArmorItem.Type type : new ArmorItem.Type[]{ArmorItem.Type.HELMET, ArmorItem.Type.CHESTPLATE, ArmorItem.Type.LEGGINGS, ArmorItem.Type.BOOTS}) {
            PIECES.add(Kanto.ITEMS.register(id + "_" + type.getName(), () -> new ArmorItem(material, type,
                    new Item.Properties().durability(type.getDurability(DURABILITY)).arch$tab(Kanto.TAB))));
        }
    }

    /** Called from Kanto's static setup, before the registers register. */
    static void setup() {
        set("kantonian");
        for (String outfit : OUTFITS) set("kantonian_" + outfit);
    }
}
