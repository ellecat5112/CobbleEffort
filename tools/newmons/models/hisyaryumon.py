"""Hisyaryumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the flying-car dragon: an eastern dragon coiled upright, its red scaled body banded with silver chain-scales on its
belly, a black-and-gold horned head with a golden mane, clutching a red orb and a green orb, little clawed limbs and a
long tail ending in a tuft. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import gem, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "floater"
K = 3
LOOK = ("an eastern dragon coiled upright with a red scaled body, silver belly scales, a black-and-gold horned head, a "
        "golden mane and red and green orbs in its claws")
BASE = {"red": (190, 40, 40), "red_dark": (110, 14, 18), "silver": (210, 214, 224), "silver_dark": (110, 114, 126),
        "black": (34, 32, 38), "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "orb_r": (230, 80, 40),
        "orb_g": (60, 200, 90), "light": (255, 255, 230), "eye": (250, 220, 60)}
SHINY = {"red": (40, 60, 170), "red_dark": (14, 24, 100)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    if face == "north" or face == "down":
        return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)
    return scales(P, "red", "red_dark", size=1.2)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hisyaryumon")
    top = m.bone("hisyaryumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    pts = [(2.0, 2.0, 6.0), (6.0, 6.0, 2.0), (4.0, 12.0, -4.0), (-3.0, 18.0, -2.0), (-4.0, 26.0, 3.0), (2.0, 32.0, 2.0),
           (2.0, 38.0, -2.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(3, 5 - j // 2), bodyf, extend=0.6)
    h = pts[-1]
    hd = m.bone("head", bd, h)
    m.round_box(hd, h[0], h[2] - 2.0, 2.6, 4.0, h[1], h[1] + 4.0, metal(P, "black", dark="black"), cut=1)
    m.round_box(hd, h[0], h[2] - 6.0, 1.6, 1.8, h[1], h[1] + 2.4, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, h[0] + min(sx * 2.6, sx * 2.8), h[1] + 2.4, h[2] - 4.0, h[0] + max(sx * 2.6, sx * 2.8), h[1] + 3.2,
              h[2] - 3.0, solid(P, "eye", glow=True))
        pts2 = [(h[0] + sx * 1.6, h[1] + 4.0, h[2] - 1.0), (h[0] + sx * 3.0, h[1] + 9.0, h[2] + 1.0)]
        rod(m, hd, pts2[0], pts2[1], 1, metal(P, "gold", dark="gold_dark"), extend=0.3, t2=2)
    for j in range(6):
        spike(m, hd, (h[0], h[1] + 3.0, h[2] + j * 0.8), (0.3 * (j % 2 - 0.5), 0.3, 1), 1.2, 5.0,
              strands(P, "gold", "gold_dark"), tip=0.8)
    for sx, nm, orb in ((1, "arm_left", "orb_g"), (-1, "arm_right", "orb_r")):                # clawed limbs + orbs
        ab = m.bone(nm, bd, (sx * 3.0, 26.0, -2.0))
        rod(m, ab, (sx * 3.0, 26.0, -2.0), (sx * 7.0, 24.0, -6.0), 1, bodyf, extend=0.3, t2=2)
        m.round_box(ab, sx * 8.0, -7.0, 2.0, 2.0, 22.0, 26.0, gem(P, orb, "light"), cut=1)
    tb = m.bone("tail", bd, (2, 2, 6))
    rod(m, tb, (2.0, 2.0, 6.0), (-6.0, 1.0, 12.0), 2, bodyf, extend=0.4)
    for j in range(3):
        spike(m, tb, (-6.0, 1.0, 12.0), (-1, 0.2 * (j - 1), 0.4), 1.0, 3.0, strands(P, "gold", "gold_dark"), tip=0.8)
    return m
