package io.github.cobbleeffort.kanto;

import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.Level;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * CobbleEffort: Kanto's game rules (/gamerule, per world): whether each region dimension keeps only its own generation,
 * a generation-only overworld (kantoOverworldGeneration 1-9; 0 = off), the Essence of Olde drop chance, how long
 * Noble and totem bosses take to come back, and whether the Elite Four want every badge first.
 */
public final class KantoRules {
    static final Map<String, GameRules.Key<?>> ALL = new LinkedHashMap<>();

    public static final GameRules.Key<GameRules.BooleanValue> REGION_SPAWNS = bool("kantoRegionSpawns", true);
    public static final GameRules.Key<GameRules.IntegerValue> OVERWORLD_GENERATION = integer("kantoOverworldGeneration", 0);
    public static final GameRules.Key<GameRules.IntegerValue> ESSENCE_CHANCE = integer("kantoEssenceDropChance", 5);
    public static final GameRules.Key<GameRules.IntegerValue> BOSS_RESPAWN_MINUTES = integer("kantoBossRespawnMinutes", 3);
    public static final GameRules.Key<GameRules.BooleanValue> ELITE_NEEDS_BADGES = bool("kantoEliteFourNeedsBadges", true);

    private KantoRules() {
    }

    private static GameRules.Key<GameRules.BooleanValue> bool(String name, boolean value) {
        GameRules.Key<GameRules.BooleanValue> key = GameRules.register(name, GameRules.Category.MISC, GameRules.BooleanValue.create(value));
        ALL.put(name, key);
        return key;
    }

    private static GameRules.Key<GameRules.IntegerValue> integer(String name, int value) {
        GameRules.Key<GameRules.IntegerValue> key = GameRules.register(name, GameRules.Category.MISC, GameRules.IntegerValue.create(value));
        ALL.put(name, key);
        return key;
    }

    static boolean on(Level level, GameRules.Key<GameRules.BooleanValue> key) {
        return level.getGameRules().getBoolean(key);
    }

    static int value(Level level, GameRules.Key<GameRules.IntegerValue> key) {
        return level.getGameRules().getInt(key);
    }

    /** The region whose generation the overworld is limited to (game rule kantoOverworldGeneration), or null. */
    static Region overworldRegion(Level level) {
        int gen = value(level, OVERWORLD_GENERATION);
        for (Region r : Region.values()) if (r != Region.HISUI && r.generation == gen) return r;
        return null;
    }

    static void init() {
        // registration happens in the static fields above; this just loads the class during mod init
    }
}
