package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.resources.ResourceLocation;

/**
 * What a fusion is, shared by the server (stats, types, battles) and the client (drawing the head):
 *
 * A fused Pokémon is its BODY: it keeps the body's identity, species, form, gender, nature, IVs and EVs. The HEAD is
 * recorded in the body's forced aspects, which Cobblemon saves and syncs to every client:
 *   "fusion_head=<namespace:species>"   the head's species
 *   "fusion_head_aspect=<aspect>"       each of the head's own aspects (shiny, regional forms...)
 * (the whole head Pokémon is also kept in the body's persistent data, to give it back on unfusing; see Fusing).
 *
 * The rules follow Pokémon Infinite Fusion's:
 *   - base stats: the head gives two thirds of HP, Sp. Atk and Sp. Def, the body two thirds of Atk, Def and Speed
 *     (the other third comes from the other Pokémon);
 *   - types: the head's primary type, then the body's secondary type (or its primary type if it has only one); a
 *     repeated type is replaced by the body's other type, or dropped; a Normal/Flying head gives Flying.
 */
public final class FusionRules {
    public static final String HEAD = "fusion_head=";
    public static final String HEAD_ASPECT = "fusion_head_aspect=";

    private FusionRules() {
    }

    /** The head species of a fused Pokémon (from its aspects), or null. */
    public static ResourceLocation headSpecies(Set<String> aspects) {
        if (aspects == null) return null;                      // Pokémon still being constructed
        for (String a : aspects) {
            if (a.startsWith(HEAD)) return ResourceLocation.tryParse(a.substring(HEAD.length()));
        }
        return null;
    }

    public static Set<String> headAspects(Set<String> aspects) {
        Set<String> out = new LinkedHashSet<>();
        if (aspects == null) return out;
        for (String a : aspects) {
            if (a.startsWith(HEAD_ASPECT)) out.add(a.substring(HEAD_ASPECT.length()));
        }
        return out;
    }

    public static boolean isFused(Pokemon pokemon) {
        return headSpecies(pokemon.getForcedAspects()) != null;
    }

    /** The head's form data, or null when the Pokémon isn't fused (or the head species no longer exists). */
    public static FormData headForm(Pokemon pokemon) {
        Set<String> aspects = pokemon.getForcedAspects();
        ResourceLocation id = headSpecies(aspects);
        if (id == null) return null;
        Species species = PokemonSpecies.INSTANCE.getByIdentifier(id);
        if (species == null) return null;
        return species.getForm(headAspects(aspects));
    }

    /** Fusion aspects to add to the body for this head. */
    public static Set<String> aspectsFor(Pokemon head) {
        Set<String> out = new LinkedHashSet<>();
        out.add(HEAD + head.getSpecies().getResourceIdentifier());
        for (String a : head.getAspects()) out.add(HEAD_ASPECT + a);
        return out;
    }

    /** The body's forced aspects without any fusion aspects. */
    public static Set<String> withoutFusion(Set<String> aspects) {
        Set<String> out = new HashSet<>();
        if (aspects == null) return out;
        for (String a : aspects) {
            if (!a.startsWith(HEAD) && !a.startsWith(HEAD_ASPECT)) out.add(a);
        }
        return out;
    }

    private static boolean headWeighted(Stat stat) {
        return stat == Stats.HP || stat == Stats.SPECIAL_ATTACK || stat == Stats.SPECIAL_DEFENCE;
    }

    /** One fused base stat: two thirds from the Pokémon that leads it, one third from the other. */
    public static int fusedBase(Stat stat, int head, int body) {
        return headWeighted(stat) ? (2 * head + body) / 3 : (2 * body + head) / 3;
    }

    public static Map<Stats, Integer> fusedBaseStats(FormData head, FormData body) {
        Map<Stats, Integer> out = new EnumMap<>(Stats.class);
        for (Stats stat : List.of(Stats.HP, Stats.ATTACK, Stats.DEFENCE, Stats.SPECIAL_ATTACK, Stats.SPECIAL_DEFENCE, Stats.SPEED)) {
            out.put(stat, fusedBase(stat, base(head, stat), base(body, stat)));
        }
        return out;
    }

    private static int base(FormData form, Stat stat) {
        Integer v = form.getBaseStats().get(stat);
        return v == null ? 1 : v;
    }

    /** The fused types (one or two), Infinite Fusion's rule. */
    public static List<ElementalType> fusedTypes(FormData head, FormData body) {
        ElementalType first = head.getPrimaryType();
        if (first == ElementalTypes.NORMAL && head.getSecondaryType() == ElementalTypes.FLYING) first = ElementalTypes.FLYING;
        ElementalType second = body.getSecondaryType() != null ? body.getSecondaryType() : body.getPrimaryType();
        if (second == first) second = body.getPrimaryType();
        List<ElementalType> out = new ArrayList<>();
        out.add(first);
        if (second != null && second != first) out.add(second);
        return out;
    }

    /**
     * A fusion name from the two species' names: the first part of the head's name and the last part of the body's
     * (Bulbasaur + Charmander = Bulbmander), the way Infinite Fusion names its fusions.
     */
    public static String fusedName(String head, String body) {
        if (head.isEmpty()) return body;
        if (body.isEmpty()) return head;
        String a = head.substring(0, cutPoint(head, true));
        String b = body.substring(cutPoint(body, false));
        while (!a.isEmpty() && !b.isEmpty() && Character.toLowerCase(a.charAt(a.length() - 1)) == Character.toLowerCase(b.charAt(0))) {
            b = b.substring(1);                                     // no doubled letter at the seam
        }
        String name = a + b.toLowerCase();
        return name.isEmpty() ? head : Character.toUpperCase(name.charAt(0)) + name.substring(1);
    }

    /** Where to cut a name: after the first syllable-ish half for the head, before the last half for the body. */
    private static int cutPoint(String name, boolean head) {
        int n = name.length();
        if (n <= 3) return head ? n : 0;
        int mid = n / 2;
        // move the cut to just after a vowel run so the halves keep their sounds (Bulb|asaur, Char|mander)
        for (int d = 0; d <= n / 3; d++) {
            for (int i : new int[]{mid - d, mid + d}) {
                if (i <= 1 || i >= n - 1) continue;
                if (isVowel(name.charAt(i - 1)) != isVowel(name.charAt(i))) return head ? i : i;
            }
        }
        return mid;
    }

    private static boolean isVowel(char c) {
        return "aeiouyAEIOUY".indexOf(c) >= 0;
    }
}
