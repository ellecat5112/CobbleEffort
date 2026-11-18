"""Gogmamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ore golem: a hunched giant of brown-gold boulders with great clusters of pale crystal growing from
its shoulders and back, a small fierce face under a flaming orange-and-red crest, one arm ending in a huge crystal
club-fist strapped and chained, and stubby rock legs. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, gem, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hunched giant of brown-gold boulders with great pale crystal clusters, a flaming crest and a huge strapped "
        "crystal club-fist")
BASE = {"rock": (160, 130, 80), "rock_dark": (90, 70, 40), "rock_light": (210, 190, 140), "crystal": (220, 230, 240),
        "crystal_light": (255, 255, 255), "flame": (250, 140, 40), "flame_dark": (200, 40, 30), "strap": (110, 70, 40),
        "strap_dark": (60, 36, 16), "steel": (180, 184, 196), "steel_dark": (90, 94, 106), "eye": (240, 220, 60)}
SHINY = {"rock": (110, 110, 130), "rock_dark": (60, 60, 76), "crystal": (240, 170, 220)}


def P(v):
    return pal(BASE, SHINY, v)


ROCK0 = skin(P, "rock", dark="rock_dark", light="rock_light")
CRYS = gem(P, "crystal", "crystal_light", glow=False)


def rockf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if fbm(x * 0.4, y * 0.4, z * 0.4, seed=11) > 0.66:
        return tone(p["rock_dark"], face), None
    return ROCK0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gogmamon")
    top = m.bone("gogmamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    for c, r in (((0, 22.0, 0), 9.0), ((-4.0, 30.0, 2.0), 7.0), ((5.0, 30.0, 2.0), 7.0), ((0, 16.0, -2.0), 6.0)):
        ball(m, bd, c, r, rockf, layers=5)
    for j, (at, d) in enumerate((((-8.0, 34.0, 2.0), (-0.6, 1, 0.2)), ((8.0, 34.0, 2.0), (0.6, 1, 0.2)),
                                  ((-4.0, 36.0, 6.0), (-0.2, 1, 0.6)), ((4.0, 36.0, 6.0), (0.3, 1, 0.6)),
                                  ((0.0, 32.0, 8.0), (0, 0.6, 1)), ((-10.0, 30.0, 0.0), (-1, 0.6, 0)),
                                  ((10.0, 30.0, 0.0), (1, 0.6, 0)))):
        spike(m, bd, at, d, 3.0, 10.0 - (j % 3) * 1.6, CRYS, tip=1.4)                  # crystal clusters
    hd = m.bone("head", bd, (0, 30, -7))
    m.round_box(hd, 0, -8.0, 3.0, 2.0, 25.0, 30.0, rockf, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.0), 27.6, -10.1, max(sx * 0.6, sx * 2.0), 28.4, -9.9, solid(P, "eye", glow=True))
    for j in range(5):                                                                  # flaming crest
        spike(m, hd, ((j - 2) * 1.0, 30.0, -8.0 + j * 0.4), ((j - 2) * 0.2, 1, 0.3), 1.4, 6.0 - abs(j - 2),
              strands(P, "flame", "flame_dark"), tip=0.8)
    ab = m.bone("arm_right", bd, (-9.0, 26.0, -2.0))                                     # crystal club-fist
    rod(m, ab, (-9.0, 26.0, -2.0), (-16.0, 18.0, -8.0), 4, rockf, extend=0.6)
    m.round_box(ab, -18.0, -14.0, 4.6, 6.0, 12.0, 22.0, CRYS, cut=2)
    m.round_box(ab, -18.0, -9.0, 5.0, 1.0, 13.0, 21.0, leather(P, "strap", "strap_dark", stitch="steel"), cut=0)
    for j in range(4):
        m.round_box(ab, -13.0, -9.0 + j * 0.0, 0.8, 0.8, 8.0 - j * 1.6, 9.4 - j * 1.6, metal(P, "steel", dark="steel_dark"),
                    cut=0)
    al = m.bone("arm_left", bd, (9.0, 26.0, -2.0))
    rod(m, al, (9.0, 26.0, -2.0), (14.0, 14.0, -6.0), 4, rockf, extend=0.6)
    m.round_box(al, 14.0, -6.0, 3.0, 3.0, 8.0, 14.0, rockf, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 14.0, 0))
        rod(m, lg, (sx * 5.0, 15.0, 0), (sx * 6.0, 3.0, -1.0), 5, rockf, extend=0.6)
        m.round_box(lg, sx * 6.0, -2.0, 3.6, 4.4, 0.0, 4.0, rockf, cut=1)
    return m
