package io.github.cobbleeffort.kanto.client;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.pokemon.interaction.PokemonInteractionGUICreationEvent;
import com.cobblemon.mod.common.client.CobblemonClient;
import com.cobblemon.mod.common.client.gui.interact.wheel.InteractWheelOption;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.networking.NetworkManager;
import io.github.cobbleeffort.kanto.DenCall;
import io.github.cobbleeffort.kanto.Kanto;
import kotlin.Unit;
import net.minecraft.client.Minecraft;
import net.minecraft.resources.ResourceLocation;
import org.joml.Vector3f;

/** The Call of the Den option in Cobblemon's interaction wheel: on a Hopple that knows it, with 3+ Hopples in the party. */
public final class DenCallWheelOption {
    public static final ResourceLocation ICON = Kanto.id("textures/gui/interact/call_of_the_den.png");

    private DenCallWheelOption() {
    }

    public static void init() {
        CobblemonEvents.POKEMON_INTERACTION_GUI_CREATION.subscribe(Priority.NORMAL, DenCallWheelOption::add);
    }

    private static void add(PokemonInteractionGUICreationEvent event) {
        try {
            var party = CobblemonClient.INSTANCE.getStorage().getParty();
            Pokemon pokemon = party.findByUUID(event.getPokemonID());
            if (pokemon == null || !DenCall.canCall(pokemon, party)) return;
            event.addFillingOption(new InteractWheelOption(ICON, null, true, Kanto.MOD_ID + ".ui.call_of_the_den",
                    () -> new Vector3f(1F),
                    () -> {
                        NetworkManager.sendToServer(new DenCall.CallPacket(event.getPokemonID()));
                        Minecraft.getInstance().setScreen(null);
                        return Unit.INSTANCE;
                    }));
        } catch (Throwable t) {
            Kanto.LOG.error("Couldn't add the Call of the Den wheel option", t);
        }
    }
}
