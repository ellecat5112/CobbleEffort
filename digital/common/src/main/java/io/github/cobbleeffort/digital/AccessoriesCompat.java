package io.github.cobbleeffort.digital;

import io.wispforest.accessories.api.AccessoriesCapability;
import io.wispforest.accessories.api.slot.SlotEntryReference;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/** Only loaded when Accessories is installed (Crests.findTag checks): the Tag worn in its necklace slot. */
final class AccessoriesCompat {
    private AccessoriesCompat() {
    }

    static ItemStack worn(Player player, Item item) {
        AccessoriesCapability cap = AccessoriesCapability.get(player);
        if (cap == null) return ItemStack.EMPTY;
        SlotEntryReference ref = cap.getFirstEquipped(item);
        return ref == null ? ItemStack.EMPTY : ref.stack();
    }
}
