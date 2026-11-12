package io.github.cobbleeffort.kanto;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * The regions, one dimension each: only that generation's Pokémon spawn there (by National Pokédex number), and each
 * is reached through its own portal (Kanto: the glitchy PC; the others: their landmark's portal block, see Regions).
 */
public enum Region {
    KANTO("kanto", 1, 1, 151),
    JOHTO("johto", 2, 152, 251),
    HOENN("hoenn", 3, 252, 386),
    SINNOH("sinnoh", 4, 387, 493),
    UNOVA("unova", 5, 494, 649),
    KALOS("kalos", 6, 650, 721),
    ALOLA("alola", 7, 722, 809),
    GALAR("galar", 8, 810, 905),
    PALDEA("paldea", 9, 906, 1025);

    public final String id;
    public final int generation;
    public final int firstDex;
    public final int lastDex;
    public final ResourceKey<Level> dimension;

    Region(String id, int generation, int firstDex, int lastDex) {
        this.id = id;
        this.generation = generation;
        this.firstDex = firstDex;
        this.lastDex = lastDex;
        this.dimension = ResourceKey.create(Registries.DIMENSION, Kanto.id(id));
    }

    public boolean contains(int dex) {
        return dex >= firstDex && dex <= lastDex;
    }

    /** The region whose dimension this is, or null. */
    public static Region of(ResourceKey<Level> dimension) {
        for (Region r : values()) {
            if (r.dimension == dimension || r.dimension.equals(dimension)) return r;
        }
        return null;
    }
}
