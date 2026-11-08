"""
Shared toolkit for the Naruto / Naruto Shippuden / Boruto collection.

Looks (one per line, dealt round-robin):
  akatsuki      black cloak with red, white-edged clouds; Sharingan eyes
  leaf_shinobi  navy-toned uniform, olive flak vest with scroll pockets, Leaf forehead protector
  anbu          dark grey armour plates and a white porcelain mask with red markings
  sage_mode     orange sage pigment round the eyes, toad eyes, red cloak hem with black flames
  uzumaki       Naruto's orange and black, whisker marks, red swirl, Leaf forehead protector
  byakugan      pale lavender robes, pupil-less glowing eyes with bulging veins
  karma         Boruto's spreading black Karma seal and one glowing blue Jougan eye
plus kurama (the Nine-Tails, for the Vulpix line).

Faces, torsos and ears come from the model's geometry (WANTS_HINTS); eyes from Cobblemon's eye mask.
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from ._animatronic import Face, put, scaled, shine_layer
from ._festive import digest
from ._horror import components, find_eye_mask, mix, value_noise

EYESHINE = {"name": "eyeshine", "emissive": True, "translucent": True}
CHAKRA = {"name": "chakra", "emissive": True, "translucent": True, "frames": 4, "fps": 6}

NAVY = (34, 44, 78)
STEEL = [(120, 126, 136), (176, 182, 192), (214, 220, 228)]
CLOAK = (22, 20, 26)
CLOUD = (196, 30, 40)
OLIVE = (98, 110, 58)
ORANGE = (242, 138, 34)


def hls(c):
    return colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255)


def from_hls(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return (int(r * 255), int(g * 255), int(b * 255))


def ramp(stops, v):
    v = max(0.0, min(1.0, v))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if v <= p1:
            return mix(c0, c1, (v - p0) / (p1 - p0))
    return stops[-1][1]


# ---------------------------------------------------------------------------------------------
# colour schemes
# ---------------------------------------------------------------------------------------------

KURAMA = [(0.0, (110, 34, 10)), (0.45, (222, 98, 26)), (0.8, (250, 150, 60)), (1.0, (255, 196, 110))]
KURAMA_GOLD = [(0.0, (130, 80, 10)), (0.5, (246, 190, 40)), (1.0, (255, 236, 140))]


def recolour(look, c, shiny):
    h, l, s = hls(c)
    lum = (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255
    if look == "kurama":
        return ramp(KURAMA_GOLD if shiny else KURAMA, 0.15 + lum * 0.9)
    if look == "akatsuki":
        return mix(CLOAK, (70, 64, 78), lum * 0.6)
    if look == "leaf_shinobi":
        return mix(from_hls(h, l, s * 0.5), mix(NAVY, (150, 160, 190), l), 0.6)
    if look == "anbu":
        return mix((38, 40, 44), (150, 154, 160), lum)
    if look == "sage_mode":
        return from_hls(h, l, min(1.0, s * 1.05))
    if look == "uzumaki":
        if s < 0.18:
            return c
        return mix((120, 50, 6), (255, 178, 90), l) if l > 0.15 else (20, 16, 18)
    if look == "byakugan":
        return mix((232, 228, 240), (150, 140, 178), max(0.0, 0.8 - l))
    if look == "karma":
        return from_hls(h, l * 0.95, s * 0.85)
    return c


# ---------------------------------------------------------------------------------------------
# details
# ---------------------------------------------------------------------------------------------

def headband(px, alpha, w, h, face, scale):
    """Forehead protector: a navy band across the head, a steel plate with an engraved Leaf swirl."""
    if not face.ok or not face.front:
        return
    x0, y0, fw, fh = face.front
    band_top = y0 + max(1, int(fh * 0.12))
    band_h = max(2, int(fh * 0.22))
    for y in range(band_top, band_top + band_h):
        if not (0 <= y < h):
            continue
        x = face.cx
        while x > 0 and alpha[y][x - 1]:
            x -= 1
        while x < w and alpha[y][x]:
            put(px, alpha, x, y, NAVY if y not in (band_top, band_top + band_h - 1) else (24, 30, 56))
            x += 1
    pw = max(4, int(fw * 0.55))
    px0 = face.cx - pw // 2
    for y in range(band_top, band_top + band_h):
        for x in range(px0, px0 + pw):
            edge = x in (px0, px0 + pw - 1) or y in (band_top, band_top + band_h - 1)
            put(px, alpha, x, y, STEEL[0] if edge else STEEL[2 if (x + y) % 3 else 1])
    # engraved Leaf: a small spiral/notch in the middle of the plate
    cy = band_top + band_h // 2
    for dx in (-1, 0, 1):
        put(px, alpha, face.cx + dx * max(1, scale), cy, (60, 64, 72))
    put(px, alpha, face.cx + max(1, scale), cy - max(1, scale // 2 + 1) + 1, (60, 64, 72))


def whiskers(px, alpha, face, scale, colour=(40, 22, 14)):
    if not face.ok or not face.front:
        return
    x0, y0, fw, fh = face.front
    for side in (-1, 1):
        for k in range(3):
            y = y0 + int(fh * (0.58 + 0.1 * k))
            for t in range(max(2, fw // 5)):
                x = face.cx + side * (fw // 6 + t)
                put(px, alpha, x, y, colour)


def clouds(px, alpha, eye, w, h, rng, scale, count):
    """Akatsuki clouds: three overlapping puffs, red with a white outline."""
    placed = 0
    for _ in range(count * 60):
        if placed >= count:
            break
        r = rng.choice((2, 2, 3)) * scale
        x, y = rng.randrange(w), rng.randrange(h)
        centres = [(x - r, y), (x, y - r // 2), (x + r, y)]
        cells = [(xx, yy) for yy in range(y - 2 * r, y + 2 * r) for xx in range(x - 3 * r, x + 3 * r)]
        inside = lambda xx, yy, rr: any((xx - cx) ** 2 + (yy - cy) ** 2 <= rr * rr for cx, cy in centres)
        if not all(0 <= xx < w and 0 <= yy < h and alpha[yy][xx] and not eye[yy][xx]
                   for xx, yy in cells if inside(xx, yy, r + 1)):
            continue
        for xx, yy in cells:
            if inside(xx, yy, r):
                put(px, alpha, xx, yy, CLOUD)
            elif inside(xx, yy, r + 1):
                put(px, alpha, xx, yy, (240, 236, 232))
        placed += 1


def flak_vest(px, alpha, face, scale):
    if not face.torso:
        return
    x0, y0, fw, fh = face.torso
    for y in range(y0, y0 + fh):
        for x in range(x0, x0 + fw):
            put(px, alpha, x, y, OLIVE if (x + y) % 5 else (86, 96, 50))
    # two scroll pockets on the chest
    pw, ph = max(2, fw // 4), max(2, fh // 4)
    for side in (-1, 1):
        cx = x0 + fw // 2 + side * fw // 4
        for y in range(y0 + fh // 5, y0 + fh // 5 + ph):
            for x in range(cx - pw // 2, cx + pw // 2 + 1):
                edge = y in (y0 + fh // 5, y0 + fh // 5 + ph - 1)
                put(px, alpha, x, y, (70, 78, 40) if edge else (128, 140, 78))


def swirl(px, alpha, cx, cy, r, colour=(200, 40, 30)):
    for t in range(0, 360 * 2, 12):
        a = math.radians(t)
        rr = r * t / 720
        put(px, alpha, int(cx + math.cos(a) * rr), int(cy + math.sin(a) * rr), colour)


def eye_groups(eye_mask, w, h):
    return components([(x, y) for y in range(h) for x in range(w) if eye_mask[y][x]])


def paint_eyes(px, alpha, groups, kind, scale, shiny=False):
    """Returns glowing pixels [(x, y, colour)] for the eyeshine layer."""
    lit = []
    for gi, g in enumerate(groups):
        cells = set(g)
        xs, ys = [p[0] for p in g], [p[1] for p in g]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        for x, y in g:
            dx, dy = x - cx, y - cy
            if kind == "sharingan":
                c = (210, 20, 30)
                if abs(dx) < 0.6 and abs(dy) < 0.6 or (abs(abs(dx) - 1.2) < 0.5 and abs(dy) < 0.5 and (x + y) % 2):
                    c = (12, 6, 8)            # pupil, tomoe
            elif kind == "kurama":
                c = (230, 30, 30) if abs(dx) > 0.5 else (14, 8, 8)    # red with a vertical slit
            elif kind == "byakugan":
                c = (228, 222, 244)
            elif kind == "sage":
                c = (238, 196, 40) if abs(dy) > 0.5 else (20, 14, 10)  # toad eyes: horizontal bar pupil
            elif kind == "jougan":
                if gi != 0:
                    continue
                c = (70, 150, 255) if (abs(dx) > 0.6 or abs(dy) > 0.6) else (240, 248, 255)
            else:
                continue
            put(px, alpha, x, y, c)
            if kind in ("sharingan", "kurama", "byakugan", "sage", "jougan") and c != (12, 6, 8):
                lit.append((x, y, c))
    return lit


# ---------------------------------------------------------------------------------------------
# planning
# ---------------------------------------------------------------------------------------------

_cache: dict = {}


def plan(look, base, eyes_img, seed, shiny, hints):
    key = (look, digest(base), digest(eyes_img), seed, shiny, repr(hints))
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    scale = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye_mask = find_eye_mask(base, eyes_img)
    face = Face(eye_mask, alpha, w, h, hints)
    groups = eye_groups(eye_mask, w, h)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    memo = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            if (r, g, b) not in memo:
                memo[(r, g, b)] = recolour(look, (r, g, b), shiny)
            px[x, y] = memo[(r, g, b)] + (a,)
    units = max(1, (w * h) // (64 * 64 * scale * scale))
    lit, edges = [], []

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and alpha[y][x]

    if look == "kurama":
        if face.ok and face.front:   # black markings: eyeliner sweeping out from the eyes
            x0, y0, fw, fh = face.front
            for side in (-1, 1):
                for t in range(max(2, fw // 4)):
                    x = face.cx + side * (fw // 2 - t)
                    y = y0 + int(fh * 0.45) + t // 3
                    put(px, alpha, x, y, (16, 10, 8))
        for rect in (hints or {}).get("ears", []):   # black ear tips / insides
            ex, ey, ew, eh = scaled(rect, hints, w, h)
            for y in range(ey, ey + max(1, eh // 2)):
                for x in range(ex, ex + ew):
                    put(px, alpha, x, y, (20, 12, 10))
        if shiny:   # Kurama Link Mode: black seal lines
            for y in range(h):
                for x in range(w):
                    if alpha[y][x] and not eye_mask[y][x] and y % (8 * scale) == 0:
                        put(px, alpha, x, y, (24, 16, 8))
            if face.torso:
                tx, ty, tw_, th_ = face.torso
                swirl(px, alpha, tx + tw_ / 2, ty + th_ / 2, min(tw_, th_) / 2, (24, 16, 8))
        lit = paint_eyes(px, alpha, groups, "kurama", scale)
        edges = [(x, y) for y in range(h) for x in range(w)
                 if alpha[y][x] and not all(opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    elif look == "akatsuki":
        clouds(px, alpha, eye_mask, w, h, rng, scale, 4 * units)
        lit = paint_eyes(px, alpha, groups, "sharingan", scale)
    elif look == "leaf_shinobi":
        flak_vest(px, alpha, face, scale)
        headband(px, alpha, w, h, face, scale)
    elif look == "anbu":
        if face.ok and face.front:   # the porcelain mask
            x0, y0, fw, fh = face.front
            for y in range(y0, y0 + fh):
                for x in range(x0, x0 + fw):
                    c = (240, 238, 232)
                    if abs(x - face.cx) <= max(0, scale // 2) and y < y0 + fh // 3:
                        c = (190, 30, 36)                 # red forehead stripe
                    if abs(abs(x - face.cx) - fw // 4) <= max(0, scale // 2) and y > y0 + fh // 2:
                        c = (190, 30, 36)                 # red cheek stripes
                    put(px, alpha, x, y, c)
        for g in groups:
            for x, y in g:
                put(px, alpha, x, y, (10, 10, 12))
    elif look == "sage_mode":
        if face.ok and face.front:   # orange sage pigment round the eyes
            x0, y0, fw, fh = face.front
            for side in (-1, 1):
                for y in range(y0 + int(fh * 0.25), y0 + int(fh * 0.45)):
                    for x in range(face.cx + side * fw // 6, face.cx + side * fw // 2, side):
                        put(px, alpha, x, y, (226, 110, 30))
        for y in range(h):      # red cloak hem with black flames along the bottom of each painted area
            for x in range(w):
                if alpha[y][x] and not opaque(x, y + 2 * scale):
                    flame = (x // scale) % 4 < 2 and not opaque(x, y + scale)
                    put(px, alpha, x, y, (16, 12, 12) if flame else (192, 50, 30))
        lit = paint_eyes(px, alpha, groups, "sage", scale)
    elif look == "uzumaki":
        for y in range(h):      # black shoulders: the top band of each painted area
            for x in range(w):
                if alpha[y][x] and not opaque(x, y - 2 * scale):
                    put(px, alpha, x, y, (24, 22, 26))
        whiskers(px, alpha, face, scale)
        headband(px, alpha, w, h, face, scale)
        if face.torso:
            tx, ty, tw_, th_ = face.torso
            swirl(px, alpha, tx + tw_ / 2, ty + th_ / 2, min(tw_, th_) / 3)
        for g in groups:
            for x, y in g:
                put(px, alpha, x, y, (60, 150, 240))
    elif look == "byakugan":
        if face.ok and face.front:   # bulging veins beside the eyes
            x0, y0, fw, fh = face.front
            for side in (-1, 1):
                for k in range(3):
                    x, y = face.cx + side * fw // 3, y0 + int(fh * 0.35) + k * scale
                    for t in range(max(2, fw // 5)):
                        put(px, alpha, x + side * t, y + ((t + k) % 3 - 1), (110, 90, 150))
        lit = paint_eyes(px, alpha, groups, "byakugan", scale)
    elif look == "karma":
        # the Karma seal spreading from one point: diamond outlines and radiating lines
        isles = components([(x, y) for y in range(h) for x in range(w) if alpha[y][x] and not eye_mask[y][x]])
        if isles:
            biggest = max(isles, key=len)
            ox = sum(p[0] for p in biggest) // len(biggest)
            oy = sum(p[1] for p in biggest) // len(biggest)
            ink = (14, 12, 16)
            for ring in range(1, 6):
                rr = ring * 3 * scale
                for t in range(0, 360, 3):
                    a = math.radians(t)
                    f = 1 / (abs(math.cos(a)) + abs(math.sin(a)))      # a diamond, not a circle
                    x, y = int(ox + math.cos(a) * rr * f), int(oy + math.sin(a) * rr * f)
                    if ring % 2 == 1 or (t // 15) % 2 == 0:            # solid and dashed rings
                        put(px, alpha, x, y, ink)
                        put(px, alpha, x + 1, y, ink)
            for t in range(0, 360, 45):
                a = math.radians(t)
                for k in range(18 * scale):
                    x, y = int(ox + math.cos(a) * k), int(oy + math.sin(a) * k)
                    if opaque(x, y) and (k // scale) % 4 != 3:
                        put(px, alpha, x, y, ink)
                        put(px, alpha, x, y + 1, ink)
        lit = paint_eyes(px, alpha, groups, "jougan", scale)
    _cache[key] = (img, lit, edges, scale)
    return _cache[key]


def make(look):
    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None):
        if layer:
            return base.convert("RGBA").copy()
        return plan(look, base, eyes_img, seed, shiny, hints)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None):
        img, lit, edges, scale = plan(look, base, eyes_img, seed, shiny, hints)
        if name == "chakra":
            if not edges and not lit:
                return None
            out = Image.new("RGBA", img.size, (0, 0, 0, 0))
            o = out.load()
            frng = random.Random(f"chakra:{seed}:{shiny}:{frame}")
            glow = (255, 214, 60) if shiny else (255, 120, 20)
            for x, y in edges:
                if frng.random() < 0.55:
                    o[x, y] = glow + (200,)
            for x, y, c in lit:
                o[x, y] = c + (255,)
            return out
        return shine_layer(img.size, lit) if lit else None

    return retexture, extra_layer
