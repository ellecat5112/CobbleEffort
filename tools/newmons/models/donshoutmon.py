"""Don Shoutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the drum-beat hero. A round red drum-bodied little dragon with a big drumhead crown ringed in silver studs, a jagged
red V crest, one confident eye, a yellow lightning mark on its cheek, white gloves and claws, a yellow flag-ribbon
streaming from the crown, and a steel drumstick-mace with a spiked yellow tip in each hand. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a round red drum-bodied dragon with a studded drumhead crown, a jagged V crest, one confident eye, white gloves "
        "and two spiked steel drumstick-maces")
BASE = {"red": (220, 40, 40), "red_dark": (130, 14, 18), "red_light": (255, 140, 130), "head": (240, 232, 214),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "yellow": (250, 220, 40), "white": (250, 250, 250),
        "white_dark": (200, 200, 210), "black": (30, 26, 26), "gold": (240, 200, 60)}
SHINY = {"red": (40, 140, 200), "red_dark": (10, 70, 130), "red_light": (140, 210, 250)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark", light="red_light", var=0.03)
STEEL = metal(P, "steel", dark="steel_dark")
WHITE = skin(P, "white", dark="white_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up":
        return tone(p["head"], face), None
    if face == "north":
        if math.hypot(x + 2.0, y - 22.0) < 1.6:
            return tone(p["black"] if math.hypot(x + 2.0, y - 22.0) < 0.7 else p["white"], face), None
        if abs(x - 3.0) < 1.2 and abs(y - 21.0 + (x - 3.0) * 0.8) < 0.4:
            return tone(p["yellow"], face), None                     # lightning cheek mark
        if 15.0 < y < 18.0 and abs(x) < 4.0:
            return tone(p["black"] if abs(y - 16.5) < 0.6 else p["white"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def mace(m, bone, a, b):
    rod(m, bone, a, b, 1, STEEL, extend=0, t2=2)
    m.round_box(bone, b[0], b[2], 3.0, 3.0, b[1] - 2.6, b[1] + 2.6, STEEL, cut=1)
    d = tuple(bb - aa for aa, bb in zip(a, b))
    n = math.sqrt(sum(v * v for v in d))
    spike(m, bone, b, tuple(v / n for v in d), 2.0, 5.0, solid(P, "yellow"), tip=0.4)
    for ang in (0, 120, 240):
        r = math.radians(ang)
        spike(m, bone, (b[0] + 2.8 * math.cos(r), b[1], b[2] + 2.8 * math.sin(r)), (math.cos(r), 0, math.sin(r)), 1.4,
              2.6, solid(P, "yellow"), tip=0.3)


def build():
    m = Model("donshoutmon")
    top = m.bone("donshoutmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    for i, (r, y0) in enumerate(((6.0, 8.0), (7.4, 11.0), (8.0, 14.0), (8.0, 17.0), (8.0, 20.0), (8.4, 23.0))):
        m.round_box(bd, 0, 0, r, r, y0, y0 + 3.2, bodyf, cut=max(1, round(r * 0.35)))
    hd = m.bone("head", bd, (0, 26, 0))
    m.round_box(hd, 0, 0, 8.6, 8.6, 25.6, 27.0, armour(P, "steel", "steel_dark"), cut=3)   # studded rim
    for sx in (-1, 1):                                                                   # jagged V crest
        pts = [(0, 27.0, -7.0), (sx * 4.0, 31.0, -7.6), (sx * 7.0, 36.0, -7.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.4, t2=3)
    rp = [(6.0, 27.0, 4.0), (10.0, 33.0, 6.0), (16.0, 34.0, 8.0)]                       # yellow flag-ribbon
    for p0, p1 in zip(rp, rp[1:]):
        rod(m, hd, p0, p1, 1, fabric(P, "yellow", "gold"), extend=0.3, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 18.0, 0))
        rod(m, ab, (sx * 8.0, 18.0, 0), (sx * 12.0, 15.0, -3.0), 2, RED, extend=0.4)
        m.round_box(ab, sx * 12.6, -3.0, 2.4, 2.4, 13.0, 17.0, WHITE, cut=1)
        mace(m, ab, (sx * 12.6, 15.0, -3.0), (sx * 22.0, 8.0 if sx < 0 else 28.0, -6.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 8.0, 0))
        rod(m, lg, (sx * 3.6, 9.0, 0), (sx * 4.6, 2.0, -1.0), 3, RED, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 4.6 + (j - 1) * 1.2, 0.8, -1.6), ((j - 1) * 0.3, -0.1, -1), 1.0, 3.0, WHITE, tip=0.25)
    return m
