"""Kiwimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
plant bird: a round brown feather-tufted body on two long grey legs with hooked pink talons, a pale skull-white head
with a long downcurved beak and a big green eye, a spiky crown of green leaves and a pair of tiny kiwi chicks
(Pickmon) flitting about it. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a round brown feather-tufted bird on long grey legs with pink talons, a pale head with a long beak and a crown of green leaves"
BASE = {"brown": (130, 90, 60), "brown_dark": (70, 44, 24), "white": (236, 236, 240), "white_dark": (170, 170, 186),
        "grey": (110, 110, 120), "grey_dark": (60, 60, 70), "pink": (220, 60, 110), "green": (90, 200, 70),
        "green_dark": (30, 120, 30), "eye": (60, 160, 90), "pupil": (20, 20, 24)}
SHINY = {"brown": (120, 140, 180), "brown_dark": (60, 70, 110), "green": (240, 140, 60), "green_dark": (170, 70, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        if math.hypot(z - (-2.0), y - 30.0) < 0.6:
            return tone(p["pupil"], face), None
        if math.hypot(z - (-2.0), y - 30.0) < 1.4:
            return tone(p["eye"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kiwimon")
    top = m.bone("kiwimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 22.0, 3.0), 8.0, feathers(P, "brown", "brown_dark", size=(1.2, 2.0)), layers=5)
    hd = m.bone("head", bd, (0, 26, -2))
    m.round_box(hd, 0, -1.0, 3.2, 3.6, 26.0, 33.0, headf, cut=1)
    pts = [(0, 28.0, -4.4), (0, 24.0, -10.0), (0, 18.0, -12.0)]                      # long downcurved beak
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 2 - j, solid(P, "white"), extend=0.3, t2=2 - j)
    for i in range(9):                                                               # leaf crown
        ang = math.radians(-80 + i * 20)
        spike(m, hd, (2.4 * math.sin(ang), 32.6, 0.4), (math.sin(ang) * 0.8, 1, 0.6), 1.4, 5.0 + (i % 2) * 1.6,
              strands(P, "green", "green_dark"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # long grey legs
        lg = m.bone(nm, top, (sx * 3.0, 16.0, 2.0))
        rod(m, lg, (sx * 3.0, 16.0, 2.0), (sx * 4.0, 8.0, -2.0), 2, skin(P, "grey", dark="grey_dark"), extend=0.4)
        rod(m, lg, (sx * 4.0, 8.0, -2.0), (sx * 4.0, 1.0, 1.0), 1, skin(P, "grey", dark="grey_dark"), extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 1.0, 0.8, 0.6), ((j - 1) * 0.4, -0.3, -1), 1.0, 3.6, solid(P, "pink"),
                  tip=0.8)
    for j, (cx, cy, cz) in enumerate(((10.0, 34.0, -4.0), (-11.0, 22.0, -6.0))):    # Pickmon chicks
        m.round_box(top, cx, cz, 1.2, 1.4, cy - 1.2, cy + 1.2, skin(P, "white", dark="white_dark"), cut=0)
        spike(m, top, (cx, cy, cz - 1.4), (0, -0.3, -1), 0.8, 1.6, solid(P, "white"), tip=0.8)
    return m
