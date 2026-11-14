package io.github.cobbleeffort.kanto;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.architectury.platform.Platform;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Random;

/**
 * config/cobbleeffort_kanto.json, read when a server starts: how much of their host biomes the Ashtray Wastes and the
 * Liquor Meadows take over ("frequency", 0 to 1) and how big their patches are ("patch_size", in blocks). Missing
 * values are filled in with the defaults and written back, so the file always lists every setting.
 */
public final class KantoConfig {
    public static final double DEFAULT_FREQUENCY = 0.35;
    public static final int DEFAULT_PATCH = 192;

    public record Patches(double frequency, int patchSize) {
        /** Patch size in quarts (4 blocks), the noise's cell. */
        int cell() {
            return Math.max(4, patchSize / 4);
        }

        /** The noise value above which a host biome is swapped, so that about `frequency` of it is. */
        double threshold() {
            return thresholdFor(frequency, cell());
        }
    }

    public static volatile Patches ashtray = new Patches(DEFAULT_FREQUENCY, DEFAULT_PATCH);
    public static volatile Patches liquor = new Patches(DEFAULT_FREQUENCY, DEFAULT_PATCH);

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    private KantoConfig() {}

    static void load() {
        Path file = Platform.getConfigFolder().resolve(Kanto.MOD_ID + ".json");
        JsonObject root = new JsonObject();
        try {
            if (Files.exists(file)) root = JsonParser.parseString(Files.readString(file, StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (Exception e) {
            Kanto.LOG.error("Couldn't read {} (using the defaults)", file, e);
        }
        ashtray = read(root, "ashtray_wastes");
        liquor = read(root, "liquor_meadows");
        root.addProperty("_help", "frequency: share of the host biomes each biome takes over (0 = never, 1 = all of them); "
                + "patch_size: roughly how wide its patches are, in blocks. Changes apply to chunks generated afterwards.");
        try {
            Files.createDirectories(file.getParent());
            Files.writeString(file, GSON.toJson(root), StandardCharsets.UTF_8);
        } catch (Exception e) {
            Kanto.LOG.error("Couldn't write {}", file, e);
        }
        Kanto.LOG.info("Ashtray Wastes: {}% of their hosts in {}-block patches; Liquor Meadows: {}% in {}-block patches",
                Math.round(ashtray.frequency() * 100), ashtray.patchSize(), Math.round(liquor.frequency() * 100), liquor.patchSize());
    }

    private static Patches read(JsonObject root, String key) {
        JsonObject o = root.has(key) && root.get(key).isJsonObject() ? root.getAsJsonObject(key) : new JsonObject();
        double f = o.has("frequency") ? o.get("frequency").getAsDouble() : DEFAULT_FREQUENCY;
        int size = o.has("patch_size") ? o.get("patch_size").getAsInt() : DEFAULT_PATCH;
        f = Math.max(0, Math.min(1, f));
        size = Math.max(16, Math.min(4096, size));
        o.addProperty("frequency", f);
        o.addProperty("patch_size", size);
        root.add(key, o);
        return new Patches(f, size);
    }

    /** The noise's quantile: sampled once, the value distribution barely depends on the seed. */
    static double thresholdFor(double frequency, int cell) {
        if (frequency <= 0) return 2;
        if (frequency >= 1) return -1;
        Random r = new Random(1234);
        double[] v = new double[20000];
        for (int i = 0; i < v.length; i++) v[i] = Ashtray.noise(r.nextInt(2_000_000) - 1_000_000, r.nextInt(2_000_000) - 1_000_000, cell, 99L);
        Arrays.sort(v);
        return v[(int) Math.min(v.length - 1, Math.round(v.length * (1 - frequency)))];
    }
}
