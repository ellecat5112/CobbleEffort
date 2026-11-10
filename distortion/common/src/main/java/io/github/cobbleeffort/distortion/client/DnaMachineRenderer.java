package io.github.cobbleeffort.distortion.client;

import com.cobblemon.mod.common.CobblemonEntities;
import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import io.github.cobbleeffort.distortion.Distortion;
import io.github.cobbleeffort.distortion.dna.DnaMachineBlock;
import io.github.cobbleeffort.distortion.dna.DnaMachineBlockEntity;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.entity.EntityRenderDispatcher;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import org.joml.Matrix4f;

import java.util.Map;
import java.util.WeakHashMap;

/**
 * Draws what's inside the DNA machine's glass: the glowing fluid (rising as the tank fills, full while it works) and
 * the Pokémon floating in it (Mew, then Mewtwo), as Cobblemon's habitat block does: a client-only display entity.
 */
public class DnaMachineRenderer implements BlockEntityRenderer<DnaMachineBlockEntity> {
    private static final ResourceLocation FLUID = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/block/dna_fluid.png");
    private static final float X0 = 2.7F / 16, X1 = 13.3F / 16, Y0 = 6F / 16, H = 20F / 16;
    private final Map<DnaMachineBlockEntity, PokemonEntity> displays = new WeakHashMap<>();
    private final Map<DnaMachineBlockEntity, String> keys = new WeakHashMap<>();
    private boolean failed;

    public DnaMachineRenderer(BlockEntityRendererProvider.Context context) {
    }

    @Override
    public boolean shouldRenderOffScreen(DnaMachineBlockEntity be) {
        return true;                                           // two blocks tall
    }

    @Override
    public void render(DnaMachineBlockEntity be, float partial, PoseStack pose, MultiBufferSource buffers, int light, int overlay) {
        long time = be.getLevel() == null ? 0 : be.getLevel().getGameTime();
        float level = "mew".equals(be.inside()) ? 1F : be.fillLevel() / (float) DnaMachineBlockEntity.CAPACITY;
        if (be.occupied()) {
            try {
                renderPokemon(be, partial, pose, buffers, time);
            } catch (Throwable t) {
                if (!failed) Distortion.LOG.error("Couldn't draw the Pokémon in a DNA machine", t);
                failed = true;                                 // never crash the game over the display
            }
        }
        if (level > 0) renderFluid(pose, buffers, level, time + partial);
    }

    private void renderFluid(PoseStack pose, MultiBufferSource buffers, float level, float t) {
        VertexConsumer vc = buffers.getBuffer(RenderType.entityTranslucentEmissive(FLUID));
        float top = Y0 + H * level - 0.01F * (float) Math.sin(t * 0.08);
        float span = (top - Y0) * 2F, scroll = (t * 0.004F) % 1F;
        Matrix4f m = pose.last().pose();
        int r = 150, g = 255, b = 210, a = 150, l = LightTexture.FULL_BRIGHT;
        side(vc, pose, m, X0, X0, X1, X0, top, scroll, span, r, g, b, a, l, 0, 0, -1);   // north
        side(vc, pose, m, X1, X1, X0, X1, top, scroll, span, r, g, b, a, l, 0, 0, 1);    // south
        side(vc, pose, m, X0, X1, X0, X0, top, scroll, span, r, g, b, a, l, -1, 0, 0);   // west
        side(vc, pose, m, X1, X0, X1, X1, top, scroll, span, r, g, b, a, l, 1, 0, 0);    // east
        vertex(vc, pose, m, X0, top, X0, 0, 0, r, g, b, a, l, 0, 1, 0);                    // the surface
        vertex(vc, pose, m, X0, top, X1, 0, 1, r, g, b, a, l, 0, 1, 0);
        vertex(vc, pose, m, X1, top, X1, 1, 1, r, g, b, a, l, 0, 1, 0);
        vertex(vc, pose, m, X1, top, X0, 1, 0, r, g, b, a, l, 0, 1, 0);
    }

    /** A wall of fluid from (xa, za) to (xb, zb), from the tank floor to the surface, its texture scrolling upwards. */
    private static void side(VertexConsumer vc, PoseStack pose, Matrix4f m, float xa, float za, float xb, float zb, float top,
                             float scroll, float span, int r, int g, int b, int a, int l, float nx, float ny, float nz) {
        vertex(vc, pose, m, xa, Y0, za, 0, scroll + span, r, g, b, a, l, nx, ny, nz);
        vertex(vc, pose, m, xb, Y0, zb, 1, scroll + span, r, g, b, a, l, nx, ny, nz);
        vertex(vc, pose, m, xb, top, zb, 1, scroll, r, g, b, a, l, nx, ny, nz);
        vertex(vc, pose, m, xa, top, za, 0, scroll, r, g, b, a, l, nx, ny, nz);
    }

    private static void vertex(VertexConsumer vc, PoseStack pose, Matrix4f m, float x, float y, float z, float u, float v,
                               int r, int g, int b, int a, int l, float nx, float ny, float nz) {
        vc.addVertex(m, x, y, z).setColor(r, g, b, a).setUv(u, v).setOverlay(OverlayTexture.NO_OVERLAY).setLight(l)
                .setNormal(pose.last(), nx, ny, nz);
    }

    private void renderPokemon(DnaMachineBlockEntity be, float partial, PoseStack pose, MultiBufferSource buffers, long time) {
        if (failed) return;
        PokemonEntity entity = display(be);
        if (entity == null) return;
        Direction facing = be.getBlockState().getValue(DnaMachineBlock.FACING);
        float yaw = facing.toYRot();
        entity.setYRot(yaw);
        entity.yRotO = yaw;
        entity.yBodyRot = yaw;
        entity.yBodyRotO = yaw;
        entity.yHeadRot = yaw;
        entity.yHeadRotO = yaw;
        entity.tickCount = (int) time;
        float height = Math.max(0.3F, entity.getBbHeight());
        float target = "mewtwo".equals(be.inside()) ? 1.35F : 0.8F;
        float scale = Math.min(1.5F, target / height);
        float bob = 0.04F * (float) Math.sin((time + partial) * 0.06);
        pose.pushPose();
        pose.translate(0.5, Y0 + 0.08 + bob, 0.5);
        pose.scale(scale, scale, scale);
        EntityRenderDispatcher dispatcher = Minecraft.getInstance().getEntityRenderDispatcher();
        dispatcher.setRenderShadow(false);
        try {
            dispatcher.render(entity, 0, 0, 0, yaw, partial, pose, buffers, LightTexture.FULL_BRIGHT);
        } catch (Throwable t) {
            Distortion.LOG.error("Couldn't draw the Pokémon in a DNA machine", t);
            displays.remove(be);
        } finally {
            dispatcher.setRenderShadow(true);
            pose.popPose();
        }
    }

    private PokemonEntity display(DnaMachineBlockEntity be) {
        String key = be.inside() + (be.shiny() ? ":shiny" : "");
        if (!key.equals(keys.get(be)) || !displays.containsKey(be)) {
            keys.put(be, key);
            Species species = PokemonSpecies.getByName(be.inside());
            if (species == null || be.getLevel() == null) {
                displays.remove(be);
                return null;
            }
            // as Cobblemon's habitat block builds its display Pokémon
            Pokemon pokemon = new Pokemon();
            pokemon.setSpecies(species);
            pokemon.initialize();
            pokemon.setShiny(be.shiny());
            PokemonEntity entity = new PokemonEntity(be.getLevel(), pokemon, CobblemonEntities.POKEMON);
            entity.setNoGravity(true);
            entity.setPos(be.getBlockPos().getX() + 0.5, be.getBlockPos().getY() + 0.5, be.getBlockPos().getZ() + 0.5);
            displays.put(be, entity);
        }
        return displays.get(be);
    }
}
