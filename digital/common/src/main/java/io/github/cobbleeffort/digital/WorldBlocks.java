package io.github.cobbleeffort.digital;

import com.mojang.serialization.MapCodec;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;

/** The Digital World's interactive blocks: the Ancient Terminal (the way in and out) and the Digitama Cradle. */
public final class WorldBlocks {
    private WorldBlocks() {
    }

    /** Use it holding a Digivice: to the Digital World, or home from it. */
    public static class Terminal extends net.minecraft.world.level.block.HorizontalDirectionalBlock {
        public Terminal(Properties properties) {
            super(properties);
            registerDefaultState(stateDefinition.any().setValue(FACING, net.minecraft.core.Direction.NORTH));
        }

        @Override
        protected MapCodec<? extends net.minecraft.world.level.block.HorizontalDirectionalBlock> codec() {
            return simpleCodec(Terminal::new);
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(FACING);
        }

        @Override
        public BlockState getStateForPlacement(net.minecraft.world.item.context.BlockPlaceContext ctx) {
            return defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
        }

        @Override
        protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                                  InteractionHand hand, BlockHitResult hit) {
            if (!(stack.getItem() instanceof Digivice)) return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
            if (!level.isClientSide && player instanceof ServerPlayer sp) DigitalWorld.travel(sp);
            return ItemInteractionResult.sidedSuccess(level.isClientSide);
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            if (!level.isClientSide) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".world.terminal_needs_digivice").withStyle(ChatFormatting.AQUA), true);
            }
            return InteractionResult.sidedSuccess(level.isClientSide);
        }

        @Override
        public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
            if (random.nextInt(2) == 0) {
                level.addParticle(DigitalWorld.CYAN, pos.getX() + 0.2 + random.nextDouble() * 0.6, pos.getY() + 1.1,
                        pos.getZ() + 0.2 + random.nextDouble() * 0.6, 0, 0.02, 0);
            }
        }
    }

    /**
     * A Digitama cradle (Primary Village): holds an egg ("egg" state). Trade for it with 4 Digi-Meat (use them on the
     * cradle), or, out in the ruins, rescue it for free. An empty cradle lays a new egg now and then (random ticks).
     */
    public static class Cradle extends Block {
        public static final BooleanProperty EGG = BooleanProperty.create("egg");
        public static final int MEAT_PRICE = 4;
        private final boolean free;

        public Cradle(Properties properties, boolean free) {
            super(properties);
            this.free = free;
            registerDefaultState(stateDefinition.any().setValue(EGG, true));
        }

        @Override
        protected MapCodec<? extends Block> codec() {
            return simpleCodec(p -> new Cradle(p, free));
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(EGG);
        }

        @Override
        protected boolean isRandomlyTicking(BlockState state) {
            return !free;
        }

        /** Primary Village cradles lay new eggs, and keep an Elecmon guard about. */
        @Override
        protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            if (!state.getValue(EGG) && random.nextInt(24) == 0) level.setBlock(pos, state.setValue(EGG, true), 3);
            if (random.nextInt(6) == 0) Guards.ensure(level, pos);
        }

        @Override
        protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                                  InteractionHand hand, BlockHitResult hit) {
            if (!state.getValue(EGG) || free || !stack.is(Digital.DIGIMEAT.get())) return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
            if (stack.getCount() < MEAT_PRICE && !player.getAbilities().instabuild) {
                if (!level.isClientSide) player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".cradle.price", MEAT_PRICE), true);
                return ItemInteractionResult.sidedSuccess(level.isClientSide);
            }
            if (!level.isClientSide) {
                if (!player.getAbilities().instabuild) stack.shrink(MEAT_PRICE);
                take(state, level, pos, player, "traded");
            }
            return ItemInteractionResult.sidedSuccess(level.isClientSide);
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            if (level.isClientSide) return InteractionResult.SUCCESS;
            if (!state.getValue(EGG)) {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".cradle.empty"), true);
            } else if (free) {
                take(state, level, pos, player, "rescued");
            } else {
                player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".cradle.price", MEAT_PRICE), true);
            }
            return InteractionResult.CONSUME;
        }

        private static void take(BlockState state, Level level, BlockPos pos, Player player, String how) {
            level.setBlock(pos, state.setValue(EGG, false), 3);
            ItemStack egg = new ItemStack(Digital.DIGITAMA.get());
            if (!player.getInventory().add(egg)) player.drop(egg, false);
            level.playSound(null, pos, SoundEvents.SNIFFER_EGG_PLOP, SoundSource.BLOCKS, 1F, 1.2F);
            ((ServerLevel) level).sendParticles(ParticleTypes.HAPPY_VILLAGER, pos.getX() + 0.5, pos.getY() + 0.8, pos.getZ() + 0.5, 8, 0.3, 0.2, 0.3, 0);
            player.displayClientMessage(Component.translatable(Digital.MOD_ID + ".cradle." + how).withStyle(ChatFormatting.GOLD), true);
        }
    }
}
