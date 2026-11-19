package io.github.cobbleeffort.distortion;

import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.GameRules;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * CobbleEffort: Distortion's game rules (/gamerule, per world): whether wild and NPC Pokémon distort in battle, and how
 * rare wild Shadow and Crystal Pokémon are (1 in N; 0 = never).
 */
public final class DistortionGameRules {
    static final Map<String, GameRules.Key<?>> ALL = new LinkedHashMap<>();

    public static final GameRules.Key<GameRules.BooleanValue> WILD_DISTORT = bool("distortionWildDistort", true);
    public static final GameRules.Key<GameRules.IntegerValue> SHADOW_CHANCE = integer("distortionShadowChance", 256);
    public static final GameRules.Key<GameRules.IntegerValue> CRYSTAL_CHANCE = integer("distortionCrystalChance", 256);

    private DistortionGameRules() {
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

    static GameRules rules() {
        MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
        return server == null ? null : server.getGameRules();
    }

    /** Wild and NPC Pokémon may distort (true when no server is at hand). */
    static boolean wildDistort() {
        GameRules r = rules();
        return r == null || r.getBoolean(WILD_DISTORT);
    }

    static void init() {
        // registration happens in the static fields above; this just loads the class during mod init
    }
}
