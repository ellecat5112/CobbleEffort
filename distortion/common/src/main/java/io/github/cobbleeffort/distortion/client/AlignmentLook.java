package io.github.cobbleeffort.distortion.client;

import com.cobblemon.mod.common.api.types.ElementalType;
import com.cobblemon.mod.common.client.render.models.blockbench.PosableState;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.mojang.blaze3d.platform.NativeImage;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.BufferUploader;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.Tesselator;
import com.mojang.blaze3d.vertex.VertexFormat;
import dev.architectury.event.events.client.ClientTickEvent;
import io.github.cobbleeffort.distortion.Alignment;
import io.github.cobbleeffort.distortion.Distortion;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.GameRenderer;
import net.minecraft.client.renderer.texture.AbstractTexture;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.util.RandomSource;
import org.joml.Matrix4f;

import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/**
 * How Shadow and Crystal Pokémon look, for every species at once: their textures are recoloured at runtime (Shadow:
 * a dark violet, its own markings showing through; Crystal: pale glassy cyan with facet glints, see-through: rendered
 * translucent by AlignRenderTypeMixin), Shadow Pokémon trail a dark aura and Crystal ones sparkle. Also draws the two
 * type icons (Cobblemon's type sheet only holds its 18).
 */
public final class AlignmentLook {
    public static final ResourceLocation ICONS = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/gui/alignment_types.png");
    public static final ResourceLocation ICONS_SMALL = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID, "textures/gui/alignment_types_small.png");
    private static final ResourceLocation TYPES = ResourceLocation.fromNamespaceAndPath("cobblemon", "textures/gui/types.png");
    private static final ResourceLocation TYPES_SMALL = ResourceLocation.fromNamespaceAndPath("cobblemon", "textures/gui/types_small.png");
    private static final Map<String, ResourceLocation> CACHE = new HashMap<>();
    private static int counter;
    private static boolean warned;

    private AlignmentLook() {
    }

    public static void init() {
        ClientTickEvent.CLIENT_POST.register(AlignmentLook::tick);
    }

    // --- icons ------------------------------------------------------------------------------------------------------
    public static boolean ours(ElementalType type) {
        return type == Alignment.SHADOW || type == Alignment.CRYSTAL;
    }

    /** One type icon, `size` px square, at (x, y) in the current pose; any type, ours or Cobblemon's. */
    public static void icon(PoseStack pose, ElementalType type, float x, float y, int size, boolean small, float alpha) {
        boolean own = ours(type);
        ResourceLocation tex = own ? (small ? ICONS_SMALL : ICONS) : (small ? TYPES_SMALL : TYPES);
        int index = own ? (type == Alignment.SHADOW ? 0 : 1) : type.getTextureXMultiplier();
        int sheetW = (own ? 2 : 18) * size;
        float u0 = (float) (index * size) / sheetW, u1 = (float) ((index + 1) * size) / sheetW;
        RenderSystem.setShader(GameRenderer::getPositionTexShader);
        RenderSystem.setShaderTexture(0, tex);
        RenderSystem.enableBlend();
        RenderSystem.defaultBlendFunc();
        RenderSystem.setShaderColor(1F, 1F, 1F, alpha);
        Matrix4f m = pose.last().pose();
        BufferBuilder b = Tesselator.getInstance().begin(VertexFormat.Mode.QUADS, DefaultVertexFormat.POSITION_TEX);
        b.addVertex(m, x, y, 0).setUv(u0, 0);
        b.addVertex(m, x, y + size, 0).setUv(u0, 1);
        b.addVertex(m, x + size, y + size, 0).setUv(u1, 1);
        b.addVertex(m, x + size, y, 0).setUv(u1, 0);
        BufferUploader.drawWithShader(b.buildOrThrow());
        RenderSystem.setShaderColor(1F, 1F, 1F, 1F);
    }

    // --- the look ---------------------------------------------------------------------------------------------------
    public static String flag(Set<String> aspects) {
        if (aspects == null) return null;
        if (aspects.contains(Alignment.SHADOW_FLAG)) return Alignment.SHADOW_FLAG;
        if (aspects.contains(Alignment.CRYSTAL_FLAG)) return Alignment.CRYSTAL_FLAG;
        return null;
    }

    public static String flag(PokemonEntity entity) {
        try {
            return flag(entity.getEntityData().get(PokemonEntity.getASPECTS()));
        } catch (Throwable t) {
            return null;
        }
    }

    /** The texture Cobblemon picked, recoloured when the state is a Shadow or Crystal Pokémon (else null). */
    public static ResourceLocation texture(PosableState state, ResourceLocation original) {
        try {
            if (state == null || original == null) return null;
            String flag = flag(state.getCurrentAspects());
            if (flag == null) return null;
            String key = flag + "|" + original;
            ResourceLocation done = CACHE.get(key);
            if (done != null) return done;
            ResourceLocation out = make(original, Alignment.SHADOW_FLAG.equals(flag));
            CACHE.put(key, out);
            return out;
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Distortion.LOG.warn("Couldn't recolour a Shadow/Crystal Pokémon", t);
            }
            return null;
        }
    }

    public static boolean isCrystalTexture(ResourceLocation id) {
        return id != null && id.getNamespace().equals(Distortion.MOD_ID) && id.getPath().startsWith("aligned/crystal_");
    }

    private static NativeImage read(ResourceLocation texture) throws Exception {
        Minecraft mc = Minecraft.getInstance();
        Optional<Resource> res = mc.getResourceManager().getResource(texture);
        if (res.isPresent()) {
            try (InputStream in = res.get().open()) {
                return NativeImage.read(in);
            }
        }
        AbstractTexture tex = mc.getTextureManager().getTexture(texture, null);
        if (tex instanceof DynamicTexture dyn && dyn.getPixels() != null) {      // e.g. a fusion's recoloured texture
            NativeImage copy = new NativeImage(dyn.getPixels().getWidth(), dyn.getPixels().getHeight(), false);
            copy.copyFrom(dyn.getPixels());
            return copy;
        }
        return null;
    }

    private static int lerp(int a, int b, double t) {
        return (int) Math.round(a + (b - a) * t);
    }

    private static int[] ramp(int[][] stops, double t) {
        t = Math.max(0, Math.min(1, t));
        double s = t * (stops.length - 1);
        int i = Math.min(stops.length - 2, (int) s);
        double f = s - i;
        return new int[]{lerp(stops[i][0], stops[i + 1][0], f), lerp(stops[i][1], stops[i + 1][1], f), lerp(stops[i][2], stops[i + 1][2], f)};
    }

    private static final int[][] SHADOW = {{14, 6, 26}, {58, 26, 92}, {132, 70, 184}, {222, 182, 250}};
    private static final int[][] CRYSTAL = {{64, 140, 186}, {130, 214, 238}, {206, 246, 252}, {255, 255, 255}};

    private static ResourceLocation make(ResourceLocation texture, boolean shadow) throws Exception {
        NativeImage img = read(texture);
        if (img == null) return texture;
        int w = img.getWidth(), h = img.getHeight();
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                int abgr = img.getPixelRGBA(x, y);
                int a = abgr >>> 24;
                if (a == 0) continue;
                int r = abgr & 0xFF, g = (abgr >> 8) & 0xFF, b = (abgr >> 16) & 0xFF;
                double lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255.0;
                int[] c;
                int alpha = a;
                if (shadow) {
                    int[] grad = ramp(SHADOW, Math.pow(lum, 0.85));
                    c = new int[]{lerp(grad[0], r / 2, 0.22), lerp(grad[1], g / 2, 0.22), lerp(grad[2], b / 2, 0.22)};
                } else {
                    int[] grad = ramp(CRYSTAL, 0.2 + 0.8 * lum);
                    c = new int[]{lerp(grad[0], r, 0.18), lerp(grad[1], g, 0.18), lerp(grad[2], b, 0.18)};
                    alpha = 140 + (int) (70 * lum);
                    if (Math.floorMod(x + y, 12) == 0) {                            // diagonal glass streaks
                        c = new int[]{lerp(c[0], 255, 0.55), lerp(c[1], 255, 0.55), lerp(c[2], 255, 0.55)};
                        alpha = 205;
                    }
                    if ((x * 31 + y * 17 + x * y * 7) % 97 == 0) {                 // a few bright glints
                        c = new int[]{255, 255, 255};
                        alpha = 240;
                    }
                    alpha = Math.min(a, alpha);
                }
                img.setPixelRGBA(x, y, (alpha << 24) | (c[2] << 16) | (c[1] << 8) | c[0]);
            }
        }
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(Distortion.MOD_ID,
                "aligned/" + (shadow ? "shadow_" : "crystal_") + (counter++));
        Minecraft.getInstance().getTextureManager().register(id, new DynamicTexture(img));
        return id;
    }

    // --- aura -------------------------------------------------------------------------------------------------------
    private static void tick(Minecraft mc) {
        if (mc.level == null || mc.player == null || mc.isPaused()) return;
        RandomSource random = mc.level.getRandom();
        for (PokemonEntity e : mc.level.getEntitiesOfClass(PokemonEntity.class, mc.player.getBoundingBox().inflate(32))) {
            String flag = flag(e);
            if (flag == null || e.isInvisible()) continue;
            double w = e.getBbWidth() * 0.6, hgt = e.getBbHeight();
            if (Alignment.SHADOW_FLAG.equals(flag)) {
                if (random.nextInt(3) == 0) {
                    mc.level.addParticle(ParticleTypes.WITCH, e.getX() + (random.nextDouble() - 0.5) * 2 * w,
                            e.getY() + random.nextDouble() * hgt, e.getZ() + (random.nextDouble() - 0.5) * 2 * w, 0, 0.02, 0);
                }
                if (random.nextInt(5) == 0) {
                    mc.level.addParticle(ParticleTypes.SQUID_INK, e.getX() + (random.nextDouble() - 0.5) * 2 * w,
                            e.getY() + random.nextDouble() * hgt * 0.8, e.getZ() + (random.nextDouble() - 0.5) * 2 * w, 0, 0.03, 0);
                }
            } else if (random.nextInt(6) == 0) {
                mc.level.addParticle(ParticleTypes.END_ROD, e.getX() + (random.nextDouble() - 0.5) * 2 * w,
                        e.getY() + random.nextDouble() * hgt, e.getZ() + (random.nextDouble() - 0.5) * 2 * w, 0, 0.005, 0);
            }
        }
    }
}
