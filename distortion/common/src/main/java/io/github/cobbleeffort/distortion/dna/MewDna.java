package io.github.cobbleeffort.distortion.dna;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.battles.BattleFaintedEvent;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;

/**
 * Mew DNA: when a Pokémon is defeated in battle, every player on the other side with a Mew in their party gets 3-8
 * Mew DNA, dropped where the defeated Pokémon was (or at the player, if it wasn't out in the world).
 */
public final class MewDna {
    private MewDna() {
    }

    public static void init() {
        CobblemonEvents.BATTLE_FAINTED.subscribe(Priority.NORMAL, event -> {
            try {
                onFainted(event);
            } catch (Throwable t) {
                Distortion.LOG.error("Mew DNA drop failed", t);
            }
        });
    }

    private static boolean hasMew(ServerPlayer player) {
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(player)) {
            if (p != null && "mew".equals(p.getSpecies().getName().toLowerCase())) return true;
        }
        return false;
    }

    private static void onFainted(BattleFaintedEvent event) {
        BattlePokemon killed = event.getKilled();
        BattleActor loser = killed.getActor();
        for (BattleActor actor : event.getBattle().getActors()) {
            if (!(actor instanceof PlayerBattleActor player) || actor.getSide() == loser.getSide()) continue;
            ServerPlayer entity = player.getEntity();
            if (entity == null || !hasMew(entity)) continue;
            int n = 3 + entity.getRandom().nextInt(6);                 // 3-8
            ItemStack stack = new ItemStack(Distortion.MEW_DNA.get(), n);
            PokemonEntity at = killed.getEntity();
            if (at != null && at.level() == entity.level()) {
                ItemEntity drop = new ItemEntity(at.level(), at.getX(), at.getY() + 0.5, at.getZ(), stack);
                drop.setDefaultPickUpDelay();
                at.level().addFreshEntity(drop);
            } else if (!entity.getInventory().add(stack)) {
                entity.drop(stack, false);
            }
            entity.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.dropped", n), true);
        }
    }
}
