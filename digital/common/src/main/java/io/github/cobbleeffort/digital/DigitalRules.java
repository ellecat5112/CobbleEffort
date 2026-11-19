package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.Level;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * CobbleEffort: Digital's game rules (/gamerule, per world) and the wild-spawn rules they drive:
 * digitalDigimonOnly turns every wild Pokémon that spawns into a Digimon (same primary type where one exists, at a
 * stage that suits its level); digitalNoWildDigimon stops Digimon spawning outside the Digital World.
 */
public final class DigitalRules {
    /** Every Digital game rule, in the order /digital rules lists them (first: the keys below register into it). */
    static final Map<String, GameRules.Key<?>> ALL = new LinkedHashMap<>();

    public static final GameRules.Key<GameRules.BooleanValue> DIGIMON_ONLY = bool("digitalDigimonOnly", false);
    public static final GameRules.Key<GameRules.BooleanValue> NO_WILD_DIGIMON = bool("digitalNoWildDigimon", false);
    public static final GameRules.Key<GameRules.BooleanValue> AUTO_HATCH = bool("digitalAutoHatch", false);
    public static final GameRules.Key<GameRules.IntegerValue> HATCH_SECONDS = integer("digitalDigitamaHatchSeconds", 300);
    public static final GameRules.Key<GameRules.IntegerValue> DIGITAMA_CHANCE = integer("digitalDigitamaDropChance", 5);
    public static final GameRules.Key<GameRules.BooleanValue> FREE_DIGIVOLUTION = bool("digitalFreeDigivolution", false);
    public static final GameRules.Key<GameRules.BooleanValue> RAIDS = bool("digitalRaids", true);
    public static final GameRules.Key<GameRules.BooleanValue> RIFTS = bool("digitalRifts", true);
    public static final GameRules.Key<GameRules.BooleanValue> DARK_AURA = bool("digitalDarkTowerAura", true);
    public static final GameRules.Key<GameRules.BooleanValue> STRICT_CATCHING = bool("digitalStrictCatching", true);


    /** Level bands -> Digivice stage indices (baby1, baby2, child, adult, perfect, ultimate, super_ultimate). */
    private static final int[][] BANDS = {{0, 6, 0, 1}, {6, 18, 2, 2}, {18, 32, 3, 3}, {32, 46, 4, 4}, {46, 62, 5, 5}, {62, 1000, 5, 6}};
    private static List<List<Species>> byStage;
    private static int speciesCount = -1;

    private DigitalRules() {
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

    public static boolean on(Level level, GameRules.Key<GameRules.BooleanValue> key) {
        return level.getGameRules().getBoolean(key);
    }

    public static int value(Level level, GameRules.Key<GameRules.IntegerValue> key) {
        return level.getGameRules().getInt(key);
    }

    /** Tamer Energy is free (game rule) or the player is in creative. */
    public static boolean freeEnergy(ServerPlayer player) {
        return player.getAbilities().instabuild || on(player.level(), FREE_DIGIVOLUTION);
    }

    static void init() {
        ALL.put(Raids.DIGITIZATION.getId(), Raids.DIGITIZATION);
        ALL.put(MoveEffects.GRIEFING.getId(), MoveEffects.GRIEFING);
        // runs after other add-ons' spawn swaps (CobbleEffort: Kanto's region rule), so Digimon-only has the last word
        CobblemonEvents.ENTITY_SPAWN.subscribe(Priority.LOW, event -> {
            try {
                if (event.getEntity() instanceof PokemonEntity entity && !event.isCanceled()) {
                    Level level = entity.level();
                    Pokemon p = entity.getPokemon();
                    boolean digimon = Attributes.isDigimon(p);
                    if (digimon && on(level, NO_WILD_DIGIMON) && level.dimension() != DigitalWorld.DIMENSION) {
                        event.cancel();
                    } else if (!digimon && on(level, DIGIMON_ONLY)) {
                        Pokemon replacement = digimonFor(p, level.getRandom());
                        if (replacement != null) entity.setPokemon(replacement);
                    }
                }
            } catch (Throwable t) {
                Digital.LOG.error("Digimon spawn rule failed", t);
            }
            return kotlin.Unit.INSTANCE;
        });
    }

    /** A wild Digimon to stand in for a Pokémon: same level, a stage that suits it, its primary type if one shares it. */
    static Pokemon digimonFor(Pokemon p, RandomSource random) {
        List<List<Species>> stages = stages();
        int level = p.getLevel();
        List<Species> band = new ArrayList<>();
        for (int[] b : BANDS) {
            if (level >= b[0] && level < b[1]) for (int i = b[2]; i <= b[3]; i++) band.addAll(stages.get(i));
        }
        if (band.isEmpty()) for (List<Species> st : stages) band.addAll(st);
        if (band.isEmpty()) return null;
        List<Species> same = new ArrayList<>();
        for (Species s : band) if (s.getPrimaryType() == p.getSpecies().getPrimaryType()) same.add(s);
        List<Species> pool = same.isEmpty() ? band : same;
        Species pick = pool.get(random.nextInt(pool.size()));
        Pokemon out = PokemonProperties.Companion.parse(pick.getResourceIdentifier() + " level=" + level).create();
        if (p.getShiny()) out.setShiny(true);
        return out;
    }

    /** Implemented Digimon (not legendary or mythical) by Digivice stage, rebuilt when the species list changes. */
    private static synchronized List<List<Species>> stages() {
        int n = PokemonSpecies.getImplemented().size();
        if (byStage != null && n == speciesCount) return byStage;
        List<List<Species>> out = new ArrayList<>();
        for (int i = 0; i < Digivice.STAGES.length; i++) out.add(new ArrayList<>());
        for (Species s : PokemonSpecies.getImplemented()) {
            if (!s.getLabels().contains(DigiBall.LABEL) || s.getLabels().contains("legendary") || s.getLabels().contains("mythical")) continue;
            int st = Digivice.stageIndex(s);
            if (st >= 0) out.get(st).add(s);
        }
        byStage = out;
        speciesCount = n;
        return out;
    }
}
