"""Vorvomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little rock dragon: a chunky charcoal body of faceted volcanic stone with glowing orange cracks, a
big square head with yellow eyes and a jaw full of embers, red-tipped stone spikes, stubby rock wings and clawed
feet. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, plane, solid
from _route import pal, tone

HEIGHT = 21
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 12}
LOOK = "a little charcoal rock dragon with glowing orange cracks, yellow eyes, red-tipped stone spikes and stubby rock wings"
BASE = {"rock": (60, 58, 64), "rock_dark": (24, 22, 28), "ember": (255, 150, 40), "red": (230, 60, 40),
        "eye": (255, 220, 60), "black": (20, 20, 24)}
SHINY = {"rock": (150, 140, 120), "rock_dark": (90, 80, 60), "ember": (90, 200, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def rockf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 1.3 + y * 0.9) * math.cos(z * 1.1 - y * 0.5)) < 0.06:
        return p["ember"], p["ember"]
    return armour(P, "rock", "rock_dark", panel=(2.0, 2.0))(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(a - sx * 2.0) < 0.9 and abs(b - 18.6) < 0.6:
                return p["eye"], p["eye"]
        if 13.6 < b < 15.6 and abs(a) < 3.0:
            return (p["ember"], p["ember"]) if abs(b - 14.6) < 0.4 else (p["black"], None)
    return rockf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vorvomon")
    top = m.bone("vorvomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 0.6, 4.0, 4.0, 4.0, 12.0, rockf, cut=1)
    hd = m.bone("head", bd, (0, 12, -1))
    m.round_box(hd, 0, -1.6, 4.0, 3.8, 12.0, 20.6, headf, cut=1)
    for j in range(4):
        spike(m, hd, ((j - 1.5) * 1.6, 20.4, -1.0 + j * 0.4), ((j - 1.5) * 0.3, 1, 0.3), 1.2, 2.4, solid(P, "red"),
              tip=0.8)
    for sx in (-1, 1):
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.6, 11.0, 2.0))
        for j in range(3):
            spike(m, wb, (sx * 3.6, 11.0, 2.0), (sx, 0.6 - j * 0.4, 0.4), 1.6, 6.0 - j, rockf, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 5.0, 0))
        m.round_box(lg, sx * 2.4, -0.4, 1.6, 2.4, 0.0, 5.0, rockf, cut=1)
        for t in range(3):
            spike(m, lg, (sx * 2.4 + (t - 1) * 1.0, 0.8, -2.8), (0, -0.2, -1), 0.8, 1.6, solid(P, "red"), tip=0.8)
    tl = m.bone("tail", bd, (0, 6, 4))
    rod(m, tl, (0, 6.0, 4.0), (0, 4.0, 9.0), 2, rockf, extend=0.4)
    spike(m, tl, (0, 4.0, 9.0), (0, 0, 1), 1.6, 2.4, solid(P, "red"), tip=0.8)
    return m
