package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.battles.model.PokemonBattle;
import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.item.battle.BagItem;
import com.cobblemon.mod.common.item.battle.SimpleBagItemLike;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;

/**
 * Digi-Modify cards: swiped through your Digivice mid-battle (use the card on your battling Digimon, with a Digivice
 * somewhere in your inventory) for a boost. They work like Cobblemon's X items: the swipe takes your turn and the card
 * is used up. The effects are Showdown bag-item scripts: data/cobbleeffort_digital/bag_items/digimodify.js.
 */
public class DigiModifyCard extends Item implements SimpleBagItemLike {
    private final String card;
    private final BagItem bagItem;

    public DigiModifyCard(Properties properties, String card) {
        super(properties);
        this.card = card;
        String name = "item." + Digital.MOD_ID + "." + card;
        this.bagItem = new BagItem() {
            @Override
            public String getItemName() {
                return name;
            }

            @Override
            public Item getReturnItem() {
                return Items.AIR;
            }

            @Override
            public boolean canUse(ItemStack stack, PokemonBattle battle, BattlePokemon target) {
                return target.getHealth() > 0 && Attributes.isDigimon(target.getEffectedPokemon());
            }

            @Override
            public String getShowdownInput(BattleActor actor, BattlePokemon battlePokemon, String data) {
                battlePokemon.getEffectedPokemon().incrementFriendship(1, true);
                return "digimodify " + card;
            }
        };
    }

    @Override
    public BagItem getBagItem() {
        return bagItem;
    }

    @Override
    public boolean handleInteraction(ServerPlayer player, BattlePokemon battlePokemon, ItemStack stack) {
        if (!Digivice.has(player)) {
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".card.no_digivice").withStyle(ChatFormatting.RED), true);
            return false;
        }
        if (!Attributes.isDigimon(battlePokemon.getEffectedPokemon())) {
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".use.not_digimon",
                    battlePokemon.getEffectedPokemon().getDisplayName(false)).withStyle(ChatFormatting.RED), true);
            return false;
        }
        return SimpleBagItemLike.super.handleInteraction(player, battlePokemon, stack);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
        lines.add(Component.translatable(getDescriptionId() + ".tooltip").withStyle(ChatFormatting.AQUA));
        lines.add(Component.translatable(Digital.MOD_ID + ".card.how").withStyle(ChatFormatting.GRAY));
    }
}
