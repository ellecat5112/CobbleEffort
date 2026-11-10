package io.github.cobbleeffort.distortion.dna;

import com.mojang.serialization.MapCodec;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.block.state.properties.DoubleBlockHalf;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

/**
 * The DNA machine: a two-block-tall glass tank (the cloning tank Mewtwo comes from in the first movie). Fill it with
 * Mew DNA (click with it; sneak to pour the whole stack), then click it with Mew selected in your party: Mew goes in,
 * and five minutes later it has become Mewtwo. Click again to take Mewtwo out. The lower half holds the block entity.
 */
public class DnaMachineBlock extends BaseEntityBlock {
    public static final MapCodec<DnaMachineBlock> CODEC = simpleCodec(DnaMachineBlock::new);
    public static final EnumProperty<DoubleBlockHalf> HALF = BlockStateProperties.DOUBLE_BLOCK_HALF;
    public static final DirectionProperty FACING = HorizontalDirectionalBlock.FACING;
    private static final VoxelShape LOWER = Shapes.or(Block.box(0, 0, 0, 16, 6, 16), Block.box(1.5, 6, 1.5, 14.5, 16, 14.5));
    private static final VoxelShape UPPER = Shapes.or(Block.box(1.5, 0, 1.5, 14.5, 10, 14.5), Block.box(0, 10, 0, 16, 16, 16));

    public DnaMachineBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(HALF, DoubleBlockHalf.LOWER).setValue(FACING, Direction.NORTH));
    }

    @Override
    protected MapCodec<? extends BaseEntityBlock> codec() {
        return CODEC;
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(HALF, FACING);
    }

    @Override
    protected RenderShape getRenderShape(BlockState state) {
        return RenderShape.MODEL;
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return state.getValue(HALF) == DoubleBlockHalf.LOWER ? LOWER : UPPER;
    }

    // --- the two halves (like a door) ---------------------------------------------------------------------------
    @Nullable
    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        BlockPos pos = context.getClickedPos();
        Level level = context.getLevel();
        if (pos.getY() >= level.getMaxBuildHeight() - 1 || !level.getBlockState(pos.above()).canBeReplaced(context)) return null;
        return defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
    }

    @Override
    public void setPlacedBy(Level level, BlockPos pos, BlockState state, @Nullable LivingEntity placer, ItemStack stack) {
        level.setBlock(pos.above(), state.setValue(HALF, DoubleBlockHalf.UPPER), 3);
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        if (state.getValue(HALF) == DoubleBlockHalf.LOWER) return true;
        BlockState below = level.getBlockState(pos.below());
        return below.is(this) && below.getValue(HALF) == DoubleBlockHalf.LOWER;
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighbor, LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        DoubleBlockHalf half = state.getValue(HALF);
        if (direction.getAxis() == Direction.Axis.Y && (half == DoubleBlockHalf.LOWER) == (direction == Direction.UP)) {
            return neighbor.is(this) && neighbor.getValue(HALF) != half ? state : Blocks.AIR.defaultBlockState();
        }
        return super.updateShape(state, direction, neighbor, level, pos, neighborPos);
    }

    @Override
    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
        if (!level.isClientSide && state.getValue(HALF) == DoubleBlockHalf.UPPER) {
            BlockPos below = pos.below();
            BlockState lower = level.getBlockState(below);
            if (lower.is(this) && lower.getValue(HALF) == DoubleBlockHalf.LOWER) {
                if (!player.isCreative()) Block.dropResources(lower, level, below, level.getBlockEntity(below), player, player.getMainHandItem());
                level.setBlock(below, Blocks.AIR.defaultBlockState(), 35);
            }
        }
        return super.playerWillDestroy(level, pos, state, player);
    }

    /** Can't be broken while a Pokémon is inside (take it out first). */
    @Override
    protected float getDestroyProgress(BlockState state, Player player, BlockGetter level, BlockPos pos) {
        DnaMachineBlockEntity machine = machine(level, pos, state);
        if (machine != null && machine.occupied()) return 0F;
        return super.getDestroyProgress(state, player, level, pos);
    }

    @Override
    protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean moved) {
        if (!state.is(newState.getBlock()) && state.getValue(HALF) == DoubleBlockHalf.LOWER
                && level.getBlockEntity(pos) instanceof DnaMachineBlockEntity machine) {
            machine.dropContents();
        }
        super.onRemove(state, level, pos, newState, moved);
    }

    // --- block entity -----------------------------------------------------------------------------------------------
    @Nullable
    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return state.getValue(HALF) == DoubleBlockHalf.LOWER ? new DnaMachineBlockEntity(pos, state) : null;
    }

    @Nullable
    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide || state.getValue(HALF) != DoubleBlockHalf.LOWER) return null;
        return createTickerHelper(type, Distortion.DNA_MACHINE_ENTITY.get(), (l, p, s, be) -> be.serverTick());
    }

    @Nullable
    static DnaMachineBlockEntity machine(BlockGetter level, BlockPos pos, BlockState state) {
        BlockPos lower = state.getValue(HALF) == DoubleBlockHalf.LOWER ? pos : pos.below();
        return level.getBlockEntity(lower) instanceof DnaMachineBlockEntity machine ? machine : null;
    }

    // --- using it ---------------------------------------------------------------------------------------------------
    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                              InteractionHand hand, BlockHitResult hit) {
        if (!stack.is(Distortion.MEW_DNA.get())) return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        DnaMachineBlockEntity machine = machine(level, pos, state);
        if (machine == null) return ItemInteractionResult.FAIL;
        if (machine.occupied() || machine.full()) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;     // full: the hand click puts Mew in
        }
        if (!level.isClientSide) {
            int poured = machine.fill(player.isShiftKeyDown() ? stack.getCount() : 1);
            if (!player.isCreative()) stack.shrink(poured);
            level.playSound(null, pos, SoundEvents.BUCKET_EMPTY, SoundSource.BLOCKS, 0.8F, 1.3F);
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.filled", machine.fillLevel(),
                    DnaMachineBlockEntity.CAPACITY), true);
        }
        return ItemInteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        DnaMachineBlockEntity machine = machine(level, pos, state);
        if (machine == null) return InteractionResult.PASS;
        if (level.isClientSide) {
            // the party selection lives on the client: tell the server which Pokémon to put in
            if (!machine.occupied() && machine.full()) DnaMachineClientHook.sendInsert(machine.getBlockPos());
            return InteractionResult.SUCCESS;
        }
        if (!(player instanceof ServerPlayer serverPlayer)) return InteractionResult.PASS;
        if (machine.occupied()) {
            machine.retrieve(serverPlayer);
        } else if (!machine.full()) {
            player.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.needs",
                    DnaMachineBlockEntity.CAPACITY - machine.fillLevel()), true);
        }
        return InteractionResult.CONSUME;
    }

    /** Bubbles rising through the tank while it works. */
    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (state.getValue(HALF) != DoubleBlockHalf.LOWER) return;
        DnaMachineBlockEntity machine = machine(level, pos, state);
        if (machine == null || machine.fillLevel() == 0) return;
        for (int i = 0; i < (machine.occupied() ? 3 : 1); i++) {
            level.addParticle(ParticleTypes.GLOW, pos.getX() + 0.3 + random.nextDouble() * 0.4,
                    pos.getY() + 0.45, pos.getZ() + 0.3 + random.nextDouble() * 0.4, 0, 0.04, 0);
        }
    }
}
