package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.drop.DropEntry;
import com.cobblemon.mod.common.api.drop.DropTable;
import com.cobblemon.mod.common.api.drop.ItemDropEntry;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import java.util.Map;
import java.util.TreeMap;

/**
 * Testing commands for drops (operators):
 * <ul>
 *   <li>{@code /kanto drops <pokemon>} / {@code /kanto drops roll <rolls> <pokemon>}: rolls the Pokémon's drop table
 *   that many times (default 100) exactly as Cobblemon does when it is defeated, and lists how often each item came up;
 *   nothing is given.</li>
 *   <li>{@code /kanto drops give <rolls> <pokemon>}: the same, but really drops the items into your inventory.</li>
 *   <li>{@code /kanto drops force <pokemon>}: gives one of every entry in its drop table, chance or no chance (e.g. the
 *   Garbage Bag from Garbodor).</li>
 *   <li>{@code /kanto dna [battles]}: simulates winning that many battles with a Mew in your party (CobbleEffort:
 *   Distortion gives 3-8 Mew DNA per Pokémon defeated) and gives you the Mew DNA.</li>
 * </ul>
 * {@code <pokemon>} is a Pokémon properties string (the rest of the line), e.g. {@code slugma cobbleeffortian}.
 */
public final class KantoDrops {
    private KantoDrops() {
    }

    static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        // the Pokemon comes last and takes the rest of the line, so ids with ':' and spaces need no quotes
        var drops = Commands.literal("drops").requires(src -> src.hasPermission(2))
                .then(Commands.literal("roll").then(Commands.argument("rolls", IntegerArgumentType.integer(1, 100000))
                        .then(Commands.argument("pokemon", StringArgumentType.greedyString())
                                .executes(ctx -> roll(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon"),
                                        IntegerArgumentType.getInteger(ctx, "rolls"), false)))))
                .then(Commands.literal("give").then(Commands.argument("rolls", IntegerArgumentType.integer(1, 1000))
                        .then(Commands.argument("pokemon", StringArgumentType.greedyString())
                                .executes(ctx -> roll(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon"),
                                        IntegerArgumentType.getInteger(ctx, "rolls"), true)))))
                .then(Commands.literal("force").then(Commands.argument("pokemon", StringArgumentType.greedyString())
                        .executes(ctx -> force(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon")))))
                .then(Commands.argument("pokemon", StringArgumentType.greedyString())
                        .executes(ctx -> roll(ctx.getSource(), StringArgumentType.getString(ctx, "pokemon"), 100, false)));
        var dna = Commands.literal("dna").requires(src -> src.hasPermission(2))
                .executes(ctx -> dna(ctx.getSource(), 1))
                .then(Commands.argument("battles", IntegerArgumentType.integer(1, 1000))
                        .executes(ctx -> dna(ctx.getSource(), IntegerArgumentType.getInteger(ctx, "battles"))));
        dispatcher.register(Commands.literal("kanto").then(drops).then(dna));
    }

    private static Pokemon make(CommandSourceStack src, String props) {
        try {
            Pokemon p = PokemonProperties.Companion.parse(props).create();
            if (p.getSpecies() == null) throw new IllegalArgumentException("no species");
            return p;
        } catch (Throwable t) {
            src.sendFailure(Component.literal("Unknown Pokémon: " + props));
            return null;
        }
    }

    private static String itemName(ItemDropEntry e) {
        Item item = BuiltInRegistries.ITEM.get(e.getItem());
        String name = new ItemStack(item).getHoverName().getString();
        // our data-made items (Garbage Bag, fossils) are vanilla items told apart by their components
        if (e.getComponents() != null && e.getComponents().toString().contains("custom_name")) {
            String json = e.getComponents().toString();
            int i = json.indexOf("item.");
            if (i >= 0) {
                int j = json.indexOf('\\', i);
                if (j < 0) j = json.indexOf('"', i);
                if (j > i) name = Component.translatable(json.substring(i, j)).getString();
            }
        }
        return name;
    }

    private static int roll(CommandSourceStack src, String props, int rolls, boolean give) {
        Pokemon p = make(src, props);
        if (p == null) return 0;
        DropTable table = p.getForm().getDrops();
        ServerPlayer player = src.getPlayer();
        if (give && player == null) {
            src.sendFailure(Component.literal("Only a player can be given drops."));
            return 0;
        }
        Map<String, Integer> counts = new TreeMap<>();
        int nothing = 0;
        for (int i = 0; i < rolls; i++) {
            var drops = table.getDrops(table.getAmount(), p);
            if (drops.isEmpty()) nothing++;
            for (DropEntry e : drops) {
                String key = e instanceof ItemDropEntry ide ? itemName(ide) : e.getClass().getSimpleName();
                counts.merge(key, 1, Integer::sum);
                if (give) e.drop(null, src.getLevel(), player.position(), player);
            }
        }
        src.sendSuccess(() -> Component.literal(p.getSpecies().getTranslatedName().getString() + ": " + rolls
                + (rolls == 1 ? " defeat" : " defeats") + (give ? " (items given)" : " (simulated)")).withStyle(ChatFormatting.GOLD), false);
        for (var c : counts.entrySet()) {
            String pct = String.format("%.1f%%", 100.0 * c.getValue() / rolls);
            src.sendSuccess(() -> Component.literal("  " + c.getKey() + ": " + c.getValue() + " (" + pct + ")"), false);
        }
        int none = nothing;
        if (counts.isEmpty()) src.sendSuccess(() -> Component.literal("  nothing dropped"), false);
        else if (none > 0) src.sendSuccess(() -> Component.literal("  nothing at all: " + none).withStyle(ChatFormatting.GRAY), false);
        return counts.size();
    }

    private static int force(CommandSourceStack src, String props) {
        Pokemon p = make(src, props);
        ServerPlayer player = src.getPlayer();
        if (p == null || player == null) {
            if (player == null) src.sendFailure(Component.literal("Only a player can be given drops."));
            return 0;
        }
        int n = 0;
        for (DropEntry e : p.getForm().getDrops().getEntries()) {
            e.drop(null, src.getLevel(), player.position(), player);
            n++;
        }
        int given = n;
        src.sendSuccess(() -> Component.literal("Gave every drop of " + p.getSpecies().getTranslatedName().getString()
                + " (" + given + " entries).").withStyle(ChatFormatting.GOLD), false);
        return n;
    }

    private static int dna(CommandSourceStack src, int battles) {
        ServerPlayer player = src.getPlayer();
        if (player == null) {
            src.sendFailure(Component.literal("Only a player can be given Mew DNA."));
            return 0;
        }
        Item dna = BuiltInRegistries.ITEM.get(ResourceLocation.parse("cobbleeffort_distortion:mew_dna"));
        if (dna == BuiltInRegistries.ITEM.get(BuiltInRegistries.ITEM.getDefaultKey())) {
            src.sendFailure(Component.literal("CobbleEffort: Distortion's Mew DNA isn't installed."));
            return 0;
        }
        boolean mew = false;
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            if (p != null && "mew".equalsIgnoreCase(p.getSpecies().getName())) mew = true;
        }
        int total = 0;
        for (int i = 0; i < battles; i++) total += 3 + player.getRandom().nextInt(6);     // Distortion's 3-8 per defeat
        int left = total;
        while (left > 0) {
            ItemStack stack = new ItemStack(dna, Math.min(64, left));
            left -= stack.getCount();
            if (!player.getInventory().add(stack)) player.drop(stack, false);
        }
        int got = total;
        boolean hasMew = mew;
        src.sendSuccess(() -> Component.literal("Simulated " + battles + (battles == 1 ? " defeat" : " defeats")
                + ": " + got + " Mew DNA" + (hasMew ? "." : " (no Mew in your party: real battles would give none).")).withStyle(ChatFormatting.GOLD), false);
        return total;
    }
}
