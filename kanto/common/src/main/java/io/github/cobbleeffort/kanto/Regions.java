package io.github.cobbleeffort.kanto;

import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.phys.shapes.Shapes;

import java.util.EnumMap;
import java.util.Map;
import java.util.function.Supplier;

/**
 * Each region's portal block, found in its landmark (structures in tools/make_regions.py, generated in the overworld and
 * any dimension with the right biomes): Johto's bell (the pagoda), Hoenn's statue stone (the Groudon statue in the
 * granite cave), Sinnoh's boarded doorway (the old manor's basement), Unova's golden wardrobe (the castle), Kalos's
 * giant Poké Ball (the ball factory), Alola's telescope (the observatory), Galar's engraved bark (the giant tree by the
 * shrine) and Paldea's academy PC (the academy's front desk).
 */
public final class Regions {
    public static final Map<Region, RegistrySupplier<Block>> PORTALS = new EnumMap<>(Region.class);

    private Regions() {
    }

    private static BlockBehaviour.Properties like(Block block) {
        return BlockBehaviour.Properties.ofFullCopy(block).strength(3F, 1200F);
    }

    private static void portal(Region region, String name, Supplier<Block> block) {
        RegistrySupplier<Block> b = Kanto.BLOCKS.register(name, block);
        Kanto.ITEMS.register(name, () -> new BlockItem(b.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(Kanto.TAB)));
        PORTALS.put(region, b);
    }

    static void register() {
        portal(Region.HISUI, "hisui_arceus_statue", () -> new RegionPortalBlock.Plain(Region.HISUI, SoundEvents.BEACON_POWER_SELECT, null,
                like(Blocks.CALCITE).lightLevel(st -> 4)));
        portal(Region.JOHTO, "johto_bell", () -> new RegionPortalBlock.Plain(Region.JOHTO, SoundEvents.BELL_BLOCK,
                Shapes.or(Block.box(3, 0, 3, 13, 3, 13), Block.box(4, 3, 4, 12, 12, 12), Block.box(6, 12, 6, 10, 16, 10)),
                like(Blocks.BELL).noOcclusion()));
        portal(Region.HOENN, "hoenn_statue_stone", () -> new RegionPortalBlock.Plain(Region.HOENN, SoundEvents.PORTAL_TRIGGER, null,
                like(Blocks.GRANITE)));
        portal(Region.SINNOH, "sinnoh_boarded_doorway", () -> new RegionPortalBlock.Tall(Region.SINNOH, SoundEvents.WOODEN_DOOR_OPEN,
                like(Blocks.DARK_OAK_PLANKS)));
        portal(Region.UNOVA, "unova_wardrobe", () -> new RegionPortalBlock.Tall(Region.UNOVA, SoundEvents.CHEST_OPEN,
                like(Blocks.GOLD_BLOCK)));
        portal(Region.KALOS, "kalos_ball_shell", () -> new RegionPortalBlock.Parts(Region.KALOS, SoundEvents.IRON_DOOR_OPEN,
                like(Blocks.IRON_BLOCK)));
        portal(Region.ALOLA, "alola_telescope", () -> new RegionPortalBlock.Plain(Region.ALOLA, SoundEvents.AMETHYST_BLOCK_CHIME, null,
                like(Blocks.WHITE_CONCRETE)));
        portal(Region.GALAR, "galar_engraved_bark", () -> new RegionPortalBlock.Facing(Region.GALAR, SoundEvents.BEACON_ACTIVATE, null,
                like(Blocks.DARK_OAK_PLANKS).mapColor(MapColor.COLOR_BROWN)));   // not the log's: its colour reads "axis"
        portal(Region.PALDEA, "paldea_pc", () -> new RegionPortalBlock.Facing(Region.PALDEA, SoundEvents.UI_BUTTON_CLICK.value(),
                Shapes.or(Block.box(1, 0, 1, 15, 2, 15), Block.box(1, 2, 7, 15, 14, 10)), like(Blocks.IRON_BLOCK).noOcclusion()
                .lightLevel(s -> 7)));
    }
}
