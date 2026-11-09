package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.battles.ActiveBattlePokemon;
import com.cobblemon.mod.common.battles.MoveActionResponse;
import com.cobblemon.mod.common.battles.ShowdownMoveset;
import io.github.cobbleeffort.distortion.DistortionBattle;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Cobblemon only accepts the gimmick ids of its own gimmicks. A move chosen with the "distort" gimmick is valid when
 * the move itself is valid (checked as an ordinary move) and the trainer wears the Distortion Band; Showdown then
 * checks the Pokémon (crystal, a distorted forme, once per battle).
 */
@Mixin(value = MoveActionResponse.class, remap = false)
public abstract class MoveActionResponseMixin {
    @Inject(method = "isValid", at = @At("HEAD"), cancellable = true)
    private void cobbleeffortDistortion$allowDistort(ActiveBattlePokemon active, ShowdownMoveset moveset, boolean forceSwitch,
                                                     CallbackInfoReturnable<Boolean> cir) {
        MoveActionResponse self = (MoveActionResponse) (Object) this;
        if (!DistortionBattle.GIMMICK.equals(self.getGimmickID())) return;
        boolean valid;
        self.setGimmickID(null);
        try {
            valid = self.isValid(active, moveset, forceSwitch);
        } finally {
            self.setGimmickID(DistortionBattle.GIMMICK);
        }
        cir.setReturnValue(valid && DistortionBattle.trainerMayDistort(active));
    }
}
