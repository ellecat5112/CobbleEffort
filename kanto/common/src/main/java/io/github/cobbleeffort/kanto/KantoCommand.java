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

    private static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(Commands.literal("kanto")
                .then(Commands.literal("gyms").executes(ctx -> {
                    ctx.getSource().sendSuccess(KantoGyms::where, false);
                    return 1;
                }))
                .then(Commands.literal("rebuild").requires(src -> src.hasPermission(2)).executes(ctx -> {
                    ServerLevel kanto = ctx.getSource().getServer().getLevel(Kanto.KANTO);
                    if (kanto == null) {
                        ctx.getSource().sendFailure(Component.translatable(Kanto.MOD_ID + ".pc.no_kanto"));
                        return 0;
                    }
                    KantoGyms.ensureBuilt(kanto, true);
                    ctx.getSource().sendSuccess(() -> Component.translatable(Kanto.MOD_ID + ".gyms.building"), true);
                    return 1;
                })));
    }
}
