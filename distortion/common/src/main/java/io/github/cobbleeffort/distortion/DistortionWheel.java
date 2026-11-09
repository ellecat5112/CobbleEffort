package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.events.pokemon.HeldItemEvent;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.networking.NetworkManager;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Distorting outside battle, from Cobblemon's interaction wheel (the radial menu, where Mega Showdown puts Mega
 * Evolution): the Distort option toggles the Pokémon's "distorted" flag feature (its distorted form and look, saved
 * with it). Rules: the trainer wears the band, the Pokémon holds the crystal (Arceus: a plate), it has Distorted
 * forms, the trainer isn't battling, and one distorted Pokémon per party at a time. Since 0.10.0 the crystal does it
 * by itself: giving it distorts the Pokémon at once (no band needed), taking it away reverts it (sync).
 * A Pokémon distorted outside battle enters battle distorted (with its twin moves; the Showdown scripts count it as the
 * side's distortion).
 */
public final class DistortionWheel {
    private static final Logger LOG = LoggerFactory.getLogger("CobbleEffort Distortion");

    private DistortionWheel() {
    }

    public static void init() {
        NetworkManager.registerReceiver(NetworkManager.Side.C2S, DistortPacket.TYPE, DistortPacket.STREAM_CODEC,
                (packet, context) -> context.queue(() -> {
                    try {
                        if (context.getPlayer() instanceof ServerPlayer player) toggle(player, packet);
                    } catch (Throwable t) {
                        LOG.error("Distort from the wheel failed", t);
                    }
                }));
        CobblemonEvents.HELD_ITEM_POST.subscribe(Priority.NORMAL, DistortionWheel::onHeldItem);
        CobblemonEvents.POKEMON_SENT_POST.subscribe(Priority.NORMAL, event -> {
            try {
                sync(event.getPokemon(), false);
            } catch (Throwable t) {
                LOG.error("Distortion check on send-out failed", t);
            }
        });
    }

    private static void toggle(ServerPlayer player, DistortPacket packet) {
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        Pokemon pokemon = party.get(packet.pokemonId());
        if (pokemon == null) return;
        if (BattleRegistry.getBattleByParticipatingPlayer(player) != null) {
            player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.in_battle"));
            return;
        }
        if (DistortionRules.distortedOutside(pokemon) || pokemon.getForcedAspects().contains(DistortionBattle.ASPECT)) {
            DistortionRules.setDistortedOutside(pokemon, false);
            DistortionBattle.clearForcedAspect(pokemon);          // left over if a battle never ended cleanly
            effects(pokemon, false);
            player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.reverted", pokemon.getDisplayName(false)));
            return;
        }
        if (!DistortionRules.hasDistortedForm(pokemon.getSpecies()) || !DistortionRules.holdsSource(pokemon)) return;
        if (!DistortionRules.wearsBand(player)) {
            player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.need_band"));
            return;
        }
        for (Pokemon other : party) {
            if (other != pokemon && DistortionRules.distortedOutside(other)) {
                player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.one_at_a_time", other.getDisplayName(false)));
                return;
            }
        }
        DistortionRules.setDistortedOutside(pokemon, true);
        effects(pokemon, true);
        player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.distorted", pokemon.getDisplayName(false)));
    }

    /** Giving a Pokémon the crystal distorts it at once; taking it (or Arceus's plate) away turns it back. */
    private static void onHeldItem(HeldItemEvent.Post event) {
        try {
            sync(event.getPokemon(), true);
        } catch (Throwable t) {
            LOG.error("Distorting on a held item change failed", t);
        }
    }

    /**
     * The look follows the held item: a distortable Pokémon holding the Distortion Crystal is distorted, one holding
     * neither the crystal nor (Arceus) a plate isn't. Run when the held item changes and when it's sent out (a crystal
     * given another way, e.g. by command, or held from before this version).
     */
    static void sync(Pokemon pokemon, boolean announce) {
        if (pokemon == null || pokemon.isBattleClone()) return;
        boolean distorted = DistortionRules.distortedOutside(pokemon);
        boolean crystal = pokemon.heldItem().is(Distortion.CRYSTAL.get());
        ServerPlayer owner = pokemon.getOwnerPlayer();
        if (crystal && !distorted && DistortionRules.hasDistortedForm(pokemon.getSpecies())) {
            if (owner != null && BattleRegistry.getBattleByParticipatingPlayer(owner) != null) return;   // the battle's own toggle
            DistortionRules.setDistortedOutside(pokemon, true);
            effects(pokemon, true);
            LOG.info("{} distorted (holding the Distortion Crystal)", pokemon.getSpecies().getName());
            if (owner != null) {
                owner.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.distorted", pokemon.getDisplayName(false)));
            }
        } else if (distorted && !DistortionRules.holdsSource(pokemon)) {
            DistortionRules.setDistortedOutside(pokemon, false);
            DistortionBattle.clearForcedAspect(pokemon);
            effects(pokemon, false);
            LOG.info("{} returned to normal (no Distortion Crystal)", pokemon.getSpecies().getName());
            if (owner != null) {
                owner.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".message.reverted", pokemon.getDisplayName(false)));
            }
        }
    }

    /** A burst of reverse-portal particles (the Distortion World) and a whoosh around the Pokémon, if it's out. */
    private static void effects(Pokemon pokemon, boolean distorting) {
        PokemonEntity entity = pokemon.getEntity();
        if (entity == null || !(entity.level() instanceof ServerLevel level)) return;
        double w = entity.getBbWidth() * 0.6, h = entity.getBbHeight();
        level.sendParticles(distorting ? ParticleTypes.REVERSE_PORTAL : ParticleTypes.PORTAL,
                entity.getX(), entity.getY() + h * 0.5, entity.getZ(), distorting ? 120 : 60, w, h * 0.4, w, 0.08);
        level.playSound(null, entity.getX(), entity.getY(), entity.getZ(),
                distorting ? SoundEvents.ILLUSIONER_MIRROR_MOVE : SoundEvents.ENDERMAN_TELEPORT, SoundSource.NEUTRAL, 1.0F, distorting ? 0.6F : 1.2F);
    }
}
