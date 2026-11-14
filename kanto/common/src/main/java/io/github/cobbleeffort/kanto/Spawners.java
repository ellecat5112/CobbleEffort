package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.npc.NPCClass;
import com.cobblemon.mod.common.api.npc.NPCClasses;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.storage.party.NPCPartyStore;
import com.cobblemon.mod.common.battles.BattleBuilder;
import com.cobblemon.mod.common.battles.BattleFormat;
import com.cobblemon.mod.common.entity.npc.NPCBattleActor;
import com.cobblemon.mod.common.entity.npc.NPCEntity;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.serialization.MapCodec;
import dev.architectury.event.events.common.TickEvent;
import dev.architectury.networking.NetworkManager;
import dev.architectury.registry.registries.DeferredRegister;
import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import java.util.function.BiConsumer;

/**
 * The Pokémon Spawner and the Trainer Spawner: creative/operator blocks configured like command blocks (right-click
 * opens a screen) that, on a rising redstone signal, summon a configured Pokémon (any Cobblemon properties: species,
 * level, shiny, moves, IVs...; optionally uncatchable, glowing, giant, and battling the nearest player at once) or a
 * trainer (name, optional player skin, a team of Pokémon property lines, a default level, skill, singles/doubles;
 * optionally challenging the nearest player at once and leaving after it loses). Made for scripted encounters.
 */
public final class Spawners {
    public static final String SPAWNED_TAG = Kanto.MOD_ID + "_spawned";
    public static final String DESPAWN_TAG = Kanto.MOD_ID + "_despawn_on_defeat";
    static final double BATTLE_RANGE = 24;

    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Kanto.MOD_ID, Registries.BLOCK_ENTITY_TYPE);

    public static final RegistrySupplier<Block> POKEMON_SPAWNER = Kanto.BLOCKS.register("pokemon_spawner", () -> new SpawnerBlock(false));
    public static final RegistrySupplier<Block> TRAINER_SPAWNER = Kanto.BLOCKS.register("trainer_spawner", () -> new SpawnerBlock(true));
    static {
        Kanto.ITEMS.register("pokemon_spawner", () -> new BlockItem(POKEMON_SPAWNER.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(Kanto.TAB)));
        Kanto.ITEMS.register("trainer_spawner", () -> new BlockItem(TRAINER_SPAWNER.get(), new Item.Properties().rarity(Rarity.EPIC).arch$tab(Kanto.TAB)));
    }
    public static final RegistrySupplier<BlockEntityType<SpawnerBlockEntity>> SPAWNER_ENTITY = BLOCK_ENTITIES.register("spawner",
            () -> BlockEntityType.Builder.of(SpawnerBlockEntity::new, POKEMON_SPAWNER.get(), TRAINER_SPAWNER.get()).build(null));

    /** The client opens the config screen through this (set by the client init, so the block never loads client classes). */
    public static BiConsumer<BlockPos, Boolean> screenOpener = (pos, trainer) -> {
    };

    /** Battles to start a little after a spawn (the new entity must be in the world first): due tick, task. */
    private static final List<Object[]> DELAYED = new ArrayList<>();

    private Spawners() {}

    /** Queues the blocks/items (class load) and wires the packet and events; BLOCK_ENTITIES registers after BLOCKS. */
    static void register() {
        NetworkManager.registerReceiver(NetworkManager.Side.C2S, SavePacket.TYPE, SavePacket.STREAM_CODEC,
                (packet, context) -> context.queue(() -> {
                    try {
                        if (context.getPlayer() instanceof ServerPlayer player && player.canUseGameMasterBlocks()
                                && player.distanceToSqr(Vec3.atCenterOf(packet.pos())) < 64 * 64
                                && player.level().getBlockEntity(packet.pos()) instanceof SpawnerBlockEntity be) {
                            be.setConfig(packet.config());
                            player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".spawner.saved"), true);
                        }
                    } catch (Throwable t) {
                        Kanto.LOG.error("Saving a spawner failed", t);
                    }
                }));
        TickEvent.SERVER_POST.register(Spawners::tick);
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            List<BattleActor> losers = new ArrayList<>(event.getLosers());
            for (BattleActor loser : losers) {
                if (loser instanceof NPCBattleActor npc && npc.getEntity() != null && npc.getEntity().getTags().contains(DESPAWN_TAG)) {
                    NPCEntity entity = npc.getEntity();
                    MinecraftServer server = entity.getServer();
                    if (server != null) later(server, 60, () -> ((Entity) entity).discard());
                }
            }
        });
    }

    static void later(MinecraftServer server, int ticks, Runnable task) {
        synchronized (DELAYED) {
            DELAYED.add(new Object[]{server.getTickCount() + ticks, task});
        }
    }

    private static void tick(MinecraftServer server) {
        List<Runnable> due = new ArrayList<>();
        synchronized (DELAYED) {
            for (Iterator<Object[]> it = DELAYED.iterator(); it.hasNext(); ) {
                Object[] e = it.next();
                if ((int) e[0] <= server.getTickCount()) {
                    due.add((Runnable) e[1]);
                    it.remove();
                }
            }
        }
        for (Runnable r : due) {
            try {
                r.run();
            } catch (Throwable t) {
                Kanto.LOG.error("A spawner task failed", t);
            }
        }
    }

    // --- config ------------------------------------------------------------------------------------------------------

    /** Keeps only the known settings, with sane bounds (the packet comes from a client). */
    static CompoundTag clean(CompoundTag in, boolean trainer) {
        CompoundTag out = new CompoundTag();
        out.putString("name", cut(in.getString("name"), 64));
        out.putBoolean("battle", in.getBoolean("battle"));
        out.putBoolean("one", in.getBoolean("one"));
        if (trainer) {
            out.putString("skin", cut(in.getString("skin"), 16));
            out.putString("team", cut(in.getString("team"), 4000));
            out.putInt("level", Math.max(1, Math.min(100, in.contains("level") ? in.getInt("level") : 50)));
            out.putInt("skill", Math.max(0, Math.min(5, in.contains("skill") ? in.getInt("skill") : 3)));
            out.putBoolean("doubles", in.getBoolean("doubles"));
            out.putBoolean("despawn", in.getBoolean("despawn"));
        } else {
            out.putString("pokemon", cut(in.getString("pokemon"), 1000));
            out.putInt("level", Math.max(1, Math.min(100, in.contains("level") ? in.getInt("level") : 50)));
            out.putFloat("scale", Math.max(0.1F, Math.min(10F, in.contains("scale") ? in.getFloat("scale") : 1F)));
            out.putBoolean("uncatchable", in.getBoolean("uncatchable"));
            out.putBoolean("glowing", in.getBoolean("glowing"));
        }
        return out;
    }

    private static String cut(String s, int max) {
        return s.length() > max ? s.substring(0, max) : s;
    }

    // --- spawning ----------------------------------------------------------------------------------------------------

    static void trigger(ServerLevel level, BlockPos pos, SpawnerBlockEntity be, boolean trainer) {
        CompoundTag c = be.config();
        if (c.getBoolean("one") && be.lastSpawned != null) {
            Entity old = level.getEntity(be.lastSpawned);
            if (old != null && old.isAlive()) return;
        }
        Vec3 at = Vec3.atBottomCenterOf(pos.above());
        Entity spawned;
        try {
            spawned = trainer ? spawnTrainer(level, at, c) : spawnPokemon(level, at, c);
        } catch (Throwable t) {
            Kanto.LOG.error("Spawner at {} failed", pos, t);
            spawned = null;
        }
        if (spawned == null) return;
        be.lastSpawned = spawned.getUUID();
        be.setChanged();
        if (c.getBoolean("battle")) {
            Entity target = spawned;
            later(level.getServer(), 10, () -> startBattle(level, target, trainer, c.getBoolean("doubles")));
        }
    }

    private static Entity spawnPokemon(ServerLevel level, Vec3 at, CompoundTag c) {
        String props = c.getString("pokemon").trim();
        if (props.isEmpty()) return null;
        if (c.getBoolean("uncatchable")) props += " uncatchable";
        PokemonProperties properties = PokemonProperties.Companion.parse(props);
        if (properties.getLevel() == null) properties.setLevel(c.getInt("level"));
        Pokemon pokemon = properties.create();
        pokemon.setScaleModifier(c.getFloat("scale"));
        pokemon.getPersistentData().putBoolean(SPAWNED_TAG, true);
        PokemonEntity entity = new PokemonEntity(level, pokemon, CobblemonEntities.POKEMON);
        net.minecraft.world.entity.Mob mob = entity;
        mob.moveTo(at.x, at.y, at.z, level.getRandom().nextFloat() * 360F, 0F);
        mob.setPersistenceRequired();
        mob.addTag(SPAWNED_TAG);
        String name = c.getString("name").trim();
        if (!name.isEmpty()) {
            mob.setCustomName(Component.literal(name));
            mob.setCustomNameVisible(true);
        }
        if (c.getBoolean("glowing")) {
            mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, MobEffectInstance.INFINITE_DURATION, 0, false, false));
        }
        level.addFreshEntity(mob);
        return mob;
    }

    private static Entity spawnTrainer(ServerLevel level, Vec3 at, CompoundTag c) {
        NPCClass npcClass = NPCClasses.getByIdentifier(Kanto.id("spawner_trainer"));
        if (npcClass == null) {
            Kanto.LOG.error("Missing NPC class {}", Kanto.id("spawner_trainer"));
            return null;
        }
        NPCEntity npc = new NPCEntity(level);
        float yaw = level.getRandom().nextFloat() * 360F;
        npc.moveTo(at.x, at.y, at.z, yaw, 0F);
        npc.setNpc(npcClass);
        int lvl = c.getInt("level");
        npc.initialize(lvl);
        NPCPartyStore party = new NPCPartyStore(npc);
        int members = 0;
        for (String line : c.getString("team").split("[;\\n]")) {
            String props = line.trim();
            if (props.isEmpty() || members >= 6) continue;
            PokemonProperties properties = PokemonProperties.Companion.parse(props);
            if (properties.getLevel() == null) properties.setLevel(lvl);
            party.add(properties.create());
            members++;
        }
        if (members == 0) return null;
        npc.setParty(party);
        npc.setSkill(c.getInt("skill"));
        String name = c.getString("name").trim();
        npc.setCustomName(Component.literal(name.isEmpty() ? "Trainer" : name));
        npc.setCustomNameVisible(true);
        npc.setInvulnerable(Boolean.TRUE);
        npc.setPersistenceRequired();
        npc.addTag(SPAWNED_TAG);
        if (c.getBoolean("despawn")) npc.addTag(DESPAWN_TAG);
        level.addFreshEntity(npc);
        String skin = c.getString("skin").trim();
        if (!skin.isEmpty()) {
            try {
                npc.loadTextureFromGameProfileName(skin);
            } catch (Throwable t) {
                Kanto.LOG.warn("Couldn't load the skin of {} for a spawned trainer", skin, t);
            }
        }
        return npc;
    }

    private static void startBattle(ServerLevel level, Entity spawned, boolean trainer, boolean doubles) {
        if (!spawned.isAlive()) return;
        ServerPlayer player = null;
        double best = BATTLE_RANGE * BATTLE_RANGE;
        for (ServerPlayer p : level.players()) {
            double d = p.distanceToSqr(spawned);
            if (d < best && !p.isSpectator()) {
                best = d;
                player = p;
            }
        }
        if (player == null) return;
        BattleFormat format = doubles ? BattleFormat.Companion.getGEN_9_DOUBLES() : BattleFormat.Companion.getGEN_9_SINGLES();
        if (trainer) {
            BattleBuilder.INSTANCE.pvn(player, (NPCEntity) spawned, null, format, false, false);
        } else {
            BattleBuilder.INSTANCE.pve(player, (PokemonEntity) spawned, null, format);
        }
    }

    // --- the block, its block entity and its packet -----------------------------------------------------------------

    public static final class SpawnerBlock extends BaseEntityBlock {
        private final boolean trainer;

        SpawnerBlock(boolean trainer) {
            super(BlockBehaviour.Properties.ofFullCopy(Blocks.COMMAND_BLOCK).strength(-1.0F, 3600000.0F).noLootTable());
            this.trainer = trainer;
        }

        public boolean isTrainer() {
            return trainer;
        }

        @Override
        protected MapCodec<? extends BaseEntityBlock> codec() {
            return simpleCodec(p -> new SpawnerBlock(trainer));
        }

        @Override
        protected RenderShape getRenderShape(BlockState state) {
            return RenderShape.MODEL;
        }

        @Override
        public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
            return new SpawnerBlockEntity(pos, state);
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            if (!player.canUseGameMasterBlocks()) {
                if (!level.isClientSide) {
                    player.displayClientMessage(Component.translatable(Kanto.MOD_ID + ".wand.not_allowed").withStyle(ChatFormatting.RED), true);
                }
                return InteractionResult.PASS;
            }
            if (level.isClientSide) screenOpener.accept(pos, trainer);
            return InteractionResult.sidedSuccess(level.isClientSide);
        }

        @Override
        protected void neighborChanged(BlockState state, Level level, BlockPos pos, Block neighbor, BlockPos from, boolean moved) {
            if (level.isClientSide || !(level.getBlockEntity(pos) instanceof SpawnerBlockEntity be)) return;
            boolean powered = level.hasNeighborSignal(pos);
            if (powered && !be.powered) level.scheduleTick(pos, this, 1);
            be.powered = powered;
        }

        @Override
        protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            if (level.getBlockEntity(pos) instanceof SpawnerBlockEntity be) trigger(level, pos, be, trainer);
        }
    }

    public static final class SpawnerBlockEntity extends BlockEntity {
        private CompoundTag config = new CompoundTag();
        boolean powered;
        UUID lastSpawned;

        public SpawnerBlockEntity(BlockPos pos, BlockState state) {
            super(SPAWNER_ENTITY.get(), pos, state);
        }

        public CompoundTag config() {
            return config;
        }

        boolean trainer() {
            return getBlockState().getBlock() instanceof SpawnerBlock b && b.isTrainer();
        }

        void setConfig(CompoundTag tag) {
            config = clean(tag, trainer());
            setChanged();
            if (level != null) level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), 3);
        }

        @Override
        protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.saveAdditional(tag, registries);
            tag.put("config", config.copy());
            tag.putBoolean("powered", powered);
            if (lastSpawned != null) tag.putUUID("last", lastSpawned);
        }

        @Override
        protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.loadAdditional(tag, registries);
            config = tag.getCompound("config");
            powered = tag.getBoolean("powered");
            lastSpawned = tag.hasUUID("last") ? tag.getUUID("last") : null;
        }

        @Override
        public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
            CompoundTag tag = new CompoundTag();
            tag.put("config", config.copy());
            return tag;
        }

        @Override
        public Packet<ClientGamePacketListener> getUpdatePacket() {
            return ClientboundBlockEntityDataPacket.create(this);
        }

        @Override
        public boolean onlyOpCanSetNbt() {
            return true;
        }
    }

    /** Client to server: the screen's settings for the spawner at pos. */
    public record SavePacket(BlockPos pos, CompoundTag config) implements CustomPacketPayload {
        public static final Type<SavePacket> TYPE = new Type<>(Kanto.id("spawner_save"));
        public static final StreamCodec<RegistryFriendlyByteBuf, SavePacket> STREAM_CODEC = StreamCodec.composite(
                BlockPos.STREAM_CODEC, SavePacket::pos, ByteBufCodecs.COMPOUND_TAG, SavePacket::config, SavePacket::new);

        @Override
        public Type<? extends CustomPacketPayload> type() {
            return TYPE;
        }
    }
}
