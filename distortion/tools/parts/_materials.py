"""
Materials for the part kit: each paints a cube's faces (new cubes) or repaints an existing cube's UV areas (reskin,
keeping the original silhouette). Clean colours with soft baked shading, like Cobblemon's textures; glowing parts go in
animated layers.

paint(ctx, rects, size, reskin): rects is face -> (u, v, w, h); faces with no area are skipped.
"""
from __future__ import annotations

import math

from _kit import clamp, mix, shade

SIDES = ("east", "north", "west", "south")
LIGHT = {"up": 1.12, "down": 0.72, "north": 1.0, "south": 0.9, "east": 0.95, "west": 0.95}


def _iter(rects):
    for face, (u, v, w, h) in rects.items():
        if w <= 0 or h <= 0:
            continue
        for y in range(h):
            for x in range(w):
                yield face, u + x, v + y, (x + 0.5) / w, (y + 0.5) / h, x, y, w, h


def _solid_alpha(ctx, X, Y, reskin):
    """Reskins keep the original's silhouette: only where it's painted."""
    return not reskin or ctx.body[X, Y][3] > 0


def _edge(ctx, X, Y, rect):
    u, v, w, h = rect
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x, y = X + dx, Y + dy
        if not (u <= x < u + w and v <= y < v + h) or ctx.body[x, y][3] == 0:
            return True
    return False


def _hash(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h / 0xFFFFFFFF


class Solid:
    """One colour, lit from the top, a slightly darker rim."""

    def __init__(self, normal, shiny=None, rim=0.85, noise=0.03):
        self.c = {False: normal, True: shiny or normal}
        self.rim, self.noise = rim, noise

    def colour(self, ctx, face, s, t, X, Y):
        c = self.c[ctx.shiny]
        f = LIGHT[face] * (1.04 - 0.12 * t if face in SIDES else 1.0)
        f *= 1 + self.noise * (_hash(X, Y, 7) - 0.5) * 2
        return shade(c, f)

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if not _solid_alpha(ctx, X, Y, reskin):
                continue
            c = self.colour(ctx, face, s, t, X, Y)
            if x in (0, w - 1) or y in (0, h - 1):
                c = shade(c, self.rim)
            ctx.put(X, Y, c)


class Bands(Solid):
    """Growth rings: horizontal bands round the sides, concentric rings on the top (prototaxite trunks, bark)."""

    def __init__(self, normal, shiny, period=2):
        super().__init__(normal[0], shiny[0])
        self.bands = {False: normal, True: shiny}
        self.period = period

    def colour(self, ctx, face, s, t, X, Y):
        cols = self.bands[ctx.shiny]
        if face in ("up", "down"):
            r = math.hypot(s - 0.5, t - 0.5) * 2
            c = cols[int(r * len(cols) * 1.2) % len(cols)]
        else:
            row = int(Y - 0) // self.period
            wobble = int(_hash(X // 2, row) * 1.6)
            c = cols[(row + wobble) % len(cols)]
        return shade(c, LIGHT[face] * (1 + 0.04 * (_hash(X, Y) - 0.5)))


class Rock(Solid):
    """Speckled stone."""

    def __init__(self, normal=(96, 84, 78), shiny=(84, 86, 104)):
        super().__init__(normal, shiny, noise=0.0)

    def colour(self, ctx, face, s, t, X, Y):
        c = self.c[ctx.shiny]
        r = _hash(X, Y, 3)
        if r < 0.18:
            c = shade(c, 0.72)
        elif r > 0.85:
            c = shade(c, 1.25)
        return shade(c, LIGHT[face] * (1.05 - 0.15 * t if face in SIDES else 1.0))


class Flame:
    """Raging animated flames. On planes: the flame's silhouette, flickering (the body stays clear, the glow is the
    layer); on boxes and reskins: a glowing surface."""

    PALETTE = {False: [(255, 250, 210), (255, 214, 80), (250, 128, 30), (214, 50, 22)],
               True: [(255, 236, 255), (240, 160, 255), (178, 84, 240), (110, 40, 200)]}

    def __init__(self, layer, tongues=1.5, palette=None):
        self.layer, self.tongues = layer, tongues
        self.palette = palette or self.PALETTE

    @staticmethod
    def shape(s, t, f, tongues):
        """0 outside, else 0..1 (1 = the hot core). t = 0 at the top."""
        y = 1 - t
        x = abs(s - 0.5) * 2
        top = 0.72 + 0.28 * math.cos(2 * math.pi * (s * tongues + f / 4.0))
        if y > top:
            return 0
        width = (1 - y / top) ** 0.55 + 0.06 * math.sin(7 * y + f * 1.6)
        if x > width:
            return 0
        return max(0.0, 1 - (x / max(width, 1e-3)) * 0.7 - y * 0.6)

    def colour(self, ctx, heat):
        p = self.palette[ctx.shiny]
        if heat > 0.75:
            return p[0]
        if heat > 0.5:
            return p[1]
        if heat > 0.25:
            return p[2]
        return p[3]

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        plane = min(size) == 0 and not reskin
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if not plane and not _solid_alpha(ctx, X, Y, reskin):
                continue
            for f in range(frames):
                if plane:
                    heat = self.shape(s, t, f, self.tongues)
                else:
                    heat = 0.35 + 0.4 * _hash(X, Y, f) * (1 - t * 0.5)
                if heat > 0:
                    ctx.glow(self.layer, f, X, Y, self.colour(ctx, heat))
            if plane:
                ctx.put(X, Y, (0, 0, 0, 0))
            else:
                ctx.put(X, Y, shade(self.palette[ctx.shiny][3], 0.8))


class Charred:
    """Charcoal with glowing, flickering edges and embers: burning leaves, a burnt stump."""

    def __init__(self, layer, glow=None):
        self.layer = layer
        self.glow = glow or Flame.PALETTE

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        for face, (u, v, w, h) in rects.items():
            if w <= 0 or h <= 0:
                continue
            for y in range(h):
                for x in range(w):
                    X, Y = u + x, v + y
                    if not _solid_alpha(ctx, X, Y, reskin):
                        continue
                    edge = _edge(ctx, X, Y, (u, v, w, h)) if reskin else x in (0, w - 1) or y in (0, h - 1)
                    base = (44, 36, 34) if not ctx.shiny else (40, 38, 52)
                    ctx.put(X, Y, shade(base, 0.8 + 0.4 * _hash(X, Y, 11)))
                    for f in range(frames):
                        r = _hash(X, Y, f, 5)
                        if edge and r > 0.62:
                            ctx.glow(self.layer, f, X, Y, self.glow[ctx.shiny][1 if r > 0.85 else 2])
                        elif r > 0.95:
                            ctx.glow(self.layer, f, X, Y, self.glow[ctx.shiny][2])


class LavaRock:
    """Dark basalt with glowing lava cracks that pulse (a volcano's flanks, a lava flow)."""

    def __init__(self, layer, crack=0.16):
        self.layer, self.crack = layer, crack

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if not _solid_alpha(ctx, X, Y, reskin):
                continue
            base = (58, 48, 46) if not ctx.shiny else (54, 52, 70)
            ctx.put(X, Y, shade(base, LIGHT[face] * (0.85 + 0.3 * _hash(X, Y, 2))))
            cr = abs(math.sin(X * 1.7 + math.sin(Y * 0.9) * 2.1)) < self.crack or _hash(X // 2, Y // 2, 9) > 0.92
            if cr:
                for f in range(frames):
                    k = 0.5 + 0.5 * math.sin(f / frames * 2 * math.pi + X * 0.4)
                    ctx.glow(self.layer, f, X, Y, Flame.PALETTE[ctx.shiny][1 if k > 0.5 else 2])


class Glow:
    """A molten, glowing surface (a crater's lava): the body dark red, the layer bright and pulsing. Another palette
    (hot core first, darkest last) makes other glows: ELECTRIC for crackling lightning."""

    def __init__(self, layer, palette=None):
        self.layer = layer
        self.palette = palette or Flame.PALETTE

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        p = self.palette[ctx.shiny]
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if not _solid_alpha(ctx, X, Y, reskin):
                continue
            ctx.put(X, Y, p[3])
            for f in range(frames):
                k = _hash(X, Y, f, 21)
                ctx.glow(self.layer, f, X, Y, p[0 if k > 0.8 else 1 if k > 0.35 else 2])


ELECTRIC = {False: [(255, 255, 230), (255, 236, 96), (240, 190, 40), (60, 50, 30)],
            True: [(240, 255, 255), (120, 230, 255), (60, 150, 240), (30, 40, 70)]}


class Cutout:
    """A shape cut out of a plane (both faces the same): shape(s, t) -> None (clear) or 0..1 (dark..light), painted
    with a three-colour ramp; `veins(s, t)` lightens lines (a leaf's midrib, a fin's rays). On a reskin it keeps the
    original silhouette and just repaints it."""

    def __init__(self, shape, normal, shiny, veins=None):
        self.shape, self.ramp, self.veins = shape, {False: normal, True: shiny}, veins

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if reskin:
                if ctx.body[X, Y][3] == 0:
                    continue
                k = self.shape(s, t)
                k = 0.5 if k is None else k
            else:
                k = self.shape(s, t)
                if k is None:
                    ctx.put(X, Y, (0, 0, 0, 0))
                    continue
            dark, mid, light = self.ramp[ctx.shiny]
            c = mix(dark, mid, min(1, k * 2)) if k < 0.5 else mix(mid, light, (k - 0.5) * 2)
            if self.veins and self.veins(s, t):
                c = mix(c, light, 0.6)
            ctx.put(X, Y, clamp(c))


# --- shapes ------------------------------------------------------------------------------------------------------------

def leaf(s, t):
    """A pointed leaf, tip at the top."""
    half = math.sin(math.pi * min(1, (1 - t) * 1.05)) ** 0.8 * 0.46
    d = abs(s - 0.5)
    return None if d > half else 1 - d / max(half, 1e-3) * 0.6


def midrib(s, t):
    return abs(s - 0.5) < 0.06


def fern(s, t):
    """A fern frond: leaflets either side of a stem, smaller towards the tip."""
    d = abs(s - 0.5)
    if d < 0.06:
        return 0.3
    seg = (t * 6) % 1
    reach = 0.48 * (0.35 + 0.65 * t)
    return None if d > reach * (1 - abs(seg - 0.5) * 1.2) else 0.4 + 0.6 * (1 - d / reach)


def petal(s, t):
    """A round petal, widest near the top."""
    y = 1 - t
    half = 0.5 * math.sqrt(max(0, 1 - ((y - 0.62) / 0.62) ** 2))
    d = abs(s - 0.5)
    return None if d > half else 0.3 + 0.7 * (1 - d / max(half, 1e-3)) * (0.6 + 0.4 * y)


def tentacles(n=4):
    """Anemone tentacles rising from the base, rounded tips (lighter towards the tips)."""
    def shape(s, t):
        y = 1 - t
        for k in range(n):
            c = (k + 0.5) / n + 0.06 * math.sin(y * 9 + k * 2.3)
            top = 0.75 + 0.25 * _hash(k, n)
            if y < top and abs(s - c) < 0.42 / n * (1 - 0.3 * y):
                return 0.25 + 0.75 * y / top
        return None
    return shape


def coral(seed=1):
    """A branching coral fan."""
    def shape(s, t):
        y = 1 - t
        x = (s - 0.5) * 2
        for b in range(5):
            ang = (b - 2) * 0.38
            bx = math.sin(ang) * y * 1.1 + 0.08 * math.sin(y * 11 + b + seed)
            if abs(x - bx) < 0.16 * (1 - 0.5 * y) and y < 0.95 - 0.12 * abs(b - 2):
                return 0.3 + 0.7 * y
        return None
    return shape


def fin_shape(s, t):
    """A fin membrane: tall at the front edge, sweeping back, scalloped trailing edge."""
    y = 1 - t
    top = 1 - s * 0.55 + 0.06 * math.sin(s * 18)
    return None if y > top else 0.35 + 0.65 * (1 - y / max(top, 1e-3)) * 0.6 + 0.3 * y


def fin_rays(s, t):
    return (s * 7) % 1 < 0.18


def shelf_fungus(s, t):
    """A bracket fungus seen from the side: a half disc with growth lines."""
    y = 1 - t
    r = math.hypot((s - 0.5) * 2, y * 1.6)
    return None if r > 1 else 0.3 + 0.7 * (1 - r)


class Remap:
    """A reskin that keeps the texels' shapes and detail but maps their brightness onto a new colour ramp (flames
    painted on planes -> fins, kelp or anemones; leaves -> lava)."""

    def __init__(self, normal, shiny, invert=False):
        self.ramp, self.invert = {False: normal, True: shiny}, invert

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            r, g, b, a = ctx.body[X, Y]
            if a == 0:
                continue
            k = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            k = 1 - k if self.invert else k
            dark, mid, light = self.ramp[ctx.shiny]
            c = mix(dark, mid, min(1, k * 2)) if k < 0.5 else mix(mid, light, (k - 0.5) * 2)
            ctx.put(X, Y, clamp(c) + (a,))


# sea anemone colours: deep magenta at the base, pink, teal tips (the shiny: navy, sky blue, pale gold)
ANEMONE = ([(140, 36, 116), (236, 118, 186), (120, 236, 226)], [(36, 70, 140), (110, 170, 240), (244, 236, 160)])


def sealife_from_layers(names=("emissive", "flame", "fire"), ramp=ANEMONE, keep_glow=False):
    """A body op for fire starters: every texel an emissive flame layer lights becomes sea life (opaque, its brightness
    mapped onto the ramp, hottest = the base colour, the flame's tips = the light tips), so the flames' own shapes read
    as anemone tentacles; the flame layers themselves are dropped (unless keep_glow)."""
    import numpy as np
    from PIL import Image

    def op(img, shiny, src_layers):
        a = np.array(img.convert("RGBA")).astype(np.float64)
        dark, mid, light = (np.array(c, float) for c in ramp[1 if shiny else 0])
        for n, lay in src_layers.items():
            if n not in names:
                continue
            l = np.array(lay.convert("RGBA").resize(img.size)).astype(np.float64)
            m = l[..., 3] > 0
            k = 1 - (0.3 * l[..., 0] + 0.59 * l[..., 1] + 0.11 * l[..., 2]) / 255   # bright core -> 0, red tips -> 1
            c = np.where((k < 0.5)[..., None], dark + (mid - dark) * np.clip(k * 2, 0, 1)[..., None],
                         mid + (light - mid) * np.clip((k - 0.5) * 2, 0, 1)[..., None])
            a[m, :3] = c[m]
            a[m, 3] = 255
        return Image.fromarray(a.round().astype(np.uint8), "RGBA")
    return op


class Flytrap:
    """A Venus flytrap's lobe on a plane: green outside, red inside, pale cilia teeth along the rim."""

    def paint(self, ctx, rects, size, reskin):
        green = (70, 150, 52) if not ctx.shiny else (90, 150, 140)
        red = (204, 44, 56) if not ctx.shiny else (220, 120, 200)
        teeth = (232, 240, 176)
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            yy = 1 - t
            d = math.hypot((s - 0.5) * 2, (yy - 0.05) * 1.05)
            spike = w >= 6 and d < 1.2 and yy > 0.3 and (x % 2 == 0) and d > 1.0
            if d > 1.0 and not spike:
                ctx.put(X, Y, (0, 0, 0, 0))
                continue
            if spike:
                ctx.put(X, Y, teeth)
            elif d < 0.78 and yy > 0.12:
                ctx.put(X, Y, shade(red, 0.9 + 0.2 * (1 - d)))
            else:
                ctx.put(X, Y, shade(green, 0.9 + 0.2 * yy))


# shared ramps (normal, shiny)
LEAF_RAMP = ([(36, 96, 38), (86, 166, 64), (170, 228, 128)], [(40, 100, 104), (92, 170, 156), (180, 234, 218)])
PINE_RAMP = ([(24, 70, 40), (50, 120, 62), (120, 180, 100)], [(30, 70, 90), (60, 120, 140), (140, 190, 200)])
BARK_RAMP = ([(70, 46, 30), (122, 86, 56), (176, 136, 94)], [(60, 56, 70), (110, 104, 124), (170, 164, 186)])
BAMBOO_RAMP = ([(66, 108, 40), (140, 180, 70), (222, 232, 150)], [(60, 100, 100), (120, 176, 160), (210, 236, 220)])
PETAL_RAMP = ([(176, 60, 120), (242, 140, 190), (255, 228, 242)], [(170, 130, 40), (242, 204, 96), (255, 246, 206)])
CORAL_RAMP = ([(150, 40, 70), (246, 120, 110), (255, 210, 190)], [(60, 60, 160), (150, 140, 240), (230, 226, 255)])
JELLY_RAMP = ([(84, 40, 156), (170, 110, 240), (232, 214, 255)], [(30, 110, 130), (90, 210, 220), (220, 255, 250)])
NUDI_RAMP = ([(70, 40, 140), (150, 90, 230), (255, 170, 90)], [(30, 100, 120), (80, 200, 200), (255, 230, 120)])
MOSS_RAMP = ([(52, 84, 36), (104, 146, 62), (176, 204, 112)], [(52, 80, 90), (100, 140, 150), (170, 200, 210)])


def pine(s, t):
    """A little pine tree: three tiers of needles over a short trunk."""
    y = 1 - t
    d = abs(s - 0.5)
    if y < 0.16:
        return 0.15 if d < 0.08 else None
    for lo, hi, w in ((0.16, 0.5, 0.48), (0.42, 0.76, 0.36), (0.68, 1.0, 0.24)):
        if lo <= y <= hi:
            k = (hi - y) / (hi - lo)
            if d < w * k:
                return 0.35 + 0.6 * (1 - d / max(w * k, 1e-3)) * (0.6 + 0.4 * (y - lo) / (hi - lo))
    return None


def speckles(dark=(40, 40, 46), every=7):
    """A body op: the sea bunny's dark speckles over pale fur (only on near-white texels)."""
    import numpy as np
    from PIL import Image

    def op(img, shiny, src_layers):
        a = np.array(img.convert("RGBA")).astype(np.int32)
        h, w = a.shape[:2]
        rgb = a[..., :3]
        mx, mn = rgb.max(-1), rgb.min(-1)
        pale = (mx > 170) & (mx - mn < 40) & (a[..., 3] > 0)
        ys, xs = np.mgrid[0:h, 0:w]
        dots = ((xs * 7 + ys * 13 + (xs * ys) % 5) % every == 0) & ((xs + ys * 3) % 3 == 0)
        m = pale & dots
        a[m, 0], a[m, 1], a[m, 2] = dark
        return Image.fromarray(a.astype(np.uint8), "RGBA")
    return op



class Membrane:
    """A translucent membrane drawn as a disc on each face (so a box reads as a bubble): faint in the middle, a thicker
    rim, branching veins, gently pulsing (a heartbeat across the frames). Only in its (translucent) layer; the body
    stays clear."""

    def __init__(self, layer, tint=(255, 196, 206), vein=(196, 52, 84), shiny_tint=(214, 200, 255), shiny_vein=(110, 70, 190)):
        self.layer, self.tint, self.vein = layer, {False: tint, True: shiny_tint}, {False: vein, True: shiny_vein}

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            ctx.put(X, Y, (0, 0, 0, 0))
            r = math.hypot(s - 0.5, t - 0.5) * 2
            if r > 1:
                continue
            ang = math.atan2(t - 0.5, s - 0.5)
            vein = abs(math.sin(ang * 4 + 0.7 * math.sin(r * 5))) < 0.14 and r > 0.2     # vessels branching out
            for f in range(frames):
                beat = 1 + 0.18 * math.sin(f / frames * 2 * math.pi)
                if vein:
                    c, a = self.vein[ctx.shiny], int(170 * beat)
                else:
                    c, a = self.tint[ctx.shiny], int((34 + 150 * r ** 4) * beat)
                ctx.glow(self.layer, f, X, Y, tuple(c) + (max(0, min(255, a)),))


class Muscle:
    """Translucent muscle: pink, with striations running along the length and a firmer rim. Only in its
    (translucent) layer; the body stays clear."""

    def __init__(self, layer, colour=(246, 120, 186), shiny=(150, 200, 255)):
        self.layer, self.c = layer, {False: colour, True: shiny}

    def paint(self, ctx, rects, size, reskin):
        frames = len(ctx.layers[self.layer])
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            ctx.put(X, Y, (0, 0, 0, 0))
            base = self.c[ctx.shiny]
            stria = (x + (y // 3)) % 3 == 0
            rim = x in (0, w - 1) or y in (0, h - 1)
            c = shade(base, 1.25 if stria else 0.95)
            a = 210 if rim else (165 if stria else 135)
            for f in range(frames):
                ctx.glow(self.layer, f, X, Y, tuple(c) + (a,))


class Cord:
    """An umbilical cord (a reskin): pale and glossy, with two arteries and a vein spiralling round it."""

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if ctx.body[X, Y][3] == 0:
                continue
            k = (X + Y) % 6
            if ctx.shiny:
                c = (120, 110, 210) if k == 0 else (200, 120, 200) if k == 3 else (236, 226, 246)
            else:
                c = (110, 130, 214) if k == 0 else (204, 70, 96) if k == 3 else (240, 214, 222)
            ctx.put(X, Y, shade(c, LIGHT[face]))


class Placenta:
    """The placenta where the cord meets the orb's wall: a round, dark-red, lobed disc with branching vessels."""

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            r = math.hypot(s - 0.5, t - 0.5) * 2
            if r > 1:
                ctx.put(X, Y, (0, 0, 0, 0))
                continue
            ang = math.atan2(t - 0.5, s - 0.5)
            vessel = abs(math.sin(ang * 6 + r * 4)) < 0.16
            base = (150, 40, 60) if not ctx.shiny else (90, 60, 160)
            c = (110, 120, 200) if vessel else shade(base, 0.85 + 0.35 * (1 - r) + 0.1 * _hash(X, Y))
            ctx.put(X, Y, c)



class Stripes:
    """Bold bands across a part (a reskin keeping its silhouette): a lionfish's striped spines."""

    def __init__(self, normal, shiny, width=2):
        self.c, self.width = {False: normal, True: shiny}, width

    def paint(self, ctx, rects, size, reskin):
        for face, X, Y, s, t, x, y, w, h in _iter(rects):
            if ctx.body[X, Y][3] == 0:
                continue
            a, b = self.c[ctx.shiny]
            ctx.put(X, Y, shade(a if (y // self.width) % 2 == 0 else b, LIGHT[face]))
