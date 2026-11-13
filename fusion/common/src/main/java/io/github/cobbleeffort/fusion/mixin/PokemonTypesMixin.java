package io.github.cobbleeffort.fusion.mixin;

import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.fusion.FusionStats;
import java.util.List;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A fused Pokémon's types are the fusion's (Infinite Fusion's rule), outside battle too. */
@Mixin(value = Pokemon.class, remap = false)
public abstract class PokemonTypesMixin {
    @Inject(method = "getTypes", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortFusion$types(CallbackInfoReturnable<Iterable<ElementalType>> cir) {
        List<ElementalType> types = FusionStats.types((Pokemon) (Object) this);
        if (types != null) cir.setReturnValue(types);
    }

    @Inject(method = "getPrimaryType", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortFusion$primary(CallbackInfoReturnable<ElementalType> cir) {
        List<ElementalType> types = FusionStats.types((Pokemon) (Object) this);
        if (types != null) cir.setReturnValue(types.get(0));
    }

    @Inject(method = "getSecondaryType", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortFusion$secondary(CallbackInfoReturnable<ElementalType> cir) {
        List<ElementalType> types = FusionStats.types((Pokemon) (Object) this);
        if (types != null) cir.setReturnValue(types.size() > 1 ? types.get(1) : null);
    }
}
