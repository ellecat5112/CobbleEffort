package io.github.cobbleeffort.digital;

import dev.architectury.registry.client.rendering.RenderTypeRegistry;
import net.minecraft.client.renderer.RenderType;

/** Client setup: the cut-out blocks (the wireframe block's see-through faces). */
public final class DigitalClient {
    private DigitalClient() {
    }

    public static void init() {
        dev.architectury.event.events.client.ClientLifecycleEvent.CLIENT_SETUP.register(mc ->
                RenderTypeRegistry.register(RenderType.cutout(), Digital.WIREFRAME_BLOCK.get(), Digital.CRADLE.get(), Digital.WILD_CRADLE.get()));
    }
}
