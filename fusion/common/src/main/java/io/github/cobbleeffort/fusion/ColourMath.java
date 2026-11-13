package io.github.cobbleeffort.fusion;

/**
 * The colour maths of fusion designs (no Minecraft classes, so it can be checked against fusion/tools/fusion_palette.py
 * outside the game): CIELAB conversion and the soft-weighted cluster shift that recolours one texel.
 */
public final class ColourMath {
    private static final float SIGMA = 14f;

    private ColourMath() {
    }

    /** One texel (Minecraft NativeImage ABGR int) recoloured; cos/sin turn the hue (a shiny part). */
    public static int shift(int abgr, float[][] source, float[][] target, double cos, double sin) {
        int r = abgr & 0xFF, g = abgr >> 8 & 0xFF, b = abgr >> 16 & 0xFF, a = abgr >>> 24;
        double[] lab = toLab(r, g, b);
        int n = source.length;
        double[] d2 = new double[n];
        double min = Double.MAX_VALUE;
        for (int j = 0; j < n; j++) {
            double dl = lab[0] - source[j][0], da = lab[1] - source[j][1], db = lab[2] - source[j][2];
            d2[j] = dl * dl + da * da + db * db;
            min = Math.min(min, d2[j]);
        }
        double sum = 0, sl = 0, sa = 0, sb = 0;
        for (int j = 0; j < n; j++) {
            double w = Math.exp(-(d2[j] - min) / (2 * SIGMA * SIGMA));
            sum += w;
            sl += w * (target[j][0] - source[j][0]);
            sa += w * (target[j][1] - source[j][1]);
            sb += w * (target[j][2] - source[j][2]);
        }
        double L = lab[0] + sl / sum, A = lab[1] + sa / sum, B = lab[2] + sb / sum;
        double A2 = A * cos - B * sin, B2 = A * sin + B * cos;
        int[] rgb = toRgb(L, A2, B2);
        return a << 24 | rgb[2] << 16 | rgb[1] << 8 | rgb[0];
    }

    // ---- CIELAB (D65), as in fusion_palette.py -----------------------------------------------------------------------

    private static double lin(int c) {
        double v = c / 255.0;
        return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    }

    private static double f(double t) {
        double d = 6.0 / 29;
        return t > d * d * d ? Math.cbrt(t) : t / (3 * d * d) + 4.0 / 29;
    }

    static double[] toLab(int r, int g, int b) {
        double R = lin(r), G = lin(g), B = lin(b);
        double x = (0.4124564 * R + 0.3575761 * G + 0.1804375 * B) / 0.95047;
        double y = 0.2126729 * R + 0.7151522 * G + 0.0721750 * B;
        double z = (0.0193339 * R + 0.1191920 * G + 0.9503041 * B) / 1.08883;
        double fx = f(x), fy = f(y), fz = f(z);
        return new double[] {116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)};
    }

    private static double finv(double t) {
        double d = 6.0 / 29;
        return t > d ? t * t * t : 3 * d * d * (t - 4.0 / 29);
    }

    private static int gamma(double v) {
        v = Math.max(0, Math.min(1, v));
        double s = v <= 0.0031308 ? v * 12.92 : 1.055 * Math.pow(v, 1 / 2.4) - 0.055;
        return (int) Math.max(0, Math.min(255, Math.round(s * 255)));
    }

    static int[] toRgb(double L, double a, double b) {
        double fy = (L + 16) / 116, fx = fy + a / 500, fz = fy - b / 200;
        double x = finv(fx) * 0.95047, y = finv(fy), z = finv(fz) * 1.08883;
        double R = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z;
        double G = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z;
        double B = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z;
        return new int[] {gamma(R), gamma(G), gamma(B)};
    }
}
