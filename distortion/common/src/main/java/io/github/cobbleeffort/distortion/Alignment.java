package io.github.cobbleeffort.distortion;

import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.api.moves.Move;
import com.cobblemon.mod.common.api.moves.MoveSet;
import com.cobblemon.mod.common.api.moves.MoveTemplate;
import com.cobblemon.mod.common.api.moves.Moves;
import com.cobblemon.mod.common.api.pokemon.feature.FlagSpeciesFeature;
import com.cobblemon.mod.common.api.pokemon.feature.SpeciesFeature;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import org.jetbrains.annotations.Nullable;

import java.util.Iterator;
import java.util.List;
import java.util.Set;

/**
 * The Shadow and Crystal types: every Pokémon has a Shadow and a Crystal counterpart (the flags shadow_pokemon and
 * crystal_pokemon, global species features, so any species can carry them; they're also its aspects, so the client
 * knows to recolour it). A counterpart's types are [its first type, Shadow|Crystal], outside battle (AlignTypesMixin)
 * and in it (AlignmentEngine). Turning into one swaps in the counterpart's own moves (the originals are kept in the
 * Pokémon's persistent data); the DNA Purifier turns it back and returns them.
 *
 * Shadow (Pokémon XD): Shadow moves, 2x on every non-Shadow Pokémon. Crystal (the Crystal Onix): a glassy body that
 * refracts special attacks. Made with the Shadow Heart and the Prism Crystal; rarely met in the wild (Shadow at night,
 * Crystal deep underground).
 */
public final class Alignment {
    public static final String SHADOW_FLAG = "shadow_pokemon";
    public static final String CRYSTAL_FLAG = "crystal_pokemon";
    private static final String KEY = "cobbleeffort_alignment";
    /** One wild spawn in this many becomes a Shadow (at night) or Crystal (underground) Pokémon. */

    public static final ElementalType SHADOW = ElementalTypes.register("Shadow", Component.translatable("cobblemon.type.shadow"),
            0x8A4FC0, 18, 0x3A1E54, 0x9646C8, 18);
    public static final ElementalType CRYSTAL = ElementalTypes.register("Crystal", Component.translatable("cobblemon.type.crystal"),
            0x9EEAF2, 19, 0x3C96BE, 0xC8F5FA, 19);

    private Alignment() {
    }

    public static void init() {
        // touching the fields registers both types (common init, so the server and the client both know them)
        Distortion.LOG.info("Registered the {} and {} types", SHADOW.getName(), CRYSTAL.getName());
        CobblemonEvents.POKEMON_ENTITY_SPAWN.subscribe(Priority.NORMAL, event -> {
            try {
                if (!(event.getEntity() instanceof PokemonEntity entity)) return kotlin.Unit.INSTANCE;
                Pokemon p = entity.getPokemon();
                if (p.isPlayerOwned() || of(p) != null) return kotlin.Unit.INSTANCE;
                var pos = event.getSpawnablePosition();
                var random = pos.getWorld().getRandom();
                var rules = pos.getWorld().getGameRules();                     // 1 in N (game rules; 0 = never)
                int shadow = rules.getInt(DistortionGameRules.SHADOW_CHANCE), crystal = rules.getInt(DistortionGameRules.CRYSTAL_CHANCE);
                if (pos.getWorld().isNight() && pos.getCanSeeSky() && shadow > 0 && random.nextInt(shadow) == 0) {
                    convert(p, SHADOW_FLAG);
                } else if (!pos.getCanSeeSky() && pos.getPosition().getY() < 40 && crystal > 0 && random.nextInt(crystal) == 0) {
                    convert(p, CRYSTAL_FLAG);
                }
            } catch (Throwable t) {
                Distortion.LOG.error("Couldn't make a wild Shadow/Crystal Pokémon", t);
            }
            return kotlin.Unit.INSTANCE;
        });
    }

    private static boolean flag(Pokemon pokemon, String key) {
        try {
            SpeciesFeature f = pokemon.getFeature(key);
            if (f instanceof FlagSpeciesFeature flag) return flag.getEnabled();
            Set<String> aspects = pokemon.getAspects();
            return aspects != null && aspects.contains(key);
        } catch (Throwable t) {
            return false;                    // a Pokémon still being built
        }
    }

    /** SHADOW_FLAG, CRYSTAL_FLAG or null. */
    @Nullable
    public static String of(Pokemon pokemon) {
        if (pokemon == null) return null;
        if (flag(pokemon, SHADOW_FLAG)) return SHADOW_FLAG;
        if (flag(pokemon, CRYSTAL_FLAG)) return CRYSTAL_FLAG;
        return null;
    }

    public static ElementalType typeOf(String flag) {
        return SHADOW_FLAG.equals(flag) ? SHADOW : CRYSTAL;
    }

    /** A counterpart's types from the types it would have: [its first type, Shadow|Crystal]. */
    @Nullable
    public static List<ElementalType> types(Pokemon pokemon, Iterable<ElementalType> plain) {
        String a = of(pokemon);
        if (a == null || plain == null) return null;
        ElementalType first = null;
        for (Iterator<ElementalType> it = plain.iterator(); it.hasNext(); ) {
            ElementalType t = it.next();
            if (t != SHADOW && t != CRYSTAL) {
                first = t;
                break;
            }
        }
        if (first == null) first = ElementalTypes.NORMAL;
        return List.of(first, typeOf(a));
    }

    // --- the counterpart's moves ---------------------------------------------------------------------------------------
    /** The moves a counterpart gets in its first slots: chosen by its stronger attacking stat, first type and level. */
    static List<String> moves(Pokemon p, String flag) {
        boolean physical = p.getForm().getBaseStats().getOrDefault(Stats.ATTACK, 0)
                >= p.getForm().getBaseStats().getOrDefault(Stats.SPECIAL_ATTACK, 0);
        int level = p.getLevel();
        String type = p.getForm().getPrimaryType().getName().toLowerCase();
        if (SHADOW_FLAG.equals(flag)) {
            String first = level < 20 ? (physical ? "shadowblitz" : "shadowwave") : (physical ? "shadowrush" : "shadowblast");
            String second = switch (type) {
                case "fire" -> "shadowfire";
                case "electric" -> "shadowbolt";
                case "ice", "water" -> "shadowchill";
                default -> physical ? (level >= 40 ? "shadowend" : "shadowbreak") : (level >= 40 ? "shadowstorm" : "shadowrave");
            };
            String[] status = {"shadowhold", "shadowmist", "shadowdown", "shadowpanic", "shadowshed", "shadowhalf"};
            String third = status[Math.floorMod(p.getUuid().hashCode(), status.length)];
            return List.of(first, second, third);
        }
        String attack = physical ? (level >= 40 ? "crystalcrash" : "shardvolley") : "prismbeam";
        boolean specialWall = p.getForm().getBaseStats().getOrDefault(Stats.SPECIAL_DEFENCE, 0)
                > p.getForm().getBaseStats().getOrDefault(Stats.DEFENCE, 0);
        return List.of(attack, specialWall ? "refraction" : "glassguard");
    }

    /** Turn a Pokémon into its Shadow or Crystal counterpart (false when it already is one). */
    public static boolean convert(Pokemon pokemon, String flag) {
        if (of(pokemon) != null) return false;
        CompoundTag data = pokemon.getPersistentData();
        ListTag originals = new ListTag(), given = new ListTag();
        MoveSet set = pokemon.getMoveSet();
        List<String> ids = moves(pokemon, flag);
        for (int i = 0; i < ids.size(); i++) {
            MoveTemplate t = Moves.getByName(ids.get(i));
            Move old = set.get(i);
            originals.add(StringTag.valueOf(old == null ? "" : old.getName()));
            if (t == null) {
                given.add(StringTag.valueOf(""));
                continue;
            }
            set.setMove(i, t.create());
            given.add(StringTag.valueOf(t.getName()));
        }
        CompoundTag saved = new CompoundTag();
        saved.put("moves", originals);
        saved.put("given", given);
        saved.putString("flag", flag);
        data.put(KEY, saved);
        new FlagSpeciesFeature(flag, true).apply(pokemon);
        pokemon.updateAspects();
        return true;
    }

    /** Back to normal (the DNA Purifier): the flag goes and its own moves return. False when it wasn't a counterpart. */
    public static boolean restore(Pokemon pokemon) {
        String flag = of(pokemon);
        if (flag == null) return false;
        new FlagSpeciesFeature(flag, false).apply(pokemon);
        CompoundTag data = pokemon.getPersistentData();
        if (data.contains(KEY)) {
            CompoundTag saved = data.getCompound(KEY);
            ListTag originals = saved.getList("moves", Tag.TAG_STRING), given = saved.getList("given", Tag.TAG_STRING);
            MoveSet set = pokemon.getMoveSet();
            for (int i = 0; i < Math.min(4, originals.size()); i++) {
                Move now = set.get(i);
                if (now == null || !now.getName().equals(given.getString(i))) continue;   // changed since: keep
                String orig = originals.getString(i);
                MoveTemplate t = orig.isEmpty() ? null : Moves.getByName(orig.toLowerCase().replaceAll("[^a-z0-9]", ""));
                set.setMove(i, t == null ? null : t.create());
            }
            data.remove(KEY);
        }
        pokemon.updateAspects();
        return true;
    }

    // --- the items --------------------------------------------------------------------------------------------------
    /** Shadow Heart / Prism Crystal: used on one of your Pokémon that's out of its ball, it becomes that counterpart. */
    public static final class ConvertItem extends Item {
        private final String flag;

        public ConvertItem(Properties properties, String flag) {
            super(properties);
            this.flag = flag;
        }

        @Override
        public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
            if (!(target instanceof PokemonEntity entity)) return InteractionResult.PASS;
            if (player.level().isClientSide) return InteractionResult.SUCCESS;
            String m = Distortion.MOD_ID + ".align.";
            Pokemon p = entity.getPokemon();
            if (!(player instanceof ServerPlayer sp) || !player.getUUID().equals(p.getOwnerUUID())) {
                player.displayClientMessage(Component.translatable(m + "not_yours"), true);
                return InteractionResult.FAIL;
            }
            if (entity.isBattling() || BattleRegistry.getBattleByParticipatingPlayer(sp) != null) {
                player.displayClientMessage(Component.translatable(m + "in_battle"), true);
                return InteractionResult.FAIL;
            }
            String now = of(p);
            if (now != null) {
                Component kind = Component.translatable(m + (SHADOW_FLAG.equals(now) ? "shadow" : "crystal"));
                player.displayClientMessage(Component.translatable(m + (now.equals(flag) ? "already" : "other"),
                        p.getDisplayName(false), kind), true);
                return InteractionResult.FAIL;
            }
            if (!convert(p, flag)) return InteractionResult.FAIL;
            if (!player.getAbilities().instabuild) stack.shrink(1);
            boolean shadow = SHADOW_FLAG.equals(flag);
            player.level().playSound(null, entity.blockPosition(), shadow ? SoundEvents.WITHER_AMBIENT : SoundEvents.AMETHYST_CLUSTER_PLACE,
                    SoundSource.PLAYERS, shadow ? 0.5F : 1F, shadow ? 1.4F : 0.8F);
            if (player.level() instanceof net.minecraft.server.level.ServerLevel server) {
                server.sendParticles(shadow ? net.minecraft.core.particles.ParticleTypes.WITCH : net.minecraft.core.particles.ParticleTypes.END_ROD,
                        entity.getX(), entity.getY() + entity.getBbHeight() / 2, entity.getZ(), 40,
                        entity.getBbWidth() / 2, entity.getBbHeight() / 2, entity.getBbWidth() / 2, 0.05);
            }
            player.sendSystemMessage(Component.translatable(m + (shadow ? "shadowed" : "crystallized"), p.getDisplayName(false)));
            return InteractionResult.CONSUME;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
            tooltip.add(Component.translatable(getDescriptionId() + ".tooltip").withStyle(net.minecraft.ChatFormatting.GRAY));
        }
    }
}
