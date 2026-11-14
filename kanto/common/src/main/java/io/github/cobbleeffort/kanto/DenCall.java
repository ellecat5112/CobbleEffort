package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.moves.Move;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.evolution.Evolution;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.networking.NetworkManager;
import net.minecraft.core.UUIDUtil;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Call of the Den (CobbleEffort's Hopple, the user's design): with three or more Hopples in the party, a Hopple that
 * knows Call of the Den can use it from Cobblemon's interaction wheel. Every Hopple in the party then fuses into the
 * caller: the others leave the party (their held items go back to the trainer) and the caller evolves for good into
 * Rabbrute, the titanic "family" form (its evolution needs the den_called flag, set here first).
 */
public final class DenCall {
    public static final ResourceLocation HOPPLE = ResourceLocation.fromNamespaceAndPath("cobbleeffort", "hopple");
    public static final String RABBRUTE = "cobbleeffort:rabbrute";
    public static final String MOVE = "calloftheden";
    public static final int NEEDED = 3;

    private DenCall() {}

    static void register() {
        NetworkManager.registerReceiver(NetworkManager.Side.C2S, CallPacket.TYPE, CallPacket.STREAM_CODEC,
                (packet, context) -> context.queue(() -> {
                    try {
                        if (context.getPlayer() instanceof ServerPlayer player) call(player, packet.pokemonId());
                    } catch (Throwable t) {
                        Kanto.LOG.error("Call of the Den failed", t);
                    }
                }));
    }

    public static boolean isHopple(Pokemon pokemon) {
        return pokemon != null && HOPPLE.equals(pokemon.getSpecies().getResourceIdentifier());
    }

    public static boolean knowsCall(Pokemon pokemon) {
        for (Move move : pokemon.getMoveSet()) {
            if (move != null && MOVE.equals(move.getName())) return true;
        }
        return false;
    }

    public static int hopples(Iterable<Pokemon> party) {
        int n = 0;
        for (Pokemon p : party) if (isHopple(p)) n++;
        return n;
    }

    /** What the wheel shows the option for (the server checks it all again). */
    public static boolean canCall(Pokemon pokemon, Iterable<Pokemon> party) {
        return isHopple(pokemon) && knowsCall(pokemon) && hopples(party) >= NEEDED;
    }

    static void call(ServerPlayer player, UUID id) {
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        Pokemon caller = party.get(id);
        if (caller == null || !isHopple(caller)) return;
        if (BattleRegistry.getBattleByParticipatingPlayer(player) != null) {
            player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".den.in_battle"));
            return;
        }
        if (!knowsCall(caller)) {
            player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".den.no_move", caller.getDisplayName(false)));
            return;
        }
        List<Pokemon> family = new ArrayList<>();
        for (Pokemon p : party) if (p != caller && isHopple(p)) family.add(p);
        if (family.size() + 1 < NEEDED) {
            player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".den.too_few", NEEDED));
            return;
        }
        Evolution evolution = null;
        for (Evolution e : caller.getEvolutions()) {
            if (e.getResult().getSpecies() != null && RABBRUTE.equals(e.getResult().getSpecies())) evolution = e;
        }
        if (evolution == null) {
            Kanto.LOG.error("Hopple has no evolution into {} (is CobbleEffort 0.81.0+ installed?)", RABBRUTE);
            return;
        }
        for (Pokemon p : family) {
            ItemStack held = p.removeHeldItem();
            if (!held.isEmpty()) player.getInventory().placeItemBackInInventory(held);
            party.remove(p);
        }
        PokemonProperties.Companion.parse("den_called").apply(caller);
        evolution.forceEvolve(caller);
        player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".den.fused", family.size() + 1));
    }

    /** Client to server: Call of the Den from the wheel of this party Pokémon. */
    public record CallPacket(UUID pokemonId) implements CustomPacketPayload {
        public static final Type<CallPacket> TYPE = new Type<>(Kanto.id("call_of_the_den"));
        public static final StreamCodec<RegistryFriendlyByteBuf, CallPacket> STREAM_CODEC =
                StreamCodec.composite(UUIDUtil.STREAM_CODEC, CallPacket::pokemonId, CallPacket::new);

        @Override
        public Type<? extends CustomPacketPayload> type() {
            return TYPE;
        }
    }
}
