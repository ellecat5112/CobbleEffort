package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.battles.runner.ShowdownService;
import com.cobblemon.mod.common.pokemon.Pokemon;

import java.io.InputStream;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;

/**
 * Digimon rules in Cobblemon's battle engine (Showdown, in a GraalJS context): data/cobbleeffort_digital/digital/
 * digital_engine.js. The attribute triangle: a Digimon hitting the attribute it beats does 1.25x damage, hitting the
 * one that beats it 0.8x. Every battling Pokémon's attribute goes in globalThis.__ceDigi (by UUID) as a battle starts.
 * Talks to the engine by reflection (the Graal service's getContext().eval), so no GraalVM jar is needed to compile.
 */
public final class DigitalEngine {
    private static String install;
    private static boolean warned, logged;

    private DigitalEngine() {
    }

    private static synchronized String script() {
        if (install == null) {
            try (InputStream in = DigitalEngine.class.getResourceAsStream("/data/cobbleeffort_digital/digital/digital_engine.js")) {
                install = in == null ? "" : new String(in.readAllBytes(), StandardCharsets.UTF_8);
            } catch (Exception e) {
                install = "";
            }
        }
        return install;
    }

    static String eval(String js) {
        try {
            ShowdownService service = ShowdownService.Companion.getService();
            Method getContext = service.getClass().getMethod("getContext");
            Object context = getContext.invoke(service);
            Method eval = context.getClass().getMethod("eval", String.class, CharSequence.class);
            return String.valueOf(eval.invoke(context, "js", js));
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Digital.LOG.warn("Couldn't reach the battle engine (Digimon attributes won't count in battle): {}", t.toString());
            }
            return null;
        }
    }

    /** Queue on the Showdown thread: install (idempotent), then js. */
    static void run(String js) {
        Cobblemon.INSTANCE.getShowdownThread().queue(service -> {
            String result = eval(script());
            if (!logged && result != null) {
                logged = true;
                Digital.LOG.info("Digimon rules installed in the battle engine ({})", result);
            }
            if (js != null) eval(js);
            return kotlin.Unit.INSTANCE;
        });
    }

    /** Before a battle: every battling Digimon's attribute goes in the engine's table. */
    static void prepare(PokemonBattle battle) {
        StringBuilder js = new StringBuilder("globalThis.__ceDigi = globalThis.__ceDigi || {};globalThis.__ceDigiField = globalThis.__ceDigiField || {};");
        java.util.Set<String> fields = FieldBuffs.active(battle);
        for (BattleActor actor : battle.getActors()) {
            for (BattlePokemon bp : actor.getPokemonList()) {
                Pokemon p = bp.getEffectedPokemon();
                Attributes.Attribute a = Attributes.of(p);
                js.append(a == null
                        ? "delete globalThis.__ceDigi['" + p.getUuid() + "'];"
                        : "globalThis.__ceDigi['" + p.getUuid() + "'] = '" + a.display() + "';");
                String f = FieldBuffs.boosted(p, fields);
                js.append(f == null ? "delete globalThis.__ceDigiField['" + p.getUuid() + "'];"
                        : "globalThis.__ceDigiField['" + p.getUuid() + "'] = '" + f + "';");
            }
        }
        run(js.toString());
    }

    static void installNow() {
        run(null);
    }
}
