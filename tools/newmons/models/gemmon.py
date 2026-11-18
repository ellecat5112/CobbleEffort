"""Gemmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
little white winged creature with a big diamond set in its brow, violet eyes with red cheek marks, a collar of
crystal fringe, tiny clawed paws and great curled wings, riding on a billowing lavender cloud studded with crystal
shards. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, gem, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "floater"
K = 4
LOOK = ("a little white winged creature with a big diamond in its brow and violet eyes, riding a billowing lavender "
        "cloud studded with crystal shards")
BASE = {"white": (248, 246, 250), "white_dark": (200, 196, 214), "cloud": (200, 196, 230), "cloud_dark": (150, 140, 190),
        "gem": (200, 220, 255), "gem_light": (255, 255, 255), "eye": (110, 80, 170), "cheek": (230, 80, 90),
        "crystal": (180, 240, 230), "crystal_light": (240, 255, 250), "wing": (240, 236, 250),
        "wing_dark": (190, 180, 220)}
SHINY = {"cloud": (250, 210, 160), "cloud_dark": (210, 160, 100), "gem": (255, 200, 120)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = skin(P, "white", dark="white_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.0, y - 16.6) < 0.8:
                return tone(p["eye"], face), None
            if abs(x - sx * 3.0) < 0.3 and 15.0 < y < 16.4:
                return tone(p["cheek"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gemmon")
    top = m.bone("gemmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for c, r in (((0, 5.0, 3.0), 5.0), ((5.0, 7.0, 5.0), 4.4), ((-4.0, 4.0, 5.0), 4.0), ((2.0, 9.0, 9.0), 4.6),
                 ((-3.0, 8.0, 8.0), 3.6)):
        ball(m, bd, c, r, fur(P, "cloud", "cloud_dark", length=0.6, density=2.0), layers=4)
    for j, (at, d) in enumerate((((5.0, 11.0, 6.0), (0.6, 1, 0.4)), ((-6.0, 6.0, 6.0), (-1, 0.6, 0.2)),
                                  ((8.0, 4.0, 3.0), (1, 0.2, -0.2)), ((1.0, 13.0, 10.0), (0, 1, 0.6)))):
        spike(m, bd, at, d, 1.6, 3.6, gem(P, "crystal", "crystal_light", glow=False), tip=0.9)     # crystal shards
    hd = m.bone("head", bd, (0, 14, -2))
    m.round_box(bd, 0, -2.0, 2.6, 2.2, 9.0, 14.0, WHITE, cut=1)
    m.round_box(hd, 0, -2.0, 3.6, 3.2, 13.6, 20.6, headf, cut=2)
    m.round_box(hd, 0, -5.4, 1.4, 0.4, 17.4, 20.2, gem(P, "gem", "gem_light"), cut=0)         # brow diamond
    for j in range(8):                                                                          # crystal fringe collar
        ang = math.radians(-160 + j * 45)
        spike(m, hd, (3.0 * math.cos(ang), 13.8, -2.0 + 2.4 * math.sin(ang)), (0, -1, 0), 1.0, 1.6,
              gem(P, "crystal", "crystal_light", glow=False))
    for sx in (-1, 1):                                                                          # great curled wings
        for j in range(3):
            spike(m, hd, (sx * 2.6, 19.6, -1.0 + j * 0.6), (sx * 0.6, 1, 0.3 + j * 0.15), 2.4 - j * 0.4,
                  9.0 - j * 1.6, skin(P, "wing", dark="wing_dark"), tip=1.0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 2.6, 12.0, -2.0))
        rod(m, ab, (sx * 2.6, 12.0, -2.0), (sx * 4.6, 10.0, -4.0), 1, WHITE, extend=0.3, t2=1)
    return m
