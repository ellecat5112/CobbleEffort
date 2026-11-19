package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Jogress (DNA digivolution): two Digimon digivolve together, ExVeemon + Stingmon into Paildramon, WarGreymon + Metal
 * Garurumon into Omegamon and every other pair wikimon lists between Digimon in the mod
 * (data/cobbleeffort_digital/digital/jogress.json, written by the species generator). In battle, the Digivice used on
 * one of them with its partner in your party (healthy) or battling on your side makes the battling one the Jogress
 * form for the rest of the battle (JOGRESS energy).
 */
final class Jogress {
    record Pair(String partner, String result) {
    }

    private static Map<String, List<Pair>> table;

    private Jogress() {
    }

    static synchronized Map<String, List<Pair>> table() {
        if (table != null) return table;
        Map<String, List<Pair>> t = new HashMap<>();
        try (InputStream in = Jogress.class.getResourceAsStream("/data/cobbleeffort_digital/digital/jogress.json")) {
            if (in != null) {
                JsonObject root = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
                JsonArray pairs = root.getAsJsonArray("pairs");
                for (JsonElement e : pairs) {
                    JsonObject o = e.getAsJsonObject();
                    String a = o.get("a").getAsString(), b = o.get("b").getAsString(), r = o.get("result").getAsString();
                    t.computeIfAbsent(a, k -> new ArrayList<>()).add(new Pair(b, r));
                    t.computeIfAbsent(b, k -> new ArrayList<>()).add(new Pair(a, r));
                }
            }
        } catch (Exception ex) {
            Digital.LOG.warn("Couldn't read the Jogress table: {}", ex.toString());
        }
        table = t;
        return t;
    }

    /** The Jogress result for a battling Digimon whose partner is at hand, or null. */
    static Species find(ServerPlayer player, BattlePokemon bp) {
        Pokemon p = bp.getEffectedPokemon();
        List<Pair> pairs = table().get(p.getSpecies().getResourceIdentifier().toString());
        if (pairs == null) return null;
        List<String> near = new ArrayList<>();
        for (Pokemon q : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            if (!q.getUuid().equals(p.getUuid()) && !q.isFainted()) near.add(q.getSpecies().getResourceIdentifier().toString());
        }
        for (BattleActor a : bp.getActor().getSide().getActors()) {
            for (var active : a.getActivePokemon()) {
                BattlePokemon o = active.getBattlePokemon();
                if (o != null && o != bp && o.getHealth() > 0) near.add(o.getEffectedPokemon().getSpecies().getResourceIdentifier().toString());
            }
        }
        for (Pair pair : pairs) {
            if (near.contains(pair.partner())) {
                Species r = PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.parse(pair.result()));
                if (r != null) return r;
            }
        }
        return null;
    }
}
