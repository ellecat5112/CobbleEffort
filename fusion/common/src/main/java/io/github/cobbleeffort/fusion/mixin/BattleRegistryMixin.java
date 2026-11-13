package io.github.cobbleeffort.fusion.mixin;

import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.BattleFormat;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.battles.BattleSide;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import io.github.cobbleeffort.fusion.FusionEngine;
import io.github.cobbleeffort.fusion.FusionRules;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Before any battle starts, the engine learns every fused Pokémon in it (see FusionEngine). */
@Mixin(value = BattleRegistry.class, remap = false)
public abstract class BattleRegistryMixin {
    @Inject(method = "startBattle", at = @At("HEAD"), remap = false)
    private static void cobbleeffortFusion$register(BattleFormat format, BattleSide side1, BattleSide side2, boolean canPreempt,
                                                    CallbackInfoReturnable<?> cir) {
        try {
            for (BattleSide side : new BattleSide[]{side1, side2}) {
                for (BattleActor actor : side.getActors()) {
                    for (BattlePokemon bp : actor.getPokemonList()) {
                        if (FusionRules.isFused(bp.getEffectedPokemon())) FusionEngine.register(bp.getEffectedPokemon());
                    }
                }
            }
        } catch (Throwable ignored) {
            // never stop a battle from starting
        }
    }
}
