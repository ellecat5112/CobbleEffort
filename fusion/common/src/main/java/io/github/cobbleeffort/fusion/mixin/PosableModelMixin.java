package io.github.cobbleeffort.fusion.mixin;

import com.cobblemon.mod.common.client.render.models.blockbench.PosableModel;
import com.cobblemon.mod.common.client.render.models.blockbench.repository.RenderContext;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import io.github.cobbleeffort.fusion.client.FusionRender;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Around every posable model render: a fusion's body is drawn without its head, then the head species' head on it. */
@Mixin(value = PosableModel.class, remap = false)
public abstract class PosableModelMixin {
    @Inject(method = "render", at = @At("HEAD"), remap = false)
    private void cobbleeffortFusion$before(RenderContext context, PoseStack stack, VertexConsumer buffer, int light, int overlay,
                                          int color, CallbackInfo ci) {
        FusionRender.before((PosableModel) (Object) this);
    }

    @Inject(method = "render", at = @At("RETURN"), remap = false)
    private void cobbleeffortFusion$after(RenderContext context, PoseStack stack, VertexConsumer buffer, int light, int overlay,
                                         int color, CallbackInfo ci) {
        FusionRender.after((PosableModel) (Object) this, stack, light, overlay, color);
    }
}
