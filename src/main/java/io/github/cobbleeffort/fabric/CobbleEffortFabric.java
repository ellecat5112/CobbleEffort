package io.github.cobbleeffort.fabric;

import io.github.cobbleeffort.CreativeTab;
import net.fabricmc.api.ModInitializer;

/** Fabric entry point (fabric.mod.json "main"): adds the creative tab. Never loaded on NeoForge. */
public final class CobbleEffortFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        try {
            new CreativeTab(true).registerFabric();
        } catch (Throwable t) {
            CreativeTab.log("creative tab not registered", t);
        }
    }
}
