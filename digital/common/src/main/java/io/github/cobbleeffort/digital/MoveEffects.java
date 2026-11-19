package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.moves.MoveTemplate;
import com.cobblemon.mod.common.api.moves.categories.DamageCategories;
import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseFireBlock;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

import java.util.Locale;
import java.util.Set;

/**
 * Digimon attacks out in the world (MoveInstructionMixin calls `used` for every move in a battle): a Digimon's fire
 * attacks (Pepper Breath, Mega Flame, any Fire move) burst into flame where they land, its missiles and cannons (Giga
 * Destroyer, Garuru Cannon, anything named cannon/missile/bomb/destroyer) explode, its water attacks splash and douse
 * fires. With the gamerule digitalMoveGriefing on (off by default) they also change the world: fires catch on
 * flammable ground, sand nearby turns to glass, blasts break blocks, water leaves puddles that drain away.
 */
public final class MoveEffects {
    public static final GameRules.Key<GameRules.BooleanValue> GRIEFING =
            GameRules.register("digitalMoveGriefing", GameRules.Category.MISC, GameRules.BooleanValue.create(false));
    static final Set<String> BLASTS = Set.of("gigadestroyer", "garurucannon");

    private MoveEffects() {
    }

    public static void used(MoveTemplate move, BattlePokemon user, BattlePokemon target) {
        if (move == null || user == null || target == null || !Attributes.isDigimon(user.getEffectedPokemon())) return;
        if (move.getDamageCategory() == DamageCategories.INSTANCE.getSTATUS()) return;
        PokemonEntity at = target.getEffectedPokemon().getEntity();
        if (at == null || !(at.level() instanceof ServerLevel level)) return;
        String id = move.getName().toLowerCase(Locale.ROOT);
        String kind = BLASTS.contains(id) || id.contains("cannon") || id.contains("missile") || id.contains("bomb") || id.contains("destroyer") ? "blast"
                : move.getElementalType() == ElementalTypes.INSTANCE.getFIRE() ? "fire"
                : move.getElementalType() == ElementalTypes.INSTANCE.getWATER() ? "water" : null;
        if (kind == null) return;
        MinecraftServer server = level.getServer();
        Vec3 pos = at.position();
        Scheduler.later(server, 18, () -> {
            try {
                boolean grief = level.getGameRules().getBoolean(GRIEFING);
                switch (kind) {
                    case "fire" -> fire(level, pos, grief);
                    case "blast" -> blast(level, pos, grief);
                    default -> water(level, pos, grief);
                }
            } catch (Throwable t) {
                Digital.LOG.error("Move world effect failed", t);
            }
        });
    }

    static void fire(ServerLevel level, Vec3 at, boolean grief) {
        level.sendParticles(ParticleTypes.FLAME, at.x, at.y + 0.5, at.z, 60, 1.2, 0.4, 1.2, 0.05);
        level.sendParticles(ParticleTypes.LAVA, at.x, at.y + 0.3, at.z, 8, 1, 0.2, 1, 0);
        level.playSound(null, BlockPos.containing(at), SoundEvents.FIRECHARGE_USE, SoundSource.HOSTILE, 1F, 1F);
        if (!grief) return;
        BlockPos c = BlockPos.containing(at);
        for (BlockPos p : BlockPos.betweenClosed(c.offset(-3, -2, -3), c.offset(3, 2, 3))) {
            BlockState s = level.getBlockState(p);
            if (s.is(BlockTags.SAND)) {
                level.setBlock(p, Blocks.GLASS.defaultBlockState(), 3);
            } else if (s.isAir() && level.random.nextInt(5) == 0 && BaseFireBlock.canBePlacedAt(level, p, net.minecraft.core.Direction.UP)) {
                level.setBlock(p, BaseFireBlock.getState(level, p), 11);
            }
        }
    }

    static void blast(ServerLevel level, Vec3 at, boolean grief) {
        if (grief) {
            level.explode(null, at.x, at.y + 0.5, at.z, 2.2F, Level.ExplosionInteraction.MOB);
        } else {
            level.sendParticles(ParticleTypes.EXPLOSION_EMITTER, at.x, at.y + 0.5, at.z, 1, 0, 0, 0, 0);
            level.sendParticles(ParticleTypes.LARGE_SMOKE, at.x, at.y + 0.5, at.z, 40, 1, 0.6, 1, 0.05);
            level.playSound(null, BlockPos.containing(at), SoundEvents.GENERIC_EXPLODE.value(), SoundSource.HOSTILE, 1.2F, 1F);
        }
    }

    static void water(ServerLevel level, Vec3 at, boolean grief) {
        level.sendParticles(ParticleTypes.SPLASH, at.x, at.y + 0.5, at.z, 120, 1.5, 0.4, 1.5, 0.2);
        level.sendParticles(ParticleTypes.BUBBLE_POP, at.x, at.y + 0.5, at.z, 30, 1, 0.4, 1, 0.05);
        level.playSound(null, BlockPos.containing(at), SoundEvents.GENERIC_SPLASH, SoundSource.HOSTILE, 1F, 1F);
        BlockPos c = BlockPos.containing(at);
        for (BlockPos p : BlockPos.betweenClosed(c.offset(-5, -2, -5), c.offset(5, 3, 5))) {
            if (level.getBlockState(p).getBlock() instanceof BaseFireBlock) level.removeBlock(p, false);
        }
        if (!grief) return;
        BlockPos spot = c.above(0);
        if (level.getBlockState(spot).isAir() && level.getBlockState(spot.below()).isFaceSturdy(level, spot.below(), net.minecraft.core.Direction.UP)) {
            level.setBlock(spot, Blocks.WATER.defaultBlockState(), 3);
            BlockPos fixed = spot.immutable();
            Scheduler.later(level.getServer(), 100, () -> {
                if (level.getBlockState(fixed).is(Blocks.WATER)) level.setBlock(fixed, Blocks.AIR.defaultBlockState(), 3);
            });
        }
    }
}
