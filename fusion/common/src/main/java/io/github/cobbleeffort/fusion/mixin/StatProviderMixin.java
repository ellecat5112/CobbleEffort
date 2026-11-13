package io.github.cobbleeffort.fusion.mixin;

import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.stat.CobblemonStatProvider;
import io.github.cobbleeffort.fusion.FusionStats;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Fused Pokémon's stats come from the fused base stats (server and client, so the summary shows them too). */
@Mixin(value = CobblemonStatProvider.class, remap = false)
public abstract class StatProviderMixin {
    @Inject(method = "getStatForPokemon", at = @At("HEAD"), cancellable = true, remap = false)
    private void cobbleeffortFusion$stat(Pokemon pokemon, Stat stat, CallbackInfoReturnable<Integer> cir) {
        Integer fused = FusionStats.stat(pokemon, stat);
        if (fused != null) cir.setReturnValue(fused);
    }
}
