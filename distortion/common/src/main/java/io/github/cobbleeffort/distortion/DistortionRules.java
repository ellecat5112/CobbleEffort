package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.api.pokemon.feature.FlagSpeciesFeature;
import com.cobblemon.mod.common.api.pokemon.feature.SpeciesFeature;
import com.cobblemon.mod.common.pokemon.FormData;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import io.wispforest.accessories.api.AccessoriesCapability;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

/** Who may distort, shared by the battle button, the interaction wheel and the server. */
public final class DistortionRules {
    /** The species feature (a flag, data/cobbleeffort_distortion/species_features/distorted.json) and its aspect. */
    public static final String FEATURE = "distorted";

    private DistortionRules() {
    }

    /** The trainer wears the Distortion Band (in the Distortion accessory slot). */
    public static boolean wearsBand(Player player) {
        if (player == null) return false;
        AccessoriesCapability capability = AccessoriesCapability.get(player);
        return capability != null && capability.isEquipped(Distortion.BAND.get());
    }

    /** The Pokémon holds the Distortion Crystal, or is Arceus holding a plate (its power, and it can only hold one item). */
    public static boolean holdsSource(Pokemon pokemon) {
        ItemStack held = pokemon.heldItem();
        if (held.is(Distortion.CRYSTAL.get())) return true;
        return pokemon.getSpecies().getNationalPokedexNumber() == 493 && !held.isEmpty() && held.getItem().toString().endsWith("_plate");
    }

    /** The species has Distorted forms (the add-on's first set: Giratina, Dialga, Palkia, Arceus). */
    public static boolean hasDistortedForm(Species species) {
        for (FormData form : species.getForms()) {
            if (form.getAspects().contains(DistortionBattle.ASPECT)) return true;
        }
        return false;
    }

    /** Distorted outside battle (the wheel's flag feature, saved with the Pokémon). */
    public static boolean distortedOutside(Pokemon pokemon) {
        SpeciesFeature feature = pokemon.getFeature(FEATURE);
        return feature instanceof FlagSpeciesFeature flag && flag.getEnabled();
    }

    /** Distort or revert outside battle: the form and look (the flag feature), and the moves and ability (their twins). */
    public static void setDistortedOutside(Pokemon pokemon, boolean distorted) {
        if (distorted) {
            DistortionTwins.apply(pokemon);                       // before the form changes the types
        }
        new FlagSpeciesFeature(FEATURE, distorted).apply(pokemon);
        pokemon.updateAspects();
        if (!distorted) {
            DistortionTwins.restore(pokemon);
        }
    }
}
