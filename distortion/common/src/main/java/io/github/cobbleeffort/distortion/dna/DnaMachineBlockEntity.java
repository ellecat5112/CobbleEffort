package io.github.cobbleeffort.distortion.dna;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Containers;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

import java.util.UUID;

/**
 * The DNA machine's state: how much Mew DNA it holds, and the Pokémon inside (Mew while it works, then Mewtwo) with
 * its owner and the time it went in. Saved with the world; the client gets the fill level, the species shown inside
 * and the start time (for the renderer), never the Pokémon itself.
 */
public class DnaMachineBlockEntity extends BlockEntity {
    /** Mew DNA to fill the tank (a win with Mew in the party drops 3-8). */
    public static final int CAPACITY = 16;
    /** Five minutes. */
    public static final long BREW_TICKS = 5 * 60 * 20;

    private int fill;
    @Nullable
    private CompoundTag pokemon;             // server only
    @Nullable
    private UUID owner;
    private String inside = "";              // "", "mew" or "mewtwo" (synced)
    private boolean shiny;                   // synced, for the look
    private long started;                    // game time Mew went in (synced)

    public DnaMachineBlockEntity(BlockPos pos, BlockState state) {
        super(Distortion.DNA_MACHINE_ENTITY.get(), pos, state);
    }

    public int fillLevel() {
        return fill;
    }

    public boolean full() {
        return fill >= CAPACITY;
    }

    public boolean occupied() {
        return !inside.isEmpty();
    }

    public String inside() {
        return inside;
    }

    public boolean shiny() {
        return shiny;
    }

    public long started() {
        return started;
    }

    /** Pour in up to n DNA; returns how many went in. */
    int fill(int n) {
        int poured = Math.max(0, Math.min(n, CAPACITY - fill));
        fill += poured;
        changed();
        return poured;
    }

    /** Server: the player's selected party Pokémon goes in, if it's Mew and the tank is full. */
    public void insert(ServerPlayer player, UUID pokemonId) {
        if (occupied() || !full() || level == null) return;
        if (BattleRegistry.getBattleByParticipatingPlayer(player) != null) return;
        if (player.distanceToSqr(worldPosition.getX() + 0.5, worldPosition.getY() + 1, worldPosition.getZ() + 0.5) > 64) return;
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        Pokemon mew = party.get(pokemonId);
        if (mew == null) return;
        if (!"mew".equals(mew.getSpecies().getName().toLowerCase())) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.not_mew", mew.getDisplayName(false)), true);
            return;
        }
        if (mew.getEntity() != null) mew.recall();
        if (!party.remove(mew)) return;
        pokemon = mew.saveToNBT(level.registryAccess(), new CompoundTag());
        owner = player.getUUID();
        shiny = mew.getShiny();
        inside = "mew";
        started = level.getGameTime();
        changed();
        level.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1F, 1.4F);
        player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.inserted"), false);
    }

    void serverTick() {
        if (!"mew".equals(inside) || level == null || level.getGameTime() - started < BREW_TICKS) return;
        try {
            awaken();
        } catch (Throwable t) {
            Distortion.LOG.error("The DNA machine couldn't make Mewtwo", t);
            started = level.getGameTime() - BREW_TICKS + 200;     // try again in ten seconds, never crash the server
        }
    }

    private void awaken() {
        // done: the Mew in the tank has become Mewtwo (its level and shininess carried over)
        Pokemon mew = load();
        int lvl = mew == null ? 70 : mew.getLevel();
        Pokemon mewtwo = PokemonProperties.Companion.parse("mewtwo level=" + lvl + (shiny ? " shiny=yes" : " shiny=no")).create();
        pokemon = mewtwo.saveToNBT(level.registryAccess(), new CompoundTag());
        inside = "mewtwo";
        fill = 0;
        changed();
        level.playSound(null, worldPosition, SoundEvents.WITHER_SPAWN, SoundSource.BLOCKS, 0.6F, 1.6F);
        if (level instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.REVERSE_PORTAL, worldPosition.getX() + 0.5, worldPosition.getY() + 1.0,
                    worldPosition.getZ() + 0.5, 80, 0.35, 0.6, 0.35, 0.05);
        }
        ServerPlayer player = owner == null ? null : server().getPlayerList().getPlayer(owner);
        if (player != null) player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".dna.done"));
    }

    /** Server: click while a Pokémon is inside. */
    void retrieve(ServerPlayer player) {
        if ("mew".equals(inside)) {
            long left = Math.max(0, BREW_TICKS - (level.getGameTime() - started));
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.working", left / 1200, (left / 20) % 60), true);
            return;
        }
        if (owner != null && !owner.equals(player.getUUID())) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.not_yours"), true);
            return;
        }
        Pokemon mewtwo = load();
        if (mewtwo == null) return;
        give(player, mewtwo);
        clear();
        level.playSound(null, worldPosition, SoundEvents.BEACON_DEACTIVATE, SoundSource.BLOCKS, 1F, 1.2F);
        player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".dna.retrieved", mewtwo.getDisplayName(false)));
    }

    /** The machine is gone (only possible empty, or in creative): DNA drops, a Pokémon goes back to its owner. */
    void dropContents() {
        if (level == null || level.isClientSide) return;
        if (fill > 0 && "".equals(inside)) {
            Containers.dropItemStack(level, worldPosition.getX() + 0.5, worldPosition.getY() + 0.5, worldPosition.getZ() + 0.5,
                    new ItemStack(Distortion.MEW_DNA.get(), fill));
        }
        Pokemon p = load();
        ServerPlayer player = owner == null ? null : server().getPlayerList().getPlayer(owner);
        if (p != null && player != null) give(player, p);
        else if (p != null) Distortion.LOG.warn("A {} in a removed DNA machine had no online owner to return to", p.getSpecies().getName());
        clear();
    }

    private static void give(ServerPlayer player, Pokemon pokemon) {
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        if (!party.add(pokemon)) Cobblemon.INSTANCE.getStorage().getPC(player).add(pokemon);
    }

    @Nullable
    private Pokemon load() {
        if (pokemon == null || level == null) return null;
        try {
            return new Pokemon().loadFromNBT(level.registryAccess(), pokemon);
        } catch (Throwable t) {
            Distortion.LOG.error("Couldn't load the Pokémon in a DNA machine", t);
            return null;
        }
    }

    private void clear() {
        pokemon = null;
        owner = null;
        inside = "";
        shiny = false;
        started = 0;
        changed();
    }

    private net.minecraft.server.MinecraftServer server() {
        return ((ServerLevel) level).getServer();
    }

    private void changed() {
        setChanged();
        if (level != null && !level.isClientSide) level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), 3);
    }

    // --- saving and syncing -----------------------------------------------------------------------------------------
    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        writeShared(tag);
        if (pokemon != null) tag.put("Pokemon", pokemon);
        if (owner != null) tag.putUUID("Owner", owner);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        fill = tag.getInt("Fill");
        inside = tag.getString("Inside");
        shiny = tag.getBoolean("Shiny");
        started = tag.getLong("Started");
        pokemon = tag.contains("Pokemon") ? tag.getCompound("Pokemon") : null;
        owner = tag.hasUUID("Owner") ? tag.getUUID("Owner") : null;
    }

    private void writeShared(CompoundTag tag) {
        tag.putInt("Fill", fill);
        tag.putString("Inside", inside);
        tag.putBoolean("Shiny", shiny);
        tag.putLong("Started", started);
    }

    @Override
    public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
        CompoundTag tag = new CompoundTag();
        writeShared(tag);
        return tag;
    }

    @Nullable
    @Override
    public Packet<ClientGamePacketListener> getUpdatePacket() {
        return ClientboundBlockEntityDataPacket.create(this);
    }
}
