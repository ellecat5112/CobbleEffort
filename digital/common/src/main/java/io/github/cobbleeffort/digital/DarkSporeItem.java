package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokemon.evolution.Evolution;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
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
import net.minecraft.world.item.ItemStack;

/**
 * A Dark Spore (a dark evolution item): used on your own Digimon, it rewrites it to Virus and forces a digivolution
 * into a Virus Digimon of a higher stage, if it has one (whatever its level). Found in Dark Towers and sold on the
 * black market.
 */
public class DarkSporeItem extends TooltipItem {
    public DarkSporeItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
        if (player.level().isClientSide) return InteractionResult.SUCCESS;
        Pokemon p = PartnerUse.own(player, target, true);
        if (p == null) return InteractionResult.FAIL;
        Evolution pick = null;
        for (Evolution e : p.getForm().getEvolutions()) {
            Species r = Digivice.result(e);
            if (r != null && r.getLabels().contains("digimon_virus") && Digivice.stageIndex(r) > Digivice.stageIndex(p.getSpecies())) {
                pick = e;
                break;
            }
        }
        if (pick == null) {
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".spore.none", p.getDisplayName(false)), true);
            return InteractionResult.FAIL;
        }
        Attributes.set(p, Attribute.VIRUS);
        if (!player.getAbilities().instabuild) stack.shrink(1);
        player.sendSystemMessage(Component.translatable(Digital.MOD_ID + ".spore.used", p.getDisplayName(false)).withStyle(ChatFormatting.DARK_PURPLE));
        player.level().playSound(null, target.blockPosition(), SoundEvents.WITHER_AMBIENT, SoundSource.PLAYERS, 0.5F, 1.5F);
        PartnerUse.particles(target, ParticleTypes.SQUID_INK, 30);
        pick.forceEvolve(p);
        return InteractionResult.CONSUME;
    }
}
