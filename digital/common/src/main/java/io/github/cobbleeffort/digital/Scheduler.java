package io.github.cobbleeffort.digital;

import dev.architectury.event.events.common.TickEvent;
import net.minecraft.server.MinecraftServer;

import java.util.ArrayList;
import java.util.List;

/** Run something a few ticks later on the server thread. */
final class Scheduler {
    private static final List<Object[]> TASKS = new ArrayList<>();

    private Scheduler() {
    }

    static void later(MinecraftServer server, int ticks, Runnable task) {
        synchronized (TASKS) {
            TASKS.add(new Object[]{(long) server.getTickCount() + ticks, task});
        }
    }

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            List<Runnable> due = new ArrayList<>();
            synchronized (TASKS) {
                TASKS.removeIf(t -> {
                    if ((long) t[0] <= server.getTickCount()) {
                        due.add((Runnable) t[1]);
                        return true;
                    }
                    return false;
                });
            }
            for (Runnable r : due) {
                try {
                    r.run();
                } catch (Throwable t) {
                    Digital.LOG.error("Scheduled task failed", t);
                }
            }
        });
    }
}
