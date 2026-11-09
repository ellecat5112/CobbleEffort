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
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.network.chat.Component;

/**
 * The server side of distorting:
 * - the Distortion Crystal is the Showdown item "distortioncrystal" (its Showdown script and the distort choice,
 *   forme change and move swaps are data: data/cobbleeffort_distortion/mega_showdown/showdown/...);
 * - when the engine distorts a Pokémon it sends a forme change to "<species>-Distorted", which Cobblemon posts as
 *   FORME_CHANGE with the form name "distorted": the Pokémon gets the "distorted" aspect (its look and form) until it
 *   reverts ("<species>-Reverted": "reverted") or the battle ends; distorting and reverting are free, any turn;
 * - a trainer can only choose to distort while wearing the Distortion Band (checked by MoveActionResponseMixin).
 */
public final class DistortionBattle {
    public static final String GIMMICK = "distort";
    public static final String ASPECT = "distorted";
    /** The form name the engine sends when a Pokémon reverts ("<species>-Reverted"). */
    public static final String REVERTED = "reverted";
    public static final org.slf4j.Logger LOG = org.slf4j.LoggerFactory.getLogger("CobbleEffort Distortion");
    private static final Map<UUID, Set<Pokemon>> DISTORTED = new ConcurrentHashMap<>();
    /** AI actors (by battle) that have chosen to distort: once per battle. */
    private static final Map<UUID, Set<UUID>> AI_DISTORTED = new ConcurrentHashMap<>();
    /** Pokémon that reverted in a battle (by battle): distorted again afterwards if they still hold the crystal. */
    private static final Map<UUID, Set<Pokemon>> REVERTED_IN_BATTLE = new ConcurrentHashMap<>();

    private DistortionBattle() {
    }

    public static void init() {
        HeldItemProvider.register(new CrystalItems(), Priority.HIGH);
        CobblemonEvents.FORME_CHANGE.subscribe(Priority.NORMAL, DistortionBattle::onFormeChange);
        CobblemonEvents.BATTLE_ENDED.subscribe(Priority.NORMAL, DistortionBattle::onBattleEnded);
    }

    private static void onFormeChange(FormeChangeEvent event) {
        if (REVERTED.equals(event.getFormeName())) {
            // reverted in battle: the look goes, and a distortion made outside battle is undone too
            Pokemon pokemon = event.getPokemon().getEffectedPokemon();
            clearForcedAspect(pokemon);
            if (DistortionRules.distortedOutside(pokemon)) {
                DistortionRules.setDistortedOutside(pokemon, false);
                REVERTED_IN_BATTLE.computeIfAbsent(event.getBattle().getBattleId(), id -> ConcurrentHashMap.newKeySet()).add(pokemon);
            }
            return;
        }
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
        AI_DISTORTED.remove(event.getBattle().getBattleId());
        Set<Pokemon> reverted = REVERTED_IN_BATTLE.remove(event.getBattle().getBattleId());
        if (reverted != null) {
            for (Pokemon pokemon : reverted) {
                try {
                    DistortionWheel.sync(pokemon, false);            // still holding the crystal: distorted again
                } catch (Throwable t) {
                    LOG.error("Re-distorting after battle failed", t);
                }
            }
        }
        Set<Pokemon> list = DISTORTED.remove(event.getBattle().getBattleId());
        if (list == null) return;
        for (Pokemon pokemon : list) clearForcedAspect(pokemon);
    }

    static void clearForcedAspect(Pokemon pokemon) {
        Set<String> aspects = new HashSet<>(pokemon.getForcedAspects());
        if (aspects.remove(ASPECT)) {
            pokemon.setForcedAspects(aspects);
            pokemon.updateAspects();
        }
    }

    /** May this trainer distort? Only while wearing the Distortion Band. NPC trainers may always (if their data lets them). */
    public static boolean trainerMayDistort(ActiveBattlePokemon active) {
        BattleActor actor = active.getActor();
        if (!(actor instanceof PlayerBattleActor player)) return true;
        return DistortionRules.wearsBand(player.getEntity());
    }

    /**
     * Should this AI actor's Pokémon distort with its move now? Its first chance only: it can distort (crystal, or
     * Arceus with a plate, and Distorted forms), no Pokémon of the actor is distorted (in battle, or from outside it),
     * and the actor hasn't chosen to distort before in this battle.
     */
    public static boolean aiMayDistort(BattleActor actor, ActiveBattlePokemon active) {
        BattlePokemon battlePokemon = active.getBattlePokemon();
        if (battlePokemon == null) return false;
        Pokemon pokemon = battlePokemon.getEffectedPokemon();
        if (!DistortionRules.holdsSource(pokemon) || !DistortionRules.hasDistortedForm(pokemon.getSpecies())) return false;
        UUID battleId = actor.getBattle().getBattleId();
        Set<UUID> chosen = AI_DISTORTED.computeIfAbsent(battleId, id -> ConcurrentHashMap.newKeySet());
        if (chosen.contains(actor.getUuid())) return false;
        for (BattlePokemon member : actor.getPokemonList()) {
            if (member.getEffectedPokemon().getAspects().contains(ASPECT)) return false;
        }
        chosen.add(actor.getUuid());
        return true;
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
