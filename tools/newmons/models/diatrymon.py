"""Diatrymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the terror bird. A big flightless bird with a lime-green body and a fiery orange chest, a huge
scaly blue-grey head with a hooked fanged beak and a spiky dark crest, steel-grey armoured scales down its neck and
legs, short orange-and-red feathered wings tipped with bone claws, a fan of red tail feathers and big taloned feet.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a big flightless terror bird with a lime body and fiery orange chest, a huge scaly blue-grey head with a hooked "
        "fanged beak, spiky crest, short red wings and big taloned feet")
BASE = {"lime": (170, 220, 60), "lime_dark": (90, 140, 20), "lime_light": (220, 250, 140), "orange": (250, 150, 40),
        "orange_dark": (200, 70, 20), "red": (210, 50, 40), "red_dark": (130, 20, 20), "scale": (100, 130, 150),
        "scale_dark": (40, 60, 80), "scale_light": (170, 200, 220), "crest": (40, 60, 70), "beak": (200, 200, 190),
        "beak_dark": (120, 120, 110), "tooth": (250, 250, 246), "mouth": (180, 40, 50), "eye": (250, 200, 40),
        "talon": (230, 226, 216)}
SHINY = {"lime": (230, 120, 170), "lime_dark": (150, 50, 100), "lime_light": (255, 200, 230), "scale": (150, 110, 90),
         "scale_dark": (80, 50, 30)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = feathers(P, "lime", "lime_dark", size=(1.2, 2.0), tip="lime_light")
CHEST = feathers(P, "orange", "orange_dark", size=(1.2, 2.0))
SCALES = scales(P, "scale", "scale_dark", size=1.2, light="scale_light", rim_mix=0.4)
WING = feathers(P, "red", "red_dark", size=(1.2, 2.6), tip="orange")


def build():
    m = Model("diatrymon")
    top = m.bone("diatrymon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 20.0, 2.0), 8.0, BODY, layers=7, squash=1.2)                        # round body
    ball(m, bd, (0, 21.0, -3.0), 6.0, CHEST, layers=6, squash=0.8)                      # orange chest
    nk = m.bone("neck", bd, (0, 26, -4))
    pts = [(0, 25.0, -4.0), (0, 30.0, -6.0), (0, 34.0, -6.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 4, SCALES, extend=0.6)
    hd = m.bone("head", nk, (0, 35, -6))
    m.round_box(hd, 0, -7.0, 3.4, 5.0, 32.0, 38.0, SCALES, cut=1)                        # huge head
    m.box(hd, -2.4, 33.6, -16.0, 2.4, 36.4, -11.0, metal(P, "beak", dark="beak_dark"))   # hooked beak
    spike(m, hd, (0, 34.6, -16.0), (0, -1, -0.4), 2.4, 3.0, metal(P, "beak", dark="beak_dark"), tip=0.6)
    m.box(hd, -2.2, 31.0, -15.0, 2.2, 33.0, -10.0, metal(P, "beak", dark="beak_dark"))   # lower jaw
    m.box(hd, -2.0, 33.0, -15.0, 2.0, 33.6, -10.0, solid(P, "mouth"))
    for j in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 33.6, -14.4 + j * 1.2), (0, -1, 0), 0.6, 1.0, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.3, sx * 3.6), 35.6, -8.0, max(sx * 3.3, sx * 3.6), 36.6, -6.8, solid(P, "eye", glow=True))
    for i in range(7):                                                                  # spiky dark crest
        spike(m, hd, (0, 37.6, -8.0 + i * 1.6), (0, 1, 0.6 + i * 0.1), 1.4, 4.0 + (i % 3) * 1.4, solid(P, "crest"),
              tip=0.3)
    for side in (1, -1):                                                                # short red wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 24.0, 0))
        feather_wing(m, wb, (side * 6.0, 24.0, 0), 10.0, 6.0, 2, WING, side=side, sweep=30, droop=4.0)
        spike(m, wb, (side * 15.0, 25.0, 2.0), (side, -0.4, -0.4), 1.0, 3.0, solid(P, "talon"), tip=0.25)
    for i in range(6):                                                                  # red tail fan
        ang = math.radians(-50 + i * 20)
        spike(m, bd, (0, 22.0, 9.0), (math.sin(ang), 0.6, 1.0), 2.0, 9.0, WING, tip=0.6)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                 # scaly legs, big talons
        lg = m.bone(nm, top, (sx * 4.0, 14.0, 1.0))
        rod(m, lg, (sx * 4.0, 16.0, 1.0), (sx * 4.6, 8.0, 3.0), 4, BODY, extend=0.6)
        rod(m, lg, (sx * 4.6, 8.0, 3.0), (sx * 4.6, 1.0, 0.0), 2, SCALES, extend=0.6)
        for j in range(3):
            spike(m, lg, (sx * 4.6 + (j - 1) * 1.6, 0.8, -0.6), ((j - 1) * 0.3, -0.1, -1), 1.2, 4.6,
                  solid(P, "talon"), tip=0.3)
        spike(m, lg, (sx * 4.6, 0.8, 1.0), (0, -0.1, 1), 1.0, 2.6, solid(P, "talon"), tip=0.3)
    return m
