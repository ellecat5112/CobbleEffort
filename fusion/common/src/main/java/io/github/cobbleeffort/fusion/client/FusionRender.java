package io.github.cobbleeffort.fusion.client;

import com.cobblemon.mod.common.client.render.models.blockbench.FloatingState;
import com.cobblemon.mod.common.client.render.models.blockbench.PosableModel;
import com.cobblemon.mod.common.client.render.models.blockbench.PosableState;
import com.cobblemon.mod.common.client.render.models.blockbench.pose.Bone;
import com.cobblemon.mod.common.client.render.models.blockbench.repository.VaryingModelRepository;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import io.github.cobbleeffort.fusion.Fusion;
import io.github.cobbleeffort.fusion.FusionDesigns;
import io.github.cobbleeffort.fusion.FusionRules;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.WeakHashMap;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.resources.ResourceLocation;
import org.joml.Vector4f;

/**
 * The automatic head-and-body look for any fusion (Infinite Fusion's idea, in 3D): the BODY's model is drawn as usual
 * but without its "head" bone, and the HEAD species' "head" bone (with everything on it: eyes, ears, horns, hair) is
 * drawn in its place, on the body's head joint, so it turns and bobs with the body's animations and looks at things the
 * way the body's head would. The head is scaled to the size of the head it replaces and uses its own texture (and
 * its own shiny or regional look, from the fusion's head aspects).
 *
 * Works wherever Cobblemon draws a posable model with a state (the world, the party, the PC, the summary). Models
 * without a "head" bone are drawn as the plain body. Custom per-pair forms can replace this later.
 */
public final class FusionRender {
    private static final class Pending {
        ModelPart bodyHead;
        boolean bodyHeadVisible;
        PosableModel headModel;
        ModelPart headPart;
        ResourceLocation texture;
        List<Bone> chain;
    }

    private static final Deque<Pending> PENDING = new ArrayDeque<>();
    private static final Map<String, FloatingState> STATES = new HashMap<>();
    private static final Map<ModelPart, Float> SIZES = new WeakHashMap<>();
    /** Each fusion body's species, by its render state (remembered when Cobblemon looks up the body's texture). */
    private static final Map<PosableState, ResourceLocation> BODIES = new WeakHashMap<>();
    private static boolean warned;

    private FusionRender() {
    }

    public static void init() {
        // nothing to set up: PosableModelMixin calls before/after around every posable model render
    }

    private static FloatingState stateFor(ResourceLocation species, Set<String> aspects) {
        String key = species + "|" + String.join(",", aspects);
        return STATES.computeIfAbsent(key, k -> {
            FloatingState state = new FloatingState();
            state.setCurrentAspects(aspects);
            return state;
        });
    }

    /** Called before a posable model renders: hides the body's head if this model is a fusion's body. */
    public static void before(PosableModel model) {
        Pending pending = null;
        try {
            pending = prepare(model);
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Fusion.LOG.warn("Couldn't draw a fusion's head", t);
            }
        }
        PENDING.push(pending == null ? NONE : pending);
    }

    private static final Pending NONE = new Pending();

    private static Pending prepare(PosableModel model) {
        PosableState state = model.getCurrentState();
        if (state == null) return null;
        Set<String> aspects = state.getCurrentAspects();
        ResourceLocation headId = FusionRules.headSpecies(aspects);
        if (headId == null) return null;
        ModelPart bodyHead = model.getRelevantPartsByName().get("head");
        if (bodyHead == null) return null;
        FloatingState headState = stateFor(headId, FusionRules.headAspects(aspects));
        PosableModel headModel = VaryingModelRepository.INSTANCE.getPoser(headId, headState);
        if (headModel == null || headModel == model) return null;               // same model: nothing to swap
        ModelPart headPart = headModel.getRelevantPartsByName().get("head");
        if (headPart == null) return null;
        List<Bone> chain = new ArrayList<>();
        if (!path(model.getRootPart(), (Bone) (Object) bodyHead, chain)) return null;
        Pending p = new Pending();
        p.bodyHead = bodyHead;
        p.bodyHeadVisible = bodyHead.visible;
        p.headModel = headModel;
        p.headPart = headPart;
        p.texture = headTexture(headId, headState, BODIES.get(state), aspects);
        p.chain = chain;
        bodyHead.visible = false;
        return p;
    }

    /** Hue turn for a shiny part of a designed fusion (Infinite Fusion turns a shiny fusion's colours round the wheel). */
    private static float hueTurn(String headKey, String bodyKey, boolean shiny) {
        if (!shiny) return 0f;
        return 90f + Math.floorMod((headKey + "/" + bodyKey).hashCode(), 180);
    }

    private static Set<String> plain(Set<String> aspects) {
        Set<String> out = new HashSet<>(FusionRules.withoutFusion(aspects));
        out.remove("shiny");
        return out;
    }

    /** The head species' texture, recoloured by the fusion's design when Infinite Fusion has one for the pair. */
    private static ResourceLocation headTexture(ResourceLocation headId, FloatingState headState, ResourceLocation bodyId, Set<String> bodyAspects) {
        ResourceLocation tex = VaryingModelRepository.INSTANCE.getTexture(headId, headState);
        if (bodyId == null) return tex;
        Set<String> headAspects = headState.getCurrentAspects();
        String hk = FusionDesigns.key(headId, headAspects), bk = FusionDesigns.key(bodyId, bodyAspects);
        FusionDesigns.Design d = FusionDesigns.find(hk, bk);
        if (d == null) return tex;
        boolean shiny = headAspects.contains("shiny");
        if (shiny) tex = VaryingModelRepository.INSTANCE.getTexture(headId, stateFor(headId, plain(headAspects)));
        return FusionColours.recolour(tex, d.headSource, d.headTarget, hueTurn(hk, bk, shiny));
    }

    /**
     * Called (by TextureMixin) whenever Cobblemon looks up a texture: for a fusion's body, the body texture recoloured
     * by the pair's design; null to keep Cobblemon's. Also remembers the body species for the head drawn after it.
     */
    public static ResourceLocation bodyTexture(ResourceLocation species, PosableState state, ResourceLocation original) {
        try {
            if (state == null) return null;
            Set<String> aspects = state.getCurrentAspects();
            ResourceLocation headId = FusionRules.headSpecies(aspects);
            if (headId == null) return null;
            BODIES.put(state, species);
            String hk = FusionDesigns.key(headId, FusionRules.headAspects(aspects)), bk = FusionDesigns.key(species, aspects);
            FusionDesigns.Design d = FusionDesigns.find(hk, bk);
            if (d == null) return null;
            boolean shiny = aspects.contains("shiny");
            ResourceLocation tex = original;
            if (shiny) tex = VaryingModelRepository.INSTANCE.getTexture(species, stateFor(species, plain(aspects)));
            return FusionColours.recolour(tex, d.bodySource, d.bodyTarget, hueTurn(hk, bk, shiny));
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Fusion.LOG.warn("Couldn't recolour a fusion's body", t);
            }
            return null;
        }
    }

    /** The bones from root down to target (both included), or false when target isn't under root. */
    private static boolean path(Bone root, Bone target, List<Bone> out) {
        out.add(root);
        if (root == target) return true;
        for (Bone child : root.getChildren().values()) {
            if (path(child, target, out)) return true;
        }
        out.remove(out.size() - 1);
        return false;
    }

    /** Called after the posable model rendered: puts the body's head back and draws the head species' head. */
    public static void after(PosableModel model, PoseStack stack, int light, int overlay, int color) {
        Pending p = PENDING.isEmpty() ? NONE : PENDING.pop();
        if (p == NONE) return;
        p.bodyHead.visible = p.bodyHeadVisible;
        MultiBufferSource buffers = model.getBufferProvider();
        if (buffers == null || !p.bodyHeadVisible) return;
        try {
            stack.pushPose();
            for (Bone bone : p.chain) bone.transform(stack);
            float scale = size(p.bodyHead) / Math.max(0.05f, size(p.headPart));
            scale = Math.max(0.5f, Math.min(2.5f, scale));
            stack.scale(scale, scale, scale);
            p.headModel.setDefault();
            ModelPart head = p.headPart;
            float x = head.x, y = head.y, z = head.z;
            boolean visible = head.visible;
            head.x = 0;
            head.y = 0;
            head.z = 0;
            head.visible = true;
            VertexConsumer consumer = buffers.getBuffer(p.headModel.getLayer(p.texture, false, false, false));
            head.render(stack, consumer, light, overlay, color);
            head.x = x;
            head.y = y;
            head.z = z;
            head.visible = visible;
        } catch (Throwable t) {
            if (!warned) {
                warned = true;
                Fusion.LOG.warn("Couldn't draw a fusion's head", t);
            }
        } finally {
            stack.popPose();
        }
    }

    /** The biggest extent of a part (with its children), in model units, from its cubes. Cached per part. */
    private static float size(ModelPart part) {
        Float cached = SIZES.get(part);
        if (cached != null) return cached;
        float[] box = {Float.MAX_VALUE, Float.MAX_VALUE, Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE, -Float.MAX_VALUE};
        PoseStack stack = new PoseStack();
        float x = part.x, y = part.y, z = part.z;
        part.x = 0;
        part.y = 0;
        part.z = 0;
        part.visit(stack, (pose, path, index, cube) -> {
            for (int i = 0; i < 8; i++) {
                Vector4f v = new Vector4f((i & 1) == 0 ? cube.minX : cube.maxX, (i & 2) == 0 ? cube.minY : cube.maxY,
                        (i & 4) == 0 ? cube.minZ : cube.maxZ, 1f).mul(pose.pose());
                box[0] = Math.min(box[0], v.x);
                box[1] = Math.min(box[1], v.y);
                box[2] = Math.min(box[2], v.z);
                box[3] = Math.max(box[3], v.x);
                box[4] = Math.max(box[4], v.y);
                box[5] = Math.max(box[5], v.z);
            }
        });
        part.x = x;
        part.y = y;
        part.z = z;
        float s = box[3] < box[0] ? 1f : Math.max(box[3] - box[0], Math.max(box[4] - box[1], box[5] - box[2]));
        SIZES.put(part, s);
        return s;
    }
}
