"""Jyagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
potato beast: a squat four-legged creature whose back is a great heap of lumpy tan potato-stones, a round grey face
with a little horn, big orange eyes, rosy cheeks and a fanged grin, stumpy potato legs with grey claws and a leafy
green sprout curling from its rump. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, local, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a squat beast with a back of lumpy tan potato-stones, a round grey face with orange eyes and a fanged grin and a leafy sprout"
BASE = {"tan": (220, 190, 130), "tan_dark": (150, 120, 70), "tan_light": (246, 226, 180), "spot": (120, 90, 50),
        "grey": (130, 120, 140), "grey_dark": (70, 64, 80), "eye": (240, 140, 40), "pupil": (24, 20, 20),
        "cheek": (240, 120, 110), "tooth": (250, 250, 246), "mouth": (40, 30, 40), "leaf": (80, 150, 50),
        "leaf_dark": (30, 90, 20), "claw": (180, 180, 196)}
SHINY = {"tan": (200, 120, 160), "tan_dark": (130, 60, 100), "tan_light": (240, 190, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def potatof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if min(u, v, W - u, H - v) < 0.3:
        return tone(p["tan_dark"], face), None
    if ((u * 7.3 + v * 3.1) % 3.7) < 0.35:
        return tone(p["spot"], face), None
    return tone(p["tan_light"] if face == "up" else p["tan"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.6, y - 13.6)
            if d < 0.7:
                return tone(p["pupil"], face), None
            if d < 1.5:
                return tone(p["eye"], face), None
            if math.hypot(x - sx * 3.8, y - 11.4) < 0.8:
                return tone(p["cheek"], face), None
        if abs(y - 10.4) < 0.5 and abs(x) < 2.4:
            return tone(p["tooth"] if (x + 3.0) % 1.6 < 0.5 else p["mouth"], face), None
    return skin(P, "grey", dark="grey_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jyagamon")
    top = m.bone("jyagamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 2))
    lumps = [(0, 18, 2, 4.0), (-5, 16, 0, 3.4), (5, 16, 0, 3.4), (-3, 20, 6, 3.2), (3, 20, 6, 3.2), (0, 21, -2, 3.0),
             (-7, 12, 4, 3.0), (7, 12, 4, 3.0), (0, 16, 9, 3.6), (-5, 14, 9, 3.0), (5, 14, 9, 3.0), (0, 12, 13, 3.0),
             (-4, 22, 2, 2.4), (4, 22, 2, 2.4), (0, 24, 4, 2.0)]
    for i, (cx, cy, cz, s) in enumerate(lumps):                                   # heap of potato-stones
        m.box(bd, cx - s, cy - s * 0.8, cz - s, cx + s, cy + s * 0.8, cz + s, potatof,
              rotation=(10 * ((i % 3) - 1), 15 * ((i % 5) - 2), 8 * ((i % 4) - 1.5)), pivot=(cx, cy, cz))
    m.round_box(bd, 0, 3.0, 8.0, 9.0, 6.0, 14.0, potatof, cut=3)
    hd = m.bone("head", bd, (0, 12, -6))
    m.round_box(hd, 0, -7.0, 5.4, 3.6, 7.0, 17.0, facef, cut=2)
    spike(m, hd, (0, 16.6, -8.0), (0, 1, -0.3), 1.4, 2.6, solid(P, "grey_dark"), tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 4.6, 16.4, -6.0), (sx * 0.8, 0.6, 0), 1.6, 4.0, potatof, tip=0.8)        # potato ears
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 6.0, 6.0, sz * 6.0 + 2.0))
        m.box(lg, sx * 7.0 - 3.0, 0.0, sz * 6.0 - 1.0, sx * 7.0 + 3.0, 7.0, sz * 6.0 + 5.0, potatof)
        for j in range(2):
            spike(m, lg, (sx * 7.0 + (j - 0.5) * 2.4, 1.0, sz * 6.0 - 1.0), (0, -0.2, -1), 1.4, 2.6, solid(P, "claw"),
                  tip=0.8)
    pts = [(0, 14.0, 15.0), (0, 18.0, 19.0), (-2.0, 22.0, 20.0), (-4.0, 22.0, 17.0)]   # leafy sprout
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, solid(P, "leaf"), extend=0.3, t2=2)
    return m
