package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;

/** Shared checks for items used on your own sent-out Pokémon (fragments, chips, food). */
final class PartnerUse {
    private PartnerUse() {
    }

    /** The Pokémon if `target` is the player's own, out of battle; else tells the player why not and returns null. */
    static Pokemon own(Player player, LivingEntity target, boolean digimonOnly) {
        if (!(target instanceof PokemonEntity entity) || !(player instanceof ServerPlayer sp)) return null;
        Pokemon p = entity.getPokemon();
        String m = Digital.MOD_ID + ".use.";
        if (!player.getUUID().equals(p.getOwnerUUID())) {
            player.displayClientMessage(Component.translatable(m + "not_yours"), true);
            return null;
        }
        if (entity.isBattling() || BattleRegistry.getBattleByParticipatingPlayer(sp) != null) {
            player.displayClientMessage(Component.translatable(m + "in_battle"), true);
            return null;
        }
        if (digimonOnly && !Attributes.isDigimon(p)) {
            player.displayClientMessage(Component.translatable(m + "not_digimon", p.getDisplayName(false)), true);
            return null;
        }
        return p;
    }

    static void particles(LivingEntity e, ParticleOptions particle, int count) {
        if (e.level() instanceof ServerLevel server) {
            server.sendParticles(particle, e.getX(), e.getY() + e.getBbHeight() / 2, e.getZ(), count,
                    e.getBbWidth() / 2, e.getBbHeight() / 2, e.getBbWidth() / 2, 0.05);
        }
    }
}
