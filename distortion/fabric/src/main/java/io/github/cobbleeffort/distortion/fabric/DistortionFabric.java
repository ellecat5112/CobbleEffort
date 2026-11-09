package io.github.cobbleeffort.distortion.fabric;

import io.github.cobbleeffort.distortion.Distortion;
import net.fabricmc.api.ModInitializer;

public final class DistortionFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Distortion.init();
    }
}
