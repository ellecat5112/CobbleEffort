"""Gusokumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured isopod: a huge segmented blue crustacean shell banded with red-and-white plates and
stencilled marks, a grey armoured head with a hooked face and a water-jet cannon, a fringe of golden spines, a
spread tail fan, and long scythe-like black claws and legs reaching down beneath it. 25 blocks tall.

Front is -z, y is up. 44 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = ("a huge segmented blue isopod shell banded red and white, an armoured grey head with a water-jet cannon, golden "
        "spines and long scythe-like black claws")
BASE = {"blue": (50, 100, 190), "blue_dark": (20, 50, 120), "blue_light": (120, 170, 240), "red": (200, 40, 40),
        "white": (240, 240, 246), "grey": (160, 164, 176), "grey_dark": (80, 84, 96), "black": (34, 32, 38),
        "black_dark": (12, 12, 16), "gold": (240, 200, 70), "eye": (250, 220, 60)}
SHINY = {"blue": (200, 90, 50), "blue_dark": (130, 40, 20), "blue_light": (250, 160, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL0 = armour(P, "blue", "blue_dark", light="blue_light", trim="red", trim_w=0.35)
CLAW = metal(P, "black", dark="black_dark")


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "up" and abs((z * 0.6) % 4.0 - 2.0) < 0.2:
        return tone(p["white"], face), None
    return SHELL0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gusokumon")
    top = m.bone("gusokumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    for j in range(7):                                                                   # segmented shell
        r = 9.0 - abs(j - 3) * 1.0
        m.round_box(bd, 0, -10.0 + j * 4.0, r, 2.4, 24.0, 24.0 + r * 0.9, shellf, cut=2)
    for j in range(8):                                                                   # golden spines
        spike(m, bd, (0, 32.0, -8.0 + j * 3.0), (0.3 * (j % 2 - 0.5), 1, 0.4), 1.0, 3.0, solid(P, "gold"), tip=0.8)
    for j in range(5):                                                                   # tail fan
        ang = math.radians(-50 + j * 25)
        spike(m, bd, (0, 27.0, 18.0), (math.sin(ang), 0.2, math.cos(ang)), 2.4, 7.0, shellf, tip=0.9)
    hd = m.bone("head", bd, (0, 26, -14))
    m.round_box(hd, 0, -14.0, 4.6, 3.0, 22.0, 30.0, armour(P, "grey", "grey_dark"), cut=1)
    spike(m, hd, (0, 24.0, -17.0), (0, -0.6, -1), 2.4, 4.0, metal(P, "grey", dark="grey_dark"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.0, sx * 3.6), 27.0, -17.1, max(sx * 2.0, sx * 3.6), 28.0, -16.9, solid(P, "eye", glow=True))
    rod(m, hd, (4.0, 28.0, -14.0), (6.0, 30.0, -24.0), 2, metal(P, "grey", dark="grey_dark"), extend=0)   # water cannon
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                     # scythe claws
        ab = m.bone(nm, bd, (sx * 6.0, 24.0, -10.0))
        pts = [(sx * 6.0, 24.0, -10.0), (sx * 12.0, 18.0, -16.0), (sx * 10.0, 8.0, -20.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, CLAW, extend=0.4)
        spike(m, ab, pts[-1], (-sx * 0.3, -0.4, 1), 1.6, 7.0, CLAW, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                      # long legs beneath
        lg = m.bone(nm, bd, (sx * 5.0, 24.0, 0))
        for j, z in enumerate((-4.0, 2.0, 8.0)):
            knee = (sx * 11.0, 18.0, z)
            rod(m, lg, (sx * 5.0, 24.0, z), knee, 1, CLAW, extend=0.3, t2=2)
            rod(m, lg, knee, (sx * 9.0, 2.0, z - 2.0), 1, CLAW, extend=0.3, t2=2)
            spike(m, lg, (sx * 9.0, 2.0, z - 2.0), (0, -1, -0.4), 1.0, 2.6, CLAW, tip=0.8)
    return m
