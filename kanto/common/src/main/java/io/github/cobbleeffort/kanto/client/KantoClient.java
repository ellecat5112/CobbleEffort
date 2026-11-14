package io.github.cobbleeffort.kanto.client;

import io.github.cobbleeffort.kanto.Spawners;

/** Client side of the add-on: the spawners' settings screen and the Call of the Den wheel option. */
public final class KantoClient {
    private KantoClient() {
    }

    public static void init() {
        Spawners.screenOpener = SpawnerScreen::open;
        DenCallWheelOption.init();
    }
}
