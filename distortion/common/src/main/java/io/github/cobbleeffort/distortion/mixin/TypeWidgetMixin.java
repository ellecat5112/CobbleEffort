package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.client.gui.summary.widgets.type.TypeWidget;
import com.mojang.blaze3d.vertex.PoseStack;
import io.github.cobbleeffort.distortion.client.AlignmentLook;
import net.minecraft.client.gui.components.AbstractWidget;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** The summary's type badge: the Shadow and Crystal icons come from our sheet. */
@Mixin(value = TypeWidget.class, remap = false)
public abstract class TypeWidgetMixin {
    @Inject(method = "renderType(Lcom/cobblemon/mod/common/api/types/ElementalType;Lcom/mojang/blaze3d/vertex/PoseStack;II)V",
            at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$renderType(ElementalType type, PoseStack pose, int x, int y, CallbackInfo ci) {
        if (!AlignmentLook.ours(type)) return;
        AbstractWidget self = (AbstractWidget) (Object) this;
        AlignmentLook.icon(pose, type, x + 0.5F, y, Math.max(self.getWidth(), self.getHeight()), false, 1F);
        ci.cancel();
    }
}
