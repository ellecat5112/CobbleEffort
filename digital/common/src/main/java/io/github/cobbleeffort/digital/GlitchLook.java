package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.entity.pokemon.MocKEffect;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.entity.pokemon.effects.TransformEffect;
import net.minecraft.server.MinecraftServer;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Dot Virus's look: while a Digimon is Pixelated (the engine says "-formechange <species>-Pixelated" and "-Restored")
 * it shrinks to a tiny 8-bit-sized version of itself (Cobblemon's Transform effect at a third of its size); restored,
 * it goes back to how it looked (its warp digivolution, if it had one). Wild ones are restored when the battle ends.
 */
final class GlitchLook {
    private record Before(PokemonProperties mock, float scale) {
    }

    private static final Map<UUID, Before> SHRUNK = new HashMap<>();

    private GlitchLook() {
    }

    static void init() {
        CobblemonEvents.FORME_CHANGE.subscribe(Priority.NORMAL, event -> {
            try {
                String form = event.getFormeName().toLowerCase(java.util.Locale.ROOT);
                BattlePokemon bp = event.getPokemon();
                PokemonEntity e = bp.getEffectedPokemon().getEntity();
                if (e == null) return;
                if (form.equals("pixelated")) shrink(e);
                else if (form.equals("restored")) restore(e);
            } catch (Throwable t) {
                Digital.LOG.error("Dot Virus look failed", t);
            }
        });
        CobblemonEvents.BATTLE_ENDED.subscribe(Priority.NORMAL, event -> {
            try {
                event.getBattle().getActors().forEach(a -> a.getPokemonList().forEach(bp -> {
                    PokemonEntity e = bp.getEffectedPokemon().getEntity();
                    if (e != null && SHRUNK.containsKey(e.getUUID())) {
                        SHRUNK.remove(e.getUUID());
                        if (e.isAlive()) e.getEffects().wipe();
                    }
                }));
            } catch (Throwable t) {
                Digital.LOG.error("Dot Virus look cleanup failed", t);
            }
        });
    }

    static void shrink(PokemonEntity e) {
        if (SHRUNK.containsKey(e.getUUID())) return;
        MocKEffect m = e.getEffects().getMockEffect();
        PokemonProperties mock = m != null ? m.getMock() : PokemonProperties.Companion.parse(e.getPokemon().getSpecies().getResourceIdentifier().toString());
        float scale = m != null ? m.getScale() : e.getPokemon().getForm().getBaseScale() * e.getPokemon().getScaleModifier();
        SHRUNK.put(e.getUUID(), new Before(m != null ? m.getMock() : null, scale));
        Runnable go = () -> new TransformEffect(mock, scale * 0.3F, false).start(e);
        if (m != null) {
            e.getEffects().forceWipe();
        }
        go.run();
    }

    static void restore(PokemonEntity e) {
        Before b = SHRUNK.remove(e.getUUID());
        if (b == null) return;
        e.getEffects().forceWipe();
        MinecraftServer server = e.getServer();
        if (b.mock() != null && server != null) {
            Scheduler.later(server, 2, () -> new TransformEffect(b.mock(), b.scale(), false).start(e));
        } else {
            e.getEffects().wipe();
        }
    }
}
