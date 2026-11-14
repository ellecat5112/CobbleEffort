package io.github.cobbleeffort.distortion.mixin;

import io.github.cobbleeffort.distortion.client.AlignmentLook;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Crystal Pokémon are see-through: their (recoloured, partly transparent) body renders translucent. */
@Mixin(LivingEntityRenderer.class)
public abstract class AlignRenderTypeMixin {
    @SuppressWarnings({"unchecked", "rawtypes"})
    @Inject(method = "getRenderType", at = @At("RETURN"), cancellable = true)
    private void cobbleeffortDistortion$crystal(LivingEntity entity, boolean bodyVisible, boolean translucent, boolean glowing,
                                                CallbackInfoReturnable<RenderType> cir) {
        if (cir.getReturnValue() == null || glowing) return;
        ResourceLocation tex = ((LivingEntityRenderer) (Object) this).getTextureLocation(entity);
        if (AlignmentLook.isCrystalTexture(tex)) cir.setReturnValue(RenderType.entityTranslucent(tex));
    }
}
