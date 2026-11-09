package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.api.battles.model.actor.AIBattleActor;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.ActiveBattlePokemon;
import com.cobblemon.mod.common.battles.MoveActionResponse;
import com.cobblemon.mod.common.battles.ShowdownActionResponse;
import io.github.cobbleeffort.distortion.DistortionBattle;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.List;

/**
 * Wild Pokémon and NPC trainers (AI actors) distort too: when their AI picks a move for a Pokémon that can distort
 * (it holds the Distortion Crystal, or is Arceus holding a plate, and has Distorted forms) and their side hasn't
 * distorted yet, the move goes with the "distort" gimmick. The Showdown side script falls back to the plain move if
 * it can't distort after all, so an AI's choice is never rejected.
 */
@Mixin(value = BattleActor.class, remap = false)
public abstract class AIDistortMixin {
    @Inject(method = "setActionResponses", at = @At("HEAD"))
    private void cobbleeffortDistortion$aiDistorts(List<? extends ShowdownActionResponse> responses, CallbackInfo ci) {
        try {
            BattleActor self = (BattleActor) (Object) this;
            if (!(self instanceof AIBattleActor)) return;
            List<ActiveBattlePokemon> active = self.getActivePokemon();
            for (int i = 0; i < responses.size() && i < active.size(); i++) {
                if (responses.get(i) instanceof MoveActionResponse move && move.getGimmickID() == null
                        && DistortionBattle.aiMayDistort(self, active.get(i))) {
                    move.setGimmickID(DistortionBattle.GIMMICK);
                    return;                                       // one per side
                }
            }
        } catch (Throwable t) {
            DistortionBattle.LOG.error("AI distortion check failed", t);
        }
    }
}
