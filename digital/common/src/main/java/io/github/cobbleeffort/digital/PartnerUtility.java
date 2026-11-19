package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.types.ElementalTypes;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import dev.architectury.event.EventResult;
import dev.architectury.event.events.common.BlockEvent;
import dev.architectury.event.events.common.InteractionEvent;
import dev.architectury.event.events.common.TickEvent;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.BlastFurnaceMenu;
import net.minecraft.world.inventory.ChestMenu;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleRecipeInput;
import net.minecraft.world.level.block.state.BlockState;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

/**
 * Out-of-battle jobs for your sent-out Digimon (sneak and use an empty hand on your own):
 * * Storage carriers: big Digimon (Adult and up) wearing a Chest Harness (use the harness on them) carry a double chest.
 * * Portable forges: Fire Digimon open a fuel-free blast furnace (each player's own; it keeps smelting while you're away).
 * * Mining partners (Ground, Rock and Steel Digimon, label digimon_utility_miner or those types): while one is out within
 *   6 blocks, the stone and ore you mine with a pickaxe also takes the block behind it and the two beside it (a 3-wide
 *   tunnel). It respects claims: the blocks are broken as you.
 */
public final class PartnerUtility {
    static final String HARNESS = "cobbleeffort_digital_harness", CHEST = "cobbleeffort_digital_chest";
    private static final Map<UUID, Forge> FORGES = new HashMap<>();
    private static boolean mining;

    private PartnerUtility() {
    }

    static boolean miner(Pokemon p) {
        if (!Attributes.isDigimon(p)) return false;
        if (p.getSpecies().getLabels().contains("digimon_utility_miner")) return true;
        var t = ElementalTypes.INSTANCE;
        return p.getPrimaryType() == t.getGROUND() || p.getPrimaryType() == t.getROCK() || p.getPrimaryType() == t.getSTEEL();
    }

    static boolean fiery(Pokemon p) {
        var fire = ElementalTypes.INSTANCE.getFIRE();
        return Attributes.isDigimon(p) && (p.getPrimaryType() == fire || p.getSecondaryType() == fire);
    }

    static boolean big(Pokemon p) {
        return Attributes.isDigimon(p) && Digivice.stageIndex(p.getSpecies()) >= 3;
    }

    /** Use it on your own big Digimon to give it a double chest. */
    public static class HarnessItem extends TooltipItem {
        public HarnessItem(Properties properties) {
            super(properties);
        }

        @Override
        public net.minecraft.world.InteractionResult interactLivingEntity(ItemStack stack, Player player, net.minecraft.world.entity.LivingEntity target,
                                                                          net.minecraft.world.InteractionHand hand) {
            if (player.level().isClientSide) return net.minecraft.world.InteractionResult.SUCCESS;
            Pokemon p = PartnerUse.own(player, target, true);
            if (p == null) return net.minecraft.world.InteractionResult.FAIL;
            if (!big(p)) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".harness.too_small", p.getDisplayName(false)), true);
                return net.minecraft.world.InteractionResult.FAIL;
            }
            if (p.getPersistentData().getBoolean(HARNESS)) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".harness.already", p.getDisplayName(false)), true);
                return net.minecraft.world.InteractionResult.FAIL;
            }
            p.getPersistentData().putBoolean(HARNESS, true);
            p.onChange(null);
            if (!player.getAbilities().instabuild) stack.shrink(1);
            player.level().playSound(null, target.blockPosition(), SoundEvents.HORSE_SADDLE, SoundSource.PLAYERS, 1F, 1F);
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".harness.on", p.getDisplayName(false)).withStyle(ChatFormatting.GREEN), true);
            return net.minecraft.world.InteractionResult.CONSUME;
        }
    }

    static void openChest(ServerPlayer player, Pokemon p) {
        SimpleContainer box = new SimpleContainer(54);
        HolderLookup.Provider reg = player.registryAccess();
        NonNullList<ItemStack> list = NonNullList.withSize(54, ItemStack.EMPTY);
        ContainerHelper.loadAllItems(p.getPersistentData().getCompound(CHEST), list, reg);
        for (int i = 0; i < 54; i++) box.setItem(i, list.get(i));
        box.addListener(c -> {
            NonNullList<ItemStack> out = NonNullList.withSize(54, ItemStack.EMPTY);
            for (int i = 0; i < 54; i++) out.set(i, box.getItem(i));
            CompoundTag t = new CompoundTag();
            ContainerHelper.saveAllItems(t, out, reg);
            p.getPersistentData().put(CHEST, t);
            p.onChange(null);
        });
        player.openMenu(new SimpleMenuProvider((id, inv, pl) -> ChestMenu.sixRows(id, inv, box),
                Component.translatable(Digital.MOD_ID + ".harness.title", p.getDisplayName(false))));
    }

    /** A player's portable forge: a blast furnace's three slots, smelting by itself (no fuel). */
    static final class Forge {
        final SimpleContainer slots = new SimpleContainer(3);
        final SimpleContainerData data = new SimpleContainerData(4);
        int progress;

        void tick(ServerLevel level) {
            ItemStack in = slots.getItem(0);
            data.set(0, 100);
            data.set(1, 100);
            if (in.isEmpty()) {
                progress = 0;
                data.set(2, 0);
                return;
            }
            Optional<net.minecraft.world.item.crafting.RecipeHolder<net.minecraft.world.item.crafting.BlastingRecipe>> r =
                    level.getRecipeManager().getRecipeFor(RecipeType.BLASTING, new SingleRecipeInput(in), level);
            if (r.isEmpty()) {
                progress = 0;
                return;
            }
            ItemStack result = r.get().value().assemble(new SingleRecipeInput(in), level.registryAccess());
            ItemStack out = slots.getItem(2);
            if (!out.isEmpty() && (!ItemStack.isSameItemSameComponents(out, result) || out.getCount() + result.getCount() > out.getMaxStackSize())) return;
            progress += 2;
            data.set(2, progress);
            data.set(3, 100);
            if (progress >= 100) {
                progress = 0;
                in.shrink(1);
                if (out.isEmpty()) slots.setItem(2, result.copy());
                else out.grow(result.getCount());
            }
        }
    }

    static void init() {
        InteractionEvent.INTERACT_ENTITY.register((player, entity, hand) -> {
            if (!(entity instanceof PokemonEntity e) || !player.isShiftKeyDown() || !player.getItemInHand(hand).isEmpty()) return EventResult.pass();
            Pokemon p = e.getPokemon();
            if (!player.getUUID().equals(p.getOwnerUUID()) || e.isBattling()) return EventResult.pass();
            if (player.level().isClientSide) return EventResult.interruptTrue();
            ServerPlayer sp = (ServerPlayer) player;
            if (p.getPersistentData().getBoolean(HARNESS)) {
                openChest(sp, p);
                return EventResult.interruptTrue();
            }
            if (fiery(p)) {
                Forge f = FORGES.computeIfAbsent(sp.getUUID(), k -> new Forge());
                sp.openMenu(new SimpleMenuProvider((id, inv, pl) -> new BlastFurnaceMenu(id, inv, f.slots, f.data),
                        Component.translatable(Digital.MOD_ID + ".forge.title", p.getDisplayName(false))));
                return EventResult.interruptTrue();
            }
            return EventResult.pass();
        });
        TickEvent.SERVER_POST.register(server -> {
            for (Map.Entry<UUID, Forge> en : FORGES.entrySet()) {
                ServerPlayer p = server.getPlayerList().getPlayer(en.getKey());
                if (p != null) en.getValue().tick(p.serverLevel());
            }
        });
        BlockEvent.BREAK.register((level, pos, state, player, xp) -> {
            if (mining || !(player instanceof ServerPlayer sp) || !(level instanceof ServerLevel sl)) return EventResult.pass();
            if (!sp.getMainHandItem().is(net.minecraft.tags.ItemTags.PICKAXES) || !(state.is(BlockTags.BASE_STONE_OVERWORLD) || isOre(state))) {
                return EventResult.pass();
            }
            boolean helper = !sl.getEntitiesOfClass(PokemonEntity.class, sp.getBoundingBox().inflate(6),
                    e -> sp.getUUID().equals(e.getPokemon().getOwnerUUID()) && miner(e.getPokemon()) && !e.isBattling()).isEmpty();
            if (!helper) return EventResult.pass();
            Direction face = Direction.orderedByNearest(sp)[0];
            Direction side = face.getAxis() == Direction.Axis.Y ? sp.getDirection().getClockWise() : face.getClockWise();
            mining = true;
            try {
                for (BlockPos p : Set.of(pos.relative(face), pos.relative(side), pos.relative(side.getOpposite()))) {
                    BlockState s = sl.getBlockState(p);
                    if (s.is(BlockTags.BASE_STONE_OVERWORLD) || isOre(s)) sp.gameMode.destroyBlock(p);
                }
            } finally {
                mining = false;
            }
            return EventResult.pass();
        });
    }

    static boolean isOre(BlockState s) {
        return s.is(BlockTags.COAL_ORES) || s.is(BlockTags.IRON_ORES) || s.is(BlockTags.COPPER_ORES) || s.is(BlockTags.GOLD_ORES)
                || s.is(BlockTags.REDSTONE_ORES) || s.is(BlockTags.LAPIS_ORES) || s.is(BlockTags.DIAMOND_ORES) || s.is(BlockTags.EMERALD_ORES);
    }
}
