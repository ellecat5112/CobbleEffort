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
 */
public final class AlignmentCommand {
    private AlignmentCommand() {
    }

    public static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("distortion").requires(src -> src.hasPermission(2)).then(Commands.literal("align")
                        .then(Commands.argument("kind", StringArgumentType.word()).suggests((c, b) -> b.suggest("shadow").suggest("crystal").buildFuture())
                                .then(Commands.argument("pokemon", StringArgumentType.greedyString())
                                        .executes(ctx -> run(ctx.getSource(), StringArgumentType.getString(ctx, "kind"),
                                                StringArgumentType.getString(ctx, "pokemon"))))))));
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
