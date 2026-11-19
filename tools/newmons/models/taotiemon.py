"""Taotiemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a small imp in a black suit with fluffy white fur cuffs and boots, pink claws, crouched under a
colossal teal bronze ritual-vessel mask carved with taotie spirals and hung with yellow ofuda tags, a huge lavender
cloud billowing behind it. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a small imp in a black suit under a colossal teal bronze taotie mask hung with yellow tags, a huge lavender cloud behind it"
BASE = {"bronze": (90, 160, 150), "bronze_dark": (40, 90, 90), "suit": (40, 40, 48), "suit_dark": (16, 16, 20),
        "white": (248, 248, 252), "white_dark": (200, 200, 214), "pink": (240, 110, 160), "tag": (250, 220, 60),
        "ink": (200, 40, 30), "cloud": (220, 210, 250, 200), "eye": (230, 40, 60), "gold": (220, 170, 60)}
SHINY = {"bronze": (190, 130, 60), "bronze_dark": (120, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


BRONZE = metal(P, "bronze", dark="bronze_dark")


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if face in ("north", "east", "west", "south"):
        # carved spirals: rings round a few centres
        for cx, cy in ((-6.0, 38.0), (6.0, 38.0), (-3.0, 31.0), (3.0, 31.0), (0, 44.0)):
            d = math.hypot(a - cx, b - cy)
            if d < 3.2 and (d % 1.2) < 0.35:
                return tone(p["bronze_dark"], face), None
    return BRONZE(x, y, z, face, variant, box=box, **k)


def tagf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and abs(x - box.lo[0] - box.size[0] / 2) < 0.3 and int(y * 2) % 3:
        return p["ink"], None
    return tone(p["tag"], face), None


def build():
    m = Model("taotiemon")
    top = m.bone("taotiemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 3.6, 2.8, 10.0, 20.0, fabric(P, "suit", "suit_dark"), cut=1)
    m.round_box(bd, 0, 0, 6.0, 4.4, 19.0, 24.0, fur(P, "white", "white_dark"), cut=2)       # fur collar
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 19.0, 0))
        rod(m, ab, (sx * 4.0, 19.0, 0), (sx * 8.0, 13.0, -2.0), 2, fabric(P, "suit", "suit_dark"), extend=0.4)
        ball(m, ab, (sx * 8.4, 12.4, -2.4), 2.0, fur(P, "white", "white_dark"), layers=2)
        for j in range(3):
            spike(m, ab, (sx * 8.4 + (j - 1) * 1.0, 11.0, -4.0), (0, -0.4, -1), 0.8, 2.4, solid(P, "pink"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 10.0, 0))
        rod(m, lg, (sx * 2.0, 10.0, 0), (sx * 3.0, 4.0, 0), 2, fabric(P, "suit", "suit_dark"), extend=0.4)
        ball(m, lg, (sx * 3.2, 2.6, -1.0), 2.6, fur(P, "white", "white_dark"), layers=2)
        for j in range(3):
            spike(m, lg, (sx * 3.2 + (j - 1) * 1.0, 1.0, -3.4), (0, -0.2, -1), 0.8, 2.0, solid(P, "pink"), tip=0.8)
    hd = m.bone("head", bd, (0, 24, 0))
    ball(m, hd, (0, 26.0, -2.6), 2.8, fur(P, "white", "white_dark"), layers=3)              # little face under it
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 26.4, -5.5, max(sx * 0.6, sx * 1.8), 27.2, -5.2, solid(P, "eye", glow=True))
    m.round_box(hd, 0, 0, 11.0, 7.0, 28.0, 46.0, maskf, cut=3)                             # the bronze vessel
    m.round_box(hd, 0, 0, 12.0, 8.0, 46.0, 48.0, BRONZE, cut=3)
    for sx in (-1, 1):                                                                 # curled handles
        for j in range(4):
            ang = j * math.pi / 3
            m.round_box(hd, sx * (13.0 + 2.4 * math.sin(ang)), 0, 1.6, 2.4,
                        36.0 + 6.0 * math.cos(ang) - 1.4, 36.0 + 6.0 * math.cos(ang) + 1.4, BRONZE, cut=0)
    for i, (x, y) in enumerate(((-9.0, 30.0), (9.0, 32.0), (-4.0, 40.0), (5.0, 44.0), (-11.0, 42.0), (11.0, 40.0))):
        m.box(hd, x - 0.9, y - 5.0, -7.4, x + 0.9, y, -7.1, tagf)
    cl = m.bone("cloud", bd, (0, 30, 10))                                               # lavender cloud
    for i, (x, y, z, r) in enumerate(((0, 30, 12, 9), (10, 34, 14, 8), (-10, 32, 13, 8), (16, 26, 16, 7),
                                      (-15, 25, 15, 6), (6, 40, 15, 7), (-6, 42, 14, 6), (20, 36, 18, 6))):
        ball(m, cl, (x, y, z), r, solid(P, "cloud"), layers=3)
    return m
