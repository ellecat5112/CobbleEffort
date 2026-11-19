package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import dev.architectury.event.EventResult;
import dev.architectury.event.events.common.LifecycleEvent;
import dev.architectury.event.events.common.PlayerEvent;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.entity.projectile.Snowball;
import net.minecraft.world.entity.projectile.SpectralArrow;
import net.minecraft.world.entity.projectile.WitherSkull;
import net.minecraft.world.entity.projectile.windcharge.WindCharge;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.scores.PlayerTeam;
import net.minecraft.world.scores.Scoreboard;
import net.minecraft.world.scores.Team;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Spirit Evolution (Frontier) and Bio-Merge (Tamers). A Human or Beast Spirit (found in elemental temples, or crafted)
 * turns you into its Digimon for its Spirit Gauge (60 s Human, 40 s Beast): you look the part (a costume Digimon moves
 * with you while you're invisible), your hotbar becomes the spirit's attack, a dash and a revert, and you get the
 * element's gifts (flight for Wind and Light, fire resistance for Flame, regeneration for Wood...; Beast Spirits hit
 * harder). Your hotbar comes back afterwards (saved, so even a crash or a logout returns it), and the spirit rests for
 * five minutes.
 * Bio-Merge: sneak and use the Digivice on your own sent-out Digimon at maximum friendship: you fuse into its Mega
 * (the furthest digivolution open to it) for 90 seconds (50 Tamer Energy): you keep your armor, fly, and attack with its
 * element.
 */
public final class SpiritEvolution {
    public static final List<String> ELEMENTS = List.of("flame", "light", "ice", "wind", "thunder", "darkness", "earth", "wood", "water", "steel");
    static final Map<String, String[]> SPIRITS = Map.of(
            "flame", new String[]{"agnimon", "vritramon"}, "light", new String[]{"wolfmon", "garummon"},
            "ice", new String[]{"chackmon", "blizzarmon"}, "wind", new String[]{"fairimon", "shutumon"},
            "thunder", new String[]{"blitzmon", "bolgmon"}, "darkness", new String[]{"duskmon", "velgrmon"},
            "earth", new String[]{"grottomon", "gigasmon"}, "wood", new String[]{"arbormon", "petaldramon"},
            "water", new String[]{"ranamon", "calamaramon"}, "steel", new String[]{"mercurymon", "sephirothmon"});
    static final String MARK = "cobbleeffort_spirit", COSTUME = "cobbleeffort_digital_costume", TEAM = "ce_digital_costume";
    public static final String COSTUME_ASPECT = "cobbleeffort_costume";
    static final int HUMAN_TICKS = 1200, BEAST_TICKS = 800, MERGE_TICKS = 1800, REST_TICKS = 6000, MERGE_ENERGY = 50;

    record State(String species, String element, String kind, long until, UUID costume, boolean flight) {
    }

    private static final Map<UUID, State> ACTIVE = new HashMap<>();

    private SpiritEvolution() {
    }

    // --- items -----------------------------------------------------------------------------------------------------

    /** A Human or Beast Spirit: use it to Spirit Evolve. */
    public static class SpiritItem extends Item {
        final String element;
        final boolean beast;

        public SpiritItem(Properties properties, String element, boolean beast) {
            super(properties);
            this.element = element;
            this.beast = beast;
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (level.isClientSide || !(player instanceof ServerPlayer sp)) return InteractionResultHolder.success(stack);
            String species = SPIRITS.get(element)[beast ? 1 : 0];
            if (transform(sp, species, element, beast ? "beast" : "human", beast ? BEAST_TICKS : HUMAN_TICKS)) {
                player.getCooldowns().addCooldown(this, (beast ? BEAST_TICKS : HUMAN_TICKS) + REST_TICKS);
                return InteractionResultHolder.consume(stack);
            }
            return InteractionResultHolder.fail(stack);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable(Digital.MOD_ID + ".spirit.becomes", name(SPIRITS.get(element)[beast ? 1 : 0])).withStyle(ChatFormatting.AQUA));
            lines.add(Component.translatable(Digital.MOD_ID + ".spirit.gift." + element).withStyle(ChatFormatting.GRAY));
        }
    }

    /** The spirit's own hotbar: its attack, a dash, the revert. They vanish when the spirit leaves. */
    public static class SpiritAttack extends Item {
        public SpiritAttack(Properties properties) {
            super(properties);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (level.isClientSide || !(player instanceof ServerPlayer sp)) return InteractionResultHolder.success(stack);
            CustomData d = stack.get(DataComponents.CUSTOM_DATA);
            String action = d == null ? "" : d.copyTag().getString("action");
            State st = ACTIVE.get(sp.getUUID());
            if (st == null) {
                stack.setCount(0);
                return InteractionResultHolder.fail(stack);
            }
            switch (action) {
                case "revert" -> revert(sp, true);
                case "dash" -> {
                    sp.setDeltaMovement(sp.getLookAngle().scale(st.kind().equals("human") ? 1.6 : 1.2).add(0, 0.25, 0));
                    sp.hurtMarked = true;
                    sp.serverLevel().sendParticles(ParticleTypes.CLOUD, sp.getX(), sp.getY() + 0.5, sp.getZ(), 12, 0.3, 0.3, 0.3, 0.05);
                    sp.getCooldowns().addCooldown(this, 30);
                }
                default -> {
                    attack(sp, st.element(), !st.kind().equals("human"));
                    sp.getCooldowns().addCooldown(this, 20);
                }
            }
            return InteractionResultHolder.consume(stack);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable(Digital.MOD_ID + ".spirit.attack_tooltip").withStyle(ChatFormatting.GRAY));
        }
    }

    static Component name(String species) {
        Species s = PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", species));
        return s == null ? Component.literal(species) : s.getTranslatedName();
    }

    static boolean active(Player p) {
        return ACTIVE.containsKey(p.getUUID());
    }

    // --- transforming ------------------------------------------------------------------------------------------------

    static boolean transform(ServerPlayer p, String species, String element, String kind, int ticks) {
        String m = Digital.MOD_ID + ".spirit.";
        if (ACTIVE.containsKey(p.getUUID())) {
            p.displayClientMessage(Component.translatable(m + "already"), true);
            return false;
        }
        if (BattleRegistry.getBattleByParticipatingPlayer(p) != null) {
            p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".use.in_battle"), true);
            return false;
        }
        Species sp = PokemonSpecies.INSTANCE.getByIdentifier(ResourceLocation.fromNamespaceAndPath("cobbleeffort", species));
        if (sp == null) return false;
        // the hotbar, saved first (and in the world's data, so nothing is lost to a crash)
        NonNullList<ItemStack> hotbar = NonNullList.withSize(9, ItemStack.EMPTY);
        for (int i = 0; i < 9; i++) {
            hotbar.set(i, p.getInventory().items.get(i).copy());
            p.getInventory().items.set(i, ItemStack.EMPTY);
        }
        CompoundTag saved = new CompoundTag();
        ContainerHelper.saveAllItems(saved, hotbar, p.registryAccess());
        Saved data = saved(p.server);
        data.hotbars.put(p.getStringUUID(), saved);
        data.setDirty();
        p.getInventory().items.set(0, attackItem("attack", element));
        p.getInventory().items.set(1, attackItem("dash", element));
        p.getInventory().items.set(8, attackItem("revert", element));
        p.getInventory().selected = 0;
        // the look
        ServerLevel level = p.serverLevel();
        Pokemon pk = PokemonProperties.Companion.parse("cobbleeffort:" + species + " uncatchable").create();
        float height = sp.getStandardForm().getHitbox().height() * sp.getStandardForm().getBaseScale();
        pk.setScaleModifier(Math.max(0.05F, (kind.equals("merge") ? 2.6F : 2.2F) / Math.max(0.1F, height)));
        pk.getPersistentData().putBoolean(COSTUME, true);
        java.util.Set<String> forced = new java.util.HashSet<>(pk.getForcedAspects());
        forced.add(COSTUME_ASPECT);
        pk.setForcedAspects(forced);
        pk.updateAspects();
        PokemonEntity e = new PokemonEntity(level, pk, CobblemonEntities.POKEMON);
        net.minecraft.world.entity.Mob mob = e;
        mob.moveTo(p.getX(), p.getY(), p.getZ(), p.getYRot(), 0F);
        mob.setNoAi(true);
        mob.setInvulnerable(true);
        mob.setSilent(true);
        mob.addTag(COSTUME);
        mob.setPersistenceRequired();                              // never despawned mid-spirit
        ACTIVE.put(p.getUUID(), new State(species, element, kind, level.getGameTime() + ticks, e.getUUID(), false));   // before the add: EntityEvent.ADD checks it
        level.addFreshEntity(mob);
        p.server.getScoreboard().addPlayerToTeam(e.getStringUUID(), team(p.server));
        // the gifts
        boolean flight = kind.equals("merge") || element.equals("wind") || element.equals("light");
        effect(p, MobEffects.INVISIBILITY, ticks, 0);
        gifts(p, element, kind, ticks);
        if (flight && !p.getAbilities().mayfly) {
            p.getAbilities().mayfly = true;
            p.onUpdateAbilities();
        }
        ACTIVE.put(p.getUUID(), new State(species, element, kind, level.getGameTime() + ticks, e.getUUID(), flight));
        level.playSound(null, p.blockPosition(), SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 1F, kind.equals("beast") ? 0.8F : 1.4F);
        level.sendParticles(DigitalWorld.CYAN, p.getX(), p.getY() + 1, p.getZ(), 120, 0.6, 1.2, 0.6, 0.05);
        p.sendSystemMessage(Component.translatable(m + (kind.equals("merge") ? "merged" : "evolved"), p.getDisplayName(), name(species))
                .withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        return true;
    }

    static ItemStack attackItem(String action, String element) {
        ItemStack s = new ItemStack(Digital.SPIRIT_ATTACK.get());
        CustomData.update(DataComponents.CUSTOM_DATA, s, t -> {
            t.putString("action", action);
            t.putBoolean(MARK, true);
        });
        s.set(DataComponents.ITEM_NAME, Component.translatable(Digital.MOD_ID + ".spirit." + action + (action.equals("attack") ? "." + element : "")));
        return s;
    }

    static void effect(ServerPlayer p, net.minecraft.core.Holder<MobEffect> eff, int ticks, int amp) {
        p.addEffect(new MobEffectInstance(eff, ticks, amp, false, false, true));
    }

    static void gifts(ServerPlayer p, String element, String kind, int t) {
        switch (element) {
            case "flame" -> effect(p, MobEffects.FIRE_RESISTANCE, t, 0);
            case "ice" -> effect(p, MobEffects.DAMAGE_RESISTANCE, t, 0);
            case "thunder" -> effect(p, MobEffects.MOVEMENT_SPEED, t, 1);
            case "darkness" -> effect(p, MobEffects.NIGHT_VISION, t, 0);
            case "earth" -> effect(p, MobEffects.DIG_SPEED, t, 1);
            case "wood" -> effect(p, MobEffects.REGENERATION, t, 0);
            case "water" -> {
                effect(p, MobEffects.WATER_BREATHING, t, 0);
                effect(p, MobEffects.DOLPHINS_GRACE, t, 0);
            }
            case "steel" -> effect(p, MobEffects.DAMAGE_RESISTANCE, t, 1);
            default -> { }
        }
        if (kind.equals("human")) {
            effect(p, MobEffects.MOVEMENT_SPEED, t, 0);
            effect(p, MobEffects.JUMP, t, 1);
        } else {
            effect(p, MobEffects.DAMAGE_BOOST, t, 1);
            effect(p, MobEffects.ABSORPTION, t, kind.equals("merge") ? 4 : 2);
            if (kind.equals("merge")) effect(p, MobEffects.DAMAGE_RESISTANCE, t, 1);
        }
    }

    static void revert(ServerPlayer p, boolean early) {
        State st = ACTIVE.remove(p.getUUID());
        if (st == null) return;
        ServerLevel level = p.serverLevel();
        for (ServerLevel l : p.server.getAllLevels()) {
            if (l.getEntity(st.costume()) != null) l.getEntity(st.costume()).discard();
        }
        restoreHotbar(p);
        for (var eff : List.of(MobEffects.INVISIBILITY, MobEffects.FIRE_RESISTANCE, MobEffects.DAMAGE_RESISTANCE, MobEffects.MOVEMENT_SPEED,
                MobEffects.NIGHT_VISION, MobEffects.DIG_SPEED, MobEffects.REGENERATION, MobEffects.WATER_BREATHING, MobEffects.DOLPHINS_GRACE,
                MobEffects.JUMP, MobEffects.DAMAGE_BOOST, MobEffects.ABSORPTION)) {
            MobEffectInstance i = p.getEffect(eff);
            if (i != null && !i.isVisible()) p.removeEffect(eff);
        }
        if (st.flight() && !p.isCreative() && !p.isSpectator()) {
            p.getAbilities().mayfly = false;
            p.getAbilities().flying = false;
            p.onUpdateAbilities();
            effect(p, MobEffects.SLOW_FALLING, 100, 0);
        }
        level.sendParticles(DigitalWorld.CYAN, p.getX(), p.getY() + 1, p.getZ(), 60, 0.5, 1, 0.5, 0.05);
        level.playSound(null, p.blockPosition(), SoundEvents.BEACON_DEACTIVATE, SoundSource.PLAYERS, 1F, 1.2F);
        p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".spirit.ended").withStyle(ChatFormatting.AQUA), true);
    }

    /** Takes the spirit's items away and puts the saved hotbar back (into free slots, else the inventory, else the floor). */
    static void restoreHotbar(ServerPlayer p) {
        restoreHotbar(p, false);
    }

    static void restoreHotbar(ServerPlayer p, boolean dying) {
        for (int i = 0; i < p.getInventory().getContainerSize(); i++) {
            ItemStack s = p.getInventory().getItem(i);
            if (s.is(Digital.SPIRIT_ATTACK.get())) p.getInventory().setItem(i, ItemStack.EMPTY);
        }
        if (!p.isAlive() && !dying) return;                          // dead: the saved hotbar waits for the respawn
        Saved data = saved(p.server);
        CompoundTag t = data.hotbars.getCompound(p.getStringUUID());
        if (t.isEmpty()) return;
        NonNullList<ItemStack> hotbar = NonNullList.withSize(9, ItemStack.EMPTY);
        ContainerHelper.loadAllItems(t, hotbar, p.registryAccess());
        for (int i = 0; i < 9; i++) {
            ItemStack s = hotbar.get(i);
            if (s.isEmpty()) continue;
            if (p.getInventory().items.get(i).isEmpty()) p.getInventory().items.set(i, s);
            else if (!p.getInventory().add(s)) p.drop(s, false);
        }
        data.hotbars.remove(p.getStringUUID());
        data.setDirty();
    }

    // --- attacks -----------------------------------------------------------------------------------------------------

    static void attack(ServerPlayer p, String element, boolean strong) {
        ServerLevel level = p.serverLevel();
        Vec3 eye = p.getEyePosition(), look = p.getLookAngle();
        float dmg = strong ? 8F : 5F;
        boolean griefing = level.getGameRules().getBoolean(MoveEffects.GRIEFING);
        switch (element) {
            case "flame" -> {
                if (griefing) {                                    // real fireballs light blocks: only with the gamerule
                    for (int i = -1; i <= 1; i++) {
                        SmallFireball f = new SmallFireball(level, p, look.yRot(i * 0.12F));
                        f.setPos(eye.add(look));
                        level.addFreshEntity(f);
                    }
                } else {
                    beam(level, eye, look, 10, ParticleTypes.FLAME);
                    cone(p, 10, e -> {
                        e.igniteForSeconds(4);
                        e.hurt(level.damageSources().playerAttack(p), dmg);
                    });
                }
            }
            case "light" -> {
                for (int i = -1; i <= 1; i++) {
                    SpectralArrow a = new SpectralArrow(level, p, new ItemStack(net.minecraft.world.item.Items.SPECTRAL_ARROW), null);
                    a.shootFromRotation(p, p.getXRot(), p.getYRot() + i * 6, 0, 3F, 0.5F);
                    a.pickup = AbstractArrow.Pickup.DISALLOWED;
                    a.setBaseDamage(dmg / 2.5);
                    level.addFreshEntity(a);
                }
            }
            case "ice" -> {
                for (int i = 0; i < 6; i++) {
                    Snowball s = new Snowball(level, p);
                    s.shootFromRotation(p, p.getXRot(), p.getYRot(), 0, 1.8F, 6F);
                    level.addFreshEntity(s);
                }
                cone(p, 10, e -> {
                    e.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 2));
                    e.setTicksFrozen(Math.max(e.getTicksFrozen(), 200));
                    e.hurt(level.damageSources().freeze(), dmg * 0.6F);
                });
            }
            case "wind" -> {
                WindCharge w = new WindCharge(p, level, eye.x, eye.y, eye.z);
                w.shootFromRotation(p, p.getXRot(), p.getYRot(), 0, 1.6F, 0);
                level.addFreshEntity(w);
            }
            case "thunder" -> {
                HitResult hit = level.clip(new ClipContext(eye, eye.add(look.scale(32)), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
                LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(level);
                if (bolt != null) {
                    bolt.moveTo(hit.getLocation());
                    bolt.setVisualOnly(true);                      // our own damage below; a real bolt could hit the player
                    level.addFreshEntity(bolt);
                    for (LivingEntity e : level.getEntitiesOfClass(LivingEntity.class, new AABB(BlockPos.containing(hit.getLocation())).inflate(3), x -> x != p)) {
                        e.hurt(level.damageSources().lightningBolt(), dmg);
                    }
                }
            }
            case "darkness" -> {
                if (griefing) {                                    // wither skulls blow holes: only with the gamerule
                    WitherSkull s = new WitherSkull(level, p, look);
                    s.setPos(eye.add(look));
                    level.addFreshEntity(s);
                } else {
                    beam(level, eye, look, 10, ParticleTypes.SQUID_INK);
                    cone(p, 10, e -> {
                        e.addEffect(new MobEffectInstance(MobEffects.WITHER, 100, 1));
                        e.hurt(level.damageSources().playerAttack(p), dmg * 0.7F);
                    });
                }
            }
            case "earth" -> cone(p, 8, e -> {
                e.setDeltaMovement(e.getDeltaMovement().add(0, 0.9, 0));
                e.hurtMarked = true;
                e.hurt(level.damageSources().playerAttack(p), dmg);
            });
            case "wood" -> cone(p, 9, e -> {
                e.addEffect(new MobEffectInstance(MobEffects.POISON, 120, 1));
                e.hurt(level.damageSources().playerAttack(p), dmg * 0.5F);
            });
            case "water" -> {
                level.sendParticles(ParticleTypes.SPLASH, eye.x + look.x * 3, eye.y, eye.z + look.z * 3, 120, 1.5, 0.6, 1.5, 0.3);
                cone(p, 10, e -> {
                    e.setDeltaMovement(e.getDeltaMovement().add(look.scale(1.4)).add(0, 0.3, 0));
                    e.hurtMarked = true;
                    e.clearFire();
                    e.hurt(level.damageSources().playerAttack(p), dmg * 0.7F);
                });
            }
            default -> {                                           // steel: a volley of metal shards
                for (int i = -2; i <= 2; i++) {
                    net.minecraft.world.entity.projectile.Arrow a = new net.minecraft.world.entity.projectile.Arrow(level, p,
                            new ItemStack(net.minecraft.world.item.Items.ARROW), null);
                    a.shootFromRotation(p, p.getXRot(), p.getYRot() + i * 4, 0, 3.2F, 0.3F);
                    a.pickup = AbstractArrow.Pickup.DISALLOWED;
                    a.setBaseDamage(dmg / 2.5);
                    level.addFreshEntity(a);
                }
            }
        }
        level.playSound(null, p.blockPosition(), SoundEvents.EVOKER_CAST_SPELL, SoundSource.PLAYERS, 0.7F, strong ? 0.8F : 1.3F);
    }

    static void beam(ServerLevel level, Vec3 from, Vec3 dir, double reach, net.minecraft.core.particles.SimpleParticleType type) {
        for (double d = 1; d <= reach; d += 0.5) {
            Vec3 at = from.add(dir.scale(d));
            level.sendParticles(type, at.x, at.y, at.z, 3, 0.15 * d / 3, 0.15 * d / 3, 0.15 * d / 3, 0.01);
        }
    }

    /** Living things in front of the player (a 35° cone, up to `reach` blocks). */
    static void cone(ServerPlayer p, double reach, java.util.function.Consumer<LivingEntity> hit) {
        Vec3 eye = p.getEyePosition(), look = p.getLookAngle();
        for (LivingEntity e : p.serverLevel().getEntitiesOfClass(LivingEntity.class, p.getBoundingBox().inflate(reach), x -> x != p && x.isAlive())) {
            if (e instanceof PokemonEntity pe && pe.getTags().contains(COSTUME)) continue;
            Vec3 to = e.position().add(0, e.getBbHeight() / 2, 0).subtract(eye);
            if (to.length() <= reach && to.normalize().dot(look) > Math.cos(Math.toRadians(35))) hit.accept(e);
        }
    }

    // --- Bio-Merge ---------------------------------------------------------------------------------------------------

    static String element(ElementalType t) {
        var T = ElementalTypes.INSTANCE;
        if (t == T.getFIRE()) return "flame";
        if (t == T.getWATER()) return "water";
        if (t == T.getICE()) return "ice";
        if (t == T.getELECTRIC()) return "thunder";
        if (t == T.getGRASS() || t == T.getBUG()) return "wood";
        if (t == T.getGROUND() || t == T.getROCK() || t == T.getFIGHTING()) return "earth";
        if (t == T.getSTEEL()) return "steel";
        if (t == T.getFLYING() || t == T.getDRAGON()) return "wind";
        if (t == T.getDARK() || t == T.getGHOST() || t == T.getPOISON()) return "darkness";
        return "light";
    }

    /** Sneak + Digivice on your own sent-out Digimon at full friendship: Bio-Merge into its Mega. */
    static boolean bioMerge(ServerPlayer p, PokemonEntity entity, ItemStack digivice) {
        Pokemon pk = entity.getPokemon();
        String m = Digital.MOD_ID + ".spirit.";
        if (!Attributes.isDigimon(pk) || !p.getUUID().equals(pk.getOwnerUUID())) return false;
        if (pk.getFriendship() < 255) {
            p.displayClientMessage(Component.translatable(m + "bond", pk.getDisplayName(false), pk.getFriendship()), true);
            return true;
        }
        if (Digivice.energy(digivice) < MERGE_ENERGY) {
            p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digivice.low_energy", Digivice.energy(digivice), MERGE_ENERGY), true);
            return true;
        }
        Species mega = pk.getSpecies(), step = Digivice.openEvolution(pk, mega);
        int guard = 0;
        while (step != null && guard++ < 6) {
            mega = step;
            if (Digivice.stageIndex(mega) >= 5) break;
            step = Digivice.openEvolution(pk, mega);
        }
        String element = element(pk.getPrimaryType());
        if (transform(p, mega.getResourceIdentifier().getPath(), element, "merge", MERGE_TICKS)) {
            if (!p.getAbilities().instabuild) Digivice.setEnergy(digivice, Digivice.energy(digivice) - MERGE_ENERGY);
            entity.recallWithAnimation();
        }
        return true;
    }

    // --- the tick and the safety nets ------------------------------------------------------------------------------------

    static PlayerTeam team(MinecraftServer server) {
        Scoreboard sb = server.getScoreboard();
        PlayerTeam t = sb.getPlayerTeam(TEAM);
        if (t == null) {
            t = sb.addPlayerTeam(TEAM);
            t.setCollisionRule(Team.CollisionRule.NEVER);
            t.setNameTagVisibility(Team.Visibility.NEVER);
        }
        return t;
    }

    static void init() {
        TickEvent.PLAYER_POST.register(player -> {
            if (!(player instanceof ServerPlayer p)) return;
            State st = ACTIVE.get(p.getUUID());
            if (st == null) return;
            ServerLevel level = p.serverLevel();
            if (!p.isAlive() || level.getGameTime() >= st.until() || level.getEntity(st.costume()) == null) {
                revert(p, false);
                return;
            }
            if (level.getEntity(st.costume()) instanceof PokemonEntity e) {
                e.moveTo(p.getX(), p.getY(), p.getZ(), p.getYRot(), p.getXRot());
                e.setYHeadRot(p.getYHeadRot());
                e.setYBodyRot(p.yBodyRot);
                e.setDeltaMovement(p.getDeltaMovement());
            }
            long left = st.until() - level.getGameTime();
            if (left % 10 == 0) {
                int bars = (int) Math.ceil(20.0 * left / (st.kind().equals("merge") ? MERGE_TICKS : st.kind().equals("beast") ? BEAST_TICKS : HUMAN_TICKS));
                p.displayClientMessage(Component.translatable(Digital.MOD_ID + ".spirit.gauge", name(st.species()),
                        Component.literal("|".repeat(Math.max(0, bars))).withStyle(ChatFormatting.AQUA),
                        Component.literal("|".repeat(Math.max(0, 20 - bars))).withStyle(ChatFormatting.DARK_GRAY), left / 20), true);
            }
        });
        TickEvent.SERVER_POST.register(server -> {
            if (server.getTickCount() % 100 != 0) return;
            List<PokemonEntity> orphans = new java.util.ArrayList<>();
            for (ServerLevel l : server.getAllLevels()) {
                for (net.minecraft.world.entity.Entity en : l.getAllEntities()) {
                    if (en instanceof PokemonEntity e && e.getTags().contains(COSTUME)
                            && ACTIVE.values().stream().noneMatch(st -> st.costume().equals(e.getUUID()))) {
                        orphans.add(e);
                    }
                }
            }
            orphans.forEach(PokemonEntity::discard);                   // after the walk: no removal mid-iteration
        });
        PlayerEvent.PLAYER_QUIT.register(p -> revert(p, false));
        // dying mid-spirit: back to normal before the death drops (so the hotbar drops or is kept like everything else)
        dev.architectury.event.events.common.EntityEvent.LIVING_DEATH.register((entity, source) -> {
            if (entity instanceof ServerPlayer p && ACTIVE.containsKey(p.getUUID())) {
                State st = ACTIVE.get(p.getUUID());
                restoreHotbar(p, true);
                revert(p, false);
                if (st != null) Digital.LOG.debug("{} died as {}", p.getName().getString(), st.species());
            }
            return EventResult.pass();
        });
        PlayerEvent.PLAYER_RESPAWN.register((p, end, reason) -> restoreHotbar(p));
        PlayerEvent.CHANGE_DIMENSION.register((p, from, to) -> revert(p, false));
        PlayerEvent.PLAYER_JOIN.register(p -> {
            if (!ACTIVE.containsKey(p.getUUID())) restoreHotbar(p);   // a crash or a logout mid-spirit: the hotbar comes back
        });
        PlayerEvent.DROP_ITEM.register((player, entity) -> {
            if (entity.getItem().is(Digital.SPIRIT_ATTACK.get())) {
                entity.discard();
                return EventResult.interruptFalse();
            }
            return EventResult.pass();
        });
        LifecycleEvent.SERVER_STOPPING.register(server -> {
            for (ServerPlayer p : server.getPlayerList().getPlayers()) revert(p, false);
            ACTIVE.clear();
        });
        // costumes are never battled, and leftovers (a crash) vanish when their chunk loads
        CobblemonEvents.BATTLE_STARTED_PRE.subscribe(Priority.HIGHEST, event -> {
            for (BattleActor a : event.getBattle().getActors()) {
                for (BattlePokemon bp : a.getPokemonList()) {
                    if (bp.getOriginalPokemon().getPersistentData().getBoolean(COSTUME)) {
                        event.cancel();
                        return;
                    }
                }
            }
        });
        dev.architectury.event.events.common.EntityEvent.ADD.register((entity, level) -> {
            if (entity instanceof net.minecraft.world.entity.item.ItemEntity it && it.getItem().is(Digital.SPIRIT_ATTACK.get())) {
                return EventResult.interruptFalse();
            }
            if (entity instanceof PokemonEntity e && e.getTags().contains(COSTUME)) {
                boolean owned = ACTIVE.values().stream().anyMatch(s -> s.costume().equals(e.getUUID()));
                if (!owned) return EventResult.interruptFalse();
            }
            return EventResult.pass();
        });
    }

    // --- saved hotbars ---------------------------------------------------------------------------------------------------

    static Saved saved(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(new SavedData.Factory<>(Saved::new, Saved::load, null), Digital.MOD_ID + "_spirits");
    }

    static final class Saved extends SavedData {
        final CompoundTag hotbars;

        Saved() {
            this(new CompoundTag());
        }

        Saved(CompoundTag hotbars) {
            this.hotbars = hotbars;
        }

        static Saved load(CompoundTag tag, HolderLookup.Provider registries) {
            return new Saved(tag.getCompound("hotbars"));
        }

        @Override
        public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
            tag.put("hotbars", hotbars);
            return tag;
        }
    }
}
