package io.github.cobbleeffort.distortion;

import net.minecraft.core.UUIDUtil;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

import java.util.UUID;

/** Client to server: the wheel's Distort / Revert option for one of the player's Pokémon. */
public record DistortPacket(UUID pokemonId) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<DistortPacket> TYPE =
            new CustomPacketPayload.Type<>(ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "distort"));
    public static final StreamCodec<RegistryFriendlyByteBuf, DistortPacket> STREAM_CODEC =
            StreamCodec.composite(UUIDUtil.STREAM_CODEC, DistortPacket::pokemonId, DistortPacket::new);

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
