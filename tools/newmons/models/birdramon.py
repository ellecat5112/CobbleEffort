"""Birdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a giant bird of fire. A body of orange-gold feathers that burn into flame at every edge, two great
wings of living fire raised high, a fierce eagle head with a hooked beak and a mane of flame, and big taloned feet
with pale scaly toes. 15 blocks tall.

Front is -z, y is up. 44 units tall (the wings); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, feathers, flame_inside, local, metal, scales, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a giant bird of fire: orange-gold feathers burning into flame, two great wings of living fire, a fierce eagle "
        "head with a mane of flame and big taloned feet")
BASE = {"orange": (250, 150, 40), "orange_dark": (200, 70, 20), "gold": (250, 210, 80), "flame": (255, 120, 30, 220),
        "flame_core": (255, 230, 120, 235), "beak": (250, 220, 170), "beak_dark": (180, 140, 100), "toe": (240, 210, 190),
        "toe_dark": (180, 140, 120), "claw": (240, 240, 236), "eye": (40, 90, 200)}
SHINY = {"orange": (80, 160, 250), "orange_dark": (30, 80, 200), "gold": (190, 230, 255), "flame": (60, 140, 255, 220),
         "flame_core": (200, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


PLUME = feathers(P, "orange", "orange_dark", size=(1.6, 2.6), flow=(0, -1), tip="gold")


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def build():
    m = Model("birdramon")
    top = m.bone("birdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i in range(5):
        r = 5.6 - abs(i - 2) * 0.7
        m.round_box(bd, 0, 1.0 - i * 1.6, r, r * 0.9, 12.0 + i * 2.6, 14.8 + i * 2.6, PLUME, cut=1)
    hd = m.bone("head", bd, (0, 26, -8))
    ball(m, hd, (0, 27.0, -9.0), 3.4, PLUME, layers=4)
    m.box(hd, -1.4, 25.0, -16.0, 1.4, 27.8, -11.4, metal(P, "beak", dark="beak_dark"))
    spike(m, hd, (0, 26.0, -16.0), (0, -1, -0.3), 2.0, 2.4, metal(P, "beak", dark="beak_dark"))
    for sx in (-1, 1):
        m.box(hd, sx * 2.6 - 0.4, 28.0, -11.4, sx * 2.6 + 0.4, 28.8, -11.0, solid(P, "eye"))
    fl = m.bone("mane", hd, (0, 30, -6))
    for ang in (0, 60, 120):                                     # mane of flame
        m.box(fl, -4.0, 28.0, -6.0, 4.0, 38.0, -6.0, cutout(flame_inside(4, 0.2, 2), flamef), rotation=(20, ang, 0),
              pivot=(0, 29.0, -6.0))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # wings of living fire
        wb = m.bone(nm, bd, (sx * 4.0, 22.0, 0))
        for j, (ang, dz) in enumerate(((60, 0.0), (40, 1.5), (80, 3.0))):
            x0, x1 = sorted((sx * 3.0, sx * 24.0))
            m.box(wb, x0, 14.0, dz, x1, 32.0, dz, cutout(flame_inside(5, sx * 0.2, j + 3), flamef),
                  rotation=(0, 0, sx * (ang - 30)), pivot=(sx * 4.0, 22.0, dz))
    tl = m.bone("tail", bd, (0, 14, 6))
    for ang in (-20, 0, 20):
        m.box(tl, -2.0, 4.0, 8.0, 2.0, 14.0, 8.0, cutout(flame_inside(3, 0.0, 6), flamef), rotation=(40, ang, 0),
              pivot=(0, 14.0, 6.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 13.0, 0))
        rod(m, lg, (sx * 2.6, 13.0, 0), (sx * 3.0, 4.0, -1.0), 2, scales(P, "toe", "toe_dark", size=0.8), extend=0.3)
        for d in ((0.4, -0.5, -1), (0, -0.5, -1), (-0.4, -0.5, -1), (0, -0.3, 1)):
            rod(m, lg, (sx * 3.0, 4.0, -1.0), (sx * 3.0 + d[0] * 2.4, 2.0, -1.0 + d[2] * 3.0), 1,
                scales(P, "toe", "toe_dark", size=0.8), extend=0.2)
            spike(m, lg, (sx * 3.0 + d[0] * 2.4, 2.0, -1.0 + d[2] * 3.0), (d[0], -1, d[2]), 0.8, 1.8, solid(P, "claw"))
    return m
