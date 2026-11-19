package io.github.cobbleeffort.fusion;

import net.minecraft.world.level.GameRules;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * CobbleEffort: Fusion's game rules (/gamerule, per world): splicers and reversers never used up, and DNA Splicers
 * giving the higher of the two levels (as Super Splicers do).
 */
public final class FusionGameRules {
    static final Map<String, GameRules.Key<?>> ALL = new LinkedHashMap<>();

    public static final GameRules.Key<GameRules.BooleanValue> INFINITE_SPLICERS = bool("fusionInfiniteSplicers", false);
    public static final GameRules.Key<GameRules.BooleanValue> HIGHER_LEVEL = bool("fusionHigherLevel", false);

    private FusionGameRules() {
    }

    private static GameRules.Key<GameRules.BooleanValue> bool(String name, boolean value) {
        GameRules.Key<GameRules.BooleanValue> key = GameRules.register(name, GameRules.Category.MISC, GameRules.BooleanValue.create(value));
        ALL.put(name, key);
        return key;
    }

    static void init() {
        // registration happens in the static fields above; this just loads the class during mod init
    }
}
