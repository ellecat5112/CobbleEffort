package io.github.cobbleeffort.digital.neoforge;

import io.github.cobbleeffort.digital.Digital;
import net.neoforged.fml.common.Mod;

@Mod(Digital.MOD_ID)
public final class DigitalNeoForge {
    public DigitalNeoForge() {
        Digital.init();
    }
}
