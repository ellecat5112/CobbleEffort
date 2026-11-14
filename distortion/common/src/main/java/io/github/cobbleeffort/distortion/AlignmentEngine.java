package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.BattleSide;
import com.cobblemon.mod.common.battles.runner.ShowdownService;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.pokemon.Pokemon;

import java.io.InputStream;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;

/**
 * The Shadow and Crystal types in battle. Cobblemon's battle engine (Showdown, in a GraalJS context) knows only the 18
 * types and takes each Pokémon's types from its species: data/cobbleeffort_distortion/distortion/alignment_engine.js
 * adds both types to its type chart, makes Shadow moves 2x on every non-Shadow Pokémon (0.5x on Shadow ones), makes
 * Crystal bodies refract special attacks, and gives every Pokémon whose UUID is in globalThis.__ceAlign its
 * counterpart's types. That table is filled for every Shadow/Crystal Pokémon as a battle starts (AlignBattleMixin).
 *
 * Talks to the engine by reflection (the Graal service's getContext().eval), so no GraalVM jar is needed to compile.
 */
public final class AlignmentEngine {
    private static String install;
    private static boolean warned;
    private static boolean logged;

    private AlignmentEngine() {
    }

    private static synchronized String script() {
        if (install == null) {
            try (InputStream in = AlignmentEngine.class.getResourceAsStream("/data/cobbleeffort_distortion/distortion/alignment_engine.js")) {
                install = in == null ? "" : new String(in.readAllBytes(), StandardCharsets.UTF_8);
            } catch (Exception e) {
                install = "";
            }
        }
        return install;
    }

    private static String eval(String js) {
        try {
            ShowdownService service = ShowdownService.Companion.getService();
            Method getContext = service.getClass().getMethod("getContext");
            Object context = getContext.invoke(service);
            Method eval = context.getClass().getMethod("eval", String.class, CharSequence.class);
            return String.valueOf(eval.invoke(context, "js", js));
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Distortion.LOG.warn("Couldn't reach the battle engine (Shadow/Crystal Pokémon battle with their plain types): {}", t.toString());
            }
            return null;
        }
    }

    /** Queue on the Showdown thread: install (idempotent: it re-wraps only when another add-on wrapped since), then js. */
    private static void run(String js) {
        Cobblemon.INSTANCE.getShowdownThread().queue(service -> {
            String result = eval(script());
            if (!logged && result != null) {
                logged = true;
                Distortion.LOG.info("Shadow and Crystal types installed in the battle engine ({})", result);
            }
            if (js != null) eval(js);
            return kotlin.Unit.INSTANCE;
        });
    }

    /** Before a battle: every Shadow/Crystal Pokémon in it goes in the engine's table (others are taken out). */
    public static void prepare(BattleSide... sides) {
        StringBuilder js = new StringBuilder("globalThis.__ceAlign = globalThis.__ceAlign || {};");
        for (BattleSide side : sides) {
            for (BattleActor actor : side.getActors()) {
                for (BattlePokemon bp : actor.getPokemonList()) {
                    Pokemon p = bp.getEffectedPokemon();
                    String flag = Alignment.of(p);
                    js.append(flag == null
                            ? "delete globalThis.__ceAlign['" + p.getUuid() + "'];"
                            : "globalThis.__ceAlign['" + p.getUuid() + "'] = '" + Alignment.typeOf(flag).getName() + "';");
                }
            }
        }
        run(js.toString());
    }

    /** At server start, so the type chart is in place before anything asks the engine about types. */
    public static void installNow() {
        run(null);
    }
}
