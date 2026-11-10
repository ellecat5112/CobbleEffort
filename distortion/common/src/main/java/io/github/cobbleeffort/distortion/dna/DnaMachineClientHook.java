package io.github.cobbleeffort.distortion.dna;

import net.minecraft.core.BlockPos;

import java.util.function.Consumer;

/** The client's half of "put the selected Pokémon in" (set by the client init, so the block never loads client classes). */
public final class DnaMachineClientHook {
    static Consumer<BlockPos> sender = pos -> {
    };

    private DnaMachineClientHook() {
    }

    public static void setSender(Consumer<BlockPos> s) {
        sender = s;
    }

    static void sendInsert(BlockPos pos) {
        sender.accept(pos);
    }
}
