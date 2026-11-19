package io.github.cobbleeffort.digital.mixin;

import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.battles.interpreter.instructions.MoveInstruction;
import io.github.cobbleeffort.digital.MoveEffects;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Every move used in a battle: Digimon attacks show (and, with the gamerule, have) effects in the world. */
@Mixin(value = MoveInstruction.class, remap = false)
public abstract class MoveInstructionMixin {
    @Inject(method = "invoke", at = @At("TAIL"), remap = false)
    private void cobbleeffortDigital$worldEffect(PokemonBattle battle, CallbackInfo ci) {
        try {
            MoveInstruction self = (MoveInstruction) (Object) this;
            MoveEffects.used(self.getMove(), self.getUserPokemon(), self.getTargetPokemon());
        } catch (Throwable ignored) {
            // never break a battle
        }
    }
}
