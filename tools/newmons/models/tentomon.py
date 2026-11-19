"""Tentomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little ladybird-beetle Digimon: a big domed red shell with black spots, huge glossy green compound
eyes over a grey jaw, two curling orange antennae, an olive-brown underside, and six red legs with grey hooked claws,
the front pair big and clawed. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import gem, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "floater"
K = 4
LOOK = "a little ladybird beetle with a red black-spotted shell, huge green eyes, curling orange antennae and red clawed legs"
BASE = {"red": (220, 50, 50), "red_dark": (140, 20, 24), "black": (30, 30, 34), "green": (60, 190, 70),
        "green_light": (190, 250, 170), "grey": (130, 130, 140), "grey_dark": (60, 60, 70), "olive": (120, 110, 50),
        "olive_dark": (70, 64, 24), "orange": (250, 160, 40)}
SHINY = {"red": (90, 140, 230), "red_dark": (40, 70, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    for cx, cy, cz in ((-4.0, 15.0, 2.0), (4.0, 15.0, 2.0), (-5.6, 11.0, 0.0), (5.6, 11.0, 0.0), (0, 17.6, 3.0),
                       (-3.0, 12.0, 5.6), (3.0, 12.0, 5.6)):
        if math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) < 1.8:
            return tone(p["black"], face), None
    return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tentomon")
    top = m.bone("tentomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 8.0, 0.6), 5.4, skin(P, "olive", dark="olive_dark"), layers=4)          # underside
    ball(m, bd, (0, 12.0, 1.0), 6.6, shellf, layers=6, squash=0.9)                          # domed shell
    hd = m.bone("head", bd, (0, 12, -4))
    m.round_box(hd, 0, -5.4, 3.6, 2.2, 8.0, 11.0, metal(P, "grey", dark="grey_dark"), cut=1)  # jaw
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.4, 12.6, -5.0), 2.6, gem(P, "green", "green_light"), layers=3)    # compound eyes
        pts = [(sx * 2.0, 17.0, -4.0), (sx * 2.6, 20.0, -3.0), (sx * 4.0, 21.6, -1.0), (sx * 3.4, 22.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "orange"), extend=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                 # big clawed front legs
        ab = m.bone(nm, bd, (sx * 4.0, 8.0, -3.0))
        rod(m, ab, (sx * 4.0, 8.0, -3.0), (sx * 7.0, 5.0, -6.0), 2, skin(P, "red", dark="red_dark"), extend=0.4)
        for j in range(2):
            spike(m, ab, (sx * 7.0, 5.0, -6.0), (sx * 0.3, -0.5 + j * 0.8, -1), 1.0, 3.0, metal(P, "grey"), tip=0.8)
    for i, z in enumerate((0.0, 3.0)):
        for sx in (-1, 1):
            nm = "leg_%s_%d" % ("left" if sx > 0 else "right", i)
            lg = m.bone(nm, bd, (sx * 3.6, 5.0, z))
            rod(m, lg, (sx * 3.6, 5.0, z), (sx * 6.0, 1.6, z - 1.0), 2, skin(P, "red", dark="red_dark"), extend=0.4)
            spike(m, lg, (sx * 6.0, 1.6, z - 1.0), (sx * 0.2, -1, -0.4), 1.0, 1.6, metal(P, "grey"), tip=0.8)
    return m
