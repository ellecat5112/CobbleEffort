package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.battles.runner.ShowdownService;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import java.lang.reflect.Method;
import java.util.List;
import java.util.Map;

/**
 * Fusions in battle. Cobblemon's battle engine (Showdown, in a GraalJS context) builds each Pokémon from its species
 * id and its UUID and works out stats and types from its own Pokédex; a fusion's stats and types aren't any species'.
 * So we wrap the engine's Pokemon.prototype.setSpecies (keeping whatever it was, e.g. other mods' scripts that call
 * it): after it runs, a Pokémon whose UUID is in globalThis.__ceFusion gets the fused base stats (and max HP the first
 * time, so it matches Cobblemon's own) and the fused types. The table is filled for every fused Pokémon as a battle
 * starts (BattleRegistryMixin) and whenever one is fused, reversed or unfused.
 *
 * Talks to the engine by reflection (GraalShowdownService.getContext().eval), so this add-on needs no GraalVM jar to
 * compile; if the engine isn't the in-process Graal one, fusions simply battle with the body's stats.
 */
public final class FusionEngine {
    private static final String INSTALL = String.join("\n",
            "(function () {",
            "  if (globalThis.__ceFusionInstalled) return;",
            "  globalThis.__ceFusion = globalThis.__ceFusion || {};",
            "  const P = require('./sim/pokemon').Pokemon;",
            "  const original = P.prototype.setSpecies;",
            "  P.prototype.setSpecies = function (rawSpecies, source, isTransform) {",
            "    const species = original.call(this, rawSpecies, source, isTransform);",
            "    const f = globalThis.__ceFusion[this.uuid];",
            "    if (!species || !f || isTransform) return species;",
            "    const stats = this.battle.spreadModify(f.base, this.set);",
            "    if (!this.m.ceFusionHp) {",
            "      this.m.ceFusionHp = true;",
            "      this.baseMaxhp = stats.hp; this.maxhp = stats.hp; this.hp = stats.hp;",
            "    }",
            "    this.baseStoredStats = stats;",
            "    for (const s in this.storedStats) {",
            "      this.storedStats[s] = stats[s];",
            "      if (this.modifiedStats) this.modifiedStats[s] = stats[s];",
            "    }",
            "    this.speed = this.storedStats.spe;",
            "    this.setType(f.types, true);",
            "    this.apparentType = f.types.join('/');",
            "    return species;",
            "  };",
            "  globalThis.__ceFusionInstalled = true;",
            "})();");

    private FusionEngine() {
    }

    /** Runs JS in the battle engine's context; false when it can't. */
    private static boolean eval(String js) {
        return evalValue(js) != null;
    }

    private static boolean warned;

    /** Runs JS in the battle engine's context and returns the result as text, or null when it can't. */
    private static String evalValue(String js) {
        try {
            ShowdownService service = ShowdownService.Companion.getService();
            Method getContext = service.getClass().getMethod("getContext");
            Object context = getContext.invoke(service);
            Method eval = context.getClass().getMethod("eval", String.class, CharSequence.class);
            return String.valueOf(eval.invoke(context, "js", js));
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Fusion.LOG.warn("Fusion couldn't reach the battle engine (fusions battle with their body's stats): {}", t.toString());
            }
            return null;
        }
    }

    /** For /fusion selftest: whether the engine hook is installed and which fusions it knows, sent to report. */
    public static void probe(java.util.function.Consumer<String> report) {
        Cobblemon.INSTANCE.getShowdownThread().queue(service -> {
            eval(INSTALL);
            report.accept("engine: " + evalValue("JSON.stringify({installed: !!globalThis.__ceFusionInstalled, fusions: globalThis.__ceFusion || {}})"));
            return kotlin.Unit.INSTANCE;
        });
    }

    private static void run(String js) {
        Cobblemon.INSTANCE.getShowdownThread().queue(service -> {
            eval(INSTALL);
            eval(js);
            return kotlin.Unit.INSTANCE;
        });
    }

    /** Tell the engine about a fused Pokémon (no-op for an unfused one). */
    public static void register(Pokemon pokemon) {
        FormData head = FusionRules.headForm(pokemon);
        if (head == null) return;
        FormData body = pokemon.getForm();
        Map<Stats, Integer> base = FusionRules.fusedBaseStats(head, body);
        List<ElementalType> types = FusionRules.fusedTypes(head, body);
        StringBuilder t = new StringBuilder();
        for (ElementalType type : types) {
            if (t.length() > 0) t.append(',');
            String n = type.getName();
            t.append('"').append(Character.toUpperCase(n.charAt(0))).append(n.substring(1)).append('"');
        }
        String js = "globalThis.__ceFusion = globalThis.__ceFusion || {}; globalThis.__ceFusion['" + pokemon.getUuid() + "'] = {base: {"
                + "hp: " + base.get(Stats.HP) + ", atk: " + base.get(Stats.ATTACK) + ", def: " + base.get(Stats.DEFENCE)
                + ", spa: " + base.get(Stats.SPECIAL_ATTACK) + ", spd: " + base.get(Stats.SPECIAL_DEFENCE)
                + ", spe: " + base.get(Stats.SPEED) + "}, types: [" + t + "]};";
        run(js);
    }

    public static void unregister(Pokemon pokemon) {
        run("if (globalThis.__ceFusion) delete globalThis.__ceFusion['" + pokemon.getUuid() + "'];");
    }
}
