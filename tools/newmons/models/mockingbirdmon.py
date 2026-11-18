"""Mockingbirdmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a mechanical bird of white steel: a slim armoured body ending in a long blade tail, a
narrow head with green lens eyes on a cable neck, four limbs on cables tipped with red claw pods and long green-lined
blades, and two great wings of iridescent translucent crystal feathers on steel frames. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a mechanical bird of white steel with green lens eyes, four cable limbs tipped with red claw pods and blades, a "
        "blade tail and great wings of iridescent crystal feathers")
BASE = {"white": (230, 232, 240), "white_dark": (140, 144, 160), "cable": (60, 64, 80), "red": (200, 40, 40),
        "green": (60, 200, 120), "green_light": (200, 255, 220), "pane": (220, 220, 255, 140),
        "pane_b": (255, 220, 240, 140), "pane_c": (210, 255, 240, 140)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "green": (240, 80, 120), "green_light": (255, 210, 220)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "white", "white_dark", trim="green", trim_w=0.2)
LENS = gem(P, "green", "green_light")


def panef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = (u / max(W, 1e-6) * 2 + v / max(H, 1e-6)) % 1.0
    return (p["pane"] if t < 0.33 else p["pane_b"] if t < 0.66 else p["pane_c"]), None


def limb(m, bone, root, tip, sx):
    rod(m, bone, root, tip, 1, solid(P, "cable"), extend=0.2)
    ball(m, bone, tip, 1.6, solid(P, "red"), layers=2)
    ball(m, bone, (tip[0], tip[1] + 0.6, tip[2] - 1.0), 0.8, LENS, layers=1)
    x0, x1 = sorted((tip[0], tip[0] + sx * 12.0))
    m.box(bone, x0, tip[1] - 0.6, tip[2] - 0.3, x1, tip[1] + 0.6, tip[2] + 0.3, metal(P, "white", dark="white_dark"),
          rotation=(0, 0, sx * 25), pivot=tip)


def build():
    m = Model("mockingbirdmon")
    top = m.bone("mockingbirdmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    m.round_box(bd, 0, 0, 2.6, 2.6, 26.0, 38.0, ARM, cut=1)                               # slim body
    spike(m, bd, (0, 26.0, 0), (0, -1, 0.1), 2.6, 20.0, metal(P, "white", dark="white_dark"), tip=0.8)  # blade tail
    for sx in (-1, 1):
        ball(m, bd, (sx * 3.4, 36.0, -1.0), 2.4, armour(P, "white", "white_dark"), layers=3)
        ball(m, bd, (sx * 3.4, 36.0, -3.2), 1.4, LENS, layers=2)
    hd = m.bone("head", bd, (0, 38, 0))
    pts = [(0, 38.0, 0), (1.0, 42.0, -1.0), (0, 46.0, -2.0)]
    for p0, p1 in zip(pts, pts[1:]):                                                     # cable neck
        rod(m, hd, p0, p1, 1, solid(P, "cable"), extend=0.2)
    m.round_box(hd, 0, -3.0, 1.4, 3.6, 45.6, 47.6, ARM, cut=0)
    spike(m, hd, (0, 46.6, -6.6), (0, 0, -1), 1.6, 4.0, metal(P, "white"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 1.6), 46.4, -4.0, max(sx * 1.4, sx * 1.6), 47.2, -3.0, solid(P, "green", glow=True))
        lb = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 2.6, 34.0, 0))
        limb(m, lb, (sx * 2.6, 34.0, 0), (sx * 12.0, 44.0, -3.0), sx)
        lg = m.bone("leg_left" if sx > 0 else "leg_right", bd, (sx * 2.6, 27.0, 0))
        limb(m, lg, (sx * 2.6, 27.0, 0), (sx * 12.0, 18.0, -3.0), sx)
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 2.0, 37.0, 2.0))  # crystal wings
        for j in range(6):
            ang = 30 - j * 12
            x0, x1 = sorted((sx * 2.0, sx * (24.0 - j * 1.5)))
            m.box(wb, x0, 34.0, 2.4 + j * 0.4, x1, 38.0, 2.4 + j * 0.4, panef, rotation=(0, 0, sx * ang),
                  pivot=(sx * 2.0, 37.0, 2.4 + j * 0.4))
        rod(m, wb, (sx * 2.0, 37.0, 2.0), (sx * 22.0, 47.0, 3.0), 1, metal(P, "white"), extend=0.2)
    return m
