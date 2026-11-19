package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.events.common.LifecycleEvent;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.phys.Vec3;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

/**
 * Raids: now and then (every 2-3 hours with players online; or `/digital raid start`) a Digital Rift tears open near
 * a player and a Demon Lord or Royal Knight comes through: a level 80 boss, uncatchable, in three phases (beat it and it
 * re-forms its data until the last), with a boss bar for everyone near. Everyone who battled it shares the reward
 * (Chrome Digizoid, a Crest, a Digi-Core). While it's loose, the land round the rift turns to wireframe and circuitry
 * (gamerule digitalDigitization), which comes back as it was when the raid ends.
 */
public final class Raids {
    static final String TAG = "cobbleeffort_digital_raid";
    static final List<String> BOSSES = List.of("venomvamdemon", "apocalymon", "demon", "lilithmon", "leviamon", "barbamon",
            "belphemonragemode", "beelzebumon", "lucemonsatanmode", "omegamon", "dukemon", "alphamon", "ulforcevdramon",
            "magnamon", "duftmon", "craniummon", "sleipmon", "dynasmon", "lordknightmon", "examon", "gankoomon", "jesmon");
    static final int PHASES = 3, LEVEL = 80;
    static final long LIFETIME = 20L * 60 * 30;
    public static final GameRules.Key<GameRules.BooleanValue> DIGITIZATION =
            GameRules.register("digitalDigitization", GameRules.Category.MISC, GameRules.BooleanValue.create(true));

    static final class Raid {
        ResourceKey<Level> level;
        Vec3 at;
        String species;
        int phase = 1;
        long started, nextSpawn;
        UUID boss;
        final Set<UUID> fighters = new HashSet<>();
        final ServerBossEvent bar = new ServerBossEvent(Component.empty(), BossEvent.BossBarColor.RED, BossEvent.BossBarOverlay.NOTCHED_6);
    }

    static Raid active;
    static long nextRaid = -1;

    private Raids() {
    }

    // --- starting and ending ---------------------------------------------------------------------------------------------

    static String pickBoss(RandomSource r) {
        List<String> have = new ArrayList<>();
        for (String id : BOSSES) {
            if (PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", id)) != null) have.add(id);
        }
        return have.isEmpty() ? null : have.get(r.nextInt(have.size()));
    }

    public static boolean start(ServerPlayer near) {
        if (active != null) return false;
        String species = pickBoss(near.getRandom());
        if (species == null) return false;
        Raid r = new Raid();
        r.level = near.level().dimension();
        r.at = DigitalWorld.openRift(near);
        r.species = species;
        r.started = near.serverLevel().getGameTime();
        r.nextSpawn = r.started + 100;
        active = r;
        Component name = PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", species)).getTranslatedName();
        for (ServerPlayer p : near.server.getPlayerList().getPlayers()) {
            p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".raid.started", name, (int) r.at.x, (int) r.at.z)
                    .withStyle(ChatFormatting.RED, ChatFormatting.BOLD));
        }
        return true;
    }

    public static void stop(MinecraftServer server, boolean beaten) {
        Raid r = active;
        if (r == null) return;
        active = null;
        r.bar.removeAllPlayers();
        ServerLevel level = server.getLevel(r.level);
        if (level != null && r.boss != null && level.getEntity(r.boss) != null) level.getEntity(r.boss).discard();
        restore(server);
        if (beaten) {
            for (UUID id : r.fighters) {
                ServerPlayer p = server.getPlayerList().getPlayer(id);
                if (p != null) reward(p);
            }
        }
        for (ServerPlayer p : server.getPlayerList().getPlayers()) {
            p.sendSystemMessage(Component.translatable(Digital.MOD_ID + (beaten ? ".raid.beaten" : ".raid.gone")).withStyle(ChatFormatting.GOLD));
        }
    }

    static void reward(ServerPlayer p) {
        RandomSource r = p.getRandom();
        DarkTower.give(p, new ItemStack(Digital.CHROME_INGOT.get(), 3 + r.nextInt(4)));
        DarkTower.give(p, Crests.crestStack(Crests.CRESTS.get(r.nextInt(Crests.CRESTS.size()))));
        DarkTower.give(p, new ItemStack(Digital.DIGI_CORE.get()));
        if (r.nextFloat() < 0.5F) DarkTower.give(p, new ItemStack(Digital.TAG.get()));
        p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".raid.reward").withStyle(ChatFormatting.GOLD));
    }

    static void spawnBoss(ServerLevel level, Raid r) {
        Pokemon pk = PokemonProperties.Companion.parse("cobbleeffort:" + r.species + " level=" + LEVEL + " uncatchable").create();
        pk.getPersistentData().putBoolean(TAG, true);
        PokemonEntity e = new PokemonEntity(level, pk, CobblemonEntities.POKEMON);
        net.minecraft.world.entity.Mob mob = e;
        mob.moveTo(r.at.x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, (int) r.at.x, (int) r.at.z), r.at.z,
                level.getRandom().nextFloat() * 360F, 0F);
        mob.setPersistenceRequired();
        mob.addTag(TAG);
        mob.setCustomName(Component.translatable(Digital.MOD_ID + ".raid.boss", pk.getSpecies().getTranslatedName(), r.phase, PHASES)
                .withStyle(ChatFormatting.DARK_RED));
        mob.setCustomNameVisible(true);
        mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, MobEffectInstance.INFINITE_DURATION, 0, false, false));
        level.addFreshEntity(mob);
        r.boss = e.getUUID();
        level.playSound(null, BlockPos.containing(r.at), SoundEvents.WITHER_SPAWN, SoundSource.HOSTILE, 1F, 0.8F);
    }

    // --- the tick -------------------------------------------------------------------------------------------------------

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            try {
                tick(server);
            } catch (Throwable t) {
                Digital.LOG.error("Raid tick failed", t);
            }
        });
        LifecycleEvent.SERVER_STARTED.register(server -> {
            try {
                restore(server);
            } catch (Throwable t) {
                Digital.LOG.error("Restoring digitized blocks failed", t);
            }
        });
        LifecycleEvent.SERVER_STOPPING.register(server -> {
            if (active != null) stop(server, false);
        });
        CobblemonEvents.BATTLE_STARTED_PRE.subscribe(Priority.NORMAL, event -> {
            if (active == null) return;
            boolean boss = false;
            for (BattleActor a : event.getBattle().getActors()) {
                for (BattlePokemon bp : a.getPokemonList()) if (bp.getOriginalPokemon().getPersistentData().getBoolean(TAG)) boss = true;
            }
            if (!boss) return;
            for (BattleActor a : event.getBattle().getActors()) {
                if (a instanceof PlayerBattleActor pa && pa.getEntity() != null) active.fighters.add(pa.getEntity().getUUID());
            }
        });
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            if (active == null) return;
            for (BattleActor loser : event.getLosers()) {
                for (BattlePokemon bp : loser.getPokemonList()) {
                    if (!bp.getOriginalPokemon().getPersistentData().getBoolean(TAG) || bp.getHealth() > 0) continue;
                    MinecraftServer server = Digital.server();
                    if (server == null) return;
                    server.execute(() -> {
                        Raid r = active;
                        if (r == null) return;
                        if (r.phase >= PHASES) {
                            stop(server, true);
                        } else {
                            r.phase++;
                            r.boss = null;
                            r.nextSpawn = server.overworld().getGameTime() + 60;
                            for (ServerPlayer p : server.getPlayerList().getPlayers()) {
                                p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".raid.phase", r.phase, PHASES).withStyle(ChatFormatting.RED));
                            }
                        }
                    });
                }
            }
        });
    }

    static void tick(MinecraftServer server) {
        long now = server.overworld().getGameTime();
        if (nextRaid < 0) nextRaid = now + 20L * 60 * (120 + server.overworld().getRandom().nextInt(60));
        if (active == null) {
            if (now >= nextRaid && !DigitalRules.on(server.overworld(), DigitalRules.RAIDS)) {
                nextRaid = now + 20L * 60 * (120 + server.overworld().getRandom().nextInt(60));
            } else if (now >= nextRaid) {
                nextRaid = now + 20L * 60 * (120 + server.overworld().getRandom().nextInt(60));
                List<ServerPlayer> ps = new ArrayList<>();
                for (ServerPlayer p : server.getPlayerList().getPlayers()) if (p.level().dimension() == Level.OVERWORLD && !p.isSpectator()) ps.add(p);
                if (!ps.isEmpty()) start(ps.get(server.overworld().getRandom().nextInt(ps.size())));
            }
            return;
        }
        Raid r = active;
        ServerLevel level = server.getLevel(r.level);
        if (level == null || now - r.started > LIFETIME) {
            stop(server, false);
            return;
        }
        if (r.boss == null && now >= r.nextSpawn) spawnBoss(level, r);
        if (now % 10 == 0) {
            PokemonEntity boss = r.boss == null ? null : level.getEntity(r.boss) instanceof PokemonEntity pe ? pe : null;
            float frac = boss == null ? 1F : (float) boss.getPokemon().getCurrentHealth() / Math.max(1, boss.getPokemon().getMaxHealth());
            r.bar.setProgress(Math.max(0F, Math.min(1F, ((PHASES - r.phase) + frac) / PHASES)));
            r.bar.setName(Component.translatable(Digital.MOD_ID + ".raid.bar", PokemonSpecies.INSTANCE.getByIdentifier(
                    ResourceLocation.fromNamespaceAndPath("cobbleeffort", r.species)).getTranslatedName(), r.phase, PHASES));
            for (ServerPlayer p : server.getPlayerList().getPlayers()) {
                boolean near = p.level() == level && p.position().distanceToSqr(r.at) < 160 * 160;
                if (near) r.bar.addPlayer(p);
                else r.bar.removePlayer(p);
            }
            DigitalWorld.keepRift(level, r.at, now + 200);
        }
        if (now % 100 == 0 && level.getGameRules().getBoolean(DIGITIZATION)) digitize(level, r, now);
    }

    // --- digitization (saved, so a restart still puts the land back) -----------------------------------------------------

    static void digitize(ServerLevel level, Raid r, long now) {
        int radius = (int) Math.min(18, 3 + (now - r.started) / 600);
        Digitized data = data(level.getServer());
        RandomSource rand = level.getRandom();
        for (int i = 0; i < 24; i++) {
            int x = (int) r.at.x + rand.nextInt(radius * 2 + 1) - radius, z = (int) r.at.z + rand.nextInt(radius * 2 + 1) - radius;
            if ((x - r.at.x) * (x - r.at.x) + (z - r.at.z) * (z - r.at.z) > radius * radius) continue;
            BlockPos pos = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z) - 1, z);
            BlockState s = level.getBlockState(pos);
            if (level.getBlockEntity(pos) != null || s.isAir() || !(s.is(BlockTags.DIRT) || s.is(BlockTags.SAND) || s.is(BlockTags.BASE_STONE_OVERWORLD)
                    || s.is(Blocks.GRAVEL) || s.is(Blocks.SNOW_BLOCK) || s.is(BlockTags.LEAVES))) continue;
            data.add(level, pos, s);
            level.setBlock(pos, ((x + z) & 1) == 0 ? Digital.CIRCUIT_BLOCK.get().defaultBlockState() : Digital.WIREFRAME_BLOCK.get().defaultBlockState(), 3);
        }
    }

    static void restore(MinecraftServer server) {
        Digitized data = data(server);
        if (data.list.isEmpty()) return;
        HolderLookup<net.minecraft.world.level.block.Block> blocks = server.registryAccess().lookupOrThrow(Registries.BLOCK);
        for (int i = data.list.size() - 1; i >= 0; i--) {
            CompoundTag t = data.list.getCompound(i);
            ServerLevel level = server.getLevel(ResourceKey.create(Registries.DIMENSION, ResourceLocation.parse(t.getString("dim"))));
            if (level == null) continue;
            BlockPos pos = new BlockPos(t.getInt("x"), t.getInt("y"), t.getInt("z"));
            level.setBlock(pos, NbtUtils.readBlockState(blocks, t.getCompound("state")), 3);
        }
        data.list.clear();
        data.setDirty();
    }

    static Digitized data(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(Digitized::new, Digitized::load, null), Digital.MOD_ID + "_digitized");
    }

    static final class Digitized extends SavedData {
        final ListTag list;
        final Set<String> keys = new HashSet<>();

        Digitized() {
            this(new ListTag());
        }

        Digitized(ListTag list) {
            this.list = list;
            for (int i = 0; i < list.size(); i++) {
                CompoundTag t = list.getCompound(i);
                keys.add(t.getString("dim") + t.getInt("x") + "," + t.getInt("y") + "," + t.getInt("z"));
            }
        }

        void add(ServerLevel level, BlockPos pos, BlockState s) {
            String k = level.dimension().location() + "" + pos.getX() + "," + pos.getY() + "," + pos.getZ();
            if (!keys.add(k)) return;
            CompoundTag t = new CompoundTag();
            t.putString("dim", level.dimension().location().toString());
            t.putInt("x", pos.getX());
            t.putInt("y", pos.getY());
            t.putInt("z", pos.getZ());
            t.put("state", NbtUtils.writeBlockState(s));
            list.add(t);
            setDirty();
        }

        static Digitized load(CompoundTag tag, HolderLookup.Provider registries) {
            return new Digitized(tag.getList("blocks", 10));
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("blocks", list);
            return tag;
        }
    }
}
