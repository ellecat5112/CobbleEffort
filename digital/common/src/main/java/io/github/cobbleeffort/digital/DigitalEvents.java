package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.battles.BattleFaintedEvent;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import dev.architectury.event.events.common.LootEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.EmptyLootItem;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;

import java.util.Map;

/** Where Digitama come from: defeated wild Digimon, and chests in dungeons, mineshafts, ruins and villages. */
public final class DigitalEvents {
    /** One Digimon defeated in battle: this chance of a Digitama for each player on the winning side. */
    static final double DIGITAMA_CHANCE = 0.05;
    /** Chest loot tables -> the Digitama's weight against an empty entry of weight 100. */
    static final Map<String, Integer> CHESTS = Map.of(
            "chests/simple_dungeon", 12, "chests/abandoned_mineshaft", 8, "chests/desert_pyramid", 10,
            "chests/jungle_temple", 12, "chests/ancient_city", 15,
            "chests/village/village_plains_house", 3, "chests/village/village_savanna_house", 3,
            "chests/village/village_taiga_house", 3, "chests/village/village_desert_house", 3);

    private DigitalEvents() {
    }

    static void init() {
        CobblemonEvents.BATTLE_FAINTED.subscribe(Priority.NORMAL, event -> {
            MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
            Runnable drop = () -> {
                try {
                    digitama(event);
                } catch (Throwable t) {
                    Digital.LOG.error("Digitama drop failed", t);
                }
            };
            if (server != null) server.execute(drop);
            else drop.run();
        });
        LootEvent.MODIFY_LOOT_TABLE.register((key, context, builtin) -> {
            if (!builtin || !key.location().getNamespace().equals("minecraft")) return;
            Integer weight = CHESTS.get(key.location().getPath());
            if (weight == null || weight <= 0) return;
            context.addPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1))
                    .add(LootItem.lootTableItem(Digital.DIGITAMA.get()).setWeight(weight))
                    .add(EmptyLootItem.emptyItem().setWeight(100)));
        });
    }

    static boolean digimon(BattlePokemon pokemon) {
        return pokemon.getOriginalPokemon().getSpecies().getLabels().contains(DigiBall.LABEL);
    }

    private static void digitama(BattleFaintedEvent event) {
        BattlePokemon killed = event.getKilled();
        if (!digimon(killed)) return;
        for (BattleActor actor : event.getBattle().getActors()) {
            if (!(actor instanceof PlayerBattleActor player) || actor.getSide() == killed.getActor().getSide()) continue;
            ServerPlayer entity = player.getEntity();
            if (entity == null || entity.getRandom().nextDouble() >= DIGITAMA_CHANCE) continue;
            ItemStack stack = new ItemStack(Digital.DIGITAMA.get());
            PokemonEntity at = killed.getEntity();
            if (at != null && at.level() == entity.level()) {
                ItemEntity drop = new ItemEntity(at.level(), at.getX(), at.getY() + 0.5, at.getZ(), stack);
                drop.setDefaultPickUpDelay();
                at.level().addFreshEntity(drop);
            } else if (!entity.getInventory().add(stack)) {
                entity.drop(stack, false);
            }
            entity.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digitama.dropped",
                    killed.getOriginalPokemon().getSpecies().getTranslatedName()), true);
        }
    }
}
