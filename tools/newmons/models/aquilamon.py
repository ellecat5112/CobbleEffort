"""Aquilamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a giant crimson eagle. Red feathers with white-tipped flight feathers on its great wings, a shaggy
brown ruff, a white face with a hooked yellow beak and fierce eyes, two black ram horns curling from its head,
banded tail feathers and violet scaled legs with black talons. 15 blocks tall.

Front is -z, y is up. 40 units tall (the wings); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, feathers, fur, local, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a giant crimson eagle with white-tipped flight feathers, a shaggy brown ruff, a white face with a hooked "
        "yellow beak, two black ram horns and violet scaled legs with black talons")
BASE = {"red": (210, 40, 40), "red_dark": (130, 16, 20), "white": (250, 250, 248), "white_dark": (200, 200, 206),
        "brown": (130, 80, 40), "brown_dark": (80, 44, 20), "beak": (250, 210, 60), "beak_dark": (190, 140, 30),
        "horn": (40, 40, 48), "horn_light": (110, 110, 124), "leg": (150, 130, 200), "leg_dark": (90, 70, 140),
        "talon": (30, 30, 36), "eye": (250, 200, 40), "pupil": (20, 16, 10)}
SHINY = {"red": (60, 120, 210), "red_dark": (24, 60, 140), "brown": (230, 230, 240), "brown_dark": (170, 170, 190)}


def P(v):
    return pal(BASE, SHINY, v)


PLUME = feathers(P, "red", "red_dark", size=(1.6, 2.4), flow=(0, -1))
FLIGHT = feathers(P, "red", "red_dark", size=(1.4, 3.0), flow=(0, -1), tip="white")
RUFF = fur(P, "brown", "brown_dark", length=1.4)
HORN = metal(P, "horn", light="horn_light", streak=2.0)
LEG = scales(P, "leg", "leg_dark", size=1.0, rim_mix=0.5)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 12.6, y - 27.0, 0.9, "eye", lid="red_dark")
        if c is not None:
            return c, None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("aquilamon")
    top = m.bone("aquilamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(6):                                           # the body, leaning forward
        r = 6.0 - abs(i - 2.5) * 0.6
        m.round_box(bd, 0, -1.0 - i * 1.2, r, r * 0.9, 12.0 + i * 2.4, 14.8 + i * 2.4, PLUME, cut=2)
    hd = m.bone("head", bd, (0, 25, -9))
    ball(m, hd, (0, 27.0, -10.0), 3.6, facef, layers=4)
    m.box(hd, -1.4, 25.0, -16.0, 1.4, 27.6, -12.0, metal(P, "beak", dark="beak_dark"))   # hooked beak
    spike(m, hd, (0, 26.0, -16.0), (0, -1, -0.3), 2.0, 2.0, metal(P, "beak", dark="beak_dark"))
    for sx in (-1, 1):                                           # ram horns curling
        pts = [(sx * 2.4, 29.0, -9.0), (sx * 4.6, 31.0, -7.0), (sx * 6.0, 29.0, -5.0), (sx * 5.6, 26.0, -6.0),
               (sx * 4.4, 25.0, -8.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j // 3, HORN, extend=0.3)
    for i in range(12):                                          # the shaggy ruff
        ang = math.radians(i * 30)
        spike(m, bd, (3.6 * math.sin(ang), 24.0, -8.0 + 3.6 * math.cos(ang)),
              (math.sin(ang), -0.3, math.cos(ang)), 2.0, 3.0, RUFF, tip=1.0)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # great wings raised
        wb = m.bone(nm, bd, (sx * 5.0, 22.0, -2.0))
        rod(m, wb, (sx * 5.0, 22.0, -2.0), (sx * 14.0, 32.0, 0.0), 3, PLUME, extend=0.4)
        rod(m, wb, (sx * 14.0, 32.0, 0.0), (sx * 26.0, 36.0, 2.0), 2, PLUME, extend=0.4)
        for i in range(12):
            t = i / 11
            base = (sx * (5.0 + 21.0 * t), 22.0 + 14.0 * t, -2.0 + 4.0 * t)
            ln = 7.0 + 9.0 * t
            m.box(wb, base[0] - 1.3, base[1] - ln, base[2], base[0] + 1.3, base[1], base[2], FLIGHT,
                  rotation=(-10, 0, -sx * (30 - 20 * t)), pivot=base)
    tl = m.bone("tail", bd, (0, 14, 4))
    for j in range(5):                                           # banded tail feathers
        ang = math.radians(-30 + j * 15)
        rod(m, tl, (0, 14.0, 4.0), (8.0 * math.sin(ang), 10.0, 4.0 + 10.0 * math.cos(ang)), 2, FLIGHT, extend=0.2,
            t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 12.0, 0))
        m.round_box(lg, sx * 2.6, 0, 2.2, 2.4, 8.0, 13.0, PLUME, cut=1)
        rod(m, lg, (sx * 2.6, 9.0, 0.0), (sx * 3.0, 2.0, -1.0), 2, LEG, extend=0.4)
        for d in ((sx * 0.3, -0.4, -1), (0, -0.4, -1), (-sx * 0.3, -0.4, -1), (0, -0.4, 1)):
            spike(m, lg, (sx * 3.0, 1.6, -1.0), d, 1.0, 3.0, solid(P, "talon"))
    return m
