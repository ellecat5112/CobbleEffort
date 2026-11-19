"""Iron Titan (Normal/Fighting), the paradox Regigigas, built from boxes after the pixel art the user shared (the art's
own name; artist not named; the art also labels it "Regificial").

A great white barrel of a body under a black dome crowned with glowing green crystal spikes (where Regigigas grows
moss), big gold shoulder caps, and down its front a black panel of glowing yellow lights flanked by two columns of
glowing rings, green, yellow and pink, where Regigigas wears its coloured gems. Its arms are banded black and white
with heavy gold cuffs and big white three-fingered hands; its right hand holds a glowing pink energy orb out in front
of it. Banded legs with gold knee rings end in big white boots lit with glowing green panels.

Shiny: crimson cuffs and caps, cyan crystals and an orange orb.

Front is -z, y is up. 48 units tall; about 3.7 blocks.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _regi import ellipsoid, glowing, lit, speck
from _route import pal, tone

HEIGHT = 48
SCALE = round(3.7 * 16 / HEIGHT, 3)
HITBOX = [1.6, HEIGHT / 16]
KIND = "biped"
K = 3
LOOK = ("a white barrel-bodied titan under a black dome of glowing green crystals, with gold shoulder caps, a black "
        "front panel of yellow lights between columns of coloured rings, banded arms and a glowing pink orb in one hand")

BASE = {"white": (238, 238, 242), "white_shade": (204, 204, 212), "black": (32, 32, 38), "black_light": (60, 60, 70),
        "gold": (242, 192, 46), "gold_light": (252, 224, 120), "gold_dark": (196, 146, 30),
        "green": (90, 240, 92), "green_light": (196, 255, 176), "yellow": (250, 224, 60), "pink": (246, 84, 178),
        "pink_light": (255, 180, 226), "fleck": (255, 255, 240)}
SHINY = {"white": (214, 222, 238), "white_shade": (176, 186, 208), "black": (30, 36, 70), "black_light": (56, 64, 104),
         "gold": (214, 64, 66), "gold_light": (244, 130, 130), "gold_dark": (156, 36, 44), "green": (60, 228, 255),
         "green_light": (180, 246, 255), "pink": (255, 150, 40), "pink_light": (255, 212, 150)}
RINGS = ("green", "yellow", "pink")
CY = 28.5


def P(v):
    return pal(BASE, SHINY, v)


GREEN = glowing(P, "green", light="green_light")


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    ax = abs(x)
    if face == "north":
        t = (y - 31.0) / (10.5 if y < 31 else 12.0)
        if abs(t) < 1 and ax < 5.4 * (1 - t * t) ** 0.5:            # the black oval panel of yellow lights, in a V
            for row in range(6):
                yy = 23.5 + row * 2.5
                if (ax - (0.9 + 0.55 * row)) ** 2 + (y - yy) ** 2 < 0.62 ** 2:
                    return p["yellow"], p["yellow"]
            return lit(p["black"], face, y, CY, 10), None
        for i, key in enumerate(RINGS):                              # two columns of glowing rings
            r = ((ax - 8.3) ** 2 + (y - (33.4 - i * 4.2)) ** 2) ** 0.5
            if 0.75 < r < 1.75:
                return p[key], p[key]
    return lit(p["white"] if face != "south" else p["white_shade"], face, y, CY, 10), None


def domef(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["black_light"] if face == "up" else p["black"], face), None


def goldf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["gold_light"] if face == "up" else (p["gold"] if face != "down" else p["gold_dark"]), face), None


def bandf(x, y, z, face, variant, **k):
    """Banded black and white (rods: z runs along the rod, so the bands ring it)."""
    p = P(variant)
    if face not in ("north", "south") and (z % 3.0) < 1.3:
        return tone(p["black"], face), None
    return tone(p["white"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    if face not in ("up", "down") and (y % 3.0) < 1.3:
        return tone(p["black"], face), None
    return tone(p["white"], face), None


def bootf(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if y < 1.0:
            return tone(p["black"], face), None
        u = {"north": x - sx * 6.5, "south": x - sx * 6.5}.get(face, z + 0.5)
        if face not in ("up", "down") and 2.0 < y < 4.6 and abs(u) < 1.5:
            c = p["fleck"] if speck(x, y, z, face) else p["green"]
            return c, c                                                # glowing green panels
        return tone(p["white"], face), None
    return s


def orbf(x, y, z, face, variant, **k):
    p = P(variant)
    c = p["pink_light"] if speck(x, y, z, face, cell=1.4, r=0.4, prob=0.5) else p["pink"]
    return c, c


def hand(m, bone, wrist, palm_to, fingers):
    """A gold cuff, a white palm and three white fingers (each a rod with a rounded tip)."""
    d = tuple(b - a for a, b in zip(wrist, palm_to))
    cuff_end = tuple(a + 0.35 * v for a, v in zip(wrist, d))
    rod(m, bone, wrist, cuff_end, 7, goldf, extend=0.6)
    rod(m, bone, cuff_end, palm_to, 5, solid("white"), extend=0.6, t2=4)
    for tip in fingers:
        mid = tuple(a + 0.6 * (b - a) for a, b in zip(palm_to, tip))
        rod(m, bone, palm_to, mid, 1.9, solid("white"), extend=0.4)
        rod(m, bone, mid, tip, 1.6, solid("white"), extend=0.3)


def build() -> Model:
    m = Model("irontitan")
    top = m.bone("irontitan", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ellipsoid(m, bd, 0, CY, 0, 12.5, 10.5, 9.5, bodyf, step=1, squash=0.55)           # the white barrel body
    m.round_box(bd, 0, 0, 8, 6, 15, 19, solid("black"), cut=2)                         # its hips
    for (rx, rz, y0, y1, c) in ((9.5, 7.5, 37, 39, 2.5), (8, 6.5, 39, 41, 2), (6, 5, 41, 42, 1.5), (3.5, 3, 42, 43, 1)):
        m.round_box(bd, 0, 0.5, rx, rz, y0, y1, domef, cut=c)                          # the black dome
    for sx in (-1, 1):                                                                 # green crystal spikes
        for d, L, w in (((sx * 0.25, 1, 0), 5.5, 2.6), ((sx * 0.9, 0.8, -0.1), 4.2, 2.2), ((sx * 0.1, 0.9, 0.6), 3.6, 2.0)):
            spike(m, bd, (sx * 5.5, 40.5, 0.5), d, w, L, GREEN, tip=1.0)
        spike(m, bd, (sx * 2.0, 42.5, 0), (sx * 0.2, 1, -0.2), 1.8, 3.0, GREEN, tip=0.8)
        ellipsoid(m, bd, sx * 13.0, 34.5, 0, 4.5, 4.5, 4.5, goldf, step=1)              # gold shoulder caps
    # the left arm hangs, its hand open; the right holds a glowing pink orb out in front
    al = m.bone("arm_left", bd, (-14, 33, 0))
    rod(m, al, (-15, 32, 0), (-20.5, 25.5, -1), 5, bandf, extend=0.6)
    rod(m, al, (-20.5, 25.5, -1), (-29, 23.5, -2), 5.5, bandf, extend=0.6)
    hand(m, al, (-28.5, 23.6, -2), (-33.5, 22.6, -2.4),
         [(-37.5, 24.0, -4.4), (-38.0, 21.4, -2.4), (-36.5, 19.2, -0.8)])
    ar = m.bone("arm_right", bd, (14, 33, 0))
    rod(m, ar, (15, 32, 0), (19, 23.5, -3), 5, bandf, extend=0.6)
    rod(m, ar, (19, 23.5, -3), (21, 20, -10.5), 5.5, bandf, extend=0.6)
    rod(m, ar, (21, 20.2, -10), (21.3, 19.8, -12.6), 7.5, goldf, extend=0.4)          # gold cuff
    m.box(ar, 18.5, 16.0, -14.4, 24.5, 23.0, -12.4, solid("white"))                     # the palm, facing out
    for fx, fy in ((19.4, 23.0), (21.5, 23.6), (23.6, 23.0)):
        rod(m, ar, (fx, fy - 0.8, -13.4), (fx + (fx - 21.5) * 0.25, fy + 3.2, -14.6), 1.8, solid("white"), extend=0.3)
    rod(m, ar, (18.8, 18.0, -13.4), (17.0, 20.0, -15.0), 1.8, solid("white"), extend=0.3)  # thumb
    ellipsoid(m, ar, 21.5, 19.5, -16.8, 2.6, 2.6, 2.6, orbf, step=1)                   # the glowing pink orb
    for nm, sx in (("leg_left", -1), ("leg_right", 1)):
        lg = m.bone(nm, bd, (sx * 6.5, 16, 0))
        m.round_box(lg, sx * 6.5, 0, 3, 3, 7, 17, legf, cut=1)                         # banded legs
        m.round_box(lg, sx * 6.5, 0, 3.5, 3.5, 11, 13, goldf, cut=1)                   # gold knee rings
        m.round_box(lg, sx * 6.5, -0.5, 4, 5, 0, 7, bootf(sx), cut=1.5)                # big white boots
    return m
