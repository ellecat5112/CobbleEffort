package io.github.cobbleeffort.distortion.neoforge;

import io.github.cobbleeffort.distortion.Distortion;
import net.neoforged.fml.common.Mod;

@Mod(Distortion.MOD_ID)
public final class DistortionNeoForge {
    public DistortionNeoForge() {
        Distortion.init();
    }
}
