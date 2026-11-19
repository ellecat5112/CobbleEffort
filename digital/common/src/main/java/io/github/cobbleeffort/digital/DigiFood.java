package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokemon.stats.SidemodEvSource;
import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemNameBlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.block.Block;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Digimon World's food: Digi-Meat (grows from the ground like carrots), Sirloin (a rare harvest) and Super Carrots.
 * People can eat them; fed to your own sent-out Pokémon (use it on them) they fill it up (Cobblemon's fullness, like
 * berries) and raise its friendship, and the better ones also raise EVs.
 */
public final class DigiFood {
    /** What one bite does: fullness, friendship, EVs. */
    public record Effect(int fullness, int friendship, Map<Stat, Integer> evs) {
        public static Effect of(int fullness, int friendship, Object... statAmounts) {
            Map<Stat, Integer> evs = new LinkedHashMap<>();
            for (int i = 0; i + 1 < statAmounts.length; i += 2) evs.put((Stat) statAmounts[i], (Integer) statAmounts[i + 1]);
            return new Effect(fullness, friendship, evs);
        }
    }

    private DigiFood() {
    }

    /** Feeds `p`; false (and a message) if it is full. */
    static boolean feed(Player player, LivingEntity target, Pokemon p, Effect effect) {
        String m = Digital.MOD_ID + ".food.";
        if (p.isFull()) {
            player.displayClientMessage(Component.translatable(m + "full", p.getDisplayName(false)), true);
            return false;
        }
        p.feedPokemon(effect.fullness(), true);
        p.incrementFriendship(effect.friendship(), true);
        int gained = 0;
        for (Map.Entry<Stat, Integer> e : effect.evs().entrySet()) {
            gained += p.getEvs().add(e.getKey(), e.getValue(), new SidemodEvSource(Digital.MOD_ID, p));
        }
        Crests.fed(player);
        player.level().playSound(null, target.blockPosition(), SoundEvents.GENERIC_EAT, SoundSource.NEUTRAL, 0.8F, 1.1F);
        PartnerUse.particles(target, ParticleTypes.HEART, effect.evs().isEmpty() ? 3 : 6);
        player.displayClientMessage(Component.translatable(m + (gained > 0 ? "fed_evs" : "fed"), p.getDisplayName(false), gained)
                .withStyle(ChatFormatting.GREEN), true);
        return true;
    }

    static InteractionResult feedOn(ItemStack stack, Player player, LivingEntity target, Effect effect) {
        if (player.level().isClientSide) return InteractionResult.SUCCESS;
        Pokemon p = PartnerUse.own(player, target, false);
        if (p == null || !feed(player, target, p, effect)) return InteractionResult.FAIL;
        if (!player.getAbilities().instabuild) stack.shrink(1);
        return InteractionResult.CONSUME;
    }

    static void tooltip(Effect effect, List<Component> lines) {
        String m = Digital.MOD_ID + ".food.";
        lines.add(Component.translatable(m + "tooltip").withStyle(ChatFormatting.GRAY));
        for (Map.Entry<Stat, Integer> e : effect.evs().entrySet()) {
            lines.add(Component.translatable(m + "ev", e.getValue(), e.getKey().getDisplayName()).withStyle(ChatFormatting.DARK_GREEN));
        }
    }

    /** A food that is also its own seed (Digi-Meat, Super Carrot). */
    public static class Plantable extends ItemNameBlockItem {
        private final Effect effect;

        public Plantable(Block crop, Properties properties, Effect effect) {
            super(crop, properties);
            this.effect = effect;
        }

        @Override
        public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
            return DigiFood.feedOn(stack, player, target, effect);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            tooltip(effect, lines);
        }
    }

    /** A food that isn't planted (Sirloin). */
    public static class Plain extends net.minecraft.world.item.Item {
        private final Effect effect;

        public Plain(Properties properties, Effect effect) {
            super(properties);
            this.effect = effect;
        }

        @Override
        public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
            return DigiFood.feedOn(stack, player, target, effect);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            tooltip(effect, lines);
        }
    }
}
