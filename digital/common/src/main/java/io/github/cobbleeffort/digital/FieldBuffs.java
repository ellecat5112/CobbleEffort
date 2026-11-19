package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BiomeTags;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;

import java.util.HashSet;
import java.util.Set;

/**
 * Field buffs (Digimon World / Cyber Sleuth): each Digimon belongs to fields (wikimon's: Nature Spirits, Deep Savers,
 * Nightmare Soldiers, Metal Empire, Wind Guardians, Dragon's Roar, Virus Busters, Jungle Troopers, Dark Area, Saiyu
 * Warriors, Toho Braves; species labels "digimon_field_<id>"). Where the battle is fought decides which fields are in
 * their element; a Digimon of one does 1.15x damage (digital_engine.js). Electric Digimon also count in storms.
 */
public final class FieldBuffs {
    private FieldBuffs() {
    }

    /** Where a battle happens: the first player in it, else the first Pokémon with an entity. */
    static Object[] place(PokemonBattle battle) {
        for (BattleActor a : battle.getActors()) {
            if (a instanceof PlayerBattleActor p && p.getEntity() != null) return new Object[]{p.getEntity().level(), p.getEntity().blockPosition()};
        }
        for (BattleActor a : battle.getActors()) {
            for (BattlePokemon bp : a.getPokemonList()) {
                PokemonEntity e = bp.getEffectedPokemon().getEntity();
                if (e != null) return new Object[]{e.level(), e.blockPosition()};
            }
        }
        return null;
    }

    static boolean key(Holder<Biome> b, String... parts) {
        String id = b.unwrapKey().map(k -> k.location().toString()).orElse("");
        for (String p : parts) if (id.contains(p)) return true;
        return false;
    }

    /** The fields in their element here and now. */
    static Set<String> active(Level level, BlockPos pos) {
        Set<String> f = new HashSet<>();
        Holder<Biome> b = level.getBiome(pos);
        boolean night = level.isNight(), sky = level.canSeeSky(pos.above());
        boolean underground = !sky && pos.getY() < level.getSeaLevel();
        if (b.is(BiomeTags.IS_FOREST) || b.is(BiomeTags.IS_TAIGA) || key(b, "plains", "meadow", "flower", "grove")) f.add("nature_spirits");
        if (b.is(BiomeTags.IS_OCEAN) || b.is(BiomeTags.IS_RIVER) || b.is(BiomeTags.IS_BEACH) || key(b, "swamp") || water(level, pos)) f.add("deep_savers");
        if (night || underground) f.add("nightmare_soldiers");
        if (level.isThundering()) f.add("metal_empire");
        if (b.is(BiomeTags.IS_BADLANDS) || b.is(BiomeTags.IS_SAVANNA) || b.is(BiomeTags.IS_NETHER) || key(b, "desert")) f.add("dragons_roar");
        if (b.is(BiomeTags.IS_MOUNTAIN) || b.is(BiomeTags.IS_HILL) || pos.getY() > 120) f.add("wind_guardians");
        if (!night && sky) f.add("virus_busters");
        if (b.is(BiomeTags.IS_JUNGLE) || key(b, "swamp", "bamboo")) f.add("jungle_troopers");
        if (b.is(BiomeTags.IS_NETHER) || key(b, "deep_dark", "dark_area")) f.add("dark_area");
        if (b.is(BiomeTags.IS_SAVANNA) || key(b, "desert")) f.add("saiyu_warriors");
        if (key(b, "cherry", "bamboo")) f.add("toho_braves");
        if (level.isThundering()) f.add("storm");
        return f;
    }

    static boolean water(Level level, BlockPos pos) {
        for (BlockPos p : BlockPos.betweenClosed(pos.offset(-4, -2, -4), pos.offset(4, 2, 4))) {
            if (level.getFluidState(p).is(FluidTags.WATER)) return true;
        }
        return false;
    }

    /** The field a Digimon draws power from here, or null. */
    static String boosted(Pokemon p, Set<String> active) {
        if (!Attributes.isDigimon(p) || active.isEmpty()) return null;
        Set<String> labels = new HashSet<>(p.getSpecies().getLabels());
        labels.addAll(p.getForm().getLabels());
        for (String id : active) {
            if (labels.contains("digimon_field_" + id)) return id;
        }
        if (active.contains("storm") && (p.getPrimaryType() == ElementalTypes.INSTANCE.getELECTRIC()
                || p.getSecondaryType() == ElementalTypes.INSTANCE.getELECTRIC())) return "storm";
        return null;
    }

    static Set<String> active(PokemonBattle battle) {
        Object[] at = place(battle);
        if (at == null || !(at[0] instanceof ServerLevel level)) return Set.of();
        return active(level, (BlockPos) at[1]);
    }
}
