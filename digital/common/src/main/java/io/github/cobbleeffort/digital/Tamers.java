package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.npc.NPCClass;
import com.cobblemon.mod.common.api.npc.NPCClasses;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.storage.party.NPCPartyStore;
import com.cobblemon.mod.common.entity.npc.NPCBattleActor;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.entity.npc.NPCEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.StructureTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.List;

/**
 * Tamers: wandering Tamer NPCs turn up in villages with themed Digimon teams (a Crack Team officer with machine
 * Digimon, a Nature Spirits tamer, Deep Savers, Nightmare Soldiers, Dragon's Roar, Virus Busters) and challenge you
 * (talk to them); the Colosseum (a structure on the plains) keeps three tamers for 1v1, 2v2 (doubles) and 3v3. Their
 * levels follow your party. Beating one earns Tamer Rank points (Colosseum tamers count more, once a day each) and
 * Digi-Modify cards; ranks: Rookie, Champion (100), Ultimate (300), Mega (700).
 */
public final class Tamers {
    static final String TAG = "cobbleeffort_digital_tamer", COLOSSEUM_TAG = "cobbleeffort_digital_colosseum";
    record Theme(String id, List<String> team) {
    }

    static final List<Theme> THEMES = List.of(
            new Theme("crack_team", List.of("mugendramon", "tankdramon", "andromon", "guardromon", "hagurumon", "metalgreymon")),
            new Theme("nature_spirits", List.of("leomon", "garurumon", "kyubimon", "renamon", "gabumon", "togemon")),
            new Theme("deep_savers", List.of("ikkakumon", "zudomon", "seadramon", "whamon", "gomamon", "shellmon")),
            new Theme("nightmare_soldiers", List.of("devimon", "bakemon", "wizarmon", "vamdemon", "ladydevimon", "devidramon")),
            new Theme("dragons_roar", List.of("greymon", "airdramon", "coredramonblue", "wargreymon", "vdramon", "monochromon")),
            new Theme("virus_busters", List.of("angemon", "tailmon", "angewomon", "unimon", "holyangemon", "patamon")));
    static final int[] RANKS = {0, 100, 300, 700};
    static final String[] RANK_NAMES = {"rookie", "champion", "ultimate", "mega"};

    private Tamers() {
    }

    static List<String> available(Theme t) {
        List<String> out = new ArrayList<>();
        for (String id : t.team()) {
            if (PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", id)) != null) out.add(id);
        }
        return out;
    }

    static int levelFor(ServerPlayer p) {
        int best = 5;
        for (Pokemon q : Cobblemon.INSTANCE.getStorage().getParty(p)) best = Math.max(best, q.getLevel());
        return Math.max(5, Math.min(100, best + p.getRandom().nextInt(5) - 2));
    }

    /** A Tamer NPC with a themed team of `size` at the player's level; doubles = the 2v2 class. */
    static NPCEntity spawn(ServerLevel level, BlockPos at, ServerPlayer near, int size, boolean doubles, String extraTag) {
        NPCClass cls = NPCClasses.getByIdentifier(ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, doubles ? "tamer_doubles" : "tamer"));
        if (cls == null) return null;
        RandomSource r = level.getRandom();
        Theme theme = THEMES.get(r.nextInt(THEMES.size()));
        List<String> team = available(theme);
        if (team.isEmpty()) return null;
        int lvl = levelFor(near);
        NPCEntity npc = new NPCEntity(level);
        npc.moveTo(at.getX() + 0.5, at.getY(), at.getZ() + 0.5, r.nextFloat() * 360F, 0F);
        npc.setNpc(cls);
        npc.initialize(lvl);
        NPCPartyStore party = new NPCPartyStore(npc);
        for (int i = 0; i < size; i++) party.add(PokemonProperties.Companion.parse("cobbleeffort:" + team.get(r.nextInt(team.size())) + " level=" + lvl).create());
        npc.setParty(party);
        npc.setSkill(3);
        npc.setCustomName(Component.translatable(Digital.MOD_ID + ".tamer." + theme.id()).withStyle(ChatFormatting.AQUA));
        npc.setCustomNameVisible(true);
        npc.setInvulnerable(Boolean.TRUE);
        npc.setPersistenceRequired();
        npc.addTag(TAG);
        if (extraTag != null) npc.addTag(extraTag);
        level.addFreshEntity(npc);
        return npc;
    }

    static void init() {
        TickEvent.SERVER_POST.register(server -> {
            if (server.getTickCount() % 200 != 0) return;
            for (ServerPlayer p : server.getPlayerList().getPlayers()) {
                try {
                    tick(p);
                } catch (Throwable t) {
                    Digital.LOG.error("Tamer tick failed", t);
                }
            }
        });
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            List<BattleActor> winners = new ArrayList<>(event.getWinners()), losers = new ArrayList<>(event.getLosers());
            MinecraftServer server = Digital.server();
            if (server == null) return;
            server.execute(() -> {
                for (BattleActor l : losers) {
                    if (!(l instanceof NPCBattleActor npc) || npc.getEntity() == null || !npc.getEntity().getTags().contains(TAG)) continue;
                    NPCEntity e = npc.getEntity();
                    boolean colosseum = e.getTags().contains(COLOSSEUM_TAG);
                    for (BattleActor w : winners) {
                        if (w instanceof PlayerBattleActor pa && pa.getEntity() != null) reward(pa.getEntity(), e, colosseum);
                    }
                    if (!colosseum) Scheduler.later(server, 60, () -> ((Entity) e).discard());
                }
            });
        });
    }

    static void tick(ServerPlayer p) {
        ServerLevel level = p.serverLevel();
        if (level.dimension() != Level.OVERWORLD) return;
        BlockPos pos = p.blockPosition();
        // the Colosseum: three tamers, once
        Structure colosseum = level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(ResourceLocation.fromNamespaceAndPath(Digital.MOD_ID, "colosseum"));
        if (colosseum != null) {
            StructureStart start = level.structureManager().getStructureAt(pos, colosseum);
            if (start.isValid()) {
                var box = start.getBoundingBox();
                AABB area = AABB.of(box).inflate(4);
                if (level.getEntitiesOfClass(NPCEntity.class, area, e -> e.getTags().contains(COLOSSEUM_TAG)).isEmpty()) {
                    BlockPos c = box.getCenter();
                    int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, c.getX(), c.getZ());
                    int[][] spots = {{-5, 0}, {0, -5}, {5, 0}};
                    for (int i = 0; i < 3; i++) {
                        BlockPos at = new BlockPos(c.getX() + spots[i][0], y, c.getZ() + spots[i][1]);
                        spawn(level, at, p, i + 1, i == 1, COLOSSEUM_TAG);
                    }
                    p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tamer.colosseum").withStyle(ChatFormatting.GOLD));
                }
            }
        }
        // a wandering tamer in a village now and then
        if (p.getRandom().nextInt(30) != 0) return;
        if (!level.structureManager().getStructureWithPieceAt(pos, StructureTags.VILLAGE).isValid()) return;
        if (!level.getEntitiesOfClass(NPCEntity.class, p.getBoundingBox().inflate(64), e -> e.getTags().contains(TAG) && !e.getTags().contains(COLOSSEUM_TAG)).isEmpty()) return;
        int x = pos.getX() + p.getRandom().nextInt(17) - 8, z = pos.getZ() + p.getRandom().nextInt(17) - 8;
        BlockPos at = new BlockPos(x, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z), z);
        int size = 1 + p.getRandom().nextInt(3);
        if (spawn(level, at, p, size, size == 2 && p.getRandom().nextBoolean(), null) != null) {
            p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".tamer.appears").withStyle(ChatFormatting.AQUA), true);
        }
    }

    static void reward(ServerPlayer p, NPCEntity tamer, boolean colosseum) {
        Rank data = rank(p.server);
        String key = p.getStringUUID();
        long day = p.serverLevel().getDayTime() / 24000L;
        int points = 10;
        if (colosseum) {
            String ck = key + ":" + tamer.getUUID();
            if (data.colosseum.getLong(ck) == day + 1) {
                p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tamer.already_today").withStyle(ChatFormatting.GRAY));
                return;
            }
            data.colosseum.putLong(ck, day + 1);
            points = 25;
        }
        int before = data.points.getInt(key), after = before + points;
        data.points.putInt(key, after);
        data.setDirty();
        int r = p.getRandom().nextInt(Digital.CARDS.size());
        DarkTower.give(p, new ItemStack(Digital.CARD_ITEMS.get(Digital.CARDS.get(r)).get(), colosseum ? 2 : 1));
        p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tamer.won", points, after).withStyle(ChatFormatting.GOLD));
        int rb = rankOf(before), ra = rankOf(after);
        if (ra > rb) {
            p.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".tamer.rank_up",
                    Component.translatable(Digital.MOD_ID + ".rank." + RANK_NAMES[ra])).withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        }
    }

    static int rankOf(int points) {
        int r = 0;
        for (int i = 0; i < RANKS.length; i++) if (points >= RANKS[i]) r = i;
        return r;
    }

    static int points(ServerPlayer p) {
        return rank(p.server).points.getInt(p.getStringUUID());
    }

    static Rank rank(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(Rank::new, Rank::load, null), Digital.MOD_ID + "_tamer_rank");
    }

    static final class Rank extends SavedData {
        final CompoundTag points, colosseum;

        Rank() {
            this(new CompoundTag(), new CompoundTag());
        }

        Rank(CompoundTag points, CompoundTag colosseum) {
            this.points = points;
            this.colosseum = colosseum;
        }

        static Rank load(CompoundTag tag, HolderLookup.Provider registries) {
            return new Rank(tag.getCompound("points"), tag.getCompound("colosseum"));
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("points", points);
            tag.put("colosseum", colosseum);
            return tag;
        }
    }
}
