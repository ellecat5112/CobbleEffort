package io.github.cobbleeffort.digital;

import com.mojang.brigadier.arguments.IntegerArgumentType;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

/** /digital (operators): raid start|stop, rift, crest charge, world (travel), for testing and server events. */
final class DigitalCommand {
    private DigitalCommand() {
    }

    static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("digital").requires(s -> s.hasPermission(2))
                        .then(Commands.literal("raid")
                                .then(Commands.literal("start").executes(c -> {
                                    ServerPlayer p = c.getSource().getPlayerOrException();
                                    boolean ok = Raids.start(p);
                                    c.getSource().sendSuccess(() -> Component.literal(ok ? "Raid started." : "A raid is already on (or no boss is loaded)."), true);
                                    return ok ? 1 : 0;
                                }).then(Commands.argument("player", EntityArgument.player()).executes(c -> {
                                    boolean ok = Raids.start(EntityArgument.getPlayer(c, "player"));
                                    c.getSource().sendSuccess(() -> Component.literal(ok ? "Raid started." : "A raid is already on (or no boss is loaded)."), true);
                                    return ok ? 1 : 0;
                                })))
                                .then(Commands.literal("stop").executes(c -> {
                                    Raids.stop(c.getSource().getServer(), false);
                                    c.getSource().sendSuccess(() -> Component.literal("Raid stopped."), true);
                                    return 1;
                                })))
                        .then(Commands.literal("rift").executes(c -> {
                            DigitalWorld.openRift(c.getSource().getPlayerOrException());
                            return 1;
                        }))
                        .then(Commands.literal("world").executes(c -> {
                            DigitalWorld.travel(c.getSource().getPlayerOrException());
                            return 1;
                        }))
                        .then(Commands.literal("crest").then(Commands.argument("charge", IntegerArgumentType.integer(0, 100)).executes(c -> {
                            ServerPlayer p = c.getSource().getPlayerOrException();
                            ItemStack tag = Crests.findTag(p);
                            if (tag.isEmpty()) {
                                c.getSource().sendFailure(Component.literal("No Tag in your inventory."));
                                return 0;
                            }
                            Crests.setCharge(tag, IntegerArgumentType.getInteger(c, "charge"));
                            return 1;
                        })))));
    }
}
