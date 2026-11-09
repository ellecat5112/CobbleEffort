package io.github.cobbleeffort.neoforge;

import io.github.cobbleeffort.CreativeTab;
import java.util.function.Consumer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

/** NeoForge entry point: adds the creative tab when the registries are filled. Never loaded on Fabric. */
@Mod(CreativeTab.MOD_ID)
public final class CobbleEffortNeoForge {
    @SuppressWarnings({"unchecked", "rawtypes"})
    public CobbleEffortNeoForge(IEventBus modBus) {
        try {
            CreativeTab tab = new CreativeTab(false);
            Class event = Class.forName("net.neoforged.neoforge.registries.RegisterEvent", false, CobbleEffortNeoForge.class.getClassLoader());
            Consumer listener = (Consumer<Object>) e -> {
                try {
                    tab.onRegisterEvent(e);
                } catch (Throwable t) {
                    CreativeTab.log("creative tab not registered", t);
                }
            };
            modBus.addListener(event, listener);
        } catch (Throwable t) {
            CreativeTab.log("creative tab not registered", t);
        }
    }
}
