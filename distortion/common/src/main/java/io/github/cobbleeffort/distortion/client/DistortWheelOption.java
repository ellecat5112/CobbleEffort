package io.github.cobbleeffort.distortion.client;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.pokemon.interaction.PokemonInteractionGUICreationEvent;
import com.cobblemon.mod.common.client.CobblemonClient;
import com.cobblemon.mod.common.client.gui.interact.wheel.InteractWheelOption;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.networking.NetworkManager;
import io.github.cobbleeffort.distortion.Distortion;
import io.github.cobbleeffort.distortion.DistortPacket;
import io.github.cobbleeffort.distortion.DistortionRules;
import kotlin.Unit;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import org.joml.Vector3f;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * The Distort option in Cobblemon's interaction wheel (the radial menu you get on your sent-out Pokémon, where Mega
 * Showdown adds Mega Evolution). Its own entry, through Cobblemon's POKEMON_INTERACTION_GUI_CREATION event, not tied
 * to Mega Showdown's. Shown when the player wears the band and the Pokémon can distort (crystal, or Arceus with a
 * plate, and Distorted forms), or is distorted already (then it reverts it). The server checks everything again.
 */
public final class DistortWheelOption {
    private static final Logger LOG = LoggerFactory.getLogger("CobbleEffort Distortion");
    public static final ResourceLocation ICON = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/gui/interact/distort_wheel.png");
    public static final ResourceLocation REVERT_ICON = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/gui/interact/revert_wheel.png");

    private DistortWheelOption() {
    }

    public static void init() {
        CobblemonEvents.POKEMON_INTERACTION_GUI_CREATION.subscribe(Priority.NORMAL, DistortWheelOption::add);
    }

    private static void add(PokemonInteractionGUICreationEvent event) {
        try {
            Pokemon pokemon = CobblemonClient.INSTANCE.getStorage().getParty().findByUUID(event.getPokemonID());
            if (pokemon == null || !DistortionRules.hasDistortedForm(pokemon.getSpecies())) return;
            boolean distorted = pokemon.getAspects().contains(DistortionRules.FEATURE);   // synced to the client
            if (!distorted && !(DistortionRules.wearsBand(Minecraft.getInstance().player) && DistortionRules.holdsSource(pokemon))) return;
            event.addFillingOption(new InteractWheelOption(
                    distorted ? REVERT_ICON : ICON, null, true,
                    Distortion.MOD_ID + (distorted ? ".ui.revert" : ".ui.distort"),
                    () -> new Vector3f(1F),
                    () -> {
                        NetworkManager.sendToServer(new DistortPacket(event.getPokemonID()));
                        Minecraft.getInstance().setScreen(null);
                        return Unit.INSTANCE;
                    }));
        } catch (Throwable t) {
            LOG.error("Couldn't add the Distort wheel option", t);
        }
    }
}
