package io.github.cobbleeffort.kanto;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

/**
 * A region's portal block (the bell, the statue, the boarded doorway, the wardrobe, the giant Poké Ball, the telescope,
 * the engraved bark, the academy PC): using it takes you to that region's dimension, or home again from inside it.
 * Four shapes of block: plain, facing, two blocks tall (facing), and multi-part (the Poké Ball's colours).
 */
public final class RegionPortalBlock {
    private RegionPortalBlock() {
    }

    static InteractionResult use(Region region, SoundEvent sound, Level level, BlockPos pos, Player player) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        if (sound != null) level.playSound(null, pos, sound, SoundSource.BLOCKS, 1F, 1F);
        if (player instanceof ServerPlayer serverPlayer) serverPlayer.server.execute(() -> KantoTravel.travel(serverPlayer, region));
        return InteractionResult.CONSUME;
    }

    /** A plain portal block (optionally not a full cube). */
    public static class Plain extends Block {
        final Region region;
        final SoundEvent sound;
        final VoxelShape shape;

        public Plain(Region region, SoundEvent sound, VoxelShape shape, Properties properties) {
            super(properties);
            this.region = region;
            this.sound = sound;
            this.shape = shape == null ? Shapes.block() : shape;
        }

        @Override
        protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
            return shape;
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            return use(region, sound, level, pos, player);
        }
    }

    /** A portal block that faces the way it was placed. */
    public static class Facing extends HorizontalDirectionalBlock {
        final Region region;
        final SoundEvent sound;
        final VoxelShape shape;

        public Facing(Region region, SoundEvent sound, VoxelShape shape, Properties properties) {
            super(properties);
            this.region = region;
            this.sound = sound;
            this.shape = shape == null ? Shapes.block() : shape;
            registerDefaultState(defaultState(stateDefinition.any().setValue(FACING, Direction.NORTH)));
        }

        BlockState defaultState(BlockState state) {
            return state;
        }

        @Override
        protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
            return MapCodec.unit(this);
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(FACING);
        }

        @Nullable
        @Override
        public BlockState getStateForPlacement(BlockPlaceContext context) {
            return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
        }

        @Override
        protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
            return shape;
        }

        @Override
        protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
            return use(region, sound, level, pos, player);
        }
    }

    /** A two-block-tall portal (the boarded doorway, the wardrobe): breaking either half breaks both. */
    public static class Tall extends Facing {
        public static final EnumProperty<DoubleBlockHalf> HALF = BlockStateProperties.DOUBLE_BLOCK_HALF;

        public Tall(Region region, SoundEvent sound, Properties properties) {
            super(region, sound, null, properties);
        }

        @Override
        BlockState defaultState(BlockState state) {
            return state.setValue(HALF, DoubleBlockHalf.LOWER);
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(FACING, HALF);
        }

        @Nullable
        @Override
        public BlockState getStateForPlacement(BlockPlaceContext context) {
            BlockPos pos = context.getClickedPos();
            Level level = context.getLevel();
            if (pos.getY() >= level.getMaxBuildHeight() - 1 || !level.getBlockState(pos.above()).canBeReplaced(context)) return null;
            return super.getStateForPlacement(context).setValue(HALF, DoubleBlockHalf.LOWER);
        }

        @Override
        public void setPlacedBy(Level level, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
            level.setBlock(pos.above(), state.setValue(HALF, DoubleBlockHalf.UPPER), 3);
        }

        @Override
        protected BlockState updateShape(BlockState state, Direction direction, BlockState neighbour, LevelAccessor level,
                                         BlockPos pos, BlockPos neighbourPos) {
            DoubleBlockHalf half = state.getValue(HALF);
            boolean towardsOther = (half == DoubleBlockHalf.LOWER) == (direction == Direction.UP);
            if (direction.getAxis() == Direction.Axis.Y && towardsOther
                    && !(neighbour.is(this) && neighbour.getValue(HALF) != half)) {
                return Blocks.AIR.defaultBlockState();
            }
            return super.updateShape(state, direction, neighbour, level, pos, neighbourPos);
        }
    }

    /** The giant Poké Ball's shell: one block in four colours. */
    public enum Part implements StringRepresentable {
        RED("red"), WHITE("white"), BLACK("black"), BUTTON("button");
        private final String name;

        Part(String name) {
            this.name = name;
        }

        @Override
        public String getSerializedName() {
            return name;
        }
    }

    public static class Parts extends Plain {
        public static final EnumProperty<Part> PART = EnumProperty.create("part", Part.class);

        public Parts(Region region, SoundEvent sound, Properties properties) {
            super(region, sound, null, properties);
            registerDefaultState(stateDefinition.any().setValue(PART, Part.RED));
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(PART);
        }
    }
}
