package io.github.cobbleeffort.distortion.dna;

import com.mojang.serialization.MapCodec;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.BlockHitResult;
import org.jetbrains.annotations.Nullable;

/**
 * The DNA Analyzer and the DNA Purifier: placed right beside the DNA machine (either half), they let it take Galar's
 * mixed fossils. The Analyzer reads the DNA of whatever is in the tank; the Purifier (use: pick which of the two pure
 * forms to make; sneak + use: purify, which needs the Analyzer too) turns a mixed fossil into a pure one.
 * Shadow Pokémon will be purified here too once they exist.
 */
public class DnaStationBlock extends HorizontalDirectionalBlock {
    private final boolean purifier;

    public DnaStationBlock(Properties properties, boolean purifier) {
        super(properties);
        this.purifier = purifier;
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
    }

    @Override
    protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
        return simpleCodec(p -> new DnaStationBlock(p, purifier));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Nullable
    @Override
    public BlockState getStateForPlacement(BlockPlaceContext ctx) {
        return defaultBlockState().setValue(FACING, ctx.getHorizontalDirection().getOpposite());
    }

    @Nullable
    static DnaMachineBlockEntity findMachine(Level level, BlockPos pos) {
        for (Direction d : Direction.Plane.HORIZONTAL) {
            BlockPos p = pos.relative(d);
            BlockState s = level.getBlockState(p);
            if (s.getBlock() instanceof DnaMachineBlock) return DnaMachineBlock.machine(level, p, s);
        }
        return null;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        if (!(player instanceof ServerPlayer sp)) return InteractionResult.PASS;
        DnaMachineBlockEntity machine = findMachine(level, pos);
        if (machine == null) {
            sp.displayClientMessage(Component.translatable(Distortion.MOD_ID + ".dna.station.no_machine"), true);
            return InteractionResult.CONSUME;
        }
        try {
            if (!purifier) machine.analyze(sp);
            else if (sp.isShiftKeyDown()) machine.startPurify(sp);
            else machine.cycleTarget(sp);
        } catch (Throwable t) {
            Distortion.LOG.error("The DNA {} failed", purifier ? "Purifier" : "Analyzer", t);
        }
        return InteractionResult.CONSUME;
    }
}
