"""Iron Radiance (Fire/Psychic), the future paradox Ho-Oh, built from boxes after @goldmills_'s art (the art's own
name).

A robot Ho-Oh in flight: a scarlet armoured head under a tall crest of golden curls, a gold beak and a dark eye, a
neck jointed in grey, and a body of scarlet plates round a great glowing belly that fades from gold to pale peach.
Its wings rise from scarlet armoured arms edged with white plates, trailing broad sheets of glowing feathers that
shade from orange at the arm to pale gold at their striped tips; a fan of glowing gold tail feathers hangs below,
and its dark grey legs end in black talons.

Shiny: silver plates with violet and rose light.

Front is -z, y is up. 62 units tall (wings up); about 3.4 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, band_wing, smooth_path, stars, tri
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 62
SCALE = round(3.4 * 16 / HEIGHT, 3)
HITBOX = [2.0, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a robot Ho-Oh with a scarlet armoured head under golden curls, a glowing gold-to-peach belly, scarlet wing "
        "arms trailing sheets of glowing orange-to-gold feathers and a fan of glowing gold tail feathers")

BASE = {"red": (220, 70, 56), "red_dark": (166, 40, 38), "red_light": (246, 120, 92), "gold": (246, 196, 70),
        "gold_dark": (200, 146, 40), "gold_light": (255, 230, 140), "grey": (150, 150, 160), "grey_dark": (96, 96, 108),
        "white": (234, 234, 240), "orange": (252, 150, 60), "peach": (255, 222, 170), "peach_light": (255, 244, 214),
        "black": (34, 32, 38), "eye": (40, 20, 24), "beak": (240, 196, 80), "spark": (255, 255, 255)}
SHINY = {"red": (186, 190, 206), "red_dark": (130, 134, 152), "red_light": (222, 226, 238), "orange": (196, 120, 250),
         "peach": (255, 190, 220), "peach_light": (255, 226, 240), "gold": (226, 150, 230), "gold_light": (250, 210, 250)}
CY = 30.0


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, **k):
    """Scarlet plates round a great glowing belly that fades from gold to pale peach."""
    p = P(variant)
    e = (x / 3.6) ** 2 + ((y - 28.0) / 5.6) ** 2
    if face == "north" and z < -1.0 and e < 1:
        t = max(0.0, min(1.0, (32.0 - y) / 9.0))
        c = mix(p["gold"], p["peach_light"], t)
        return c, c
    if abs(y - 34.6) < 0.3:
        return lit(p["red_dark"], face, y, CY, 7), None
    return lit(p["red"] if face != "south" else p["red_dark"], face, y, CY, 7), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 2.4, y - 45.4) < 0.55:
        return p["eye"], None
    return lit(p["red"], face, y, 45, 3), None


def wing_shader(curve, width):
    def sh(x, y, z, face, variant, u=0.0, **k):
        p = P(variant)
        t, s, lat = curve.locate(u, y)
        if lat > 0.9:
            return CLEAR
        w = width(t) * (1 - 0.18 * ((t * 8) % 1.0))                      # feather steps
        if s < -0.5 or s > w or w <= 0.2:
            return CLEAR
        f = max(0.0, s) / max(w, 0.01)
        if f > 0.78 and ((t * 8) % 1.0) < 0.12:
            return p["white"], p["white"]                                   # striped feather tips
        if stars(u, y, 0, "north", cell=2.0, r=0.3, prob=0.22):
            return p["spark"], p["spark"]
        c = mix(p["orange"], p["peach_light"], min(1.0, f * 1.15))
        return c, c
    return sh


def width(t):
    return 2.0 + 12.0 * max(0.0, math.sin(math.pi * (0.1 + 0.9 * t))) ** 0.8


ARM = [(4.0, 36.0), (12.0, 43.0), (21.0, 53.0), (27.0, 61.5)]


def tailfan(x, y, z, face, variant, **k):
    """A fan of glowing gold tail feathers hanging below the body (an xy plane)."""
    p = P(variant)
    dx, dy = x, 22.6 - y
    if dy < 0:
        return CLEAR
    a = math.degrees(math.atan2(dx, dy))
    if abs(a) > 48:
        return CLEAR
    f = (a + 48) / 96 * 7
    R = 13.0 * (1 - 0.14 * (abs(a) / 48)) - 2.4 * abs((f % 1.0) - 0.5) * 2
    r = math.hypot(dx, dy)
    if r > R:
        return CLEAR
    if abs((f % 1.0) - 0.5) < 0.06:
        return p["gold_dark"], p["gold_dark"]
    c = mix(p["gold"], p["gold_light"], r / R)
    return c, c


def build() -> Model:
    m = Model("ironradiance")
    top = m.bone("ironradiance", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 4.6, 7.4, 4.4, bodyf, step=1)                    # scarlet body, glowing belly
    for i in range(3):                                                            # grey-jointed neck
        a, b = (0, 36.6 + i * 2.2, -0.2 - i * 0.5), (0, 38.4 + i * 2.2, -0.6 - i * 0.5)
        rod(m, bd, a, b, 2.8, solid("red" if i % 2 == 0 else "grey"), extend=0.4)
    hd = m.bone("head", bd, (0, 43.0, -1.6))
    m.round_box(hd, 0, -1.8, 2.4, 2.8, 43.2, 47.6, headf, cut=1)                  # scarlet armoured head
    rod(m, hd, (0, 45.4, -4.4), (0, 44.2, -8.0), 1.8, solid("beak"), extend=0.3, t2=1.4)
    spike(m, hd, (0, 44.4, -7.8), (0, -1, -0.3), 1.2, 1.4, solid("gold_dark"))
    crest = smooth_path([(0, 47.4, -2.6), (0, 51.0, -3.2), (0, 54.0, -1.6), (0, 55.0, 1.0), (0, 53.4, 2.6)], 10)
    for i, (a, b) in enumerate(zip(crest, crest[1:])):                            # tall crest of golden curls
        w = 3.6 - 1.8 * i / len(crest)
        rod(m, hd, a, b, w, solid("gold" if i % 2 else "gold_light"), extend=0.7, t2=max(1.2, w * 0.8))
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.2, 47.0, -1.6), (sx * 2.4, 50.6, 0.6), 1.6, solid("gold_dark"), extend=0.4)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # scarlet arms, glowing feathers
        wg = m.bone(nm, bd, (sx * ARM[0][0], ARM[0][1], 0.8))
        c = band_wing(m, wg, sx, ARM, width, 1.2, wing_shader, (3.0, 36.0, 24.0, 63.0))
        knots = [c.at(t) for t in (0.0, 0.25, 0.5, 0.72, 0.9)]
        for a, b in zip(knots, knots[1:]):
            rod(m, wg, (sx * a[0], a[1], 0.6), (sx * b[0], b[1], 0.6), 2.4, solid("red"), extend=0.3)
        for kx, ky in knots[1:4]:                                                 # white plates on the arm
            m.box(wg, sx * kx - 1.3, ky - 2.2, -0.4, sx * kx + 1.3, ky - 0.4, 1.8, solid("white"))
    m.box(bd, -14.0, 8.0, 1.6, 14.0, 23.0, 1.6, tailfan)                           # glowing gold tail fan
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):                          # dark grey legs, black talons
        lg = m.bone(nm, bd, (sx * 2.4, 24.5, -0.6))
        ellipsoid(m, lg, sx * 2.4, 23.8, -0.6, 2.0, 2.2, 2.0, solid("red_dark"), step=1)
        knee, ank = (sx * 2.6, 19.6, -2.4), (sx * 2.7, 15.6, -3.4)
        rod(m, lg, (sx * 2.4, 22.0, -0.8), knee, 1.2, solid("grey_dark"), extend=0.4)
        rod(m, lg, knee, ank, 1.2, solid("grey_dark"), extend=0.4)
        for d in ((-0.45, -0.8, -1), (0, -0.9, -1), (0.45, -0.8, -1), (0, -0.5, 1)):
            spike(m, lg, ank, (d[0] * sx, d[1], d[2]), 0.9, 2.6, solid("black"), tip=0.5)
    return m
