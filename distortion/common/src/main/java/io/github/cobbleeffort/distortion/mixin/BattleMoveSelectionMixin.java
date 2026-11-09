package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.client.battle.SingleActionRequest;
import com.cobblemon.mod.common.client.gui.battle.BattleGUI;
import com.cobblemon.mod.common.client.gui.battle.subscreen.BattleGimmickButton;
import com.cobblemon.mod.common.client.gui.battle.subscreen.BattleMoveSelection;
import io.github.cobbleeffort.distortion.client.DistortButton;
import net.minecraft.client.gui.GuiGraphics;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Adds the Distort button to Cobblemon's move selection (its own gimmick buttons are a fixed set). */
@Mixin(BattleMoveSelection.class)
public abstract class BattleMoveSelectionMixin {
    @Unique
    private DistortButton cobbleeffortDistortion$button;

    @Inject(method = "<init>", at = @At("TAIL"), remap = false)
    private void cobbleeffortDistortion$create(BattleGUI gui, SingleActionRequest request, CallbackInfo ci) {
        try {
            cobbleeffortDistortion$button = DistortButton.create((BattleMoveSelection) (Object) this);
        } catch (Throwable t) {
            cobbleeffortDistortion$button = null;           // never break the move selection
        }
    }

    @Inject(method = "renderWidget", at = @At("TAIL"))
    private void cobbleeffortDistortion$render(GuiGraphics graphics, int mouseX, int mouseY, float delta, CallbackInfo ci) {
        if (cobbleeffortDistortion$button != null) cobbleeffortDistortion$button.render(graphics, mouseX, mouseY);
    }

    @Inject(method = "mousePrimaryClicked", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortDistortion$click(double mouseX, double mouseY, CallbackInfoReturnable<Boolean> cir) {
        DistortButton button = cobbleeffortDistortion$button;
        if (button == null) return;
        BattleMoveSelection self = (BattleMoveSelection) (Object) this;
        if (button.isHovered(mouseX, mouseY)) {
            for (BattleGimmickButton other : self.getGimmickButtons()) other.setToggled(false);
            self.setMoveTiles(button.toggle() ? button.tiles : self.getBaseTiles());
            cir.setReturnValue(false);
            return;
        }
        for (BattleGimmickButton other : self.getGimmickButtons()) {
            if (other.isHovered(mouseX, mouseY)) button.toggled = false;   // another gimmick takes over
        }
    }
}
