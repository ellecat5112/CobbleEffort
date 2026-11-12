package io.github.cobbleeffort.kanto;

import com.mojang.brigadier.CommandDispatcher;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;

/** /kanto gyms: where Kanto's gyms are. /kanto rebuild (operators): build the gyms and trainers again. */
public final class KantoCommand {
    private KantoCommand() {
    }

    static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> register(dispatcher));
    }

    private static Region here(CommandSourceStack src) {
        Region r = Region.of(src.getLevel().dimension());
        return r == null ? Region.KANTO : r;
    }

    private static int rebuild(CommandSourceStack src, Region region) {
        ServerLevel level = src.getServer().getLevel(region.dimension);
        if (level == null) {
            src.sendFailure(Component.translatable(Kanto.MOD_ID + ".pc.no_kanto"));
            return 0;
        }
        KantoGyms.ensureBuilt(level, region, true);
        src.sendSuccess(() -> Component.translatable(Kanto.MOD_ID + ".gyms.building"), true);
        return 1;
    }

    private static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        var rebuild = Commands.literal("rebuild").requires(src -> src.hasPermission(2))
                .executes(ctx -> rebuild(ctx.getSource(), here(ctx.getSource())));
        var gyms = Commands.literal("gyms").executes(ctx -> {
            Region r = here(ctx.getSource());
            ctx.getSource().sendSuccess(() -> KantoGyms.where(r), false);
            return 1;
        });
        for (Region r : Region.values()) {
            rebuild.then(Commands.literal(r.id).executes(ctx -> rebuild(ctx.getSource(), r)));
            gyms.then(Commands.literal(r.id).executes(ctx -> {
                ctx.getSource().sendSuccess(() -> KantoGyms.where(r), false);
                return 1;
            }));
        }
        dispatcher.register(Commands.literal("kanto").then(gyms).then(rebuild));
    }
}
