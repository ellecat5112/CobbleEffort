package io.github.cobbleeffort.fusion.fabric;

import io.github.cobbleeffort.fusion.Fusion;
import net.fabricmc.api.ModInitializer;

public final class FusionFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Fusion.init();
    }
}
