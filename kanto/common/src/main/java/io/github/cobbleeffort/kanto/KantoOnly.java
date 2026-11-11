package io.github.cobbleeffort.kanto;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.levelgen.placement.PlacementContext;
import net.minecraft.world.level.levelgen.placement.PlacementFilter;
import net.minecraft.world.level.levelgen.placement.PlacementModifierType;

/** A placement filter (cobbleeffort_kanto:in_kanto): the feature only places in the Kanto dimension (Kantonian ore). */
public final class KantoOnly extends PlacementFilter {
    public static final KantoOnly INSTANCE = new KantoOnly();
    public static final MapCodec<KantoOnly> CODEC = MapCodec.unit(INSTANCE);

    private KantoOnly() {
    }

    @Override
    protected boolean shouldPlace(PlacementContext context, RandomSource random, BlockPos pos) {
        return context.getLevel().getLevel().dimension() == Kanto.KANTO;
    }

    @Override
    public PlacementModifierType<?> type() {
        return Kanto.IN_KANTO.get();
    }
}
