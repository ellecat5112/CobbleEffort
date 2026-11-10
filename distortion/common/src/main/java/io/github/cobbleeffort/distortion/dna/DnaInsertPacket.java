package io.github.cobbleeffort.distortion.dna;

import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.UUIDUtil;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.UUID;

/** Client to server: put this party Pokémon (the one selected in the party bar) into the DNA machine at pos. */
public record DnaInsertPacket(BlockPos pos, UUID pokemonId) implements CustomPacketPayload {
    public static final Type<DnaInsertPacket> TYPE =
            new Type<>(ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "dna_insert"));
    public static final StreamCodec<RegistryFriendlyByteBuf, DnaInsertPacket> STREAM_CODEC =
            StreamCodec.composite(BlockPos.STREAM_CODEC, DnaInsertPacket::pos, UUIDUtil.STREAM_CODEC, DnaInsertPacket::pokemonId, DnaInsertPacket::new);

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
