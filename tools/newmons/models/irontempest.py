"""Iron Tempest (Electric/Steel), the future paradox Zapdos, built from boxes after the art the user shared (artist not
named, no name given; our name).

A robot Zapdos spread wide: two huge jagged lightning-bolt wings of glowing pale yellow with orange chevrons inside and
dark grey spikes jutting from behind them, all sprinkled with stars. Its head is a gold diamond face with two glowing
yellow pixel eyes inside a steel-blue throwing star, crowned by a V of tall gold spikes, and a long brown spear of a
beak juts forward and down. A small gold body with a glowing yellow chest diamond, black ball joints, a steel bulb
below and a fan of glowing tail spikes; orange legs banded in black reach forward with long black claws.

Shiny: icy blue lightning with violet chevrons.

Front is -z, y is up. 61 units tall; about 2.4 blocks (about 4.6 blocks across the wings).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _pgen1 import CLEAR, inside, scaled, stars, tri
from _regi import ellipsoid, lit
from _route import pal, tone

HEIGHT = 61
SCALE = round(2.4 * 16 / HEIGHT, 3)
HITBOX = [2.4, HEIGHT / 16]
KIND = "floater"
K = 3
LOOK = ("a robot Zapdos with huge jagged glowing yellow lightning wings, a gold diamond face with pixel eyes in a "
        "steel throwing star under a V of gold spikes, a long brown spear beak and banded orange legs with black claws")

BASE = {"bolt": (252, 250, 160), "bolt_edge": (196, 176, 40), "chev": (252, 192, 24), "chev_light": (255, 226, 120),
        "dark": (58, 58, 64), "dark_edge": (36, 36, 40), "star": (255, 255, 255), "gold": (226, 186, 112),
        "gold_dark": (176, 136, 70), "steel": (172, 184, 226), "steel_dark": (120, 132, 180), "eye": (255, 236, 60),
        "eye_dark": (150, 110, 20), "beak": (190, 110, 54), "beak_dark": (120, 64, 30), "black": (32, 32, 38),
        "orange": (210, 120, 70), "silver": (200, 206, 222)}
SHINY = {"bolt": (186, 236, 255), "bolt_edge": (80, 150, 210), "chev": (170, 110, 250), "chev_light": (214, 180, 255),
         "gold": (200, 206, 226), "gold_dark": (140, 150, 180), "eye": (120, 230, 255)}
CY = 31.0
WING = [(0, 4), (16, 24), (11, 12), (30, 14), (18, 5), (28, -4), (17, -6), (23, -20), (10, -12), (6, -22), (1, -8)]
INNER = scaled(WING, (3, 0), 0.6)
BACK = [(0, 8), (9, 22), (12, 15), (20, 21), (23, 10), (33, 5), (25, -2), (31, -11), (20, -10), (15, -25), (4, -14),
        (0, -10)]
SHOULDER = (4.0, 36.0)


def P(v):
    return pal(BASE, SHINY, v)


def solid(key):
    def s(x, y, z, face, variant, **k):
        return tone(P(variant)[key], face), None
    return s


def wingf(side):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = side * x - SHOULDER[0], y - SHOULDER[1]
        if not inside(WING, u, v):
            return CLEAR
        if not inside(scaled(WING, (3, 0), 0.94), u, v):
            return p["bolt_edge"], p["bolt_edge"]
        if stars(u, v, 0, "north", cell=1.7, r=0.3, prob=0.34):
            return p["star"], p["star"]
        if inside(INNER, u, v):
            c = p["chev_light"] if tri((u + abs(v) * 0.9) / 3.2) < 0.18 else p["chev"]   # chevrons pointing out
            return c, c
        return p["bolt"], p["bolt"]
    return s


def backf(side):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        u, v = side * x - SHOULDER[0], y - SHOULDER[1]
        if not inside(BACK, u, v):
            return CLEAR
        return (p["dark"] if inside(scaled(BACK, (3, 0), 0.95), u, v) else p["dark_edge"]), None
    return s


def tailfan(x, y, z, face, variant, **k):
    """A fan of five glowing spikes pointing down from (0, 13)."""
    p = P(variant)
    dx, dy = x, 19.5 - y
    if dy < 0:
        return CLEAR
    a = math.degrees(math.atan2(dx, dy))
    if abs(a) > 52:
        return CLEAR
    kk = (a + 50) / 25.0
    f = kk - round(kk)
    R = 5.0 + 10.0 * (0.4 + 0.6 * (1 - 2 * abs(f)))
    r = math.hypot(dx, dy)
    if r > R:
        return CLEAR
    if R - r < 0.7:
        return p["bolt_edge"], p["bolt_edge"]
    if stars(x, y, 0, "north", cell=1.5, r=0.28, prob=0.35):
        return p["star"], p["star"]
    c = p["chev"] if r < R * 0.55 else p["bolt"]
    return c, c


def starplate(x, y, z, face, variant, **k):
    """The steel-blue throwing star round the face (six points)."""
    p = P(variant)
    dx, dy = x, y - 41.6
    a = math.atan2(dy, dx)
    r = math.hypot(dx, dy)
    R = 3.4 + 4.4 * tri(a / (2 * math.pi / 6) + 0.5) ** 1.6
    if r > R:
        return CLEAR
    return (p["steel"] if (a % (2 * math.pi / 6)) < (math.pi / 6) else p["steel_dark"]), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            ex, ey = sx * 1.35, 42.3
            if abs(x - ex) < 1.0 and abs(y - ey) < 0.75:
                if ((x * 3) % 1.0 < 0.3) or ((y * 3) % 1.0 < 0.3):
                    return p["eye_dark"], None
                return p["eye"], p["eye"]
        if abs(x) + abs(y - 41.0) * 0.8 < 1.4:
            return p["bolt"], p["bolt"]
    return lit(p["gold"], face, y, 41.6, 3), None


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and z < -1.5 and abs(x) * 1.25 + abs(y - 31.5) < 3.6:
        c = p["bolt"] if abs(x) * 1.25 + abs(y - 31.5) < 2.6 else p["chev"]
        return c, c
    if abs(y - 34.8) < 0.3 or abs(y - 27.6) < 0.3:
        return lit(p["gold_dark"], face, y, CY, 6), None
    return lit(p["gold"], face, y, CY, 6), None


def beakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if d > box.size[2] * 0.8:
        return tone(p["beak_dark"], face), None
    if face == "up" and abs(x - (box.lo[0] + box.size[0] / 2)) < 0.3:
        return p["gold"], None
    return tone(p["beak"], face), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["black"] if (z % 1.8) < 0.6 else p["orange"], face), None


def build() -> Model:
    m = Model("irontempest")
    top = m.bone("irontempest", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    ellipsoid(m, bd, 0, CY, 0.4, 4.2, 6.2, 3.8, bodyf, step=1)                     # the gold body
    rod(m, bd, (0, 36.0, 0.2), (0, 39.4, 0), 2.4, solid("silver"), extend=0.3)     # neck
    for sx in (-1, 1):
        ellipsoid(m, bd, sx * 4.2, 25.6, 0.2, 2.0, 2.0, 2.0, solid("black"), step=1)   # ball joints
    ellipsoid(m, bd, 0, 22.6, 0.6, 2.6, 2.8, 2.6, solid("silver"), step=1)           # the steel bulb
    m.round_box(bd, 0, 0.8, 3.0, 2.0, 18.4, 20.4, solid("gold"), cut=1)              # tail bracket
    m.box(bd, -13, 4.0, 0.8, 13, 19.6, 0.8, tailfan)                                   # the tail fan
    hd = m.bone("head", bd, (0, 40, 0))
    m.round_box(hd, 0, -0.2, 2.8, 2.6, 39.2, 44.2, headf, cut=1)                    # gold diamond face
    m.box(hd, -8, 33.5, -1.0, 8, 50, -1.0, starplate)                                  # steel throwing star
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.2, 43.4, 0.2), (sx * 0.42, 1, 0.12), 2.6, 9.4, solid("gold"), tip=1.2)   # gold V crest
    rod(m, hd, (0, 41.0, -2.4), (0, 36.2, -11.0), 2.2, beakf, extend=0.3)          # the spear beak
    rod(m, hd, (0, 36.4, -10.6), (0, 34.4, -14.2), 1.2, beakf, extend=0.2)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):
        wg = m.bone(nm, bd, (sx * SHOULDER[0], SHOULDER[1], 0.6))
        x0, x1 = sorted((sx * 3.5, sx * 36.0))
        m.box(wg, x0, 12.0, 0.6, x1, 61.0, 0.6, wingf(sx))
        m.box(wg, x0, 10.0, 1.4, x1, 61.0, 1.4, backf(sx))
        rod(m, wg, (sx * 3.0, 35.8, 0.6), (sx * 6.5, 37.0, 0.6), 2.0, solid("gold_dark"), extend=0.3)   # wing root
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, bd, (sx * 4.2, 25.6, 0.2))
        knee, wrist = (sx * 7.2, 22.0, -3.6), (sx * 9.0, 20.4, -8.2)
        rod(m, lg, (sx * 4.6, 25.0, -0.6), knee, 1.6, legf, extend=0.5)
        rod(m, lg, knee, wrist, 1.4, legf, extend=0.4)
        for d in ((0.5, 0.3, -1), (0.1, 0.0, -1), (-0.3, -0.3, -1), (0.9, -0.2, -0.6)):
            a = (wrist[0] + sx * d[0] * 1.2, wrist[1] + d[1] * 1.2, wrist[2] + d[2] * 1.2)
            b = (a[0] + sx * d[0] * 2.4, a[1] + d[1] * 2.4 + 0.8, a[2] + d[2] * 2.4)
            rod(m, lg, wrist, a, 0.9, legf, extend=0.3)
            spike(m, lg, a, (b[0] - a[0], b[1] - a[1] - 1.6, b[2] - a[2]), 0.8, 2.6, solid("black"), tip=0.4)
    return m
