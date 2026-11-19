package io.github.cobbleeffort.digital.mixin;

import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import io.github.cobbleeffort.digital.SpiritEvolution;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * A Spirit Evolution / Bio-Merge costume (the Digimon drawn round a transformed player) can't be clicked or hit: the
 * player's crosshair, punches and projectiles go straight through it. Both sides read the synced aspect.
 */
@Mixin(LivingEntity.class)
public abstract class CostumePickMixin {
    @Inject(method = "isPickable", at = @At("HEAD"), cancellable = true)
    private void cobbleeffortDigital$costume(CallbackInfoReturnable<Boolean> cir) {
        if ((Object) this instanceof PokemonEntity e && e.getAspects().contains(SpiritEvolution.COSTUME_ASPECT)) cir.setReturnValue(false);
    }
}
