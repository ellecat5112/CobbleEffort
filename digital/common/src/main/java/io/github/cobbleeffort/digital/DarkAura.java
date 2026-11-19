package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Dark Towers' aura: within RADIUS blocks of a standing tower core no Digimon digivolves past Child (Rookie): its
 * level-up digivolutions aren't offered, and the Digivice can't warp it. Cores register themselves while their chunk is
 * loaded (DarkTowerCoreBlockEntity), so the aura only needs the loaded ones (a player nearby means a loaded chunk).
 */
public final class DarkAura {
    public static final int RADIUS = 64;
    /** Stage index (Digivice.STAGES) above which digivolving is blocked: Child. */
    static final int MAX_STAGE = 2;
    private static final Map<ResourceKey<Level>, Set<BlockPos>> CORES = new HashMap<>();

    private DarkAura() {
    }

    static synchronized void add(Level level, BlockPos pos) {
        CORES.computeIfAbsent(level.dimension(), k -> new HashSet<>()).add(pos.immutable());
    }

    static synchronized void remove(Level level, BlockPos pos) {
        Set<BlockPos> set = CORES.get(level.dimension());
        if (set != null) set.remove(pos);
    }

    /** True if a core stands within RADIUS of `at` in this level. */
    public static synchronized boolean near(Level level, Vec3 at) {
        if (!level.getGameRules().getBoolean(DigitalRules.DARK_AURA)) return false;   // game rule digitalDarkTowerAura
        Set<BlockPos> set = CORES.get(level.dimension());
        if (set == null) return false;
        for (BlockPos p : set) {
            if (p.distToCenterSqr(at) <= (double) RADIUS * RADIUS) return true;
        }
        return false;
    }

    /** Where a Pokémon is: its entity if sent out, else its trainer. */
    static boolean near(Pokemon p) {
        PokemonEntity e = p.getEntity();
        if (e != null) return near(e.level(), e.position());
        ServerPlayer owner = p.getOwnerPlayer();
        return owner != null && near(owner.level(), owner.position());
    }

    /** True if a Dark Tower's aura stops this Digimon (with its tamer here) digivolving past Child. */
    public static boolean blocks(ServerPlayer player, Pokemon p) {
        return Attributes.isDigimon(p) && (near(p) || near(player.level(), player.position()));
    }

    static boolean blocksTo(Pokemon p, Species result) {
        return Attributes.isDigimon(p) && result != null && Digivice.stageIndex(result) > MAX_STAGE && near(p);
    }

    static void init() {
        CobblemonEvents.EVOLUTION_TESTED.subscribe(Priority.NORMAL, event -> {
            try {
                if (event.getResult() && blocksTo(event.getPokemon(), Digivice.result(event.getEvolution()))) event.setResult(false);
            } catch (Throwable ignored) {
                // never break evolution checks
            }
        });
    }
}
