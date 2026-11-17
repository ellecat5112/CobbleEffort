"""Dracumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little vampire. A big round black teardrop head with a huge toothy white grin and a red and a green emblem for eyes,
a tiny body in a black bat-collared cape with blue lining and a gold clasp, pale blue hands with long red nails and
an eye set in each palm, black legs, and enormous red-spiked black shoes. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a big round black teardrop head with a huge toothy grin and red and green emblem eyes, a bat-collared cape, pale "
        "blue hands with eyes in the palms and enormous red-spiked shoes")
BASE = {"black": (34, 32, 40), "black_dark": (10, 10, 14), "black_light": (100, 100, 120), "white": (250, 250, 250),
        "red": (220, 40, 50), "green": (60, 180, 80), "blue": (40, 60, 160), "blue_dark": (14, 20, 80),
        "hand": (170, 200, 240), "hand_dark": (100, 130, 180), "gold": (240, 200, 60), "eye": (240, 240, 240),
        "pupil": (180, 30, 30)}
SHINY = {"black": (240, 240, 246), "black_dark": (170, 170, 180), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


HEAD = skin(P, "black", dark="black_dark", light="black_light", var=0.02)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 15.0 < y < 18.4 and abs(x) < 5.0 - (16.7 - y) ** 2 * 0.3:            # huge toothy grin
            return tone(p["black"] if abs(y - 16.7) < 0.2 or (x * 1.2) % 1.6 < 0.15 else p["white"], face), None
        for sx, key in ((-1, "red"), (1, "green")):                               # emblem eyes
            if math.hypot(x - sx * 2.6, y - 20.6) < 1.5:
                return tone(p[key] if math.hypot(x - sx * 2.6, y - 20.6) > 0.7 else p["white"], face), None
    return HEAD(x, y, z, face, variant, box=box, **k)


def handf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        d = math.hypot(x - cx, y - cy)
        if d < 1.2:
            return tone(p["pupil"] if d < 0.5 else p["eye"], face), None
    return skin(P, "hand", dark="hand_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dracumon")
    top = m.bone("dracumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.4, 2.6, 2.0, 6.0, 12.0, solid(P, "black"), cut=1)          # tiny body
    for sx in (-1, 1):                                                              # bat-collared cape
        x0, x1 = sorted((sx * 0.6, sx * 5.0))
        m.box(bd, x0, 6.0, 1.6, x1, 13.0, 2.4, fabric(P, "blue", "blue_dark"), rotation=(15, 0, sx * 10),
              pivot=(sx * 0.6, 13.0, 2.0))
        spike(m, bd, (sx * 2.6, 12.6, 0.6), (sx, 0.8, 0), 1.6, 3.0, solid(P, "black"), tip=0.6)
    m.round_box(bd, 0, -2.4, 0.8, 0.4, 11.6, 12.6, solid(P, "gold"), cut=0)
    hd = m.bone("head", bd, (0, 13, 0))
    ball(m, hd, (0, 18.6, 0), 6.0, headf, layers=6, squash=0.9, ry=6.0)
    spike(m, hd, (0, 23.6, 0), (0, 1, 0.3), 3.0, 5.0, HEAD, tip=1.0)                 # teardrop point
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # pale hands, eyes in palms
        ab = m.bone(nm, bd, (sx * 2.6, 11.0, 0))
        rod(m, ab, (sx * 2.6, 11.0, 0), (sx * 7.0, 12.0, -1.0), 1, solid(P, "black"), extend=0.4)
        m.box(ab, sx * 9.0 - 2.4, 10.0, -2.4, sx * 9.0 + 2.4, 14.4, -0.4, handf)
        for j in range(4):
            spike(m, ab, (sx * 9.0 + (j - 1.5) * 1.1, 14.4, -1.4), ((j - 1.5) * 0.2, 1, -0.3), 0.7, 2.6,
                  solid(P, "red"), tip=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                             # enormous spiked shoes
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.0, 0), (sx * 2.4, 3.0, 0), 1, solid(P, "black"), extend=0.4)
        m.round_box(lg, sx * 2.6, -1.0, 2.6, 4.0, 0.0, 3.6, HEAD, cut=1)
        for j in range(2):
            spike(m, lg, (sx * 2.6, 3.4, 0.6 + j * 1.6), (sx * 0.2, 1, 0.5), 1.0, 3.0, solid(P, "red"), tip=0.3)
    return m
