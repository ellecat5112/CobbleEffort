package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.Cobblemon;
import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.api.storage.party.PlayerPartyStore;
import com.cobblemon.mod.common.pokemon.Pokemon;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * A Digitama (Digi-Egg). Carried in a player's inventory it warms up (custom data "warmth", a second at a time, shown
 * by the item bar); once warm, using it hatches a baby Digimon at level 1 into the party, or the PC if the party is
 * full. The Digimon it hatches is its custom data "species" if set, else a random Baby I Digimon (label "digimon_hatch").
 */
public class DigitamaItem extends Item {
    /** Ticks in a player's inventory before it can hatch: 5 minutes. */
    public static final int HATCH_TICKS = 6000;
    /** The label of the baby Digimon a Digitama can hatch into, and the fallback. */
    public static final String HATCH_LABEL = "digimon_hatch";
    public static final String FALLBACK = "cobbleeffort:koromon";

    public DigitamaItem(Properties properties) {
        super(properties);
    }

    static int warmth(ItemStack stack) {
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        return data == null ? 0 : data.copyTag().getInt("warmth");
    }

    static boolean ready(ItemStack stack) {
        return warmth(stack) >= HATCH_TICKS;
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        if (level.isClientSide || !(entity instanceof Player) || level.getGameTime() % 20 != 0) return;
        int w = warmth(stack);
        if (w >= HATCH_TICKS) return;
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putInt("warmth", Math.min(HATCH_TICKS, w + 20)));
    }

    @Override
    public boolean isBarVisible(ItemStack stack) {
        return !ready(stack);
    }

    @Override
    public int getBarWidth(ItemStack stack) {
        return Math.round(13F * warmth(stack) / HATCH_TICKS);
    }

    @Override
    public int getBarColor(ItemStack stack) {
        return 0xFFA030;
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return ready(stack);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
        if (ready(stack)) {
            lines.add(Component.translatable(Digital.MOD_ID + ".digitama.ready").withStyle(ChatFormatting.GOLD));
        } else {
            lines.add(Component.translatable(Digital.MOD_ID + ".digitama.warming", warmth(stack) * 100 / HATCH_TICKS)
                    .withStyle(ChatFormatting.GRAY));
        }
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide || !(player instanceof ServerPlayer server)) return InteractionResultHolder.success(stack);
        if (!ready(stack)) {
            server.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digitama.not_ready",
                    warmth(stack) * 100 / HATCH_TICKS), true);
            return InteractionResultHolder.fail(stack);
        }
        try {
            Pokemon baby = hatch(stack, server);
            Crests.hatched(server);
            stack.shrink(1);
            level.playSound(null, player.blockPosition(), SoundEvents.SNIFFER_EGG_HATCH, SoundSource.PLAYERS, 1F, 1.2F);
            server.displayClientMessage(Component.translatable(Digital.MOD_ID + ".digitama.hatched",
                    baby.getSpecies().getTranslatedName()).withStyle(ChatFormatting.GOLD), false);
            return InteractionResultHolder.consume(stack);
        } catch (Throwable t) {
            Digital.LOG.error("Digitama hatch failed", t);
            return InteractionResultHolder.fail(stack);
        }
    }

    static Pokemon hatch(ItemStack stack, ServerPlayer player) {
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        String species = data != null && data.copyTag().contains("species") ? data.copyTag().getString("species") : null;
        if (species == null) {
            List<com.cobblemon.mod.common.pokemon.Species> babies = new java.util.ArrayList<>();
            for (com.cobblemon.mod.common.pokemon.Species s : com.cobblemon.mod.common.api.pokemon.PokemonSpecies.INSTANCE.getImplemented()) {
                if (s.getLabels().contains(HATCH_LABEL)) babies.add(s);
            }
            species = babies.isEmpty() ? FALLBACK : babies.get(player.getRandom().nextInt(babies.size())).getResourceIdentifier().toString();
        }
        Pokemon baby = PokemonProperties.Companion.parse(species + " level=1").create();
        float rate = Cobblemon.INSTANCE.getConfig().getShinyRate();
        if (rate >= 1 && player.getRandom().nextFloat() < 1F / rate) baby.setShiny(true);
        PlayerPartyStore party = Cobblemon.INSTANCE.getStorage().getParty(player);
        if (!party.add(baby)) Cobblemon.INSTANCE.getStorage().getPC(player).add(baby);
        return baby;
    }
}
