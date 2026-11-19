package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokeball.PokeBalls;
import com.cobblemon.mod.common.api.pokeball.catching.CatchRateModifier;
import com.cobblemon.mod.common.api.pokeball.catching.modifiers.LabelModifier;
import com.cobblemon.mod.common.pokeball.PokeBall;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;

import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The Digiballs. Cobblemon 1.8.4 has no data-driven Poké Balls (PokeBalls.reload is a to-do), so they are added to the
 * same private map Cobblemon's own balls live in. The Digiball is three times as good as a Poké Ball on any Digimon
 * (species label "digimon"); the tiers are four times as good on their own stages: the Wireframe Ball on Baby I/II and
 * Child Digimon (In-Training and Rookie), the Data-Net Ball on Adult (Champion), the Chrome Digizoid Ball on Perfect,
 * Ultimate and Super Ultimate (Ultimate and Mega), the only ball that can hold those at all (see CatchRules). Their
 * look is data: Cobblemon's poke_ball model with our textures, a 2D sprite in the inventory and a 3D ball in the hand.
 */
public final class DigiBall {
    public static final String LABEL = "digimon";
    public static final float MULTIPLIER = 3F, TIER_MULTIPLIER = 4F;
    public static final Set<String> ROOKIE = Set.of("digimon_baby1", "digimon_baby2", "digimon_child");
    public static final Set<String> CHAMPION = Set.of("digimon_adult");
    public static final Set<String> MEGA = Set.of("digimon_perfect", "digimon_ultimate", "digimon_super_ultimate");

    private DigiBall() {
    }

    /** True if the Pokémon's form or species carries any of the labels. */
    public static boolean hasAny(Pokemon p, Set<String> labels) {
        for (String l : p.getForm().getLabels()) if (labels.contains(l)) return true;
        for (String l : p.getSpecies().getLabels()) if (labels.contains(l)) return true;
        return false;
    }

    /** Multiplies the catch rate on Digimon carrying any of the labels. */
    public record StageModifier(float multiplier, Set<String> labels) implements CatchRateModifier {
        @Override
        public float value(LivingEntity thrower, Pokemon pokemon) {
            return multiplier;
        }

        @Override
        public Behavior behavior(LivingEntity thrower, Pokemon pokemon) {
            return Behavior.MULTIPLY;
        }

        @Override
        public boolean isValid(LivingEntity thrower, Pokemon pokemon) {
            return hasAny(pokemon, labels);
        }

        @Override
        public float modifyCatchRate(float current, LivingEntity thrower, Pokemon pokemon) {
            return behavior(thrower, pokemon).getMutator().invoke(current, value(thrower, pokemon));
        }
    }

    static PokeBall digiball() {
        return register("digiball", new LabelModifier(MULTIPLIER, true, LABEL), 1.25F);
    }

    static PokeBall wireframe() {
        return register("wireframe_ball", new StageModifier(TIER_MULTIPLIER, ROOKIE), 1.25F);
    }

    static PokeBall dataNet() {
        return register("data_net_ball", new StageModifier(TIER_MULTIPLIER, CHAMPION), 1.25F);
    }

    static PokeBall chrome() {
        return register("chrome_digizoid_ball", new StageModifier(TIER_MULTIPLIER, MEGA), 1.5F);
    }

    @SuppressWarnings("unchecked")
    static PokeBall register(String name, CatchRateModifier modifier, float throwPower) {
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, name);
        PokeBall ball = new PokeBall(id, modifier, List.of(), 0.8F, id,
                ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "item/" + name + "_model"), throwPower, false);
        try {
            Field defaults = PokeBalls.class.getDeclaredField("defaults");
            defaults.setAccessible(true);
            ((Map<ResourceLocation, PokeBall>) defaults.get(null)).put(id, ball);
        } catch (ReflectiveOperationException e) {
            Digital.LOG.error("Could not add {} to Cobblemon's Poké Balls", id, e);
        }
        return ball;
    }
}
