package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.distortion.Alignment;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.util.List;

/** A Shadow or Crystal Pokémon's types are [its first type, Shadow|Crystal], outside battle too (summary, PC, wheel). */
@Mixin(value = Pokemon.class, remap = false)
public abstract class AlignTypesMixin {
    @Inject(method = "getTypes", at = @At("RETURN"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$types(CallbackInfoReturnable<Iterable<ElementalType>> cir) {
        List<ElementalType> types = Alignment.types((Pokemon) (Object) this, cir.getReturnValue());
        if (types != null) cir.setReturnValue(types);
    }

    @Inject(method = "getSecondaryType", at = @At("RETURN"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$secondary(CallbackInfoReturnable<ElementalType> cir) {
        String flag = Alignment.of((Pokemon) (Object) this);
        if (flag != null) cir.setReturnValue(Alignment.typeOf(flag));
    }
}
