package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.client.gui.TypeIcon;
import com.mojang.blaze3d.vertex.PoseStack;
import io.github.cobbleeffort.distortion.client.AlignmentLook;
import net.minecraft.client.gui.GuiGraphics;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Cobblemon's type icons come from one 18-icon sheet: when a Shadow or Crystal type is shown, both icons are drawn here. */
@Mixin(value = TypeIcon.class, remap = false)
public abstract class TypeIconMixin {
    @Inject(method = "render", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$render(GuiGraphics context, CallbackInfo ci) {
        TypeIcon self = (TypeIcon) (Object) this;
        ElementalType type = self.getType(), second = self.getSecondaryType();
        if (!AlignmentLook.ours(type) && (second == null || !AlignmentLook.ours(second))) return;
        float scale = 0.5F;
        int diameter = self.getSmall() ? 18 : 36;
        float offsetX = self.getCenteredX() ? (diameter / 2F) * scale + (second != null ? self.getDoubleCenteredOffset() : 0F) : 0F;
        float x = self.getX().floatValue(), y = self.getY().floatValue();
        PoseStack pose = context.pose();
        pose.pushPose();
        pose.scale(scale, scale, 1F);
        if (second != null) {
            AlignmentLook.icon(pose, second, (x + self.getSecondaryOffset() - offsetX) / scale, y / scale, diameter, self.getSmall(), self.getOpacity());
        }
        AlignmentLook.icon(pose, type, (x - offsetX) / scale, y / scale, diameter, self.getSmall(), self.getOpacity());
        pose.popPose();
        ci.cancel();
    }
}
