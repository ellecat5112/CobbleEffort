package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.abilities.Abilities;
import com.cobblemon.mod.common.api.abilities.Ability;
import com.cobblemon.mod.common.api.abilities.AbilityTemplate;
import com.cobblemon.mod.common.api.moves.Move;
import com.cobblemon.mod.common.api.moves.MoveSet;
import com.cobblemon.mod.common.api.moves.MoveTemplate;
import com.cobblemon.mod.common.api.moves.Moves;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * A distorted Pokémon's moves and ability, outside battle: distorting swaps each move for its twin and a type-bound
 * ability for its twin (the same tables the battle engine uses, data/cobbleeffort_distortion/distortion/*.json),
 * keeping the originals in the Pokémon's persistent data; reverting puts them back (a move learned meanwhile stays).
 * The battle engine recognises moves already swapped and doesn't swap them again.
 */
public final class DistortionTwins {
    private static final String KEY = "cobbleeffort_distortion";
    private static JsonObject moves;
    private static JsonObject abilities;

    private DistortionTwins() {
    }

    private static JsonObject load(String name) {
        try (InputStream in = DistortionTwins.class.getResourceAsStream("/data/cobbleeffort_distortion/distortion/" + name)) {
            if (in == null) return new JsonObject();
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (Exception e) {
            DistortionBattle.LOG.error("Couldn't read {}", name, e);
            return new JsonObject();
        }
    }

    private static synchronized void init() {
        if (moves == null) moves = load("move_twins.json");
        if (abilities == null) abilities = load("ability_twins.json");
    }

    private static String str(JsonObject table, String key) {
        JsonElement e = table == null ? null : table.get(key);
        return e != null && e.isJsonPrimitive() ? e.getAsString() : null;
    }

    static String moveTwin(Pokemon pokemon, String id) {
        init();
        JsonObject species = moves.has("species") ? moves.getAsJsonObject("species") : null;
        String sp = pokemon.getSpecies().getName().toLowerCase().replaceAll("[^a-z0-9]", "");
        if (species != null && species.has(sp)) {
            String own = str(species.getAsJsonObject(sp), id);
            if (own != null) return own;
        }
        return str(moves.has("default") ? moves.getAsJsonObject("default") : null, id);
    }

    static String abilityTwin(Pokemon pokemon, String id) {
        init();
        if (!abilities.has(id)) return null;
        List<String> types = new ArrayList<>();
        for (ElementalType t : pokemon.getTypes()) {
            String n = t.getName();
            types.add(n.substring(0, 1).toUpperCase() + n.substring(1).toLowerCase());
        }
        types.sort(null);
        String key = String.join("/", types);
        JsonObject table = abilities.getAsJsonObject(id);
        String own = str(table, pokemon.getSpecies().getName() + ":" + key);   // a starter's random chart
        return own != null ? own : str(table, key);
    }

    private static String id(String name) {
        return name.toLowerCase().replaceAll("[^a-z0-9]", "");
    }

    /** Swap to the twins (call before the distorted form applies: the ability twin depends on the current types). */
    static void apply(Pokemon pokemon) {
        CompoundTag data = pokemon.getPersistentData();
        if (data.contains(KEY)) return;                          // already swapped
        CompoundTag saved = new CompoundTag();
        ListTag originals = new ListTag(), twins = new ListTag();
        MoveSet set = pokemon.getMoveSet();
        for (int i = 0; i < 4; i++) {
            Move move = set.get(i);
            String orig = move == null ? "" : move.getName();
            String twinId = move == null ? null : moveTwin(pokemon, id(orig));
            MoveTemplate twin = twinId == null ? null : Moves.getByName(twinId);
            if (twin != null) {
                Move m = twin.create(move.getRaisedPpStages());
                m.setCurrentPp(Math.min(move.getCurrentPp(), m.getMaxPp()));
                set.setMove(i, m);
                originals.add(StringTag.valueOf(orig));
                twins.add(StringTag.valueOf(twin.getName()));
            } else {
                originals.add(StringTag.valueOf(""));
                twins.add(StringTag.valueOf(""));
            }
        }
        saved.put("moves", originals);
        saved.put("twins", twins);
        Ability ability = pokemon.getAbility();
        String twinAbility = abilityTwin(pokemon, id(ability.getName()));
        AbilityTemplate template = twinAbility == null ? null : Abilities.get(twinAbility);
        if (template != null) {
            saved.putString("ability", ability.getName());
            saved.putBoolean("abilityForced", ability.getForced());
            pokemon.updateAbility(template.create(true, Priority.NORMAL));
        }
        data.put(KEY, saved);
    }

    /** Back to the originals (moves still in their twin's slot; a move learned while distorted stays). */
    static void restore(Pokemon pokemon) {
        CompoundTag data = pokemon.getPersistentData();
        if (!data.contains(KEY)) return;
        CompoundTag saved = data.getCompound(KEY);
        ListTag originals = saved.getList("moves", Tag.TAG_STRING), twins = saved.getList("twins", Tag.TAG_STRING);
        MoveSet set = pokemon.getMoveSet();
        for (int i = 0; i < Math.min(4, originals.size()); i++) {
            String orig = originals.getString(i), twin = twins.getString(i);
            Move now = set.get(i);
            if (orig.isEmpty() || now == null || !now.getName().equals(twin)) continue;
            MoveTemplate template = Moves.getByName(id(orig));
            if (template == null) continue;
            Move m = template.create(now.getRaisedPpStages());
            m.setCurrentPp(Math.min(now.getCurrentPp(), m.getMaxPp()));
            set.setMove(i, m);
        }
        if (saved.contains("ability")) {
            AbilityTemplate template = Abilities.get(id(saved.getString("ability")));
            if (template != null) pokemon.updateAbility(template.create(saved.getBoolean("abilityForced"), Priority.NORMAL));
        }
        data.remove(KEY);
    }
}
