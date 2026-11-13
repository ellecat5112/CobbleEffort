package io.github.cobbleeffort.fusion.client;

import com.mojang.blaze3d.platform.NativeImage;
import io.github.cobbleeffort.fusion.Fusion;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;

/**
 * Recolours a Cobblemon texture with a fusion design's colours (FusionDesigns): every texel moves by the soft-weighted
 * shift (target - source, in CIELAB) of the colour clusters near its own colour, so the texture keeps its shading and
 * detail. The same maths as fusion/tools/fusion_palette.py, which previews it. A shiny part is the designed colours
 * turned round the hue circle, the way Infinite Fusion makes shiny fusions.
 *
 * Results are dynamic textures, made once per (texture, colours, hue turn) on the render thread and cached.
 */
public final class FusionColours {
    private static final Map<String, ResourceLocation> CACHE = new HashMap<>();
    private static int counter;
    private static boolean warned;

    private FusionColours() {
    }

    /** The recoloured texture, or the original when it can't be made. */
    public static ResourceLocation recolour(ResourceLocation texture, float[][] source, float[][] target, float hueTurn) {
        if (texture == null || source == null || target == null) return texture;
        StringBuilder key = new StringBuilder(texture.toString()).append('|').append(hueTurn);
        for (float[] t : target) key.append('|').append(t[0]).append(',').append(t[1]).append(',').append(t[2]);
        String k = key.toString();
        ResourceLocation done = CACHE.get(k);
        if (done != null) return done;
        ResourceLocation out = texture;
        try {
            out = make(texture, source, target, hueTurn);
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Fusion.LOG.warn("Couldn't recolour {} for a fusion", texture, t);
            }
        }
        CACHE.put(k, out);
        return out;
    }

    private static ResourceLocation make(ResourceLocation texture, float[][] source, float[][] target, float hueTurn) throws Exception {
        Minecraft mc = Minecraft.getInstance();
        Optional<Resource> res = mc.getResourceManager().getResource(texture);
        if (res.isEmpty()) return texture;
        NativeImage img;
        try (InputStream in = res.get().open()) {
            img = NativeImage.read(in);
        }
        double cos = Math.cos(Math.toRadians(hueTurn)), sin = Math.sin(Math.toRadians(hueTurn));
        Map<Integer, Integer> memo = new HashMap<>();
        for (int y = 0; y < img.getHeight(); y++) {
            for (int x = 0; x < img.getWidth(); x++) {
                int abgr = img.getPixelRGBA(x, y);
                if ((abgr >>> 24) == 0) continue;
                Integer to = memo.get(abgr);
                if (to == null) {
                    to = io.github.cobbleeffort.fusion.ColourMath.shift(abgr, source, target, cos, sin);
                    memo.put(abgr, to);
                }
                img.setPixelRGBA(x, y, to);
            }
        }
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Fusion.MOD_ID, "fused/" + (counter++));
        mc.getTextureManager().register(id, new DynamicTexture(img));
        return id;
    }

}
