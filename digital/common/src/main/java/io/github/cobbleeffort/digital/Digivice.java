package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.pokemon.evolution.Evolution;
import com.cobblemon.mod.common.api.pokemon.requirement.Requirement;
import com.cobblemon.mod.common.api.storage.pc.PCStore;
import com.cobblemon.mod.common.api.storage.pc.link.PCLink;
import com.cobblemon.mod.common.api.storage.pc.link.PCLinkManager;
import com.cobblemon.mod.common.battles.BagItemActionResponse;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.battles.BattleRules;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.entity.pokemon.effects.TransformEffect;
import com.cobblemon.mod.common.item.battle.BagItem;
import com.cobblemon.mod.common.item.battle.SimpleBagItemLike;
import com.cobblemon.mod.common.net.messages.client.storage.pc.OpenPCPacket;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.cobblemon.mod.common.pokemon.requirements.LevelRequirement;
import com.cobblemon.mod.common.pokemon.requirements.PokemonPropertiesRequirement;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The Tamer's Digivice. Out of battle: use it on any Digimon to scan it (stage, attribute, what it digivolves into and
 * what that takes, and what it comes from); use it in the air for your Tamer Energy and your party's attributes;
 * sneak-use it to open your PC from anywhere. In battle: use it on your battling Digimon to warp-digivolve it (one
 * stage for WARP_ONE energy, two stages if you sneak, WARP_TWO) for the rest of the battle: the battle engine takes
 * the new species' stats and types, and it looks the part (Cobblemon's Transform effect, which ends with the battle).
 * With a Jogress partner at hand (see Jogress) a plain use DNA-digivolves instead, for JOGRESS energy.
 * Tamer Energy lives on the Digivice (0-100) and refills by itself, a point every REGEN_TICKS while it's carried.
 */
public class Digivice extends Item implements SimpleBagItemLike {
    public static final int MAX_ENERGY = 100, WARP_ONE = 40, WARP_TWO = 80, JOGRESS = 60, REGEN_TICKS = 120;
    private final BagItem bagItem;

    public Digivice(Properties properties) {
        super(properties);
        this.bagItem = new BagItem() {
            @Override
            public String getItemName() {
                return "item." + Digital.MOD_ID + ".digivice";
            }

            @Override
            public Item getReturnItem() {
                return Items.AIR;
            }

            @Override
            public boolean canUse(ItemStack stack, PokemonBattle battle, BattlePokemon target) {
                return target.getHealth() > 0;
            }

            @Override
            public String getShowdownInput(BattleActor actor, BattlePokemon bp, String data) {
                // data: "<showdown id> <species id>" chosen when the Digivice was used
                String[] parts = data == null ? new String[0] : data.split(" ");
                if (parts.length < 2) return "digivolve none";
                Species target = PokemonSpecies.INSTANCE.getByIdentifier(net.minecraft.resources.ResourceLocation.parse(parts[1]));
                PokemonEntity entity = bp.getEffectedPokemon().getEntity();
                if (target != null && entity != null) {
                    try {
                        PokemonProperties mock = PokemonProperties.Companion.parse(parts[1]);
                        new TransformEffect(mock, target.getStandardForm().getBaseScale() * bp.getEffectedPokemon().getScaleModifier(), true)
                                .start(entity);
                    } catch (Throwable t) {
                        Digital.LOG.error("Warp digivolution look failed", t);
                    }
                    actor.getBattle().broadcastChatMessage(Component.translatable(Digital.MOD_ID + (parts.length > 2 ? ".digivice.jogress" : ".digivice.warped"),
                            bp.getName(), target.getTranslatedName()).withStyle(ChatFormatting.GOLD));
                }
                return "digivolve " + parts[0];
            }
        };
    }

    @Override
    public BagItem getBagItem() {
        return bagItem;
    }

    // --- Tamer Energy -----------------------------------------------------------------------------------------------

    public static int energy(ItemStack stack) {
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        return data == null || !data.copyTag().contains("energy") ? MAX_ENERGY : data.copyTag().getInt("energy");
    }

    public static void setEnergy(ItemStack stack, int energy) {
        int e = Math.max(0, Math.min(MAX_ENERGY, energy));
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putInt("energy", e));
    }

    /** The first Digivice in the player's inventory, or EMPTY. */
    public static ItemStack find(Player player) {
        for (ItemStack s : player.getInventory().items) if (s.getItem() instanceof Digivice) return s;
        for (ItemStack s : player.getInventory().offhand) if (s.getItem() instanceof Digivice) return s;
        return ItemStack.EMPTY;
    }

    public static boolean has(Player player) {
        return !find(player).isEmpty();
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        if (level.isClientSide || !(entity instanceof Player) || level.getGameTime() % REGEN_TICKS != 0) return;
        int e = energy(stack);
        if (e < MAX_ENERGY) setEnergy(stack, e + 1);
    }

    @Override
    public boolean isBarVisible(ItemStack stack) {
        return energy(stack) < MAX_ENERGY;
    }

    @Override
    public int getBarWidth(ItemStack stack) {
        return Math.round(13F * energy(stack) / MAX_ENERGY);
    }

    @Override
    public int getBarColor(ItemStack stack) {
        return 0x40E0FF;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
        String m = Digital.MOD_ID + ".digivice.";
        lines.add(Component.translatable(m + "energy", energy(stack), MAX_ENERGY).withStyle(ChatFormatting.AQUA));
        lines.add(Component.translatable(m + "tooltip_scan").withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable(m + "tooltip_pc").withStyle(ChatFormatting.GRAY));
        lines.add(Component.translatable(m + "tooltip_warp", WARP_ONE, WARP_TWO).withStyle(ChatFormatting.GRAY));
    }

    // --- out of battle: scan, status, PC ------------------------------------------------------------------------------

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide || !(player instanceof ServerPlayer sp)) return InteractionResultHolder.success(stack);
        if (BattleRegistry.getBattleByParticipatingPlayer(sp) != null) return InteractionResultHolder.pass(stack);
        if (player.isShiftKeyDown()) {
            PCStore pc = Cobblemon.INSTANCE.getStorage().getPC(sp);
            PCLinkManager.INSTANCE.addLink(new PCLink(pc, sp.getUUID()));
            new OpenPCPacket(pc).sendToPlayer(sp);
            return InteractionResultHolder.consume(stack);
        }
        String m = Digital.MOD_ID + ".digivice.";
        sp.sendSystemMessage(Component.translatable(m + "status", energy(stack), MAX_ENERGY).withStyle(ChatFormatting.AQUA));
        for (Pokemon p : Cobblemon.INSTANCE.getStorage().getParty(sp)) {
            if (!Attributes.isDigimon(p)) continue;
            Attribute a = Attributes.of(p);
            sp.sendSystemMessage(Component.literal(" ▸ ").withStyle(ChatFormatting.DARK_AQUA).append(p.getDisplayName(false))
                    .append(Component.literal(" - ").withStyle(ChatFormatting.GRAY)).append(stage(p.getSpecies()))
                    .append(Component.literal(", ").withStyle(ChatFormatting.GRAY))
                    .append(a == null ? Component.literal("?") : Component.translatable(Digital.MOD_ID + ".attribute." + a.id())));
        }
        level.playSound(null, player.blockPosition(), SoundEvents.NOTE_BLOCK_BIT.value(), SoundSource.PLAYERS, 0.6F, 1.6F);
        return InteractionResultHolder.consume(stack);
    }

    @Override
    public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
        if (!(target instanceof PokemonEntity entity)) return InteractionResult.PASS;
        if (player.level().isClientSide) return InteractionResult.SUCCESS;
        if (!(player instanceof ServerPlayer sp)) return InteractionResult.PASS;
        Pokemon p = entity.getPokemon();
        if (!Attributes.isDigimon(p)) {
            sp.displayClientMessage(Component.translatable(Digital.MOD_ID + ".use.not_digimon", p.getDisplayName(false)), true);
            return InteractionResult.FAIL;
        }
        if (player.isShiftKeyDown() && sp.getUUID().equals(p.getOwnerUUID()) && !entity.isBattling()
                && SpiritEvolution.bioMerge(sp, entity, stack)) {
            return InteractionResult.CONSUME;                              // sneak on your own Digimon: Bio-Merge
        }
        scan(sp, p, sp.getUUID().equals(p.getOwnerUUID()));
        Crests.scanned(sp, p.getSpecies().getResourceIdentifier().toString());
        player.level().playSound(null, entity.blockPosition(), SoundEvents.BEACON_AMBIENT, SoundSource.PLAYERS, 0.8F, 1.8F);
        PartnerUse.particles(entity, ParticleTypes.GLOW, 16);
        return InteractionResult.CONSUME;
    }

    static final String[][] STAGES = {
            {"digimon_baby1", "baby1"}, {"digimon_baby2", "baby2"}, {"digimon_child", "child"}, {"digimon_adult", "adult"},
            {"digimon_perfect", "perfect"}, {"digimon_ultimate", "ultimate"}, {"digimon_super_ultimate", "super_ultimate"}};

    static Component stage(Species s) {
        for (String[] st : STAGES) {
            if (s.getLabels().contains(st[0])) return Component.translatable(Digital.MOD_ID + ".stage." + st[1]);
        }
        return Component.literal("?");
    }

    static int stageIndex(Species s) {
        for (int i = 0; i < STAGES.length; i++) if (s.getLabels().contains(STAGES[i][0])) return i;
        return -1;
    }

    private static Map<String, List<Species>> preEvolutions;

    static synchronized List<Species> from(Species s) {
        if (preEvolutions == null) {
            Map<String, List<Species>> map = new HashMap<>();
            for (Species sp : PokemonSpecies.INSTANCE.getImplemented()) {
                for (Evolution e : sp.getEvolutions()) {
                    String r = e.getResult().getSpecies();
                    if (r == null) continue;
                    Species rs = PokemonSpecies.INSTANCE.getByIdentifier(net.minecraft.resources.ResourceLocation.parse(r.contains(":") ? r : "cobblemon:" + r));
                    if (rs != null) map.computeIfAbsent(rs.getResourceIdentifier().toString(), k -> new ArrayList<>()).add(sp);
                }
            }
            preEvolutions = map;
        }
        return preEvolutions.getOrDefault(s.getResourceIdentifier().toString(), List.of());
    }

    static Species result(Evolution e) {
        String r = e.getResult().getSpecies();
        if (r == null) return null;
        return PokemonSpecies.INSTANCE.getByIdentifier(net.minecraft.resources.ResourceLocation.parse(r.contains(":") ? r : "cobblemon:" + r));
    }

    /** One requirement in words. */
    static MutableComponent describe(Requirement r) {
        String m = Digital.MOD_ID + ".req.";
        if (r instanceof LevelRequirement l) return Component.translatable(m + "level", l.getMinLevel());
        if (r instanceof PokemonPropertiesRequirement pr) {
            String s = pr.getTarget().getOriginalString();
            for (Attribute a : Attribute.values()) {
                if (s.contains(a.aspect())) return Component.translatable(m + "attribute", Component.translatable(Digital.MOD_ID + ".attribute." + a.id()));
            }
            return Component.translatable(m + "properties", s);
        }
        String name = r.getClass().getSimpleName().replace("Requirement", "");
        return Component.translatable(m + "other", name.replaceAll("([a-z])([A-Z])", "$1 $2").toLowerCase(java.util.Locale.ROOT));
    }

    static void scan(ServerPlayer player, Pokemon p, boolean own) {
        String m = Digital.MOD_ID + ".digivice.";
        Species s = p.getSpecies();
        Attribute a = Attributes.of(p);
        player.sendSystemMessage(Component.translatable(m + "scan_title", s.getTranslatedName()).withStyle(ChatFormatting.AQUA, ChatFormatting.BOLD));
        MutableComponent line = Component.literal(" ").append(stage(s)).append(Component.literal(" · ").withStyle(ChatFormatting.GRAY))
                .append(a == null ? Component.literal("?") : Component.translatable(Digital.MOD_ID + ".attribute." + a.id()))
                .append(Component.literal(" · ").withStyle(ChatFormatting.GRAY)).append(p.getPrimaryType().getDisplayName());
        if (p.getSecondaryType() != null) line.append(Component.literal("/")).append(p.getSecondaryType().getDisplayName());
        player.sendSystemMessage(line.withStyle(ChatFormatting.WHITE));
        if (a != null && a.beats() != null) {
            player.sendSystemMessage(Component.translatable(m + "beats", Component.translatable(Digital.MOD_ID + ".attribute." + a.beats().id()))
                    .withStyle(ChatFormatting.DARK_AQUA));
        }
        Set<Evolution> evolutions = p.getForm().getEvolutions();
        if (evolutions.isEmpty()) {
            player.sendSystemMessage(Component.translatable(m + "no_evolutions").withStyle(ChatFormatting.GRAY));
        } else {
            player.sendSystemMessage(Component.translatable(m + "evolves_into").withStyle(ChatFormatting.YELLOW));
            for (Evolution e : evolutions) {
                Species r = result(e);
                if (r == null) continue;
                MutableComponent row = Component.literal(" ▸ ").withStyle(ChatFormatting.DARK_AQUA)
                        .append(r.getTranslatedName().copy().withStyle(ChatFormatting.WHITE));
                List<Requirement> reqs = new ArrayList<>(e.getRequirements());
                if (!reqs.isEmpty()) row.append(Component.literal(": ").withStyle(ChatFormatting.GRAY));
                for (int i = 0; i < reqs.size(); i++) {
                    Requirement q = reqs.get(i);
                    MutableComponent d = describe(q);
                    if (own) d.withStyle(q.check(p) ? ChatFormatting.GREEN : ChatFormatting.RED);
                    else d.withStyle(ChatFormatting.GRAY);
                    row.append(d);
                    if (i + 1 < reqs.size()) row.append(Component.literal(", ").withStyle(ChatFormatting.GRAY));
                }
                player.sendSystemMessage(row);
            }
        }
        List<Species> pre = from(s);
        if (!pre.isEmpty()) {
            MutableComponent row = Component.translatable(m + "evolves_from").withStyle(ChatFormatting.YELLOW);
            Set<String> seen = new LinkedHashSet<>();
            for (Species x : pre) {
                if (!seen.add(x.getResourceIdentifier().toString())) continue;
                if (seen.size() > 1) row.append(Component.literal(", ").withStyle(ChatFormatting.GRAY));
                row.append(x.getTranslatedName().copy().withStyle(ChatFormatting.WHITE));
                if (seen.size() >= 8) break;
            }
            player.sendSystemMessage(row);
        }
    }

    // --- in battle: warp digivolution ---------------------------------------------------------------------------------

    /** An evolution open to this Digimon by attribute (an attribute requirement must pass; others are ignored). */
    static Species openEvolution(Pokemon p, Species from) {
        for (Evolution e : from == p.getSpecies() ? p.getForm().getEvolutions() : from.getEvolutions()) {
            Species r = result(e);
            if (r == null || !r.getLabels().contains(DigiBall.LABEL) || stageIndex(r) <= stageIndex(from)) continue;
            boolean ok = true;
            for (Requirement q : e.getRequirements()) {
                if (q instanceof PokemonPropertiesRequirement pr && pr.getTarget().getOriginalString().contains("digi_") && !pr.check(p)) ok = false;
            }
            if (ok) return r;
        }
        return null;
    }

    /** The first evolution of this Digimon open to it by attribute (the Tag's Crest digivolution). */
    static Evolution openEvolutionOf(Pokemon p) {
        for (Evolution e : p.getForm().getEvolutions()) {
            Species r = result(e);
            if (r == null || !r.getLabels().contains(DigiBall.LABEL) || stageIndex(r) <= stageIndex(p.getSpecies())) continue;
            boolean ok = true;
            for (Requirement q : e.getRequirements()) {
                if (q instanceof PokemonPropertiesRequirement pr && pr.getTarget().getOriginalString().contains("digi_") && !pr.check(p)) ok = false;
            }
            if (ok) return e;
        }
        return null;
    }

    /** The warp target: one stage up, or two when `twice`. */
    static Species warpTarget(Pokemon p, boolean twice) {
        Species one = openEvolution(p, p.getSpecies());
        if (one == null || !twice) return one;
        return openEvolution(p, one);
    }

    @Override
    public boolean handleInteraction(ServerPlayer player, BattlePokemon bp, ItemStack stack) {
        String m = Digital.MOD_ID + ".digivice.";
        PokemonBattle battle = bp.getActor().getBattle();
        Pokemon p = bp.getEffectedPokemon();
        if (!Attributes.isDigimon(p)) {
            player.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".use.not_digimon", p.getDisplayName(false)).withStyle(ChatFormatting.RED));
            return false;
        }
        if (!bp.getActor().canFitForcedAction() || battle.getFormat().getRuleSet().contains(BattleRules.BAG_CLAUSE)) {
            player.sendSystemMessage(Component.translatable("cobblemon.battle.bagitem.cannot").withStyle(ChatFormatting.RED));
            return false;
        }
        if (bp.getHealth() <= 0) return false;
        PokemonEntity entity = p.getEntity();
        if (entity != null && entity.getEffects().getMockEffect() != null) {
            player.sendSystemMessage(Component.translatable(m + "already_warped", p.getDisplayName(false)).withStyle(ChatFormatting.RED));
            return false;
        }
        if (DarkAura.blocks(player, p)) {
            player.sendSystemMessage(Component.translatable(m + "dark_tower").withStyle(ChatFormatting.DARK_RED));
            return false;
        }
        boolean twice = player.isShiftKeyDown();
        Species jogress = twice ? null : Jogress.find(player, bp);
        int cost = jogress != null ? JOGRESS : twice ? WARP_TWO : WARP_ONE;
        if (Crests.holdsCrest(p)) cost /= 2;                        // a held Crest halves the cost
        Species target = jogress != null ? jogress : warpTarget(p, twice);
        boolean crest = false;
        if (jogress == null && twice && target != null) {
            ItemStack tag = Crests.findTag(player);                // a full Tag: free, and the warp can reach Ultimate
            crest = !tag.isEmpty() && Crests.socketed(tag) != null && Crests.charge(tag) >= Crests.FULL;
            if (crest) {
                Species further = openEvolution(p, target);
                if (further != null && stageIndex(p.getSpecies()) >= 3) target = further;
                cost = 0;
            }
        }
        if (target == null) {
            player.sendSystemMessage(Component.translatable(m + (twice ? "no_warp_two" : "no_warp"), p.getDisplayName(false)).withStyle(ChatFormatting.RED));
            return false;
        }
        if (DigitalRules.freeEnergy(player)) cost = 0;               // game rule digitalFreeDigivolution (or creative)
        if (energy(stack) < cost) {
            player.sendSystemMessage(Component.translatable(m + "low_energy", energy(stack), cost).withStyle(ChatFormatting.RED));
            return false;
        }
        if (crest) Crests.spendForWarp(player);
        if (cost > 0) setEnergy(stack, energy(stack) - cost);
        bp.getActor().forceChoose(new BagItemActionResponse(bagItem, bp, target.showdownId() + " " + target.getResourceIdentifier()
                + (jogress != null ? " jogress" : "")));
        player.level().playSound(null, player.blockPosition(), SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 1F, 1.5F);
        return true;
    }
}
