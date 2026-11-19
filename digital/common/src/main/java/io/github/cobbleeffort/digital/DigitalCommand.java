package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import com.mojang.brigadier.suggestion.SuggestionProvider;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.commands.arguments.ResourceLocationArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameRules;

import java.util.Collection;
import java.util.Map;

/**
 * /digital: raid start|stop, rift, crest charge, world (travel) for testing and server events; hatch (every Digitama
 * in the players' inventories, now), digitama (give eggs, optionally of one Digimon), energy (Tamer Energy on their
 * Digivices), attribute (rewrite a party Digimon's attribute); rules (anyone: the Digital game rules and values).
 */
final class DigitalCommand {
    private DigitalCommand() {
    }

    static final SuggestionProvider<CommandSourceStack> DIGIMON = (c, b) -> SharedSuggestionProvider.suggestResource(
            PokemonSpecies.getImplemented().stream().filter(s -> s.getLabels().contains(DigiBall.LABEL)).map(Species::getResourceIdentifier), b);

    static void init() {
        CommandRegistrationEvent.EVENT.register((dispatcher, registry, selection) -> dispatcher.register(
                Commands.literal("digital")
                        .then(Commands.literal("rules").executes(DigitalCommand::rules))
                        .then(Commands.literal("hatch").requires(s -> s.hasPermission(2))
                                .executes(c -> hatch(c, java.util.List.of(c.getSource().getPlayerOrException())))
                                .then(Commands.argument("targets", EntityArgument.players())
                                        .executes(c -> hatch(c, EntityArgument.getPlayers(c, "targets")))))
                        .then(Commands.literal("digitama").requires(s -> s.hasPermission(2))
                                .then(Commands.argument("targets", EntityArgument.players())
                                        .executes(c -> digitama(c, null, 1))
                                        .then(Commands.argument("species", ResourceLocationArgument.id()).suggests(DIGIMON)
                                                .executes(c -> digitama(c, ResourceLocationArgument.getId(c, "species"), 1))
                                                .then(Commands.argument("count", IntegerArgumentType.integer(1, 64))
                                                        .executes(c -> digitama(c, ResourceLocationArgument.getId(c, "species"),
                                                                IntegerArgumentType.getInteger(c, "count")))))))
                        .then(Commands.literal("energy").requires(s -> s.hasPermission(2))
                                .then(Commands.argument("targets", EntityArgument.players())
                                        .then(Commands.argument("amount", IntegerArgumentType.integer(0, Digivice.MAX_ENERGY))
                                                .executes(DigitalCommand::energy))))
                        .then(Commands.literal("attribute").requires(s -> s.hasPermission(2))
                                .then(Commands.argument("target", EntityArgument.player())
                                        .then(Commands.argument("slot", IntegerArgumentType.integer(1, 6))
                                                .then(attribute(Attribute.VACCINE)).then(attribute(Attribute.DATA))
                                                .then(attribute(Attribute.VIRUS)).then(attribute(Attribute.FREE))
                                                .then(attribute(Attribute.VARIABLE)))))
                        .then(Commands.literal("raid").requires(s -> s.hasPermission(2))
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
                        .then(Commands.literal("rift").requires(s -> s.hasPermission(2)).executes(c -> {
                            DigitalWorld.openRift(c.getSource().getPlayerOrException());
                            return 1;
                        }))
                        .then(Commands.literal("rank").executes(c -> {
                            ServerPlayer p = c.getSource().getPlayerOrException();
                            int pts = Tamers.points(p);
                            c.getSource().sendSuccess(() -> Component.translatable(Digital.MOD_ID + ".tamer.rank", pts,
                                    Component.translatable(Digital.MOD_ID + ".rank." + Tamers.RANK_NAMES[Tamers.rankOf(pts)])), false);
                            return 1;
                        }))
                        .then(Commands.literal("world").requires(s -> s.hasPermission(2)).executes(c -> {
                            DigitalWorld.travel(c.getSource().getPlayerOrException());
                            return 1;
                        }))
                        .then(Commands.literal("crest").requires(s -> s.hasPermission(2)).then(Commands.argument("charge", IntegerArgumentType.integer(0, 100)).executes(c -> {
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

    private static com.mojang.brigadier.builder.LiteralArgumentBuilder<CommandSourceStack> attribute(Attribute a) {
        return Commands.literal(a.id()).executes(c -> {
            ServerPlayer target = EntityArgument.getPlayer(c, "target");
            int slot = IntegerArgumentType.getInteger(c, "slot");
            Pokemon p = Cobblemon.INSTANCE.getStorage().getParty(target).get(slot - 1);
            if (!Attributes.isDigimon(p)) {
                c.getSource().sendFailure(Component.literal("Slot " + slot + " of " + target.getScoreboardName() + " isn't a Digimon."));
                return 0;
            }
            Attributes.set(p, a);
            c.getSource().sendSuccess(() -> Component.literal(p.getSpecies().getName() + " is now " + a.display() + "."), true);
            return 1;
        });
    }

    private static int hatch(CommandContext<CommandSourceStack> c, Collection<ServerPlayer> players) {
        int total = 0;
        for (ServerPlayer p : players) total += DigitamaItem.hatchAll(p);
        int n = total;
        if (n == 0) c.getSource().sendFailure(Component.literal("No Digitama to hatch."));
        else c.getSource().sendSuccess(() -> Component.literal("Hatched " + n + " Digitama."), true);
        return n;
    }

    private static int digitama(CommandContext<CommandSourceStack> c, ResourceLocation species, int count) throws CommandSyntaxException {
        if (species != null) {
            Species s = PokemonSpecies.getByIdentifier(species);
            if (s == null || !s.getLabels().contains(DigiBall.LABEL)) {
                c.getSource().sendFailure(Component.literal(species + " isn't a Digimon."));
                return 0;
            }
        }
        Collection<ServerPlayer> players = EntityArgument.getPlayers(c, "targets");
        for (ServerPlayer p : players) {
            for (int i = 0; i < count; i++) {
                ItemStack egg = DigitamaItem.egg(species == null ? null : species.toString());
                if (!p.getInventory().add(egg)) p.drop(egg, false);
            }
        }
        c.getSource().sendSuccess(() -> Component.literal("Gave " + count + " Digitama" + (species == null ? "" : " (" + species + ")")
                + " to " + players.size() + " player(s)."), true);
        return players.size();
    }

    private static int energy(CommandContext<CommandSourceStack> c) throws CommandSyntaxException {
        int amount = IntegerArgumentType.getInteger(c, "amount"), n = 0;
        for (ServerPlayer p : EntityArgument.getPlayers(c, "targets")) {
            var inv = p.getInventory();
            for (int i = 0; i < inv.getContainerSize(); i++) {
                if (inv.getItem(i).getItem() instanceof Digivice) {
                    Digivice.setEnergy(inv.getItem(i), amount);
                    n++;
                }
            }
        }
        int set = n;
        if (set == 0) c.getSource().sendFailure(Component.literal("No Digivice found."));
        else c.getSource().sendSuccess(() -> Component.literal("Set Tamer Energy to " + amount + " on " + set + " Digivice(s)."), true);
        return set;
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    private static int rules(CommandContext<CommandSourceStack> c) {
        GameRules rules = c.getSource().getLevel().getGameRules();
        c.getSource().sendSuccess(() -> Component.literal("CobbleEffort: Digital game rules (/gamerule <name> <value>):")
                .withStyle(ChatFormatting.AQUA), false);
        for (Map.Entry<String, GameRules.Key<?>> e : DigitalRules.ALL.entrySet()) {
            String v = rules.getRule((GameRules.Key) e.getValue()).serialize();
            c.getSource().sendSuccess(() -> Component.literal("  " + e.getKey() + " = ").withStyle(ChatFormatting.GRAY)
                    .append(Component.literal(v).withStyle(ChatFormatting.WHITE)), false);
        }
        return DigitalRules.ALL.size();
    }
}
