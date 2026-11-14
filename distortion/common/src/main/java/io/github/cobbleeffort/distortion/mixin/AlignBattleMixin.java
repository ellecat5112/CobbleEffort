package io.github.cobbleeffort.distortion.mixin;

import com.cobblemon.mod.common.battles.BattleFormat;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.battles.BattleSide;
import io.github.cobbleeffort.distortion.AlignmentEngine;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Before any battle starts, the engine learns every Shadow/Crystal Pokémon in it (see AlignmentEngine). */
@Mixin(value = BattleRegistry.class, remap = false)
public abstract class AlignBattleMixin {
    @Inject(method = "startBattle", at = @At("HEAD"), remap = false)
    private static void cobbleeffortDistortion$align(BattleFormat format, BattleSide side1, BattleSide side2, boolean canPreempt,
                                                     CallbackInfoReturnable<?> cir) {
        try {
            AlignmentEngine.prepare(side1, side2);
        } catch (Throwable ignored) {
            // never stop a battle from starting
        }
    }
}
