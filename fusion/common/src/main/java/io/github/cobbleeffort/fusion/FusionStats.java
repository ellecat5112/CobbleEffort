package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import java.util.List;

/**
 * A fused Pokémon's stats and types, computed like Cobblemon's own (CobblemonStatProvider) but from the fused base
 * stats. Used by the mixins on both sides; returns null for a Pokémon that isn't fused, so Cobblemon carries on.
 */
public final class FusionStats {
    private FusionStats() {
    }

    public static Integer stat(Pokemon pokemon, Stat stat) {
        try {
            return fusedStat(pokemon, stat);
        } catch (RuntimeException e) {                        // never break Cobblemon's own stat code
            return null;
        }
    }

    private static Integer fusedStat(Pokemon pokemon, Stat stat) {
        if (!(stat instanceof Stats s) || s.getType() != Stat.Type.PERMANENT) return null;
        FormData head = FusionRules.headForm(pokemon);
        if (head == null) return null;
        Integer headBase = head.getBaseStats().get(stat);
        Integer bodyBase = pokemon.getForm().getBaseStats().get(stat);
        if (headBase == null || bodyBase == null) return null;
        int base = FusionRules.fusedBase(stat, headBase, bodyBase);
        int iv = pokemon.getIvs().getEffectiveBattleIV(stat);
        int ev = pokemon.getEvs().getOrDefault(stat);
        int level = pokemon.getLevel();
        if (stat == Stats.HP) {
            return (int) ((int) (2.0 * base + iv + (int) (ev / 4.0) + 100) * level / 100.0 + 10);
        }
        return pokemon.getEffectiveNature().modifyStat(stat, ((2 * base + iv + (ev / 4)) * level) / 100 + 5);
    }

    public static List<ElementalType> types(Pokemon pokemon) {
        try {
            FormData head = FusionRules.headForm(pokemon);
            if (head == null) return null;
            return FusionRules.fusedTypes(head, pokemon.getForm());
        } catch (RuntimeException e) {
            return null;
        }
    }
}
