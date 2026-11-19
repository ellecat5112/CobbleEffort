package io.github.cobbleeffort.kanto;

import com.mojang.brigadier.CommandDispatcher;
import dev.architectury.event.events.common.CommandRegistrationEvent;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.arguments.EntityArgument;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.GameRules;

/** /kanto gyms: where Kanto's gyms are. /kanto rebuild (operators): build the gyms and trainers again. /kanto forcebiome
 * (operators): paint the Ashtray Wastes or Liquor Meadows round a position, like the Biome Wand. /kanto travel <region>
 * [players] and /kanto home [players] (operators): into a region / back to where they came from. /kanto badges [player]
 * (others' need operator) and /kanto badges <player> give|clear <region> (operators). /kanto rules: the game rules. */
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

    /** /kanto forcebiome <biome> [pos] (operators): what the Biome Wand does on a block, for command blocks too. */
    private static int forceBiome(CommandSourceStack src, net.minecraft.resources.ResourceLocation biome, net.minecraft.core.BlockPos pos) {
        TestTools.forceBiome(src.getLevel(), pos, biome, c -> src.sendSuccess(() -> c, true));
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
        var force = Commands.literal("forcebiome").requires(src -> src.hasPermission(2));
        for (net.minecraft.resources.ResourceLocation biome : TestTools.BIOMES) {
            force.then(Commands.literal(biome.getPath())
                    .executes(ctx -> forceBiome(ctx.getSource(), biome, net.minecraft.core.BlockPos.containing(ctx.getSource().getPosition())))
                    .then(Commands.argument("pos", net.minecraft.commands.arguments.coordinates.BlockPosArgument.blockPos())
                            .executes(ctx -> forceBiome(ctx.getSource(), biome,
                                    net.minecraft.commands.arguments.coordinates.BlockPosArgument.getLoadedBlockPos(ctx, "pos")))));
        }
        var travel = Commands.literal("travel").requires(src -> src.hasPermission(2));
        var badgeGive = Commands.literal("give");
        var badgeClear = Commands.literal("clear");
        for (Region r : Region.values()) {
            travel.then(Commands.literal(r.id)
                    .executes(ctx -> travel(ctx.getSource(), java.util.List.of(ctx.getSource().getPlayerOrException()), r))
                    .then(Commands.argument("targets", EntityArgument.players())
                            .executes(ctx -> travel(ctx.getSource(), EntityArgument.getPlayers(ctx, "targets"), r))));
            badgeGive.then(Commands.literal(r.id).executes(ctx -> badges(ctx.getSource(), EntityArgument.getPlayer(ctx, "player"), r, true)));
            badgeClear.then(Commands.literal(r.id).executes(ctx -> badges(ctx.getSource(), EntityArgument.getPlayer(ctx, "player"), r, false)));
        }
        var home = Commands.literal("home").requires(src -> src.hasPermission(2))
                .executes(ctx -> home(ctx.getSource(), java.util.List.of(ctx.getSource().getPlayerOrException())))
                .then(Commands.argument("targets", EntityArgument.players())
                        .executes(ctx -> home(ctx.getSource(), EntityArgument.getPlayers(ctx, "targets"))));
        var badges = Commands.literal("badges")
                .executes(ctx -> listBadges(ctx.getSource(), ctx.getSource().getPlayerOrException()))
                .then(Commands.argument("player", EntityArgument.player()).requires(src -> src.hasPermission(2))
                        .executes(ctx -> listBadges(ctx.getSource(), EntityArgument.getPlayer(ctx, "player")))
                        .then(badgeGive).then(badgeClear));
        var rules = Commands.literal("rules").executes(ctx -> rules(ctx.getSource()));
        dispatcher.register(Commands.literal("kanto").then(gyms).then(rebuild).then(force).then(travel).then(home)
                .then(badges).then(rules));
        KantoDrops.register(dispatcher);                           // /kanto drops, /kanto dna (testing)
    }

    private static int travel(CommandSourceStack src, java.util.Collection<ServerPlayer> players, Region region) {
        int n = 0;
        for (ServerPlayer p : players) {
            if (p.level().dimension() == region.dimension) continue;          // already there (travelling would send it home)
            KantoTravel.travel(p, region);
            n++;
        }
        int moved = n;
        src.sendSuccess(() -> Component.literal("Sent " + moved + " player(s) to " + KantoGyms.nameOf(region) + "."), true);
        return moved;
    }

    private static int home(CommandSourceStack src, java.util.Collection<ServerPlayer> players) {
        int n = 0;
        for (ServerPlayer p : players) {
            Region r = Region.of(p.level().dimension());
            if (r == null) continue;
            KantoTravel.travel(p, r);                                           // from inside a region: home
            n++;
        }
        int moved = n;
        if (moved == 0) src.sendFailure(Component.literal("Nobody to send home (not in a region)."));
        else src.sendSuccess(() -> Component.literal("Sent " + moved + " player(s) home."), true);
        return moved;
    }

    private static int listBadges(CommandSourceStack src, ServerPlayer player) {
        src.sendSuccess(() -> Component.literal(player.getScoreboardName() + "'s badges:").withStyle(ChatFormatting.GOLD), false);
        for (Component line : KantoGyms.badgeSummary(player)) src.sendSuccess(() -> Component.literal("  ").append(line), false);
        return 1;
    }

    private static int badges(CommandSourceStack src, ServerPlayer player, Region region, boolean give) {
        int n = KantoGyms.setRegionBadges(player, region, give);
        src.sendSuccess(() -> Component.literal((give ? "Gave " : "Cleared ") + n + " " + KantoGyms.nameOf(region) + " badge(s) "
                + (give ? "to " : "from ") + player.getScoreboardName() + "."), true);
        return n;
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    private static int rules(CommandSourceStack src) {
        GameRules rules = src.getLevel().getGameRules();
        src.sendSuccess(() -> Component.literal("CobbleEffort: Kanto game rules (/gamerule <name> <value>):").withStyle(ChatFormatting.GOLD), false);
        for (java.util.Map.Entry<String, GameRules.Key<?>> e : KantoRules.ALL.entrySet()) {
            String v = rules.getRule((GameRules.Key) e.getValue()).serialize();
            src.sendSuccess(() -> Component.literal("  " + e.getKey() + " = ").withStyle(ChatFormatting.GRAY)
                    .append(Component.literal(v).withStyle(ChatFormatting.WHITE)), false);
        }
        return KantoRules.ALL.size();
    }
}
