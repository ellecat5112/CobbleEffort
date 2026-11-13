package io.github.cobbleeffort.fusion.mixin;

import com.cobblemon.mod.common.client.render.models.blockbench.PosableState;
import com.cobblemon.mod.common.client.render.models.blockbench.repository.VaryingModelRepository;
import io.github.cobbleeffort.fusion.client.FusionRender;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A fusion body's texture, recoloured by its Infinite Fusion design (every renderer looks textures up here). */
@Mixin(value = VaryingModelRepository.class, remap = false)
public abstract class TextureMixin {
    @Inject(method = "getTexture", at = @At("RETURN"), cancellable = true, remap = false)
    private void cobbleeffortFusion$texture(ResourceLocation name, PosableState state, CallbackInfoReturnable<ResourceLocation> cir) {
        ResourceLocation fused = FusionRender.bodyTexture(name, state, cir.getReturnValue());
        if (fused != null) cir.setReturnValue(fused);
    }
}
