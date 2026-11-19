package io.github.cobbleeffort.digital;

import com.mojang.serialization.MapCodec;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.CropBlock;

import java.util.function.Supplier;

/** A crop like carrots whose seed is its own harvest: Digi-Meat and Super Carrots. Drops are in its loot table. */
public class DigiCropBlock extends CropBlock {
    private final Supplier<Item> seed;

    public DigiCropBlock(Properties properties, Supplier<Item> seed) {
        super(properties);
        this.seed = seed;
    }

    @Override
    public MapCodec<? extends CropBlock> codec() {
        return simpleCodec(p -> new DigiCropBlock(p, seed));
    }

    @Override
    protected ItemLike getBaseSeedId() {
        return seed.get();
    }
}
