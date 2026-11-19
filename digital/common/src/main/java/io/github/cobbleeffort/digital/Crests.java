package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.Priority;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.events.CobblemonEvents;
import com.cobblemon.mod.common.battles.actor.PlayerBattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.EventResult;
import dev.architectury.event.events.common.BlockEvent;
import dev.architectury.event.events.common.PlayerEvent;
import dev.architectury.platform.Platform;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.StringTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.CropBlock;

import java.util.List;

/**
 * Crests and the Tag. A Crest (Courage, Friendship, Love, Knowledge, Sincerity, Reliability, Hope, Light) socketed in
 * a Tag (worn in its Accessories necklace slot, or just carried) charges as you do what it stands for. At 100% the
 * Tag unlocks Ultimate and Mega digivolution: use the Tag on your Digimon to digivolve it a stage at once (whatever its
 * level), or let the Digivice warp for free, up to two stages from Adult. Either uses up the charge. A Digimon holding
 * a Crest pays half for warps.
 */
public final class Crests {
    public static final List<String> CRESTS = List.of("courage", "friendship", "love", "knowledge", "sincerity", "reliability", "hope", "light");
    public static final int FULL = 100;

    private Crests() {
    }

    // --- items -----------------------------------------------------------------------------------------------------

    /** A Crest: use it with a Tag in your other hand to socket it. */
    public static class CrestItem extends Item {
        final String crest;

        public CrestItem(Properties properties, String crest) {
            super(properties);
            this.crest = crest;
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            ItemStack tag = player.getItemInHand(hand == InteractionHand.MAIN_HAND ? InteractionHand.OFF_HAND : InteractionHand.MAIN_HAND);
            if (!(tag.getItem() instanceof TagItem)) {
                if (!level.isClientSide) player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".crest.need_tag"), true);
                return InteractionResultHolder.fail(stack);
            }
            if (!level.isClientSide) {
                String old = socketed(tag);
                CustomData.update(DataComponents.CUSTOM_DATA, tag, t -> {
                    t.putString("crest", crest);
                    t.putInt("charge", 0);
                });
                stack.shrink(1);
                if (old != null) give(player, crestStack(old));
                level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1F, 1.2F);
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".crest.socketed",
                        Component.translatable(Digital.MOD_ID + ".crest." + crest)).withStyle(ChatFormatting.GOLD), true);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable(Digital.MOD_ID + ".crest." + crest + ".how").withStyle(ChatFormatting.GRAY));
            lines.add(Component.translatable(Digital.MOD_ID + ".crest.tooltip").withStyle(ChatFormatting.DARK_GRAY));
        }
    }

    /** The Tag: holds one Crest and its charge. Sneak-use pops the Crest out; at full charge, use it on your Digimon. */
    public static class TagItem extends Item {
        public TagItem(Properties properties) {
            super(properties);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (!player.isShiftKeyDown() || socketed(stack) == null) return InteractionResultHolder.pass(stack);
            if (!level.isClientSide) {
                give(player, crestStack(socketed(stack)));
                CustomData.update(DataComponents.CUSTOM_DATA, stack, t -> {
                    t.remove("crest");
                    t.remove("charge");
                });
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }

        @Override
        public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
            if (player.level().isClientSide) return InteractionResult.SUCCESS;
            Pokemon p = PartnerUse.own(player, target, true);
            if (p == null) return InteractionResult.FAIL;
            String m = Digital.MOD_ID + ".crest.";
            if (socketed(stack) == null || charge(stack) < FULL) {
                player.displayClientMessage(Component.translatable(m + "not_full", charge(stack)), true);
                return InteractionResult.FAIL;
            }
            var evo = Digivice.openEvolutionOf(p);
            if (evo == null) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digivice.no_warp", p.getDisplayName(false)), true);
                return InteractionResult.FAIL;
            }
            setCharge(stack, 0);
            player.level().playSound(null, target.blockPosition(), SoundEvents.TOTEM_USE, SoundSource.PLAYERS, 0.8F, 1.2F);
            PartnerUse.particles(target, ParticleTypes.TOTEM_OF_UNDYING, 60);
            player.sendSystemMessage(Component.translatable(m + "evolved", p.getDisplayName(false),
                    Component.translatable(m + socketed(stack))).withStyle(ChatFormatting.GOLD));
            evo.forceEvolve(p);
            return InteractionResult.CONSUME;
        }

        @Override
        public boolean isBarVisible(ItemStack stack) {
            return socketed(stack) != null;
        }

        @Override
        public int getBarWidth(ItemStack stack) {
            return Math.round(13F * charge(stack) / FULL);
        }

        @Override
        public int getBarColor(ItemStack stack) {
            return charge(stack) >= FULL ? 0xFFD040 : 0xFF9030;
        }

        @Override
        public boolean isFoil(ItemStack stack) {
            return charge(stack) >= FULL;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            String c = socketed(stack);
            String m = Digital.MOD_ID + ".crest.";
            if (c == null) {
                lines.add(Component.translatable(m + "empty_tag").withStyle(ChatFormatting.GRAY));
            } else {
                lines.add(Component.translatable(m + "tag_line", Component.translatable(m + c), charge(stack)).withStyle(ChatFormatting.GOLD));
                lines.add(Component.translatable(m + c + ".how").withStyle(ChatFormatting.GRAY));
            }
            lines.add(Component.translatable(m + "tag_tooltip").withStyle(ChatFormatting.DARK_GRAY));
        }
    }

    // --- state on the Tag ---------------------------------------------------------------------------------------------

    static String socketed(ItemStack tag) {
        CustomData d = tag.get(DataComponents.CUSTOM_DATA);
        return d == null || !d.copyTag().contains("crest") ? null : d.copyTag().getString("crest");
    }

    static int charge(ItemStack tag) {
        CustomData d = tag.get(DataComponents.CUSTOM_DATA);
        return d == null ? 0 : d.copyTag().getInt("charge");
    }

    static void setCharge(ItemStack tag, int c) {
        CustomData.update(DataComponents.CUSTOM_DATA, tag, t -> t.putInt("charge", Math.max(0, Math.min(FULL, c))));
    }

    static ItemStack crestStack(String crest) {
        return new ItemStack(Digital.CRESTS.get(crest).get());
    }

    static void give(Player player, ItemStack stack) {
        if (!player.getInventory().add(stack)) player.drop(stack, false);
    }

    /** The player's Tag: the Accessories necklace slot first (when Accessories is installed), else the inventory. */
    public static ItemStack findTag(Player player) {
        if (Platform.isModLoaded("accessories")) {
            try {
                ItemStack worn = AccessoriesCompat.worn(player, Digital.TAG.get());
                if (!worn.isEmpty()) return worn;
            } catch (Throwable ignored) {
                // an Accessories version without the API we use: fall back to the inventory
            }
        }
        for (ItemStack s : player.getInventory().items) if (s.getItem() instanceof TagItem) return s;
        for (ItemStack s : player.getInventory().offhand) if (s.getItem() instanceof TagItem) return s;
        return ItemStack.EMPTY;
    }

    /** Charges the player's Tag if it holds this Crest. */
    public static void charge(Player player, String crest, int amount) {
        if (!(player instanceof ServerPlayer sp)) return;
        ItemStack tag = findTag(sp);
        if (tag.isEmpty() || !crest.equals(socketed(tag))) return;
        int before = charge(tag);
        if (before >= FULL) return;
        setCharge(tag, before + amount);
        if (charge(tag) >= FULL) {
            sp.level().playSound(null, sp.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 0.8F, 1.4F);
            sp.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".crest.full", Component.translatable(Digital.MOD_ID + ".crest." + crest))
                    .withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        } else {
            sp.displayClientMessage(Component.translatable(Digital.MOD_ID + ".crest.charging", Component.translatable(Digital.MOD_ID + ".crest." + crest),
                    charge(tag)).withStyle(ChatFormatting.YELLOW), true);
        }
    }

    /** True (and the charge spent) if the player's Tag is full: a free warp, up to two stages from Adult. */
    static boolean spendForWarp(Player player) {
        ItemStack tag = findTag(player);
        if (tag.isEmpty() || socketed(tag) == null || charge(tag) < FULL) return false;
        setCharge(tag, 0);
        return true;
    }

    static boolean holdsCrest(Pokemon p) {
        return p.heldItem().getItem() instanceof CrestItem;
    }

    // --- what charges them --------------------------------------------------------------------------------------------

    static void init() {
        CobblemonEvents.BATTLE_VICTORY.subscribe(Priority.NORMAL, event -> {
            try {
                List<BattleActor> winners = new java.util.ArrayList<>(event.getWinners());
                long players = winners.stream().filter(a -> a instanceof PlayerBattleActor).count();
                for (BattleActor a : winners) {
                    if (!(a instanceof PlayerBattleActor pa) || pa.getEntity() == null) continue;
                    ServerPlayer p = pa.getEntity();
                    int healthy = 0;
                    boolean close = false;
                    for (BattlePokemon bp : a.getPokemonList()) {
                        if (bp.getHealth() > 0) healthy++;
                        if (bp.getHealth() > 0 && bp.getHealth() * 4 <= bp.getMaxHealth()) close = true;
                    }
                    if (close) charge(p, "courage", 15);
                    if (healthy == 1) charge(p, "hope", 15);
                    if (players > 1) charge(p, "reliability", 10);
                    if (!p.level().isNight() && p.level().canSeeSky(p.blockPosition())) charge(p, "light", 4);
                }
            } catch (Throwable t) {
                Digital.LOG.error("Crest charge failed", t);
            }
        });
        CobblemonEvents.TRADE_EVENT_POST.subscribe(Priority.NORMAL, event -> {
            try {
                for (ServerPlayer p : Digital.server().getPlayerList().getPlayers()) {
                    if (p.getUUID().equals(event.getTradeParticipant1().getUuid()) || p.getUUID().equals(event.getTradeParticipant2().getUuid())) {
                        charge(p, "reliability", 15);
                    }
                }
            } catch (Throwable ignored) {
                // trades without player participants
            }
        });
        CobblemonEvents.HATCH_EGG_POST.subscribe(Priority.NORMAL, event -> {
            charge(event.getPlayer(), "love", 15);
        });
        BlockEvent.BREAK.register((level, pos, state, player, xp) -> {
            if (state.getBlock() instanceof CropBlock crop && crop.isMaxAge(state)) charge(player, "sincerity", 1);
            return EventResult.pass();
        });
        PlayerEvent.CRAFT_ITEM.register((player, crafted, inventory) -> {
            if (crafted.getItem() instanceof AttributeItem || crafted.getItem() instanceof DigiModifyCard) charge(player, "knowledge", 2);
        });
    }

    /** A first scan of a species with the Digivice: Knowledge (the Tag remembers what it has seen). */
    static void scanned(ServerPlayer player, String species) {
        ItemStack tag = findTag(player);
        if (tag.isEmpty()) return;
        CompoundTag t = tag.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
        ListTag seen = t.getList("seen", 8);
        for (int i = 0; i < seen.size(); i++) if (seen.getString(i).equals(species)) return;
        seen.add(StringTag.valueOf(species));
        if (seen.size() > 2000) seen.remove(0);
        CustomData.update(DataComponents.CUSTOM_DATA, tag, x -> x.put("seen", seen));
        charge(player, "knowledge", 5);
    }

    static void fed(Player player) {
        charge(player, "friendship", 3);
    }

    static void trained(Player player) {
        charge(player, "friendship", 2);
    }

    static void hatched(Player player) {
        charge(player, "love", 15);
    }

    static boolean party(ServerPlayer player, Pokemon p) {
        for (Pokemon q : Cobblemon.INSTANCE.getStorage().getParty(player)) if (q == p) return true;
        return false;
    }
}
