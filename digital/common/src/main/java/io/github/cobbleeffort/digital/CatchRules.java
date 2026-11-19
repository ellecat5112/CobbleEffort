package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.pokeball.PokeBall;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Player;

/**
 * Ultimate- and Mega-level Digimon (Perfect, Ultimate, Super Ultimate) are too much data for an ordinary ball: in the
 * wild only the Chrome Digizoid Ball (or a guaranteed ball such as the Master Ball) can catch them.
 */
final class CatchRules {
    private CatchRules() {
    }

    static void init() {
        CobblemonEvents.POKEMON_CATCH_RATE.subscribe(Priority.LOW, event -> {
            try {
                Pokemon p = event.getPokemonEntity().getPokemon();
                if (!Attributes.isDigimon(p) || !DigiBall.hasAny(p, DigiBall.MEGA)) return kotlin.Unit.INSTANCE;
                if (!DigitalRules.on(event.getPokemonEntity().level(), DigitalRules.STRICT_CATCHING)) return kotlin.Unit.INSTANCE;
                PokeBall ball = event.getPokeBallEntity().getPokeBall();
                if (ball == Digital.CHROME_BALL || ball.getCatchRateModifier().isGuaranteed()) return kotlin.Unit.INSTANCE;
                event.setCatchRate(0F);
                if (event.getThrower() instanceof Player player) {
                    player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".catch.too_strong", p.getSpecies().getTranslatedName())
                            .withStyle(ChatFormatting.RED), true);
                }
            } catch (Throwable t) {
                Digital.LOG.error("Digimon catch rule failed", t);
            }
            return kotlin.Unit.INSTANCE;
        });
    }
}
