package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.api.moves.Move;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.brigadier.arguments.StringArgumentType;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * {@code /distortion align <shadow|crystal> <pokemon>} (operators): builds the Pokémon (a properties string), turns
 * it into that counterpart, reports its types and moves, then purifies it and reports them again. Nothing is given.
 * {@code /distortion convert <player> <slot> <shadow|crystal>} and {@code /distortion purify <player> <slot>}
 * (operators) do it to a party Pokémon; {@code /distortion distort|revert <player> <slot>} (operators) toggle its
 * Distorted form outside battle; {@code /distortion rules} (anyone) lists the game rules.
 */
public final class AlignmentCommand {
    private AlignmentCommand() {
    }

    public static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("distortion")
                        .then(Commands.literal("align").requires(src -> src.hasPermission(2))
                                .then(Commands.argument("kind", StringArgumentType.word()).suggests((c, b) -> b.suggest("shadow").suggest("crystal").buildFuture())
                                        .then(Commands.argument("pokemon", StringArgumentType.greedyString())
                                                .executes(ctx -> run(ctx.getSource(), StringArgumentType.getString(ctx, "kind"),
                                                        StringArgumentType.getString(ctx, "pokemon"))))))
                        .then(Commands.literal("convert").requires(src -> src.hasPermission(2)).then(player().then(slot()
                                .then(Commands.literal("shadow").executes(ctx -> convert(ctx, Alignment.SHADOW_FLAG)))
                                .then(Commands.literal("crystal").executes(ctx -> convert(ctx, Alignment.CRYSTAL_FLAG))))))
                        .then(Commands.literal("purify").requires(src -> src.hasPermission(2))
                                .then(player().then(slot().executes(AlignmentCommand::purify))))
                        .then(Commands.literal("distort").requires(src -> src.hasPermission(2))
                                .then(player().then(slot().executes(ctx -> distort(ctx, true)))))
                        .then(Commands.literal("revert").requires(src -> src.hasPermission(2))
                                .then(player().then(slot().executes(ctx -> distort(ctx, false)))))
                        .then(Commands.literal("rules").executes(AlignmentCommand::rules))));
    }

    private static com.mojang.brigadier.builder.RequiredArgumentBuilder<CommandSourceStack, ?> player() {
        return Commands.argument("player", net.minecraft.commands.arguments.EntityArgument.player());
    }

    private static com.mojang.brigadier.builder.RequiredArgumentBuilder<CommandSourceStack, Integer> slot() {
        return Commands.argument("slot", com.mojang.brigadier.arguments.IntegerArgumentType.integer(1, 6));
    }

    private static Pokemon member(com.mojang.brigadier.context.CommandContext<CommandSourceStack> ctx) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        var player = net.minecraft.commands.arguments.EntityArgument.getPlayer(ctx, "player");
        int slot = com.mojang.brigadier.arguments.IntegerArgumentType.getInteger(ctx, "slot");
        return com.cobblemon.mod.common.Cobblemon.INSTANCE.getStorage().getParty(player).get(slot - 1);
    }

    private static int convert(com.mojang.brigadier.context.CommandContext<CommandSourceStack> ctx, String flag) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        Pokemon p = member(ctx);
        if (p == null) {
            ctx.getSource().sendFailure(Component.literal("That party slot is empty."));
            return 0;
        }
        boolean ok = Alignment.convert(p, flag);
        ctx.getSource().sendSuccess(() -> Component.literal(ok ? p.getSpecies().getName() + " is now a "
                + (Alignment.SHADOW_FLAG.equals(flag) ? "Shadow" : "Crystal") + " Pokémon." : "It couldn't be converted (already aligned?)."), true);
        return ok ? 1 : 0;
    }

    private static int purify(com.mojang.brigadier.context.CommandContext<CommandSourceStack> ctx) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        Pokemon p = member(ctx);
        if (p == null) {
            ctx.getSource().sendFailure(Component.literal("That party slot is empty."));
            return 0;
        }
        boolean ok = Alignment.restore(p);
        ctx.getSource().sendSuccess(() -> Component.literal(ok ? p.getSpecies().getName() + " is purified." : "It wasn't Shadow or Crystal."), true);
        return ok ? 1 : 0;
    }

    private static int distort(com.mojang.brigadier.context.CommandContext<CommandSourceStack> ctx, boolean on) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
        Pokemon p = member(ctx);
        if (p == null || !DistortionRules.hasDistortedForm(p.getSpecies())) {
            ctx.getSource().sendFailure(Component.literal("That Pokémon has no Distorted form."));
            return 0;
        }
        if (DistortionRules.distortedOutside(p) == on) {
            ctx.getSource().sendFailure(Component.literal(on ? "It's already distorted." : "It isn't distorted."));
            return 0;
        }
        DistortionRules.setDistortedOutside(p, on);
        ctx.getSource().sendSuccess(() -> Component.literal(p.getSpecies().getName() + (on ? " distorted." : " reverted.")), true);
        return 1;
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    private static int rules(com.mojang.brigadier.context.CommandContext<CommandSourceStack> ctx) {
        var rules = ctx.getSource().getLevel().getGameRules();
        ctx.getSource().sendSuccess(() -> Component.literal("CobbleEffort: Distortion game rules (/gamerule <name> <value>):")
                .withStyle(net.minecraft.ChatFormatting.LIGHT_PURPLE), false);
        for (var e : DistortionGameRules.ALL.entrySet()) {
            String v = rules.getRule((net.minecraft.world.level.GameRules.Key) e.getValue()).serialize();
            ctx.getSource().sendSuccess(() -> Component.literal("  " + e.getKey() + " = ").withStyle(net.minecraft.ChatFormatting.GRAY)
                    .append(Component.literal(v).withStyle(net.minecraft.ChatFormatting.WHITE)), false);
        }
        return DistortionGameRules.ALL.size();
    }

    private static String describe(Pokemon p) {
        List<String> types = new ArrayList<>(), moves = new ArrayList<>();
        for (ElementalType t : p.getTypes()) types.add(t.getName());
        for (Move m : p.getMoveSet()) if (m != null) moves.add(m.getName());
        return p.getSpecies().getName() + " " + String.join("/", types) + " (secondary " + (p.getSecondaryType() == null ? "-"
                : p.getSecondaryType().getName()) + ", aspects " + p.getAspects() + "): " + String.join(", ", moves);
    }

    private static int run(CommandSourceStack src, String kind, String props) {
        String flag = kind.startsWith("s") ? Alignment.SHADOW_FLAG : Alignment.CRYSTAL_FLAG;
        Pokemon p;
        try {
            p = PokemonProperties.Companion.parse(props).create();
        } catch (Throwable t) {
            src.sendFailure(Component.literal("Unknown Pokémon: " + props));
            return 0;
        }
        src.sendSuccess(() -> Component.literal("before:   " + describe(p)), false);
        boolean ok = Alignment.convert(p, flag);
        src.sendSuccess(() -> Component.literal("as " + kind + " (" + ok + "): " + describe(p)), false);
        boolean back = Alignment.restore(p);
        src.sendSuccess(() -> Component.literal("purified (" + back + "): " + describe(p)), false);
        return 1;
    }
}
