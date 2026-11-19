package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.nbt.CompoundTag;

import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

/**
 * Digimon attributes: Vaccine beats Virus, Virus beats Data, Data beats Vaccine (rock-paper-scissors; Free and Variable
 * sit outside the triangle). A Digimon's attribute is its species label ("digimon_vaccine" ...) unless it has been
 * rewritten: feeding it attribute fragments (six of one kind) or using an attribute chip gives it the forced aspect
 * "digi_vaccine" / "digi_data" / "digi_virus", which wins over the species. The aspect also unlocks that attribute's
 * digivolutions (their requirement is `aspect=digi_<attribute>` when the target's attribute differs from the species').
 */
public final class Attributes {
    public enum Attribute {
        VACCINE, DATA, VIRUS, FREE, VARIABLE;

        public String id() {
            return name().toLowerCase(Locale.ROOT);
        }

        public String aspect() {
            return "digi_" + id();
        }

        public String label() {
            return "digimon_" + id();
        }

        /** The attribute this one beats in the triangle, or null outside it. */
        public Attribute beats() {
            return switch (this) {
                case VACCINE -> VIRUS;
                case VIRUS -> DATA;
                case DATA -> VACCINE;
                default -> null;
            };
        }

        public boolean triangle() {
            return beats() != null;
        }

        public String display() {
            return name().charAt(0) + id().substring(1);
        }
    }

    /** Fragments of one attribute fed in a row that rewrite a Digimon to it. */
    public static final int FRAGMENTS_TO_SHIFT = 6;
    static final String DATA_KEY = "cobbleeffort_digital";

    private Attributes() {
    }

    public static boolean isDigimon(Pokemon p) {
        return p != null && p.getSpecies().getLabels().contains(DigiBall.LABEL);
    }

    /** The species' own attribute (its label), or null. */
    public static Attribute ofSpecies(Pokemon p) {
        Set<String> labels = p.getForm().getLabels();
        Set<String> all = new HashSet<>(labels);
        all.addAll(p.getSpecies().getLabels());
        for (Attribute a : Attribute.values()) {
            if (all.contains(a.label())) return a;
        }
        return null;
    }

    /** The attribute a Digimon battles with: a rewritten one (aspect) first, else its species'. Null for Pokémon. */
    public static Attribute of(Pokemon p) {
        if (!isDigimon(p)) return null;
        for (Attribute a : Attribute.values()) {
            if (p.getForcedAspects().contains(a.aspect())) return a;
        }
        return ofSpecies(p);
    }

    /** Rewrites a Digimon's attribute (the aspect; no aspect when it matches the species and nothing else is set). */
    public static void set(Pokemon p, Attribute a) {
        Set<String> forced = new HashSet<>(p.getForcedAspects());
        for (Attribute b : Attribute.values()) forced.remove(b.aspect());
        forced.add(a.aspect());
        p.setForcedAspects(forced);
        p.updateAspects();
        CompoundTag tag = data(p);
        tag.remove("fragments");
        tag.remove("fragment_kind");
        p.onChange(null);
    }

    static CompoundTag data(Pokemon p) {
        CompoundTag root = p.getPersistentData();
        if (!root.contains(DATA_KEY)) root.put(DATA_KEY, new CompoundTag());
        return root.getCompound(DATA_KEY);
    }

    /**
     * Feeds one fragment: counts up while the same kind keeps coming (a different kind starts over), and at
     * FRAGMENTS_TO_SHIFT rewrites the attribute. Returns the new count (0 = it just shifted, -1 = already that attribute).
     */
    public static int feed(Pokemon p, Attribute a) {
        if (of(p) == a) return -1;
        CompoundTag tag = data(p);
        int n = a.id().equals(tag.getString("fragment_kind")) ? tag.getInt("fragments") + 1 : 1;
        if (n >= FRAGMENTS_TO_SHIFT) {
            set(p, a);
            return 0;
        }
        tag.putString("fragment_kind", a.id());
        tag.putInt("fragments", n);
        p.onChange(null);
        return n;
    }
}
