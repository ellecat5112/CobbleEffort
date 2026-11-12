"""
Shared toolkit for the Tarot collection: each line is one card of the Major Arcana.

Every card: the card's palette (the body recoloured by brightness, keeping a little of the original colour so markings
stay readable), a faint background pattern, a gilded card border round every painted area (gold with an ink line
inside), the card's symbol on the chest, its Roman numeral on the forehead, glowing eyes in the card's colour, and an
animated gold-foil sheen (FOIL) that runs over the gilding.
Shiny: the card REVERSED: the palette's hue turned half-way round, silver foil instead of gold, the numeral upside down.

Cards: fool (0), high_priestess (II), emperor (IV), lovers (VI), chariot (VII), strength (VIII), hermit (IX),
wheel (X), justice (XI), death (XIII), temperance (XIV), devil (XV), tower (XVI), star (XVII), moon (XVIII),
sun (XIX), judgement (XX), world (XXI). The symbols are drawn from scratch from the cards' traditional imagery.
"""
from __future__ import annotations

import colorsys
import math
import random

from PIL import Image

from ._animatronic import Face, put
from ._festive import digest
from ._horror import components, find_eye_mask, mix

EYESHINE = {"name": "eyeshine", "emissive": True, "translucent": True}
FOIL = {"name": "foil", "emissive": True, "translucent": True, "frames": 4, "fps": 6}

GOLD = [(118, 80, 18), (196, 150, 46), (246, 210, 96), (255, 244, 186)]
SILVER = [(92, 96, 108), (160, 166, 180), (214, 220, 232), (250, 252, 255)]
INK = (26, 18, 14)

# card -> (numeral, palette dark/mid/light, accent, eye colour, background pattern)
CARDS = {
    "fool":           ("0",     [(120, 86, 22), (240, 200, 64), (255, 248, 222)], (214, 50, 40), (80, 160, 250), "harlequin"),
    "high_priestess": ("II",    [(16, 24, 74), (58, 88, 168), (220, 230, 252)], (196, 40, 60), (190, 220, 255), "pomegranate"),
    "emperor":        ("IV",    [(88, 18, 10), (198, 70, 30), (255, 172, 92)], (240, 200, 80), (255, 210, 80), "steps"),
    "lovers":         ("VI",    [(116, 20, 48), (230, 92, 122), (255, 214, 224)], (70, 160, 60), (110, 230, 120), "hearts"),
    "chariot":        ("VII",   [(12, 16, 48), (38, 58, 128), (170, 190, 232)], (230, 230, 240), (220, 230, 255), "stars"),
    "strength":       ("VIII",  [(148, 108, 40), (238, 208, 140), (255, 250, 236)], (220, 90, 40), (255, 170, 40), "flowers"),
    "hermit":         ("IX",    [(28, 28, 46), (88, 90, 118), (190, 190, 210)], (255, 220, 120), (255, 214, 110), "snow"),
    "wheel":          ("X",     [(18, 58, 118), (70, 140, 210), (212, 236, 255)], (240, 200, 70), (255, 220, 90), "wheels"),
    "justice":        ("XI",    [(78, 10, 20), (168, 30, 40), (240, 150, 140)], (110, 50, 140), (255, 210, 80), "drape"),
    "death":          ("XIII",  [(8, 8, 12), (48, 46, 54), (140, 136, 150)], (240, 238, 232), (240, 244, 255), "ribs"),
    "temperance":     ("XIV",   [(52, 92, 156), (150, 190, 236), (255, 246, 226)], (240, 140, 40), (255, 200, 90), "ripples"),
    "devil":          ("XV",    [(20, 6, 8), (118, 14, 20), (220, 70, 50)], (10, 10, 10), (255, 40, 30), "chains"),
    "tower":          ("XVI",   [(40, 40, 48), (110, 108, 118), (190, 186, 190)], (255, 140, 30), (255, 150, 40), "bricks"),
    "star":           ("XVII",  [(10, 14, 50), (40, 60, 140), (160, 190, 255)], (255, 240, 140), (255, 255, 255), "sparkles"),
    "moon":           ("XVIII", [(20, 18, 60), (90, 80, 160), (220, 220, 250)], (250, 230, 140), (255, 236, 120), "drops"),
    "sun":            ("XIX",   [(170, 70, 10), (250, 170, 30), (255, 240, 160)], (220, 60, 20), (255, 130, 30), "sunflowers"),
    "judgement":      ("XX",    [(58, 88, 128), (150, 180, 210), (240, 246, 255)], (200, 30, 40), (255, 255, 255), "clouds"),
    "world":          ("XXI",   [(40, 10, 70), (110, 50, 170), (220, 180, 250)], (60, 170, 80), (120, 255, 150), "sparkles"),
}


# ---------------------------------------------------------------------------------------------
# colour
# ---------------------------------------------------------------------------------------------

def lum(c):
    return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255


def rotate_hue(c, turn):
    h, l, s = colorsys.rgb_to_hls(c[0] / 255, c[1] / 255, c[2] / 255)
    r, g, b = colorsys.hls_to_rgb((h + turn) % 1.0, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def palette(card, shiny):
    numeral, pal, accent, eye, pattern = CARDS[card]
    if shiny:
        pal = [rotate_hue(c, 0.5) for c in pal]
        accent, eye = rotate_hue(accent, 0.5), rotate_hue(eye, 0.5)
    return pal, accent, eye


def card_colour(c, pal):
    v = lum(c)
    if v < 0.5:
        out = mix(pal[0], pal[1], v / 0.5)
    else:
        out = mix(pal[1], pal[2], (v - 0.5) / 0.5)
    return mix(out, c, 0.14)                     # a trace of the original keeps the markings readable


# ---------------------------------------------------------------------------------------------
# symbols: f(u, v) -> colour or None, u and v in [-1, 1] across the drawing area (v down)
# ---------------------------------------------------------------------------------------------

def _star(u, v, points, r_out, r_in, rot=-math.pi / 2):
    a = math.atan2(v, u) - rot
    d = math.hypot(u, v)
    seg = 2 * math.pi / points
    t = (a % seg) / seg
    t = abs(t - 0.5) * 2                              # 1 at a point, 0 between points
    r = r_in + (r_out - r_in) * t ** 1.6
    return d <= r


def _rose(u, v, petal, centre):
    d = math.hypot(u, v)
    a = math.atan2(v, u)
    if d < 0.22:
        return centre
    if d < 0.62 + 0.24 * math.cos(5 * a):
        return petal
    return None


def symbol(card, u, v, gold, accent, light, dark):
    d = math.hypot(u, v)
    if card == "fool":                                       # a white rose
        return _rose(u, v, (250, 250, 246), gold)
    if card == "high_priestess":                             # a crescent moon between the two pillars
        if abs(u) > 0.78:
            return (16, 14, 18) if u < 0 else (244, 244, 240)
        if d < 0.62 and math.hypot(u - 0.26, v - 0.08) > 0.5:
            return light
        return None
    if card == "emperor":                                    # the ankh sceptre
        if abs(u) < 0.13 and -0.1 < v < 0.95:
            return gold
        if abs(v - 0.05) < 0.11 and abs(u) < 0.55:
            return gold
        if 0.18 < math.hypot(u / 0.75, (v + 0.48) / 0.85) * 0.5 < 0.27:
            return gold
        return None
    if card == "lovers":                                     # a heart with an apple-green leaf
        x, y = u * 1.25, -(v - 0.12) * 1.25
        if (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0:
            return accent if (abs(u - 0.15) < 0.12 and v < -0.55) else (220, 40, 70)
        if math.hypot(u - 0.3, v + 0.85) < 0.18:
            return accent
        return None
    if card == "chariot":                                    # a winged sun disc
        if d < 0.32:
            return gold
        if abs(v) < 0.28 - abs(u) * 0.18 and 0.3 < abs(u) < 1.0 and (int((abs(u) - 0.3) * 12) % 2 == 0 or abs(v) < 0.08):
            return light
        return None
    if card == "strength":                                   # the lemniscate (infinity) over a garland
        x, y = u * 1.15, v * 1.6
        lem = (x * x + y * y) ** 2 - (x * x - y * y)
        if abs(lem) < 0.12 and abs(v) < 0.6:
            return gold
        if v > 0.62 and (int(u * 6) % 2 == 0):
            return accent
        return None
    if card == "hermit":                                     # a lantern with a six-pointed star
        if abs(u) <= 0.5 and -0.7 <= v <= 0.75:
            if abs(u) > 0.4 or v < -0.6 or v > 0.66:
                return gold
            if _star(u * 1.5, (v - 0.05) * 1.5, 6, 0.7, 0.35):
                return (255, 238, 150)
            return (60, 50, 30)
        if abs(u) < 0.12 and -0.95 < v < -0.7:
            return gold
        return None
    if card == "wheel":                                      # the wheel: rim, hub, eight spokes
        if 0.72 < d < 0.92 or d < 0.2:
            return gold
        a = math.atan2(v, u)
        if d < 0.72 and min(abs((a % (math.pi / 4)) - 0), abs((a % (math.pi / 4)) - math.pi / 4)) * d < 0.06:
            return gold
        return None
    if card == "justice":                                    # the scales
        if abs(u) < 0.07 and -0.9 < v < 0.8:
            return gold
        if abs(v + 0.62) < 0.07 and abs(u) < 0.8:
            return gold
        for sx in (-0.62, 0.62):
            if abs(abs(u - sx) - (v + 0.62) * 0.4) < 0.06 and -0.62 < v < 0.1:
                return gold                                  # the pans' cords
            if math.hypot(u - sx, v - 0.05) < 0.3 and v > 0.05:
                return gold                                  # the pans
        if abs(v - 0.82) < 0.08 and abs(u) < 0.35:
            return gold
        return None
    if card == "death":                                      # the white rose on a black banner
        if abs(u) < 0.95 and abs(v) < 0.95:
            r = _rose(u * 1.1, v * 1.1, (244, 242, 236), (200, 170, 60))
            return r if r else (8, 8, 10)
        return None
    if card == "temperance":                                 # a triangle within a square
        if abs(u) < 0.75 and abs(v) < 0.75 and (abs(u) > 0.62 or abs(v) > 0.62):
            return (250, 250, 250)
        if -0.5 < v < 0.5 and abs(u) < (v + 0.5) * 0.55:
            return accent
        return None
    if card == "devil":                                      # an inverted pentagram in a circle
        if 0.82 < d < 0.95:
            return (200, 20, 20)
        if _star(u, v, 5, 0.8, 0.3, rot=math.pi / 2) and not _star(u, v, 5, 0.6, 0.2, rot=math.pi / 2):
            return (200, 20, 20)
        return None
    if card == "tower":                                      # the tower struck by lightning, its crown flying
        if abs(u) < 0.32 and -0.45 < v < 0.95:
            if -0.45 < v < -0.32 and int((u + 0.32) * 10) % 2 == 0:
                return None
            return (150, 146, 150) if (int((v + 1) * 8) + (1 if int((u + 1) * 6) % 2 else 0)) % 2 else (120, 116, 122)
        if abs((u - 0.1) - (v + 0.6) * -0.6) < 0.1 and -0.95 < v < -0.1 and (int((v + 1) * 6) % 2 == 0 or abs(u) > 0.3):
            return (255, 230, 60)                            # the bolt
        if -0.9 < v < -0.62 and 0.42 < u < 0.85:
            return gold                                      # the crown, knocked off
        return None
    if card == "star":                                       # the great eight-pointed star and seven small ones
        if _star(u, v, 8, 0.8, 0.28):
            return (255, 240, 140)
        for k in range(7):
            a = k / 7 * math.tau
            if _star(u - math.cos(a) * 0.85, v - math.sin(a) * 0.85, 8, 0.14, 0.05):
                return (250, 250, 255)
        return None
    if card == "moon":                                       # the moon with its face, and falling drops
        if d < 0.62:
            if math.hypot(u + 0.22, v) < 0.5:
                return (238, 226, 150)
            return (200, 186, 110)
        if 0.66 < d < 0.98 and int(math.atan2(v, u) / math.tau * 16) % 2 == 0:
            return (238, 226, 150)                           # rays
        return None
    if card == "sun":                                        # the sun with wavy rays
        a = math.atan2(v, u)
        if d < 0.5:
            return (255, 214, 60) if d < 0.42 else (220, 120, 20)
        if d < 0.62 + 0.3 * abs(math.sin(a * 6)) and int((a + math.pi) / math.tau * 12) % 2 == 0:
            return (250, 160, 30)
        return None
    if card == "judgement":                                  # the banner: a red cross on white, on a trumpet
        if abs(u) < 0.6 and -0.8 < v < 0.3:
            if abs(u) < 0.12 or abs(v + 0.25) < 0.12:
                return (200, 30, 40)
            return (246, 246, 246)
        if abs(u - (v - 0.3) * 0.2) < 0.08 and 0.3 <= v < 0.95:
            return gold
        return None
    if card == "world":                                      # the laurel wreath
        e = math.hypot(u / 0.6, v / 0.92)
        if 0.82 < e < 1.0:
            a = math.atan2(v, u)
            return (60, 160, 70) if int(a / math.tau * 28) % 2 else (40, 120, 50)
        if e < 0.82 and abs(u) < 0.08 and abs(v) < 0.4:
            return (200, 120, 230)
        return None
    return None


# ---------------------------------------------------------------------------------------------
# patterns, numerals
# ---------------------------------------------------------------------------------------------

def pattern(kind, x, y, s, pal, accent, rng_v):
    """A faint background pattern colour for texel (x, y) or None (s = texture scale)."""
    X, Y = x // s, y // s
    if kind == "harlequin":
        return pal[2] if ((X + Y) // 4 + (X - Y) // 4) % 2 == 0 else None
    if kind == "pomegranate":
        return accent if (X % 9, Y % 9) in ((3, 4), (4, 4), (3, 3)) else None
    if kind == "steps":
        return pal[0] if (Y % 6 == 0) or ((X + (Y // 6) * 3) % 8 == 0) else None
    if kind == "hearts":
        return accent if (X % 12, Y % 12) in ((2, 3), (4, 3), (3, 4)) else None
    if kind in ("stars", "sparkles"):
        return (250, 248, 220) if rng_v > 0.985 else None
    if kind == "flowers":
        return accent if (X % 10, Y % 10) in ((5, 5), (4, 5), (6, 5), (5, 4), (5, 6)) and (X // 10 + Y // 10) % 2 else None
    if kind == "snow":
        return pal[2] if rng_v > 0.988 else None
    if kind == "wheels":
        return pal[2] if (X % 14 - 7) ** 2 + (Y % 14 - 7) ** 2 in (4, 5) else None
    if kind == "drape":
        return pal[0] if X % 5 == 0 else None
    if kind == "ribs":
        return pal[2] if Y % 5 == 0 and X % 9 not in (0, 1) else None
    if kind == "ripples":
        return (120, 180, 230) if (Y + int(2 * math.sin(X / 3))) % 7 == 0 else None
    if kind == "chains":
        return (20, 16, 16) if ((X % 6 in (0, 5)) and (Y % 8 < 5)) or (Y % 8 in (0, 4) and X % 6 < 6 and X % 6 > 0) and (X // 6) % 2 else None
    if kind == "bricks":
        return pal[0] if Y % 4 == 0 or (X + (4 if (Y // 4) % 2 else 0)) % 8 == 0 else None
    if kind == "drops":
        return accent if (X % 8, Y % 11) in ((3, 2), (3, 3), (2, 3), (4, 3)) else None
    if kind == "sunflowers":
        return accent if (X % 11 - 5) ** 2 + (Y % 11 - 5) ** 2 <= 2 else None
    if kind == "clouds":
        return pal[2] if math.sin(X / 4) + math.sin(Y / 3 + X / 7) > 1.6 else None
    return None


GLYPHS = {   # 3x5 pixel numerals
    "I": ["#", "#", "#", "#", "#"],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "0": ["###", "#.#", "#.#", "#.#", "###"],
}


def numeral_cells(text, upside_down):
    """Pixel offsets of a Roman numeral (letters one column apart), centred on (0, 0)."""
    cells, x = [], 0
    for ch in text:
        g = GLYPHS[ch]
        for gy, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == "#":
                    cells.append((x + gx, gy))
        x += len(g[0]) + 1
    wdt = x - 1
    out = [(cx - wdt // 2, cy - 2) for cx, cy in cells]
    if upside_down:
        out = [(-cx, -cy) for cx, cy in out]
    return out, wdt


# ---------------------------------------------------------------------------------------------
# planning
# ---------------------------------------------------------------------------------------------

_cache: dict = {}


def plan(card, base, eyes_img, seed, shiny, hints):
    key = (card, digest(base), digest(eyes_img), seed, shiny, repr(hints))
    if key in _cache:
        return _cache[key]
    _cache.clear()
    rng = random.Random(seed)
    base = base.convert("RGBA")
    w, h = base.size
    src = base.load()
    s = max(1, w // 64)
    alpha = [[src[x, y][3] for x in range(w)] for y in range(h)]
    eye_mask = find_eye_mask(base, eyes_img)
    face = Face(eye_mask, alpha, w, h, hints)
    pal, accent, eye_c = palette(card, shiny)
    foil = SILVER if shiny else GOLD
    kind = CARDS[card][4]
    img = Image.new("RGBA", (w, h))
    px = img.load()
    memo = {}

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and alpha[y][x]

    # 1. the card's palette and its background pattern
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                px[x, y] = (0, 0, 0, 0)
                continue
            if (r, g, b) not in memo:
                memo[(r, g, b)] = card_colour((r, g, b), pal)
            c = memo[(r, g, b)]
            if not eye_mask[y][x]:
                p = pattern(kind, x, y, s, pal, accent, rng.random())
                if p is not None:
                    c = mix(c, p, 0.55)
            px[x, y] = c + (a,)
    gilt = []
    # 2-3. a tarot card on the chest (or on the biggest area when the model has no chest face): a gold frame, an ink
    # line, parchment, and the card's symbol
    area = face.torso
    if not area:
        isles = components([(x, y) for y in range(h) for x in range(w) if alpha[y][x] and not eye_mask[y][x]])
        if isles:
            big = max(isles, key=len)
            xs, ys = [p[0] for p in big], [p[1] for p in big]
            cx, cy = sum(xs) // len(xs), sum(ys) // len(ys)
            side = max(6, int(math.sqrt(len(big)) * 0.6))
            area = (cx - side // 2, cy - side // 2, side, side)
    if area:
        ax, ay, aw, ah = area
        pad = s if min(aw, ah) > 12 else 0
        cw, ch = max(5, aw - 2 * pad), max(5, ah - 2 * pad)   # the card fills the chest
        sx0, sy0 = ax + (aw - cw) // 2, ay + (ah - ch) // 2
        parchment = mix(pal[2], (250, 240, 214), 0.55)
        fr = max(1, s)
        ink = fr if min(cw, ch) >= 14 else 0
        m = fr + ink                                          # the symbol: in the biggest centred square inside
        side = max(3, min(cw, ch) - 2 * m)
        qx0, qy0 = sx0 + (cw - side) // 2, sy0 + (ch - side) // 2
        for y in range(sy0, sy0 + ch):
            for x in range(sx0, sx0 + cw):
                if not opaque(x, y) or eye_mask[y][x]:
                    continue
                edge = min(x - sx0, sx0 + cw - 1 - x, y - sy0, sy0 + ch - 1 - y)
                if edge < fr:
                    put(px, alpha, x, y, foil[3] if (x + y) % 4 == 0 else foil[2])
                    gilt.append((x, y))
                    continue
                if edge < fr + ink:
                    put(px, alpha, x, y, INK)
                    continue
                c = None
                if qx0 <= x < qx0 + side and qy0 <= y < qy0 + side:
                    u = (x + 0.5 - qx0) / side * 2 - 1
                    v = (y + 0.5 - qy0) / side * 2 - 1
                    if shiny:
                        u, v = -u, -v                       # reversed
                    c = symbol(card, u, v, foil[2], accent, pal[2], pal[0])
                put(px, alpha, x, y, c if c is not None else parchment)
                if c is not None and c in (foil[2], (255, 238, 150), (255, 240, 140)):
                    gilt.append((x, y))
    # 4. the numeral on the forehead (or above the symbol)
    cells, wdt = numeral_cells(CARDS[card][0], shiny)
    if face.ok and face.front:
        x0, y0, fw, fh = face.front
        nx, ny, ns = face.cx, y0 + max(3 * s, int(fh * 0.16)), max(1, min(s, fw // max(1, wdt + 2)))
    elif area:
        nx, ny, ns = area[0] + area[2] // 2, area[1] - 4 * s, s
    else:
        nx = None
    if nx is not None:
        for cx, cy in cells:
            for dy in range(ns):
                for dx in range(ns):
                    x, y = nx + cx * ns + dx, ny + cy * ns + dy
                    if opaque(x, y) and not eye_mask[y][x]:
                        put(px, alpha, x, y, foil[1])
                        gilt.append((x, y))
    # 5. the eyes glow in the card's colour
    lit = []
    for y in range(h):
        for x in range(w):
            if eye_mask[y][x] and alpha[y][x]:
                put(px, alpha, x, y, eye_c)
                lit.append((x, y, eye_c))
    glints = [(x, y) for y in range(h) for x in range(w) if alpha[y][x] and px[x, y][:3] == (250, 248, 220)]
    _cache[key] = (img, lit, gilt, glints, foil)
    return _cache[key]


def make(card):
    def retexture(base, eyes_img, seed, shiny, frame: int = 0, layer=False, hints=None):
        if layer:
            return base.convert("RGBA").copy()
        return plan(card, base, eyes_img, seed, shiny, hints)[0].copy()

    def extra_layer(name, base, eyes_img, seed, shiny, frame, hints=None):
        img, lit, gilt, glints, foil = plan(card, base, eyes_img, seed, shiny, hints)
        out = Image.new("RGBA", img.size, (0, 0, 0, 0))
        o = out.load()
        if name == "eyeshine":
            if not lit:
                return None
            for x, y, c in lit:
                o[x, y] = tuple(c) + (255,)
            return out
        if name == "foil":
            if not gilt and not glints:
                return None
            w, hh = img.size
            period = max(16, (w + hh) // 3)
            band = max(3, period // 6)
            for x, y in gilt:                                # a sheen sweeping diagonally across the gilding
                t = (x + y - frame * period // 4) % period
                if t < band:
                    o[x, y] = foil[3] + (235,)
                else:
                    o[x, y] = foil[2] + (70,)
            trng = random.Random(f"glint:{seed}:{shiny}:{frame}")
            for x, y in glints:                              # twinkling stars
                if trng.random() < 0.5:
                    o[x, y] = (255, 255, 236, 255)
            return out
        return None

    return retexture, extra_layer
