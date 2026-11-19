package io.github.cobbleeffort.digital;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Digimon World's training gym: punching bag, treadmill, training waterfall, meditation mat and target dummy. Using
 * one starts a timing game for your partner (see Training); a good hit raises that stat's EVs.
 */
public class TrainingBlock extends HorizontalDirectionalBlock {
    private final Training.Kind kind;
    private final VoxelShape shape;

    public TrainingBlock(Properties properties, Training.Kind kind, VoxelShape shape) {
        super(properties);
        this.kind = kind;
        this.shape = shape;
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
    }

    public Training.Kind kind() {
        return kind;
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
        return simpleCodec(p -> new TrainingBlock(p, kind, shape));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        return defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return shape;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        if (player instanceof ServerPlayer sp) Training.press(sp, pos, kind);
        return InteractionResult.CONSUME;
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (kind == Training.Kind.WATERFALL) {
            for (int i = 0; i < 3; i++) {
                level.addParticle(ParticleTypes.FALLING_WATER, pos.getX() + 0.15 + random.nextDouble() * 0.7, pos.getY() + 0.95,
                        pos.getZ() + 0.15 + random.nextDouble() * 0.7, 0, 0, 0);
            }
            if (random.nextInt(4) == 0) {
                level.addParticle(ParticleTypes.SPLASH, pos.getX() + random.nextDouble(), pos.getY() + 0.1,
                        pos.getZ() + random.nextDouble(), 0, 0.1, 0);
            }
        }
    }
}
