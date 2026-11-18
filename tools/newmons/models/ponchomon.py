"""Ponchomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a cactus spirit in a fringed orange poncho: a ribbed green cactus head with black eyes, a wide
grin and a long lolling red tongue, a huge red-and-yellow zigzag sombrero topped by blue maracas, red-gloved fists,
and a ragged skirt of green fronds where its legs would be. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, fabric, leather, local, noise2, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = "a ribbed green cactus spirit in a fringed orange poncho and a red-and-yellow zigzag sombrero, a lolling red tongue and red fists"
BASE = {"green": (90, 170, 70), "green_dark": (30, 100, 30), "orange": (240, 140, 40), "orange_dark": (180, 80, 20),
        "red": (210, 40, 40), "red_dark": (120, 14, 14), "yellow": (250, 210, 60), "blue": (40, 80, 200),
        "black": (20, 20, 24), "white": (250, 250, 250), "tongue": (230, 70, 80), "glove": (190, 50, 40),
        "glove_dark": (80, 20, 16), "frond": (110, 140, 40)}
SHINY = {"green": (80, 150, 200), "green_dark": (30, 80, 140), "orange": (150, 90, 200), "orange_dark": (90, 40, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def cactusf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.8, (y - 21.6) * 0.6) < 0.8:
                return tone(p["black"], face), None
        if 17.6 < y < 19.6 and abs(x) < 3.0 - (19.6 - y) * 0.8:
            return tone(p["black"] if y < 18.4 else p["white"], face), None
    if face in ("north", "south", "east", "west") and abs(math.sin(math.atan2(z, x) * 5)) > 0.92:
        return tone(p["green_dark"], face), None
    return skin(P, "green", dark="green_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def hatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    r = math.hypot(x, z)
    if face in ("up", "down") and r > 6.0:
        a = math.atan2(z, x) * 8
        tooth = (a / math.pi) % 2.0
        return tone(p["red"] if (r - 6.0) / 6.0 < abs(tooth - 1.0) else p["yellow"], face), None
    if face not in ("up", "down"):
        return tone(p["red"] if (y % 2.0) < 1.0 else p["yellow"], face), None
    return tone(p["yellow"], face), None


def frondf_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    f = (box.lo[0] + box.lo[2] + u) * 1.4
    return v / max(H, 1e-6) > 0.15 + 0.35 * abs(math.sin(f)) * noise2(f, 3)


FROND = cutout(frondf_in, solid(P, "frond"))
PONCHO = fabric(P, "orange", "orange_dark", axis="x", period=2.6)


def build():
    m = Model("ponchomon")
    top = m.bone("ponchomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for i in range(8):                                                                   # frond skirt
        ang = 2 * math.pi * i / 8
        cx, cz = 4.6 * math.cos(ang), 4.6 * math.sin(ang)
        m.box(bd, cx - 2.6, 0.0, cz, cx + 2.6, 11.0, cz, FROND,
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=(cx, 6.0, cz))
    m.round_box(bd, 0, 0, 8.0, 7.0, 10.0, 16.0, PONCHO, cut=2)                            # poncho
    m.round_box(bd, 0, 0, 6.4, 5.6, 15.6, 18.0, PONCHO, cut=2)
    for i in range(12):
        ang = 2 * math.pi * i / 12
        spike(m, bd, (8.0 * math.cos(ang), 10.4, 7.0 * math.sin(ang)), (math.cos(ang) * 0.3, -1, math.sin(ang) * 0.3),
              0.8, 2.0, solid(P, "white"), tip=0.8)
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, -0.4, 4.4, 3.8, 15.0, 25.0, cactusf, cut=1)                         # cactus head
    for j in range(6):
        ang = 2 * math.pi * j / 6
        spike(m, hd, (4.2 * math.cos(ang), 20.0 + (j % 2) * 2.0, -0.4 + 3.6 * math.sin(ang)),
              (math.cos(ang), 0.1, math.sin(ang)), 0.8, 1.6, solid(P, "white"), tip=0.8)
    rod(m, hd, (0, 17.8, -4.0), (0.6, 12.0, -6.0), 2, solid(P, "tongue"), extend=0.2, t2=1)  # lolling tongue
    rod(m, hd, (0.6, 12.0, -6.0), (1.6, 9.0, -5.0), 2, solid(P, "tongue"), extend=0.2, t2=1)
    m.round_box(hd, 0, 0, 12.0, 12.0, 25.0, 26.0, hatf, cut=4)                             # sombrero brim
    m.round_box(hd, 0, 0, 4.4, 4.4, 26.0, 31.0, hatf, cut=1)
    m.round_box(hd, 0, 0, 3.6, 3.6, 31.0, 33.0, hatf, cut=1)
    for sx in (-1, 1):                                                                   # blue maracas
        rod(m, hd, (sx * 2.0, 30.0, 0), (sx * 5.0, 33.0, 0), 1, solid(P, "yellow"), extend=0.2)
        ball(m, hd, (sx * 6.0, 34.0, 0), 1.6, solid(P, "blue"), layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 14.0, 0))
        ball(m, ab, (sx * 11.0, 12.0, -2.0), 3.0, leather(P, "glove", "glove_dark"), layers=3)
        m.round_box(ab, sx * 8.6, -1.0, 1.6, 2.0, 11.0, 15.0, solid(P, "black"), cut=0)
    return m
