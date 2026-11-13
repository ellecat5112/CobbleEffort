package io.github.cobbleeffort.fusion;

import java.io.DataInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.zip.GZIPInputStream;
import net.minecraft.resources.ResourceLocation;

/**
 * Fusion designs from Pokémon Infinite Fusion's custom sprites (read from the Infinite Dex by tools/make_designs.py):
 * for every head/body pair with a custom sprite, how its artist recoloured the two Pokémon (target colours for the
 * head's and the body's colour clusters, applied to Cobblemon's textures by client.FusionColours) and who drew it.
 * Also Infinite Fusion's name parts (each Pokémon's head part and body part), so fusions get the game's names.
 *
 * The sprites themselves are not included: only colours, names and credits.
 */
public final class FusionDesigns {
    /** One fusion's design. Colours are CIELAB (L, a, b) per cluster; a target equal to its source means "unchanged". */
    public static final class Design {
        public final float[][] headSource, headTarget, bodySource, bodyTarget;
        public final String artists;

        Design(float[][] headSource, float[][] headTarget, float[][] bodySource, float[][] bodyTarget, String artists) {
            this.headSource = headSource;
            this.headTarget = headTarget;
            this.bodySource = bodySource;
            this.bodyTarget = bodyTarget;
            this.artists = artists;
        }
    }

    /** Form aspects that pick a different Infinite Fusion Pokémon (and texture) for a species. */
    private static final Set<String> FORMS = Set.of("midnight-form", "meteor-form", "east-sea");

    private static boolean loaded;
    private static final Map<String, Integer> SPECIES = new HashMap<>();
    private static float[][][] palettes = new float[0][][];
    private static String[] headParts = new String[0], bodyParts = new String[0];
    private static int[] keys = new int[0], offsets = new int[0], artistOf = new int[0];
    private static byte[] blob = new byte[0];
    private static String[] artistNames = new String[0];

    private FusionDesigns() {
    }

    /** "species" or "species:form" for a Cobblemon species and its aspects. */
    public static String key(ResourceLocation species, Set<String> aspects) {
        String base = species.getPath();
        if (aspects != null) {
            for (String a : aspects) if (FORMS.contains(a)) return base + ":" + a;
        }
        return base;
    }

    private static synchronized void load() {
        if (loaded) return;
        loaded = true;
        try (InputStream raw = FusionDesigns.class.getResourceAsStream("/assets/cobbleeffort_fusion/designs.bin")) {
            if (raw == null) return;
            DataInputStream in = new DataInputStream(new GZIPInputStream(raw, 1 << 16));
            if (in.readInt() != 0x43454644 || in.readInt() != 1) return;
            int ns = in.readInt();
            palettes = new float[ns][][];
            headParts = new String[ns];
            bodyParts = new String[ns];
            for (int i = 0; i < ns; i++) {
                SPECIES.put(in.readUTF(), i);
                headParts[i] = in.readUTF();
                bodyParts[i] = in.readUTF();
                int k = in.readUnsignedByte();
                float[][] p = new float[k][3];
                for (int j = 0; j < k; j++) for (int c = 0; c < 3; c++) p[j][c] = in.readShort() / 100f;
                palettes[i] = p;
            }
            int na = in.readInt();
            String[] artists = new String[na];
            for (int i = 0; i < na; i++) artists[i] = in.readUTF();
            int nf = in.readInt();
            keys = new int[nf];
            offsets = new int[nf];
            artistOf = new int[nf];
            java.io.ByteArrayOutputStream bytes = new java.io.ByteArrayOutputStream(nf * 40);
            for (int i = 0; i < nf; i++) {
                int head = in.readUnsignedShort();
                int body = in.readUnsignedShort();
                keys[i] = head << 16 | body;                       // written in (head, body) order: sorted
                artistOf[i] = in.readInt();
                offsets[i] = bytes.size();
                for (int part = 0; part < 2; part++) {
                    int mask = in.readUnsignedByte();
                    bytes.write(mask);
                    byte[] cols = new byte[Integer.bitCount(mask) * 3];
                    in.readFully(cols);
                    bytes.write(cols);
                }
            }
            blob = bytes.toByteArray();
            artistNames = artists;
            Fusion.LOG.info("Loaded {} fusion designs from Infinite Fusion's custom sprites", nf);
        } catch (Exception e) {
            Fusion.LOG.warn("Couldn't load the fusion designs", e);
        }
    }

    /** A bit per cluster (set = changed), then each changed colour in three bytes (L * 2.55, a + 128, b + 128). */
    private static float[][] targets(int[] pos, float[][] source) {
        int mask = blob[pos[0]++] & 0xFF;
        float[][] t = new float[source.length][];
        for (int j = 0; j < source.length; j++) {
            if ((mask & (1 << j)) != 0) {
                int o = pos[0];
                t[j] = new float[] {(blob[o] & 0xFF) / 2.55f, (blob[o + 1] & 0xFF) - 128f, (blob[o + 2] & 0xFF) - 128f};
                pos[0] += 3;
            } else {
                t[j] = source[j];
            }
        }
        return t;
    }

    /** Load in the background at startup, so the first fusion doesn't wait for it. */
    public static void preload() {
        Thread t = new Thread(FusionDesigns::load, "CobbleEffort fusion designs");
        t.setDaemon(true);
        t.start();
    }

    /** The design for this head and body, or null when Infinite Fusion has no custom sprite for the pair. */
    public static Design find(String headKey, String bodyKey) {
        load();
        Integer h = SPECIES.get(headKey), b = SPECIES.get(bodyKey);
        if (h == null || b == null) return null;
        int i = java.util.Arrays.binarySearch(keys, h << 16 | b);
        if (i < 0) return null;
        int[] pos = {offsets[i]};
        float[][] ht = targets(pos, palettes[h]);
        float[][] bt = targets(pos, palettes[b]);
        int a = artistOf[i];
        return new Design(palettes[h], ht, palettes[b], bt, a >= 0 && a < artistNames.length ? artistNames[a] : "");
    }

    /** Infinite Fusion's name for the pair (head part + body part), or null when either isn't in the game. */
    public static String name(String headKey, String bodyKey) {
        load();
        Integer h = SPECIES.get(headKey), b = SPECIES.get(bodyKey);
        if (h == null || b == null || headParts[h].isEmpty() || bodyParts[b].isEmpty()) return null;
        return headParts[h] + bodyParts[b];
    }
}
