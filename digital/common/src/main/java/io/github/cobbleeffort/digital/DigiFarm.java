package io.github.cobbleeffort.digital;

import com.cobblemon.mod.common.api.pokemon.experience.SidemodExperienceSource;
import com.cobblemon.mod.common.api.pokemon.stats.SidemodEvSource;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.mojang.serialization.MapCodec;
import io.github.cobbleeffort.digital.Attributes.Attribute;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.ContainerHelper;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.DispenserMenu;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;

import java.util.List;

/**
 * The Digi-Farm Terminal (Digimon World's farm, built on Cobblemon's own Pasture block: Pokémon you put out to pasture
 * from your PC really wander there). Every minute, each Pokémon tethered to a pasture within 12 blocks of the terminal
 * works, depending on the farm goods within 6 blocks of the terminal:
 * training gym blocks: +EXP and +2 EVs in that block's stat; bookshelves: +EXP; Digi-Meat crops / composters: a Digi-Meat;
 * circuit blocks or server casings: an attribute fragment (Digimon only, their attribute); chests: something scavenged.
 * What they make goes into the terminal (9 slots; use it to open).
 */
public final class DigiFarm {
    static final int WORK_TICKS = 1200, PASTURE_RANGE = 12, GOODS_RANGE = 6;

    private DigiFarm() {
    }

    public static class TerminalBlock extends BaseEntityBlock {
        public TerminalBlock(Properties properties) {
            super(properties);
        }

        @Override
        protected MapCodec<? extends BaseEntityBlock> codec() {
            return simpleCodec(TerminalBlock::new);
        }

        @Override
        protected RenderShape getRenderShape(BlockState state) {
            return RenderShape.MODEL;
        }

        @Override
        public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
            return new TerminalEntity(pos, state);
        }

        @Override
        public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
            return level.isClientSide || type != Digital.FARM_ENTITY.get() ? null
                    : (l, p, s, be) -> ((TerminalEntity) be).tick((ServerLevel) l);
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            if (level.isClientSide) return InteractionResult.SUCCESS;
            if (level.getBlockEntity(pos) instanceof TerminalEntity t) {
                player.openMenu(new SimpleMenuProvider((id, inv, p) -> new DispenserMenu(id, inv, t),
                        Component.translatable("block." + Digital.MOD_ID + ".digi_farm_terminal")));
            }
            return InteractionResult.CONSUME;
        }

        @Override
        protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean moved) {
            if (!state.is(newState.getBlock()) && level.getBlockEntity(pos) instanceof TerminalEntity t) {
                net.minecraft.world.Containers.dropContents(level, pos, t);
            }
            super.onRemove(state, level, pos, newState, moved);
        }
    }

    public static class TerminalEntity extends BlockEntity implements net.minecraft.world.Container {
        private final NonNullList<ItemStack> items = NonNullList.withSize(9, ItemStack.EMPTY);
        private int timer;

        public TerminalEntity(BlockPos pos, BlockState state) {
            super(Digital.FARM_ENTITY.get(), pos, state);
        }

        void tick(ServerLevel level) {
            if (++timer < WORK_TICKS) return;
            timer = 0;
            Goods goods = Goods.around(level, worldPosition);
            List<PokemonEntity> workers = level.getEntitiesOfClass(PokemonEntity.class, new AABB(worldPosition).inflate(PASTURE_RANGE),
                    e -> e.getTethering() != null);
            for (PokemonEntity e : workers) work(level, e, goods);
        }

        void work(ServerLevel level, PokemonEntity e, Goods g) {
            Pokemon p = e.getPokemon();
            int xp = 4 * g.training + 3 * g.books;
            if (xp > 0) p.addExperience(new SidemodExperienceSource(Digital.MOD_ID), Math.min(60, xp));
            if (g.trainingKind != null) p.getEvs().add(g.trainingKind, 2, new SidemodEvSource(Digital.MOD_ID, p));
            if (g.meat > 0 && level.random.nextInt(3) == 0) put(new ItemStack(Digital.DIGIMEAT.get()));
            if (g.circuits > 0 && Attributes.isDigimon(p) && level.random.nextInt(2) == 0) {
                Attribute a = Attributes.of(p);
                if (a == null || !a.triangle()) a = Attribute.values()[level.random.nextInt(3)];
                put(new ItemStack(Digital.FRAGMENTS.get(a).get()));
            }
            if (g.chests > 0 && level.random.nextInt(4) == 0) {
                ItemStack[] finds = {new ItemStack(Items.IRON_NUGGET, 3), new ItemStack(Items.REDSTONE, 2), new ItemStack(Items.GLOWSTONE_DUST, 2),
                        new ItemStack(Digital.SUPER_CARROT.get()), new ItemStack(Items.EMERALD), new ItemStack(Digital.RAW_CHROME.get())};
                put(finds[level.random.nextInt(level.random.nextInt(8) == 0 ? finds.length : finds.length - 1)].copy());
            }
            level.sendParticles(ParticleTypes.HAPPY_VILLAGER, e.getX(), e.getY() + e.getBbHeight(), e.getZ(), 3, 0.3, 0.2, 0.3, 0);
        }

        void put(ItemStack stack) {
            for (int i = 0; i < items.size() && !stack.isEmpty(); i++) {
                ItemStack in = items.get(i);
                if (in.isEmpty()) {
                    items.set(i, stack.copy());
                    stack.setCount(0);
                } else if (ItemStack.isSameItemSameComponents(in, stack) && in.getCount() < in.getMaxStackSize()) {
                    int move = Math.min(stack.getCount(), in.getMaxStackSize() - in.getCount());
                    in.grow(move);
                    stack.shrink(move);
                }
            }
            setChanged();
        }

        @Override
        protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.saveAdditional(tag, registries);
            ContainerHelper.saveAllItems(tag, items, registries);
            tag.putInt("timer", timer);
        }

        @Override
        protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
            super.loadAdditional(tag, registries);
            ContainerHelper.loadAllItems(tag, items, registries);
            timer = tag.getInt("timer");
        }

        @Override
        public int getContainerSize() {
            return items.size();
        }

        @Override
        public boolean isEmpty() {
            return items.stream().allMatch(ItemStack::isEmpty);
        }

        @Override
        public ItemStack getItem(int slot) {
            return items.get(slot);
        }

        @Override
        public ItemStack removeItem(int slot, int amount) {
            ItemStack r = ContainerHelper.removeItem(items, slot, amount);
            setChanged();
            return r;
        }

        @Override
        public ItemStack removeItemNoUpdate(int slot) {
            return ContainerHelper.takeItem(items, slot);
        }

        @Override
        public void setItem(int slot, ItemStack stack) {
            items.set(slot, stack);
            setChanged();
        }

        @Override
        public boolean stillValid(Player player) {
            return player.distanceToSqr(worldPosition.getCenter()) < 64;
        }

        @Override
        public void clearContent() {
            items.clear();
        }
    }

    /** The farm goods round the terminal. */
    static final class Goods {
        int training, books, meat, circuits, chests;
        com.cobblemon.mod.common.api.pokemon.stats.Stat trainingKind;

        static Goods around(Level level, BlockPos at) {
            Goods g = new Goods();
            for (BlockPos p : BlockPos.betweenClosed(at.offset(-GOODS_RANGE, -2, -GOODS_RANGE), at.offset(GOODS_RANGE, 3, GOODS_RANGE))) {
                BlockState s = level.getBlockState(p);
                Block b = s.getBlock();
                if (b instanceof TrainingBlock t) {
                    g.training++;
                    g.trainingKind = t.kind().stat;
                } else if (b == Blocks.BOOKSHELF) {
                    g.books = Math.min(10, g.books + 1);
                } else if (b == Digital.DIGIMEAT_CROP.get() || b == Blocks.COMPOSTER) {
                    g.meat++;
                } else if (b == Digital.CIRCUIT_BLOCK.get() || b == Digital.SERVER_CASING.get()) {
                    g.circuits++;
                } else if (b == Blocks.CHEST || b == Blocks.BARREL) {
                    g.chests++;
                }
            }
            g.training = Math.min(5, g.training);
            return g;
        }
    }
}
