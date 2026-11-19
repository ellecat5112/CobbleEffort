package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.pokemon.Pokemon;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;

/**
 * Vaccine/Data/Virus Fragments (dropped by defeated wild Digimon of that attribute) and Chips (crafted from them).
 * Used on your own Digimon: a fragment counts towards rewriting its attribute (ten of one kind in a row), a chip
 * rewrites it at once. A Digimon's attribute decides who it beats in battle and which digivolutions are open to it.
 */
public class AttributeItem extends Item {
    private final Attribute attribute;
    private final boolean chip;

    public AttributeItem(Properties properties, Attribute attribute, boolean chip) {
        super(properties);
        this.attribute = attribute;
        this.chip = chip;
    }

    public Attribute attribute() {
        return attribute;
    }

    @Override
    public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
        if (player.level().isClientSide) return InteractionResult.SUCCESS;
        Pokemon p = PartnerUse.own(player, target, true);
        if (p == null) return InteractionResult.FAIL;
        String m = Digital.MOD_ID + ".attribute.";
        Component name = p.getDisplayName(false);
        Component kind = Component.translatable(m + attribute.id());
        if (Attributes.of(p) == attribute) {
            player.displayClientMessage(Component.translatable(m + "already", name, kind), true);
            return InteractionResult.FAIL;
        }
        int n;
        if (chip) {
            Attributes.set(p, attribute);
            n = 0;
        } else {
            n = Attributes.feed(p, attribute);
        }
        if (!player.getAbilities().instabuild) stack.shrink(1);
        p.incrementFriendship(chip ? 3 : 1, true);
        if (n == 0) {
            player.level().playSound(null, target.blockPosition(), SoundEvents.BEACON_POWER_SELECT, SoundSource.PLAYERS, 0.8F, 1.4F);
            PartnerUse.particles(target, ParticleTypes.END_ROD, 40);
            player.sendSystemMessage(Component.translatable(m + "rewritten", name, kind).withStyle(ChatFormatting.AQUA));
        } else {
            player.level().playSound(null, target.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 0.8F, 1.6F);
            PartnerUse.particles(target, ParticleTypes.ENCHANT, 12);
            player.displayClientMessage(Component.translatable(m + "absorbed", name, kind, n, Attributes.FRAGMENTS_TO_SHIFT), true);
        }
        return InteractionResult.CONSUME;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
        String m = Digital.MOD_ID + ".attribute.";
        Component kind = Component.translatable(m + attribute.id());
        lines.add(Component.translatable(m + (chip ? "chip_tooltip" : "fragment_tooltip"), kind, Attributes.FRAGMENTS_TO_SHIFT)
                .withStyle(ChatFormatting.GRAY));
        Attribute beats = attribute.beats();
        if (beats != null) {
            lines.add(Component.translatable(m + "beats", kind, Component.translatable(m + beats.id())).withStyle(ChatFormatting.DARK_AQUA));
        }
    }
}
