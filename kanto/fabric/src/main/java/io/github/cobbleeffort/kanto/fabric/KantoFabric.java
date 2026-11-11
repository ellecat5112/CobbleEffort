package io.github.cobbleeffort.kanto.fabric;

import io.github.cobbleeffort.kanto.Kanto;
import net.fabricmc.api.ModInitializer;

public final class KantoFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        Kanto.init();
    }
}
