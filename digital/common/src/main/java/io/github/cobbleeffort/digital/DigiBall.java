package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokeball.PokeBalls;
import com.cobblemon.mod.common.api.pokeball.catching.modifiers.LabelModifier;
import com.cobblemon.mod.common.pokeball.PokeBall;
import net.minecraft.resources.ResourceLocation;

import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;

/**
 * The Digiball. Cobblemon 1.8.4 has no data-driven Poké Balls (PokeBalls.reload is a to-do), so it is added to the
 * same private map Cobblemon's own balls live in. It is three times as good as a Poké Ball on any Pokémon whose species
 * carries the label "digimon", and an ordinary Poké Ball on anything else. Its look is data: the thrown ball is
 * Cobblemon's poke_ball model with our texture (bedrock/poke_balls/variations), the item a 2D sprite in the inventory
 * and a 3D ball in the hand (item/digiball_model, which Cobblemon's client registers for every ball it knows).
 */
public final class DigiBall {
    public static final String LABEL = "digimon";
    public static final float MULTIPLIER = 3F;

    private DigiBall() {
    }

    @SuppressWarnings("unchecked")
    static PokeBall register() {
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "digiball");
        PokeBall ball = new PokeBall(id, new LabelModifier(MULTIPLIER, true, LABEL), List.of(), 0.8F, id,
                ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "item/digiball_model"), 1.25F, false);
        try {
            Field defaults = PokeBalls.class.getDeclaredField("defaults");
            defaults.setAccessible(true);
            ((Map<ResourceLocation, PokeBall>) defaults.get(null)).put(id, ball);
            Digital.LOG.info("Added the Digiball to Cobblemon's Poké Balls ({}x on Digimon)", MULTIPLIER);
        } catch (ReflectiveOperationException e) {
            Digital.LOG.error("Could not add the Digiball to Cobblemon's Poké Balls", e);
        }
        return ball;
    }
}
