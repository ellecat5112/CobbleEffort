package io.github.cobbleeffort.fusion;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.callback.PartySelectCallbacks;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.battles.BattleRegistry;
import com.cobblemon.mod.common.pokemon.Pokemon;
import java.util.ArrayList;
import java.util.List;
import kotlin.Unit;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The DNA Splicers family (Infinite Fusion's items):
 *   DNA Splicers       pick a HEAD, then a BODY: they fuse (level = the average); used up by fusing.
 *                      Picking a fusion unfuses it instead (free: the splicers aren't used up).
 *   Super Splicers     the same, but the fusion takes the HIGHER of the two levels.
 *   Infinite Splicers  DNA Splicers that are never used up.
 *   DNA Reversers      pick a fusion: its head and body swap places; used up.
 * Not in battle; eggs can't be fused.
 */
public class SplicerItem extends Item {
    public enum Kind { SPLICERS, SUPER, INFINITE, REVERSERS }

    private final Kind kind;

    public SplicerItem(Kind kind, Properties properties) {
        super(properties);
        this.kind = kind;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        String key = "item.cobbleeffort_fusion." + switch (kind) {
            case SPLICERS -> "dna_splicers";
            case SUPER -> "super_splicers";
            case INFINITE -> "infinite_splicers";
            case REVERSERS -> "dna_reversers";
        } + ".tooltip";
        tooltip.add(Component.translatable(key).withStyle(ChatFormatting.GRAY));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide() || !(player instanceof ServerPlayer sp)) return InteractionResultHolder.success(stack);
        if (BattleRegistry.INSTANCE.getBattleByParticipatingPlayer(sp) != null) {
            sp.sendSystemMessage(Component.translatable("cobbleeffort_fusion.error.battle").withStyle(ChatFormatting.RED));
            return InteractionResultHolder.fail(stack);
        }
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(sp);
        List<Pokemon> mons = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            Pokemon p = party.get(i);
            if (p != null) mons.add(p);
        }
        if (mons.isEmpty()) return InteractionResultHolder.fail(stack);
        if (kind == Kind.REVERSERS) {
            PartySelectCallbacks.INSTANCE.createFromPokemon(sp, Component.translatable("cobbleeffort_fusion.pick.reverse"), mons,
                    FusionRules::isFused, p -> Unit.INSTANCE, picked -> {
                        report(sp, Fusing.reverse(sp, picked), hand);
                        return Unit.INSTANCE;
                    });
            return InteractionResultHolder.success(stack);
        }
        PartySelectCallbacks.INSTANCE.createFromPokemon(sp, Component.translatable("cobbleeffort_fusion.pick.head"), mons,
                p -> true, p -> Unit.INSTANCE, head -> {
                    if (FusionRules.isFused(head)) {
                        Component error = Fusing.unfuse(sp, head);
                        if (error != null) sp.sendSystemMessage(error.copy().withStyle(ChatFormatting.RED));
                        else sp.sendSystemMessage(Component.translatable("cobbleeffort_fusion.unfused").withStyle(ChatFormatting.LIGHT_PURPLE));
                        return Unit.INSTANCE;
                    }
                    List<Pokemon> bodies = new ArrayList<>(mons);
                    PartySelectCallbacks.INSTANCE.createFromPokemon(sp, Component.translatable("cobbleeffort_fusion.pick.body", head.getDisplayName(false)),
                            bodies, b -> b != head && !FusionRules.isFused(b), p -> Unit.INSTANCE, body -> {
                                Fusing.LevelRule rule = kind == Kind.SUPER ? Fusing.LevelRule.HIGHER : Fusing.LevelRule.AVERAGE;
                                report(sp, Fusing.fuse(sp, head, body, rule), hand);
                                return Unit.INSTANCE;
                            });
                    return Unit.INSTANCE;
                });
        return InteractionResultHolder.success(stack);
    }

    /** Show an error, or use the item up when it worked (except Infinite Splicers). */
    private void report(ServerPlayer player, Component error, InteractionHand hand) {
        if (error != null) {
            player.sendSystemMessage(error.copy().withStyle(ChatFormatting.RED));
            return;
        }
        if (kind == Kind.INFINITE || player.isCreative()) return;
        ItemStack held = player.getItemInHand(hand);
        if (held.getItem() == this) held.shrink(1);
        else player.getInventory().clearOrCountMatchingItems(s -> s.getItem() == this, 1, player.inventoryMenu.getCraftSlots());
    }
}
