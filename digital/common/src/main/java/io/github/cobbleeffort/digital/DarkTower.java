package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.battles.BattleBuilder;
import com.cobblemon.mod.common.battles.BattleFormat;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.actor.PokemonBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.serialization.MapCodec;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

import java.util.ArrayList;
import java.util.List;

/**
 * Dark Towers (Control Spires): obsidian-and-wireframe towers (structure dark_tower) round a core block whose aura
 * stops Digimon digivolving past Child within 64 blocks (DarkAura). Break the core and its guardian, a strong Virus
 * Digimon, appears and challenges you; beat it for Chrome Digizoid and Virus data.
 */
public final class DarkTower {
    public static final String GUARDIAN_KEY = "cobbleeffort_digital_guardian";
    /** Guardians, the first that's loaded (Perfect-level Virus Digimon; Devimon as the fallback). */
    static final List<String> GUARDIANS = List.of("skullgreymon", "vamdemon", "ladydevimon", "megadramon", "metalseadramon",
            "mugendramon", "devimon");
    static final int GUARDIAN_LEVEL = 42;

    private DarkTower() {
    }

    // --- the core ------------------------------------------------------------------------------------------------------

    public static class CoreBlock extends BaseEntityBlock {
        public CoreBlock(Properties properties) {
            super(properties);
        }

        @Override
        protected MapCodec<? extends BaseEntityBlock> codec() {
            return simpleCodec(CoreBlock::new);
        }

        @Override
        protected RenderShape getRenderShape(BlockState state) {
            return RenderShape.MODEL;
        }

        @Override
        public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
            return new CoreEntity(pos, state);
        }

        @Override
        public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
            BlockState r = super.playerWillDestroy(level, pos, state, player);
            if (!level.isClientSide && player instanceof ServerPlayer sp && !sp.isCreative()) {
                ((ServerLevel) level).getServer().execute(() -> guardian(sp, (ServerLevel) level, pos));
            }
            return r;
        }

        @Override
        public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
            for (int i = 0; i < 2; i++) {
                level.addParticle(ParticleTypes.SMOKE, pos.getX() + random.nextDouble(), pos.getY() + 1.05, pos.getZ() + random.nextDouble(), 0, 0.03, 0);
            }
            if (random.nextInt(3) == 0) {
                level.addParticle(ParticleTypes.CRIMSON_SPORE, pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(),
                        pos.getZ() + random.nextDouble(), 0, 0, 0);
            }
        }
    }

    /** Registers the core with the aura while its chunk is loaded. */
    public static class CoreEntity extends BlockEntity {
        public CoreEntity(BlockPos pos, BlockState state) {
            super(Digital.TOWER_CORE_ENTITY.get(), pos, state);
        }

        @Override
        public void setLevel(Level level) {
            super.setLevel(level);
            if (!level.isClientSide) DarkAura.add(level, getBlockPos());
        }

        @Override
        public void setRemoved() {
            super.setRemoved();
            if (level != null && !level.isClientSide) DarkAura.remove(level, getBlockPos());
        }

        @Override
        public void clearRemoved() {
            super.clearRemoved();
            if (level != null && !level.isClientSide) DarkAura.add(level, getBlockPos());
        }

        @Override
        protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.saveAdditional(tag, registries);
        }
    }

    // --- the guardian --------------------------------------------------------------------------------------------------

    static String guardianSpecies() {
        for (String id : GUARDIANS) {
            if (PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", id)) != null) return "cobbleeffort:" + id;
        }
        return null;
    }

    static void guardian(ServerPlayer player, ServerLevel level, BlockPos pos) {
        try {
            level.playSound(null, pos, SoundEvents.WITHER_SPAWN, SoundSource.HOSTILE, 0.8F, 1.4F);
            level.sendParticles(ParticleTypes.LARGE_SMOKE, pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, 60, 1, 1, 1, 0.05);
            player.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tower.broken").withStyle(ChatFormatting.DARK_RED));
            String species = guardianSpecies();
            if (species == null) return;
            Pokemon pokemon = PokemonProperties.Companion.parse(species + " level=" + GUARDIAN_LEVEL + " uncatchable").create();
            pokemon.getPersistentData().putBoolean(GUARDIAN_KEY, true);
            Attributes.set(pokemon, Attribute.VIRUS);
            PokemonEntity entity = new PokemonEntity(level, pokemon, CobblemonEntities.POKEMON);
            net.minecraft.world.entity.Mob mob = entity;
            mob.moveTo(pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, level.getRandom().nextFloat() * 360F, 0F);
            mob.setPersistenceRequired();
            mob.setCustomName(Component.translatable(Digital.MOD_ID + ".tower.guardian", pokemon.getSpecies().getTranslatedName())
                    .withStyle(ChatFormatting.DARK_RED));
            mob.setCustomNameVisible(true);
            mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, 20 * 60, 0, false, false));
            level.addFreshEntity(mob);
            Scheduler.later(level.getServer(), 30, () -> {
                if (entity.isAlive() && !entity.isBattling() && player.isAlive()) {
                    try {
                        BattleBuilder.INSTANCE.pve(player, entity, null, BattleFormat.Companion.getGEN_9_SINGLES());
                    } catch (Throwable t) {
                        Digital.LOG.error("Guardian battle failed", t);
                    }
                }
            });
        } catch (Throwable t) {
            Digital.LOG.error("Dark Tower guardian failed", t);
        }
    }

    static void init() {
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            List<BattleActor> winners = new ArrayList<>(event.getWinners()), losers = new ArrayList<>(event.getLosers());
            MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
            Runnable reward = () -> {
                try {
                    for (BattleActor loser : losers) {
                        if (!(loser instanceof PokemonBattleActor wild)) continue;
                        for (BattlePokemon bp : wild.getPokemonList()) {
                            if (!bp.getOriginalPokemon().getPersistentData().getBoolean(GUARDIAN_KEY)) continue;
                            for (BattleActor w : winners) {
                                if (w instanceof PlayerBattleActor pa && pa.getEntity() != null) reward(pa.getEntity());
                            }
                        }
                    }
                } catch (Throwable t) {
                    Digital.LOG.error("Dark Tower reward failed", t);
                }
            };
            if (server != null) server.execute(reward);
            else reward.run();
        });
    }

    static void reward(ServerPlayer player) {
        RandomSource r = player.getRandom();
        give(player, new ItemStack(Digital.CHROME_INGOT.get(), 2 + r.nextInt(3)));
        give(player, new ItemStack(Digital.FRAGMENTS.get(Attribute.VIRUS).get(), 4 + r.nextInt(5)));
        if (r.nextFloat() < 0.5F) give(player, new ItemStack(Digital.DARK_SPORE.get()));
        player.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tower.cleared").withStyle(ChatFormatting.GOLD));
    }

    static void give(ServerPlayer player, ItemStack stack) {
        if (!player.getInventory().add(stack)) {
            ItemEntity e = player.drop(stack, false);
            if (e != null) e.setNoPickUpDelay();
        }
    }
}
