package io.github.cobbleeffort.distortion.client;

import com.cobblemon.mod.common.client.CobblemonClient;
import com.cobblemon.mod.common.client.storage.ClientStorageManager;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.networking.NetworkManager;
import dev.architectury.registry.client.rendering.BlockEntityRendererRegistry;
import dev.architectury.registry.client.rendering.RenderTypeRegistry;
import io.github.cobbleeffort.distortion.Distortion;
import io.github.cobbleeffort.distortion.dna.DnaInsertPacket;
import io.github.cobbleeffort.distortion.dna.DnaMachineClientHook;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.network.chat.Component;

/** Client side of the DNA machine: its renderer, its glass render layer, and "put my selected Pokémon in". */
public final class DnaMachineClient {
    private DnaMachineClient() {
    }

    public static void init() {
        Distortion.DNA_MACHINE_ENTITY.listen(type -> BlockEntityRendererRegistry.register(type, DnaMachineRenderer::new));
        Distortion.DNA_MACHINE.listen(block -> RenderTypeRegistry.register(RenderType.translucent(), block));
        DnaMachineClientHook.setSender(pos -> {
            ClientStorageManager storage = CobblemonClient.INSTANCE.getStorage();
            Pokemon selected = storage.getParty().get(storage.getSelectedSlot());
            if (selected == null) {
                if (Minecraft.getInstance().player != null) {
                    Minecraft.getInstance().player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.select_mew"), true);
                }
                return;
            }
            NetworkManager.sendToServer(new DnaInsertPacket(pos, selected.getUuid()));
        });
    }
}
