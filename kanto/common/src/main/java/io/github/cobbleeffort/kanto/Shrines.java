package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.serialization.MapCodec;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.util.StringRepresentable;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Shrines (0.14.0): the blocks that make the landmark structures' legendary and mythical places work. Each holds a
 * config in its block entity, written into the structure template:
 *   key      what it is, once per player ("rayquaza", "red_orbs"...)
 *   mode     "encounter" (summons a wild Pokémon: props, at dx/dy/dz from the shrine), "gift" (items) or "pokemon" (a
 *            Pokémon straight into the party)
 *   props    Cobblemon properties (e.g. "rayquaza level=70"); items: a list of item ids
 *   time     "any", "night" or "day"; label/hint: lang keys for what appears and for a failed condition
 * An encounter can be called again (after a short rest) until the player catches it: catching it marks the key done.
 * Gifts are given once. Progress is per player, saved with the world; /kanto shrines reset clears it.
 */
public final class Shrines {
    public static final String TAG = Kanto.MOD_ID + "_shrine";
    static final long REST_TICKS = 20 * 60 * 5;

    public enum Look implements StringRepresentable {
        ALTAR, TERMINAL;

        @Override
        public String getSerializedName() {
            return name().toLowerCase(java.util.Locale.ROOT);
        }
    }

    public static final EnumProperty<Look> LOOK = EnumProperty.create("look", Look.class);
    /** Turns with the structure (templates say north), so an encounter's dx/dz offset turns with it too. */
    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;

    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Kanto.MOD_ID, Registries.BLOCK_ENTITY_TYPE);
    public static final RegistrySupplier<Block> SHRINE = Kanto.BLOCKS.register("shrine", ShrineBlock::new);
    static {
        Kanto.ITEMS.register("shrine", () -> new BlockItem(SHRINE.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(Kanto.TAB)));
    }
    public static final RegistrySupplier<BlockEntityType<ShrineBlockEntity>> SHRINE_ENTITY = BLOCK_ENTITIES.register("shrine",
            () -> BlockEntityType.Builder.of(ShrineBlockEntity::new, SHRINE.get()).build(null));

    /** Live encounters (player UUID + key) -> the summoned entity, and when each was last called. */
    private static final Map<String, UUID> LIVE = new HashMap<>();
    private static final Map<String, Long> CALLED = new HashMap<>();

    private Shrines() {
    }

    static void register() {
        CobblemonEvents.POKEMON_CAPTURED.subscribe(Priority.NORMAL, event -> {
            try {
                Pokemon p = event.getPokemon();
                String key = p.getPersistentData().getString(TAG);
                if (!key.isEmpty()) {
                    progress(event.getPlayer().server).mark(event.getPlayer(), key);
                    p.getPersistentData().remove(TAG);
                }
            } catch (Throwable t) {
                Kanto.LOG.error("Shrine capture check failed", t);
            }
            return kotlin.Unit.INSTANCE;
        });
    }

    // --- the block ------------------------------------------------------------------------------------------------

    public static final class ShrineBlock extends BaseEntityBlock {
        public static final MapCodec<ShrineBlock> CODEC = simpleCodec(p -> new ShrineBlock());

        ShrineBlock() {
            super(BlockBehaviour.Properties.of().mapColor(MapColor.STONE).strength(-1F, 3600000F).lightLevel(s -> 9)
                    .requiresCorrectToolForDrops());
            registerDefaultState(stateDefinition.any().setValue(LOOK, Look.ALTAR).setValue(FACING, Direction.NORTH));
        }

        @Override
        protected MapCodec<? extends BaseEntityBlock> codec() {
            return CODEC;
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(LOOK, FACING);
        }

        @Override
        protected BlockState rotate(BlockState state, Rotation rotation) {
            return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
        }

        @Override
        protected BlockState mirror(BlockState state, Mirror mirror) {
            return state.rotate(mirror.getRotation(state.getValue(FACING)));
        }

        @Override
        protected RenderShape getRenderShape(BlockState state) {
            return RenderShape.MODEL;
        }

        @Override
        public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
            return new ShrineBlockEntity(pos, state);
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            if (level.isClientSide) return InteractionResult.SUCCESS;
            if (player instanceof ServerPlayer sp && level.getBlockEntity(pos) instanceof ShrineBlockEntity be) {
                try {
                    use(sp, (ServerLevel) level, pos, be.config, state.getValue(FACING));
                } catch (Throwable t) {
                    Kanto.LOG.error("Shrine use failed", t);
                }
            }
            return InteractionResult.CONSUME;
        }
    }

    public static final class ShrineBlockEntity extends BlockEntity {
        CompoundTag config = new CompoundTag();

        public ShrineBlockEntity(BlockPos pos, BlockState state) {
            super(SHRINE_ENTITY.get(), pos, state);
        }

        @Override
        protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.loadAdditional(tag, registries);
            config = tag.getCompound("config");
        }

        @Override
        protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.saveAdditional(tag, registries);
            tag.put("config", config.copy());
        }
    }

    // --- using one --------------------------------------------------------------------------------------------------

    static void use(ServerPlayer player, ServerLevel level, BlockPos pos, CompoundTag c, Direction facing) {
        String key = c.getString("key");
        if (key.isEmpty()) return;
        String m = Kanto.MOD_ID + ".shrine.";
        Progress progress = progress(level.getServer());
        if (progress.done(player, key)) {
            player.displayClientMessage(Component.translatable(m + "done." + c.getString("mode")), true);
            return;
        }
        String time = c.getString("time");
        long day = level.getDayTime() % 24000;
        boolean night = day >= 13000 && day < 23000;
        if (("night".equals(time) && !night) || ("day".equals(time) && night)) {
            player.displayClientMessage(Component.translatable(c.getString("hint")).withStyle(ChatFormatting.GRAY), true);
            return;
        }
        switch (c.getString("mode")) {
            case "gift" -> {
                ListTag items = c.getList("items", Tag.TAG_STRING);
                for (int i = 0; i < items.size(); i++) {
                    Item item = BuiltInRegistries.ITEM.get(ResourceLocation.parse(items.getString(i)));
                    ItemStack stack = new ItemStack(item);
                    if (!player.getInventory().add(stack)) player.drop(stack, false);
                }
                progress.mark(player, key);
                effects(level, pos);
                player.sendSystemMessage(Component.translatable(c.getString("label")).withStyle(ChatFormatting.GOLD));
            }
            case "pokemon" -> {
                Pokemon p = PokemonProperties.Companion.parse(c.getString("props")).create();
                if (!Cobblemon.INSTANCE.getStorage().getParty(player).add(p)) Cobblemon.INSTANCE.getStorage().getPC(player).add(p);
                progress.mark(player, key);
                effects(level, pos);
                player.sendSystemMessage(Component.translatable(c.getString("label"), p.getSpecies().getTranslatedName()).withStyle(ChatFormatting.GOLD));
            }
            default -> encounter(player, level, pos, c, key, facing);
        }
    }

    private static void encounter(ServerPlayer player, ServerLevel level, BlockPos pos, CompoundTag c, String key, Direction facing) {
        String id = player.getStringUUID() + "/" + key;
        UUID live = LIVE.get(id);
        Entity existing = live == null ? null : level.getEntity(live);
        String m = Kanto.MOD_ID + ".shrine.";
        if (existing != null && existing.isAlive()) {
            player.displayClientMessage(Component.translatable(m + "here"), true);
            return;
        }
        long now = level.getGameTime();
        Long last = CALLED.get(id);
        if (last != null && now - last < REST_TICKS) {
            player.displayClientMessage(Component.translatable(m + "resting", (REST_TICKS - (now - last)) / 20 / 60 + 1), true);
            return;
        }
        Pokemon pokemon = PokemonProperties.Companion.parse(c.getString("props")).create();
        pokemon.getPersistentData().putString(TAG, key);
        PokemonEntity entity = new PokemonEntity(level, pokemon, CobblemonEntities.POKEMON);
        net.minecraft.world.entity.Mob mob = entity;
        int dx = c.getInt("dx"), dz = c.getInt("dz");
        int turns = Math.floorMod(facing.get2DDataValue() - Direction.NORTH.get2DDataValue(), 4);   // clockwise quarter turns
        for (int i = 0; i < turns; i++) {
            int x = dx;
            dx = -dz;
            dz = x;
        }
        mob.moveTo(pos.getX() + 0.5 + dx, pos.getY() + c.getInt("dy"), pos.getZ() + 0.5 + dz,
                level.getRandom().nextFloat() * 360F, 0F);
        mob.setPersistenceRequired();
        mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, 20 * 20, 0, false, false));
        level.addFreshEntity(mob);
        LIVE.put(id, mob.getUUID());
        CALLED.put(id, now);
        effects(level, pos);
        level.playSound(null, pos, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1F, 0.7F);
        player.sendSystemMessage(Component.translatable(c.getString("label"), pokemon.getSpecies().getTranslatedName())
                .withStyle(ChatFormatting.LIGHT_PURPLE));
    }

    private static void effects(ServerLevel level, BlockPos pos) {
        level.sendParticles(ParticleTypes.END_ROD, pos.getX() + 0.5, pos.getY() + 1.2, pos.getZ() + 0.5, 30, 0.6, 0.8, 0.6, 0.05);
        level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.BLOCKS, 1F, 1F);
    }

    // --- per-player progress ----------------------------------------------------------------------------------------

    static Progress progress(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(Progress::new, Progress::load, null), Kanto.MOD_ID + "_shrines");
    }

    /** /kanto shrines reset <player> [key]: forget what the player met or was given. */
    static int reset(ServerPlayer player, String key) {
        return progress(player.server).reset(player, key);
    }

    static final class Progress extends SavedData {
        private CompoundTag players = new CompoundTag();

        boolean done(ServerPlayer p, String key) {
            ListTag list = players.getList(p.getStringUUID(), Tag.TAG_STRING);
            for (int i = 0; i < list.size(); i++) if (list.getString(i).equals(key)) return true;
            return false;
        }

        void mark(ServerPlayer p, String key) {
            if (done(p, key)) return;
            ListTag list = players.getList(p.getStringUUID(), Tag.TAG_STRING);
            list.add(StringTag.valueOf(key));
            players.put(p.getStringUUID(), list);
            setDirty();
        }

        int reset(ServerPlayer p, String key) {
            ListTag list = players.getList(p.getStringUUID(), Tag.TAG_STRING);
            int before = list.size();
            if (key == null) list.clear();
            else list.removeIf(t -> t.getAsString().equals(key));
            players.put(p.getStringUUID(), list);
            setDirty();
            return before - list.size();
        }

        static Progress load(CompoundTag tag, HolderLookup.Provider registries) {
            Progress p = new Progress();
            p.players = tag.getCompound("players");
            return p;
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("players", players);
            return tag;
        }
    }
}
