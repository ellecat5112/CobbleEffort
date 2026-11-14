package io.github.cobbleeffort.distortion.dna;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.pokemon.Species;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Block;
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

import java.util.List;
import java.util.Map;
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
    /** One minute in the DNA Purifier. */
    public static final long PURIFY_TICKS = 60 * 20;
    /**
     * Galar's mixed fossils and the two pure Pokémon each was stitched together from (CobbleEffort's species): the
     * Fossilized Bird or Fish on top, the Drake or Dino below. With a DNA Analyzer and a DNA Purifier beside the
     * machine, a mixed fossil goes in, the Purifier picks one of its halves, and it comes out as that pure form.
     */
    public static final Map<String, String[]> MIXED = Map.of(
            "dracozolt", new String[]{"velozolt", "dracomizer"},
            "arctozolt", new String[]{"velozolt", "arctosaur"},
            "dracovish", new String[]{"dunclovish", "dracomizer"},
            "arctovish", new String[]{"dunclovish", "arctosaur"});
    static final Map<String, String[]> HALVES = Map.of(
            "dracozolt", new String[]{"Fossilized Bird", "Fossilized Drake"},
            "arctozolt", new String[]{"Fossilized Bird", "Fossilized Dino"},
            "dracovish", new String[]{"Fossilized Fish", "Fossilized Drake"},
            "arctovish", new String[]{"Fossilized Fish", "Fossilized Dino"});

    private int fill;
    @Nullable
    private CompoundTag pokemon;             // server only
    @Nullable
    private UUID owner;
    private String inside = "";              // "", "mew" or "mewtwo" (synced)
    private boolean shiny;                   // synced, for the look
    private long started;                    // game time Mew went in (synced)
    private String target = "";              // the pure form picked at the Purifier (synced)
    private long purifyStarted;              // game time purifying began, 0 = not purifying (synced)

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

    /** A mixed fossil waiting in the tank (not yet purified). */
    public boolean mixed() {
        return MIXED.containsKey(inside);
    }

    public boolean purifying() {
        return purifyStarted > 0;
    }

    // --- the DNA Analyzer and DNA Purifier beside it ------------------------------------------------------------------
    private boolean near(Block block) {
        if (level == null) return false;
        for (BlockPos base : List.of(worldPosition, worldPosition.above())) {
            for (Direction d : Direction.Plane.HORIZONTAL) {
                if (level.getBlockState(base.relative(d)).is(block)) return true;
            }
        }
        return false;
    }

    public boolean hasAnalyzer() {
        return near(Distortion.DNA_ANALYZER.get());
    }

    public boolean hasPurifier() {
        return near(Distortion.DNA_PURIFIER.get());
    }

    @Nullable
    static Species pure(String name) {
        return PokemonSpecies.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", name));
    }

    private static Component speciesName(String name) {
        Species s = pure(name);
        return s != null ? s.getTranslatedName() : Component.literal(name);
    }

    /** DNA Analyzer: what's in the tank, its DNA and what it can become. */
    void analyze(ServerPlayer player) {
        String m = Distortion.MOD_ID + ".dna.analyzer.";
        if (!occupied()) {
            player.sendSystemMessage(Component.translatable(m + "empty", hasPurifier()
                    ? Component.translatable(m + "yes") : Component.translatable(m + "no")));
            return;
        }
        Pokemon p = load();
        if (p == null) return;
        player.sendSystemMessage(Component.translatable(m + "subject", p.getSpecies().getTranslatedName(), p.getLevel()));
        if (mixed()) {
            String[] halves = HALVES.get(inside);
            String[] pures = MIXED.get(inside);
            player.sendSystemMessage(Component.translatable(m + "mixed", halves[0], speciesName(pures[0]), halves[1],
                    speciesName(pures[1])));
            player.sendSystemMessage(purifying()
                    ? Component.translatable(m + "purifying", speciesName(target), left(PURIFY_TICKS, purifyStarted))
                    : Component.translatable(m + "target", speciesName(target)));
        } else if ("mew".equals(inside)) {
            player.sendSystemMessage(Component.translatable(m + "mew"));
        } else {
            player.sendSystemMessage(Component.translatable(m + "stable"));
        }
        player.sendSystemMessage(Component.translatable(m + "shadow"));
    }

    private String left(long total, long since) {
        long t = Math.max(0, total - (level.getGameTime() - since)) / 20;
        return t / 60 + ":" + String.format("%02d", t % 60);
    }

    /** DNA Purifier, plain use: switch which of the two pure forms it will make. */
    void cycleTarget(ServerPlayer player) {
        String m = Distortion.MOD_ID + ".dna.purifier.";
        if (!mixed()) {
            player.displayClientMessage(Component.translatable(m + "nothing"), true);
            return;
        }
        if (purifying()) {
            player.displayClientMessage(Component.translatable(m + "busy", left(PURIFY_TICKS, purifyStarted)), true);
            return;
        }
        String[] pures = MIXED.get(inside);
        target = pures[0].equals(target) ? pures[1] : pures[0];
        changed();
        player.displayClientMessage(Component.translatable(m + "target", speciesName(target)), true);
    }

    /** DNA Purifier, sneak + use: start purifying (needs the Analyzer too). */
    void startPurify(ServerPlayer player) {
        String m = Distortion.MOD_ID + ".dna.purifier.";
        if (!mixed()) {
            player.displayClientMessage(Component.translatable(m + "nothing"), true);
            return;
        }
        if (purifying()) {
            player.displayClientMessage(Component.translatable(m + "busy", left(PURIFY_TICKS, purifyStarted)), true);
            return;
        }
        if (owner != null && !owner.equals(player.getUUID())) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.not_yours"), true);
            return;
        }
        if (!hasAnalyzer()) {
            player.displayClientMessage(Component.translatable(m + "no_analyzer"), true);
            return;
        }
        if (pure(target) == null) {
            player.displayClientMessage(Component.translatable(m + "no_species"), true);
            return;
        }
        purifyStarted = level.getGameTime();
        changed();
        level.playSound(null, worldPosition, SoundEvents.BEACON_POWER_SELECT, SoundSource.BLOCKS, 1F, 1.2F);
        player.sendSystemMessage(Component.translatable(m + "started", speciesName(target)));
    }

    private void purify() {
        Pokemon p = load();
        Species to = pure(target);
        if (p == null || to == null) {
            purifyStarted = 0;
            changed();
            return;
        }
        p.setSpecies(to);                                 // keeps level, nature, IVs, EVs, moves; re-checks ability
        pokemon = p.saveToNBT(level.registryAccess(), new CompoundTag());
        inside = "cobbleeffort:" + target;
        target = "";
        purifyStarted = 0;
        changed();
        level.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1F, 0.8F);
        if (level instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.END_ROD, worldPosition.getX() + 0.5, worldPosition.getY() + 1.0,
                    worldPosition.getZ() + 0.5, 60, 0.35, 0.6, 0.35, 0.03);
        }
        ServerPlayer player = owner == null ? null : server().getPlayerList().getPlayer(owner);
        if (player != null) player.sendSystemMessage(Component.translatable(Distortion.MOD_ID + ".dna.purifier.done", to.getTranslatedName()));
    }

    /** Pour in up to n DNA; returns how many went in. */
    int fill(int n) {
        int poured = Math.max(0, Math.min(n, CAPACITY - fill));
        fill += poured;
        changed();
        return poured;
    }

    /**
     * Server: the player's selected party Pokémon goes in: Mew when the tank is full of Mew DNA, or a mixed fossil when a
     * DNA Analyzer and a DNA Purifier stand beside the machine.
     */
    public void insert(ServerPlayer player, UUID pokemonId) {
        if (occupied() || level == null) return;
        if (BattleRegistry.getBattleByParticipatingPlayer(player) != null) return;
        if (player.distanceToSqr(worldPosition.getX() + 0.5, worldPosition.getY() + 1, worldPosition.getZ() + 0.5) > 64) return;
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        Pokemon mew = party.get(pokemonId);
        if (mew == null) return;
        String path = mew.getSpecies().getResourceIdentifier().getPath();
        boolean isMew = "mew".equals(path);
        boolean isMixed = MIXED.containsKey(path) && "cobblemon".equals(mew.getSpecies().getResourceIdentifier().getNamespace());
        if (isMew && !full()) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.needs", CAPACITY - fill), true);
            return;
        }
        if (isMixed && !(hasAnalyzer() && hasPurifier())) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.purifier.needs_machines"), true);
            return;
        }
        if (!isMew && !isMixed) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.not_mew", mew.getDisplayName(false)), true);
            return;
        }
        if (mew.getEntity() != null) mew.recall();
        if (!party.remove(mew)) return;
        pokemon = mew.saveToNBT(level.registryAccess(), new CompoundTag());
        owner = player.getUUID();
        shiny = mew.getShiny();
        inside = path;
        started = level.getGameTime();
        target = isMixed ? MIXED.get(path)[0] : "";
        purifyStarted = 0;
        changed();
        level.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1F, 1.4F);
        player.displayClientMessage(isMixed
                ? Component.translatable(Distortion.MOD_ID + ".dna.purifier.inserted", mew.getSpecies().getTranslatedName())
                : Component.translatable(Distortion.MOD_ID + ".dna.inserted"), false);
    }

    void serverTick() {
        if (level != null && purifying() && level.getGameTime() - purifyStarted >= PURIFY_TICKS) {
            try {
                purify();
            } catch (Throwable t) {
                Distortion.LOG.error("The DNA Purifier failed", t);
                purifyStarted = level.getGameTime() - PURIFY_TICKS + 200;
            }
            return;
        }
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
        if (purifying()) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.purifier.busy", left(PURIFY_TICKS, purifyStarted)), true);
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
        target = "";
        purifyStarted = 0;
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
        target = tag.getString("Target");
        purifyStarted = tag.getLong("PurifyStarted");
        pokemon = tag.contains("Pokemon") ? tag.getCompound("Pokemon") : null;
        owner = tag.hasUUID("Owner") ? tag.getUUID("Owner") : null;
    }

    private void writeShared(CompoundTag tag) {
        tag.putInt("Fill", fill);
        tag.putString("Inside", inside);
        tag.putBoolean("Shiny", shiny);
        tag.putLong("Started", started);
        tag.putString("Target", target);
        tag.putLong("PurifyStarted", purifyStarted);
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
