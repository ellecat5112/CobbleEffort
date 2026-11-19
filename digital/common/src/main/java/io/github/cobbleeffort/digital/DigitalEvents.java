package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.battles.BattleFaintedEvent;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.events.common.LootEvent;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.EmptyLootItem;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.functions.SetItemCountFunction;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;
import net.minecraft.world.level.storage.loot.providers.number.UniformGenerator;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * What defeated Digimon leave behind (Digitama, attribute fragments, Digi-Meat), chest loot, and the battle engine's
 * attribute table as each battle starts.
 */
public final class DigitalEvents {
    // One Digimon defeated in battle: game rule digitalDigitamaDropChance (percent, default 5) of a Digitama for each
    // player on the winning side.
    /** ... of attribute fragments (1 for babies and Child, more for higher stages). */
    static final double FRAGMENT_CHANCE = 0.65;
    /** ... of a Digi-Meat (to start a farm). */
    static final double MEAT_CHANCE = 0.15;
    /** Chest loot tables -> the Digitama's weight against an empty entry of weight 100. */
    static final Map<String, Integer> CHESTS = Map.of(
            "chests/simple_dungeon", 12, "chests/abandoned_mineshaft", 8, "chests/desert_pyramid", 10,
            "chests/jungle_temple", 12, "chests/ancient_city", 15,
            "chests/village/village_plains_house", 3, "chests/village/village_savanna_house", 3,
            "chests/village/village_taiga_house", 3, "chests/village/village_desert_house", 3);
    /** Village and dungeon chests that also hold Digi-Meat and Super Carrots (weight against empty 100). */
    static final Map<String, Integer> FOOD_CHESTS = Map.of(
            "chests/village/village_plains_house", 30, "chests/village/village_savanna_house", 30,
            "chests/village/village_taiga_house", 30, "chests/village/village_desert_house", 30,
            "chests/village/village_snowy_house", 30, "chests/simple_dungeon", 20, "chests/abandoned_mineshaft", 15);

    /** Dungeon chests that hold Digi-Modify cards (weight of one card against empty 100). */
    static final Map<String, Integer> CARD_CHESTS = Map.of(
            "chests/simple_dungeon", 10, "chests/abandoned_mineshaft", 6, "chests/ancient_city", 14,
            "chests/stronghold_library", 12, "chests/buried_treasure", 15, "chests/desert_pyramid", 8, "chests/jungle_temple", 8);

    private DigitalEvents() {
    }

    static void init() {
        CobblemonEvents.BATTLE_FAINTED.subscribe(Priority.NORMAL, event -> {
            MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
            Runnable drop = () -> {
                try {
                    drops(event);
                } catch (Throwable t) {
                    Digital.LOG.error("Digimon drops failed", t);
                }
            };
            if (server != null) server.execute(drop);
            else drop.run();
            return kotlin.Unit.INSTANCE;
        });
        CobblemonEvents.BATTLE_STARTED_PRE.subscribe(Priority.LOWEST, event -> {
            try {
                if (!event.isCanceled()) DigitalEngine.prepare(event.getBattle());
            } catch (Throwable t) {
                Digital.LOG.error("Digimon battle setup failed", t);
            }
            return kotlin.Unit.INSTANCE;
        });
        LootEvent.MODIFY_LOOT_TABLE.register((key, context, builtin) -> {
            if (!builtin || !key.location().getNamespace().equals("minecraft")) return;
            String path = key.location().getPath();
            Integer weight = CHESTS.get(path);
            if (weight != null && weight > 0) {
                context.addPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1))
                        .add(LootItem.lootTableItem(Digital.DIGITAMA.get()).setWeight(weight))
                        .add(EmptyLootItem.emptyItem().setWeight(100)));
            }
            Integer cards = CARD_CHESTS.get(path);
            if (cards != null) {
                LootPool.Builder pool = LootPool.lootPool().setRolls(ConstantValue.exactly(1)).add(EmptyLootItem.emptyItem().setWeight(100));
                for (var c : Digital.CARD_ITEMS.values()) {
                    pool.add(LootItem.lootTableItem(c.get()).setWeight(cards).apply(SetItemCountFunction.setCount(UniformGenerator.between(1, 2))));
                }
                context.addPool(pool);
            }
            Integer food = FOOD_CHESTS.get(path);
            if (food != null) {
                context.addPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1))
                        .add(LootItem.lootTableItem(Digital.DIGIMEAT.get()).setWeight(food)
                                .apply(SetItemCountFunction.setCount(UniformGenerator.between(1, 3))))
                        .add(LootItem.lootTableItem(Digital.SUPER_CARROT.get()).setWeight(food / 3))
                        .add(EmptyLootItem.emptyItem().setWeight(100)));
            }
        });
    }

    static boolean digimon(BattlePokemon pokemon) {
        return Attributes.isDigimon(pokemon.getOriginalPokemon());
    }

    /** Fragments for a defeated Digimon's stage: 1 (Baby, Child), 1-2 (Adult), 2-3 (Perfect), 3-4 (Ultimate and up). */
    static int fragments(Pokemon p, RandomSource r) {
        if (DigiBall.hasAny(p, java.util.Set.of("digimon_ultimate", "digimon_super_ultimate"))) return 3 + r.nextInt(2);
        if (DigiBall.hasAny(p, java.util.Set.of("digimon_perfect"))) return 2 + r.nextInt(2);
        if (DigiBall.hasAny(p, DigiBall.CHAMPION)) return 1 + r.nextInt(2);
        return 1;
    }

    private static void drops(BattleFaintedEvent event) {
        BattlePokemon killed = event.getKilled();
        if (!digimon(killed)) return;
        Pokemon kp = killed.getOriginalPokemon();
        boolean wild = kp.getOwnerUUID() == null;
        for (BattleActor actor : event.getBattle().getActors()) {
            if (!(actor instanceof PlayerBattleActor player) || actor.getSide() == killed.getActor().getSide()) continue;
            ServerPlayer entity = player.getEntity();
            if (entity == null) continue;
            RandomSource r = entity.getRandom();
            List<ItemStack> loot = new ArrayList<>();
            if (r.nextInt(100) < DigitalRules.value(entity.level(), DigitalRules.DIGITAMA_CHANCE)) {
                loot.add(new ItemStack(Digital.DIGITAMA.get()));
                entity.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digitama.dropped",
                        kp.getSpecies().getTranslatedName()), true);
            }
            if (wild && r.nextDouble() < FRAGMENT_CHANCE) {
                Attribute a = Attributes.ofSpecies(kp);
                if (a == null || !a.triangle()) a = new Attribute[]{Attribute.VACCINE, Attribute.DATA, Attribute.VIRUS}[r.nextInt(3)];
                Item fragment = Digital.FRAGMENTS.get(a).get();
                loot.add(new ItemStack(fragment, fragments(kp, r)));
            }
            if (wild && r.nextDouble() < MEAT_CHANCE) loot.add(new ItemStack(Digital.DIGIMEAT.get()));
            PokemonEntity at = killed.getEntity();
            for (ItemStack stack : loot) {
                if (at != null && at.level() == entity.level()) {
                    ItemEntity drop = new ItemEntity(at.level(), at.getX(), at.getY() + 0.5, at.getZ(), stack);
                    drop.setDefaultPickUpDelay();
                    at.level().addFreshEntity(drop);
                } else if (!entity.getInventory().add(stack)) {
                    entity.drop(stack, false);
                }
            }
        }
    }
}
