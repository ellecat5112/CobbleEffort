package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.client.render.models.blockbench.PosableState;
import com.cobblemon.mod.common.client.render.models.blockbench.repository.VaryingModelRepository;
import io.github.cobbleeffort.distortion.client.AlignmentLook;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A Shadow or Crystal Pokémon's texture, recoloured (every renderer looks textures up here: world, summary, PC, battle). */
@Mixin(value = VaryingModelRepository.class, remap = false, priority = 1100)   // after Fusion's recolour
public abstract class AlignTextureMixin {
    @Inject(method = "getTexture", at = @At("RETURN"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$texture(ResourceLocation name, PosableState state, CallbackInfoReturnable<ResourceLocation> cir) {
        ResourceLocation aligned = AlignmentLook.texture(state, cir.getReturnValue());
        if (aligned != null) cir.setReturnValue(aligned);
    }
}
