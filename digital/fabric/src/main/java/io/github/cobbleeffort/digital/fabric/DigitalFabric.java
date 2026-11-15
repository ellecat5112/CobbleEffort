package io.github.cobbleeffort.digital.fabric;

import io.github.cobbleeffort.digital.Digital;
import net.fabricmc.api.ModInitializer;

public final class DigitalFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Digital.init();
    }
}
