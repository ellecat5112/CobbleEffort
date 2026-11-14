package io.github.cobbleeffort.kanto.mixin;

import io.github.cobbleeffort.kanto.Ashtray;
import net.minecraft.core.Holder;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;
import net.minecraft.world.level.biome.MultiNoiseBiomeSource;
import net.minecraft.world.level.biome.MultiNoiseBiomeSourceParameterLists;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.stream.Stream;

/**
 * The overworld's biome source (only the vanilla overworld preset, not the Kanto regions' own lists): patches of some
 * host biomes become the Ashtray Wastes, and the biome joins the source's possible biomes so its features generate.
 */
@Mixin(MultiNoiseBiomeSource.class)
public abstract class MultiNoiseBiomeSourceMixin {
    @Unique
    private Boolean cobbleeffortKanto$overworld;

    @Unique
    private boolean cobbleeffortKanto$isOverworld() {
        if (cobbleeffortKanto$overworld == null) {
            cobbleeffortKanto$overworld = ((MultiNoiseBiomeSource) (Object) this).stable(MultiNoiseBiomeSourceParameterLists.OVERWORLD);
        }
        return cobbleeffortKanto$overworld;
    }

    @Inject(method = "getNoiseBiome(IIILnet/minecraft/world/level/biome/Climate$Sampler;)Lnet/minecraft/core/Holder;",
            at = @At("RETURN"), cancellable = true)
    private void cobbleeffortKanto$ashtray(int x, int y, int z, Climate.Sampler sampler, CallbackInfoReturnable<Holder<Biome>> cir) {
        if (!cobbleeffortKanto$isOverworld()) return;
        Holder<Biome> swapped = Ashtray.swap(cir.getReturnValue(), x, z);
        if (swapped != null) cir.setReturnValue(swapped);
    }

    @Inject(method = "collectPossibleBiomes", at = @At("RETURN"), cancellable = true)
    private void cobbleeffortKanto$possible(CallbackInfoReturnable<Stream<Holder<Biome>>> cir) {
        Holder<Biome> ours = Ashtray.holder();
        if (ours == null || !cobbleeffortKanto$isOverworld()) return;
        cir.setReturnValue(Stream.concat(cir.getReturnValue(), Stream.of(ours)));
    }
}
