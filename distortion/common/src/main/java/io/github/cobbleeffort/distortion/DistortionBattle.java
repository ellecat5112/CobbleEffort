package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.interpreter.BattleMessage;
import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.battles.BattleEndedEvent;
import com.cobblemon.mod.common.api.events.battles.instruction.FormeChangeEvent;
import com.cobblemon.mod.common.api.pokemon.helditem.HeldItemManager;
import com.cobblemon.mod.common.api.pokemon.helditem.HeldItemProvider;
import com.cobblemon.mod.common.battles.ActiveBattlePokemon;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.wispforest.accessories.api.AccessoriesCapability;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;

/**
 * The server side of distorting:
 * - the Distortion Crystal is the Showdown item "distortioncrystal" (its Showdown script and the distort choice,
 *   forme change and move swaps are data: data/cobbleeffort_distortion/mega_showdown/showdown/...);
 * - when Showdown changes a Pokémon into its "-Distorted" forme, Cobblemon posts FORME_CHANGE with the form name
 *   "distorted": the Pokémon gets the "distorted" aspect (its distorted look and form) until the battle ends;
 * - a trainer can only choose to distort while wearing the Distortion Band (checked by MoveActionResponseMixin).
 */
public final class DistortionBattle {
    public static final String GIMMICK = "distort";
    public static final String ASPECT = "distorted";
    private static final Map<UUID, Set<Pokemon>> DISTORTED = new ConcurrentHashMap<>();

    private DistortionBattle() {
    }

    public static void init() {
        HeldItemProvider.register(new CrystalItems(), Priority.HIGH);
        CobblemonEvents.FORME_CHANGE.subscribe(Priority.NORMAL, DistortionBattle::onFormeChange);
        CobblemonEvents.BATTLE_ENDED.subscribe(Priority.NORMAL, DistortionBattle::onBattleEnded);
    }

    private static void onFormeChange(FormeChangeEvent event) {
        if (!ASPECT.equals(event.getFormeName())) return;
        Pokemon pokemon = event.getPokemon().getEffectedPokemon();
        Set<String> aspects = new HashSet<>(pokemon.getForcedAspects());
        if (aspects.add(ASPECT)) {
            pokemon.setForcedAspects(aspects);
            pokemon.updateAspects();
        }
        DISTORTED.computeIfAbsent(event.getBattle().getBattleId(), id -> ConcurrentHashMap.newKeySet()).add(pokemon);
    }

    private static void onBattleEnded(BattleEndedEvent event) {
        Set<Pokemon> list = DISTORTED.remove(event.getBattle().getBattleId());
        if (list == null) return;
        for (Pokemon pokemon : list) {
            Set<String> aspects = new HashSet<>(pokemon.getForcedAspects());
            if (aspects.remove(ASPECT)) {
                pokemon.setForcedAspects(aspects);
                pokemon.updateAspects();
            }
        }
    }

    /** May this trainer distort? Only while wearing the Distortion Band. NPC trainers may always (if their data lets them). */
    public static boolean trainerMayDistort(ActiveBattlePokemon active) {
        BattleActor actor = active.getActor();
        if (!(actor instanceof PlayerBattleActor player)) return true;
        ServerPlayer entity = player.getEntity();
        if (entity == null) return false;
        AccessoriesCapability capability = AccessoriesCapability.get(entity);
        return capability != null && capability.isEquipped(Distortion.BAND.get());
    }

    /** The crystal as a Showdown held item. */
    static final class CrystalItems implements HeldItemManager {
        static final String ID = "distortioncrystal";

        @Override
        public String showdownId(BattlePokemon pokemon) {
            return pokemon.getEffectedPokemon().heldItem().is(Distortion.CRYSTAL.get()) ? ID : null;
        }

        @Override
        public Component nameOf(String showdownId) {
            return Component.translatable("item." + Distortion.MOD_ID + ".distortion_crystal");
        }

        @Override
        public void handleStartInstruction(BattlePokemon pokemon, PokemonBattle battle, BattleMessage battleMessage) {
        }

        @Override
        public void handleEndInstruction(BattlePokemon pokemon, PokemonBattle battle, BattleMessage battleMessage) {
        }

        @Override
        public void give(BattlePokemon pokemon, String showdownId) {
        }

        @Override
        public void take(BattlePokemon pokemon, String showdownId) {
        }
    }
}
