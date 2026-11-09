package net.neoforged.bus.api;

import java.util.function.Consumer;

/** Compile-time stand-in for NeoForge's event bus (same name and method signature); not packaged. */
public interface IEventBus {
    <T extends Event> void addListener(Class<T> eventType, Consumer<T> consumer);
}
