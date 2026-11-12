package io.github.cobbleeffort.kanto;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.npc.NPCClass;
import com.cobblemon.mod.common.api.npc.NPCClasses;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.entity.npc.NPCBattleActor;
import com.cobblemon.mod.common.entity.npc.NPCEntity;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.saveddata.SavedData;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Kanto's eight gyms and the Elite Four hall (data/cobbleeffort_kanto/kanto/sites.json, templates under
 * structure/gym/): built once, the first time anyone arrives in Kanto (one building per tick), on a brick foundation,
 * each door facing Kanto's centre, with the trainers (Cobblemon NPCs) inside. Beating a gym leader gives their badge;
 * the Elite Four only battle trainers holding all eight; beating all four gives the Champion Ribbon.
 */
public final class KantoGyms {
    private static final Deque<Job> QUEUE = new ArrayDeque<>();
    /** A non-persistent chunk ticket: a site's chunks load (and generate) off the main thread before it's built. */
    private static final net.minecraft.server.level.TicketType<net.minecraft.world.level.ChunkPos> TICKET =
            net.minecraft.server.level.TicketType.create(Kanto.MOD_ID + "_gym", java.util.Comparator.comparingLong(net.minecraft.world.level.ChunkPos::toLong));

    /** One queued step: build a site once its chunks are loaded, or (site == null) a final action. */
    static final class Job {
        final ServerLevel level;
        final Site site;
        final Runnable then;
        final List<net.minecraft.world.level.ChunkPos> chunks = new ArrayList<>();
        boolean requested;
        int waited;

        Job(ServerLevel level, Site site, Runnable then) {
            this.level = level;
            this.site = site;
            this.then = then;
            if (site != null) {
                int half = Math.max(site.w(), site.d()) / 2 + 1;
                for (int cx = (site.x() - half) >> 4; cx <= (site.x() + half) >> 4; cx++) {
                    for (int cz = (site.z() - half) >> 4; cz <= (site.z() + half) >> 4; cz++) {
                        chunks.add(new net.minecraft.world.level.ChunkPos(cx, cz));
                    }
                }
            }
        }

        /** True when done (built, or given up). */
        boolean step() {
            if (site == null) {
                then.run();
                return true;
            }
            var cache = level.getChunkSource();
            if (!requested) {
                for (var c : chunks) cache.addRegionTicket(TICKET, c, 1, c);
                requested = true;
                return false;
            }
            boolean ready = chunks.stream().allMatch(c -> cache.getChunkNow(c.x, c.z) != null);
            if (!ready && ++waited < 20 * 120) return false;                 // wait up to two minutes
            try {
                if (ready) build(level, site);
                else Kanto.LOG.warn("Gave up building {}: its chunks didn't load", site.label());
            } finally {
                for (var c : chunks) cache.removeRegionTicket(TICKET, c, 1, c);
            }
            return true;
        }
    }
    private static final Map<Region, List<Site>> SITES = new java.util.EnumMap<>(Region.class);
    /** NPC class id -> its region and badge item id (gym leaders) or "" (Elite Four). */
    private static final Map<ResourceLocation, Role> ROLES = new HashMap<>();

    private KantoGyms() {
    }

    record Role(Region region, String badge) {
    }

    record Trainer(ResourceLocation npc, int x, int y, int z, float yaw, String badge, boolean elite) {
    }

    record Site(String id, String label, ResourceLocation template, int w, int h, int d, int x, int z, List<Trainer> trainers) {
    }

    static String nameOf(Region r) {
        return r.id.substring(0, 1).toUpperCase() + r.id.substring(1);
    }

    /** Kanto's sites (sites.json) or another region's (sites_<region>.json): written by tools/make_assets.py. */
    static synchronized List<Site> sites(Region region) {
        List<Site> cached = SITES.get(region);
        if (cached != null) return cached;
        List<Site> list = new ArrayList<>();
        SITES.put(region, list);
        String file = region == Region.KANTO ? "sites.json" : "sites_" + region.id + ".json";
        try (InputStream in = KantoGyms.class.getResourceAsStream("/data/" + Kanto.MOD_ID + "/kanto/" + file)) {
            if (in == null) return list;
            JsonArray all = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonArray();
            for (JsonElement e : all) {
                JsonObject o = e.getAsJsonObject();
                JsonArray size = o.getAsJsonArray("size");
                List<Trainer> trainers = new ArrayList<>();
                for (JsonElement te : o.getAsJsonArray("trainers")) {
                    JsonObject t = te.getAsJsonObject();
                    JsonArray pos = t.getAsJsonArray("pos");
                    Trainer tr = new Trainer(ResourceLocation.parse(t.get("npc").getAsString()), pos.get(0).getAsInt(), pos.get(1).getAsInt(),
                            pos.get(2).getAsInt(), t.get("yaw").getAsFloat(), t.has("badge") ? t.get("badge").getAsString() : null,
                            t.has("elite") && t.get("elite").getAsBoolean());
                    trainers.add(tr);
                    ROLES.put(tr.npc(), new Role(region, tr.badge() != null ? tr.badge() : ""));
                }
                list.add(new Site(o.get("id").getAsString(), o.get("label").getAsString(), ResourceLocation.parse(o.get("template").getAsString()),
                        size.get(0).getAsInt(), size.get(1).getAsInt(), size.get(2).getAsInt(), o.get("x").getAsInt(), o.get("z").getAsInt(), trainers));
            }
        } catch (Exception ex) {
            Kanto.LOG.error("Couldn't read {}'s sites", region.id, ex);
        }
        return list;
    }

    static void loadAll() {
        for (Region r : Region.values()) sites(r);
    }

    /** The badge item ids of a region's gyms. */
    static List<String> badgesOf(Region region) {
        List<String> out = new ArrayList<>();
        for (Site s : sites(region)) for (Trainer t : s.trainers()) if (t.badge() != null) out.add(t.badge());
        return out;
    }

    public static void init() {
        TickEvent.SERVER_POST.register(server -> {
            Job next = QUEUE.peek();
            if (next == null) return;
            try {
                if (next.step()) QUEUE.poll();
            } catch (Throwable t) {
                QUEUE.poll();
                Kanto.LOG.error("Building a Kanto site failed", t);
            }
        });
        CobblemonEvents.BATTLE_STARTED_PRE.subscribe(Priority.NORMAL, event -> {
            try {
                eliteGate(event);
            } catch (Throwable t) {
                Kanto.LOG.error("Elite Four check failed", t);
            }
        });
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            List<BattleActor> winners = new ArrayList<>(event.getWinners()), losers = new ArrayList<>(event.getLosers());
            MinecraftServer server = com.cobblemon.mod.common.util.DistributionUtilsKt.server();
            Runnable award = () -> {
                try {
                    victory(winners, losers);
                } catch (Throwable t) {
                    Kanto.LOG.error("Awarding a Kanto badge failed", t);
                }
            };
            if (server != null) server.execute(award);
            else award.run();
        });
    }

    // --- building ---------------------------------------------------------------------------------------------------

    /** On arrival in a region: build its sites if they aren't yet, and tell the player where they are. */
    static void arrived(ServerPlayer player, ServerLevel level, Region region) {
        if (sites(region).isEmpty()) return;
        if (ensureBuilt(level, region, false)) player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".gyms.building"));
        player.sendSystemMessage(where(region));
    }

    static Component where(Region region) {
        List<String> where = new ArrayList<>();
        for (Site s : sites(region)) where.add(s.label() + " " + s.x() + ", " + s.z());
        if (region == Region.KANTO) return Component.translatable(Kanto.MOD_ID + ".gyms.list", String.join("; ", where));
        return Component.translatable(Kanto.MOD_ID + ".gyms.list.region", nameOf(region), String.join("; ", where));
    }

    /** Queue a region's sites' building (once, or again when forced: /kanto rebuild). True when queued now. */
    static boolean ensureBuilt(ServerLevel level, Region region, boolean force) {
        Built built = built(level);
        if ((built.done && !force) || built.queued) return false;
        built.queued = true;
        for (Site site : sites(region)) QUEUE.add(new Job(level, site, null));
        QUEUE.add(new Job(level, null, () -> {
            built.done = true;
            built.queued = false;
            built.setDirty();
        }));
        return true;
    }

    /** The door faces Kanto's centre (the template's door is at z = 0, facing north). */
    private static Rotation facingCentre(Site s) {
        if (s.x() == 0 && s.z() == 0) return Rotation.NONE;
        if (Math.abs(s.z()) >= Math.abs(s.x())) return s.z() < 0 ? Rotation.CLOCKWISE_180 : Rotation.NONE;
        return s.x() > 0 ? Rotation.COUNTERCLOCKWISE_90 : Rotation.CLOCKWISE_90;
    }

    private static float degrees(Rotation r) {
        return switch (r) {
            case CLOCKWISE_90 -> 90F;
            case CLOCKWISE_180 -> 180F;
            case COUNTERCLOCKWISE_90 -> -90F;
            default -> 0F;
        };
    }

    private static boolean soft(BlockState state) {
        return state.isAir() || state.canBeReplaced() || !state.getFluidState().isEmpty() || state.is(BlockTags.LEAVES)
                || state.is(BlockTags.LOGS) || state.is(BlockTags.FLOWERS);
    }

    private static void build(ServerLevel level, Site site) {
        StructureTemplate template = level.getStructureManager().get(site.template()).orElse(null);
        if (template == null) {
            Kanto.LOG.error("Missing template {}", site.template());
            return;
        }
        Rotation rot = facingCentre(site);
        int half = Math.max(site.w(), site.d()) / 2 + 1;
        // the floor sits on the highest ground under the footprint (the foundation fills the rest)
        int y = level.getMinBuildHeight() + 2;
        for (int dx = -half; dx <= half; dx += half) {
            for (int dz = -half; dz <= half; dz += half) {
                int x = site.x() + dx, z = site.z() + dz;
                level.getChunk(x >> 4, z >> 4);
                y = Math.max(y, level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z));
            }
        }
        y = Math.max(y, level.getSeaLevel() + 1);
        StructurePlaceSettings settings = new StructurePlaceSettings().setRotation(rot)
                .setRotationPivot(new BlockPos(site.w() / 2, 0, site.d() / 2));
        BlockPos origin = new BlockPos(site.x() - site.w() / 2, y, site.z() - site.d() / 2);
        // clear the space (trees, hills) and lay the foundation down to the ground
        for (int dx = -half; dx <= half; dx++) {
            for (int dz = -half; dz <= half; dz++) {
                int x = site.x() + dx, z = site.z() + dz;
                for (int yy = y; yy < y + site.h() + 16; yy++) {
                    BlockPos p = new BlockPos(x, yy, z);
                    if (!level.getBlockState(p).isAir()) level.setBlock(p, Blocks.AIR.defaultBlockState(), 2);
                }
                for (int yy = y - 1; yy > Math.max(level.getMinBuildHeight(), y - 64); yy--) {
                    BlockPos p = new BlockPos(x, yy, z);
                    if (!soft(level.getBlockState(p))) break;
                    level.setBlock(p, Kanto.BRICKS_GREY.get().defaultBlockState(), 2);
                }
            }
        }
        template.placeInWorld(level, origin, origin, settings, level.getRandom(), 2);
        for (Trainer t : site.trainers()) {
            for (NPCEntity old : level.getEntitiesOfClass(NPCEntity.class, new net.minecraft.world.phys.AABB(origin).inflate(half * 2 + 4, 20, half * 2 + 4),
                    e -> e.getNpc() != null && t.npc().equals(e.getNpc().getResourceIdentifier()))) {
                old.discard();
            }
        }
        for (Trainer t : site.trainers()) {
            NPCClass npcClass = NPCClasses.getByIdentifier(t.npc());
            if (npcClass == null) {
                Kanto.LOG.error("Missing NPC class {}", t.npc());
                continue;
            }
            BlockPos at = origin.offset(StructureTemplate.calculateRelativePosition(settings, new BlockPos(t.x(), t.y(), t.z())));
            NPCEntity npc = new NPCEntity(level);
            float yaw = t.yaw() + degrees(rot);
            npc.moveTo(at.getX() + 0.5, at.getY(), at.getZ() + 0.5, yaw, 0F);
            npc.setYHeadRot(yaw);
            npc.setYBodyRot(yaw);
            npc.setNpc(npcClass);
            npc.initialize(t.elite() ? 60 : 30);
            npc.setInvulnerable(Boolean.TRUE);
            npc.setPersistenceRequired();
            level.addFreshEntity(npc);
        }
        Kanto.LOG.info("Built {} at {}", site.label(), origin);
    }

    // --- badges and the Elite Four ----------------------------------------------------------------------------------

    private static ResourceLocation classOf(NPCBattleActor actor) {
        NPCEntity entity = actor.getEntity();
        NPCClass c = entity == null ? null : entity.getNpc();
        return c == null ? null : c.getResourceIdentifier();
    }

    private static void eliteGate(com.cobblemon.mod.common.api.events.battles.BattleStartedEvent.Pre event) {
        loadAll();
        Region region = null;
        for (BattleActor a : event.getBattle().getActors()) {
            if (a instanceof NPCBattleActor npc) {
                Role role = ROLES.get(classOf(npc));
                if (role != null && role.badge().isEmpty()) region = role.region();
            }
        }
        if (region == null) return;
        List<String> needed = badgesOf(region);
        for (BattleActor a : event.getBattle().getActors()) {
            if (!(a instanceof PlayerBattleActor p) || p.getEntity() == null) continue;
            List<String> have = progress(p.getEntity().server).badges(p.getEntity());
            int count = (int) needed.stream().filter(have::contains).count();
            if (count < needed.size()) {
                Component why = region == Region.KANTO ? Component.translatable(Kanto.MOD_ID + ".elite.locked", count)
                        : Component.translatable(Kanto.MOD_ID + ".elite.locked.region", nameOf(region), count);
                p.getEntity().sendSystemMessage(why);
                event.setReason(why.copy());
                event.cancel();
                return;
            }
        }
    }

    private static void victory(List<BattleActor> winners, List<BattleActor> losers) {
        loadAll();
        for (BattleActor loser : losers) {
            if (!(loser instanceof NPCBattleActor npc)) continue;
            ResourceLocation id = classOf(npc);
            Role role = ROLES.get(id);
            if (role == null) continue;
            Region region = role.region();
            for (BattleActor w : winners) {
                if (!(w instanceof PlayerBattleActor p) || p.getEntity() == null) continue;
                ServerPlayer player = p.getEntity();
                Progress progress = progress(player.server);
                if (!role.badge().isEmpty()) {
                    List<String> badges = progress.badges(player);
                    if (badges.contains(role.badge())) continue;
                    badges.add(role.badge());
                    progress.save(player, "badges", badges);
                    Item item = BuiltInRegistries.ITEM.get(Kanto.id(role.badge()));
                    give(player, new ItemStack(item));
                    long mine = badgesOf(region).stream().filter(badges::contains).count();
                    player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".badge.earned", item.getDescription(), mine));
                } else {
                    List<String> beaten = progress.list(player, "elite");
                    if (beaten.contains(id.toString())) continue;
                    beaten.add(id.toString());
                    progress.save(player, "elite", beaten);
                    long mine = beaten.stream().map(ResourceLocation::parse).map(ROLES::get)
                            .filter(r -> r != null && r.region() == region).count();
                    player.sendSystemMessage(Component.translatable(Kanto.MOD_ID + ".elite.beaten", npc.getName(), mine));
                    if (mine == 4) {
                        Item ribbon = region == Region.KANTO ? Kanto.RIBBON.get()
                                : BuiltInRegistries.ITEM.get(Kanto.id(region.id + "_champion_ribbon"));
                        give(player, new ItemStack(ribbon));
                        player.sendSystemMessage(region == Region.KANTO ? Component.translatable(Kanto.MOD_ID + ".champion")
                                : Component.translatable(Kanto.MOD_ID + ".champion.region", nameOf(region)));
                    }
                }
            }
        }
    }

    private static void give(ServerPlayer player, ItemStack stack) {
        if (!player.getInventory().add(stack)) player.drop(stack, false);
    }

    // --- saved state ------------------------------------------------------------------------------------------------

    private static Built built(ServerLevel kanto) {
        return kanto.getDataStorage().computeIfAbsent(new SavedData.Factory<>(Built::new, Built::load, null), Kanto.MOD_ID + "_gyms");
    }

    static final class Built extends SavedData {
        boolean done;
        transient boolean queued;

        static Built load(CompoundTag tag, HolderLookup.Provider registries) {
            Built b = new Built();
            b.done = tag.getBoolean("done");
            return b;
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.putBoolean("done", done);
            return tag;
        }
    }

    private static Progress progress(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(Progress::new, Progress::load, null),
                Kanto.MOD_ID + "_progress");
    }

    static final class Progress extends SavedData {
        final CompoundTag players;

        Progress() {
            this(new CompoundTag());
        }

        Progress(CompoundTag players) {
            this.players = players;
        }

        List<String> list(ServerPlayer player, String key) {
            List<String> out = new ArrayList<>();
            ListTag tag = players.getCompound(player.getStringUUID()).getList(key, Tag.TAG_STRING);
            for (int i = 0; i < tag.size(); i++) out.add(tag.getString(i));
            return out;
        }

        List<String> badges(ServerPlayer player) {
            return list(player, "badges");
        }

        void save(ServerPlayer player, String key, List<String> values) {
            CompoundTag mine = players.getCompound(player.getStringUUID());
            ListTag tag = new ListTag();
            for (String v : values) tag.add(StringTag.valueOf(v));
            mine.put(key, tag);
            players.put(player.getStringUUID(), mine);
            setDirty();
        }

        static Progress load(CompoundTag tag, HolderLookup.Provider registries) {
            return new Progress(tag.getCompound("players"));
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("players", players);
            return tag;
        }
    }
}
