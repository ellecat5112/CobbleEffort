"""Shutumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hybrid of wind: a slender bird-woman in a fitted silver-grey armoured suit with lilac trim (built
covered), a sleek silver bird-helm with a long curved blade-crest, swept blue-and-gold feathered wings, golden
feathered shoulder ruffs, clawed talons, and a long hooked tail-blade. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a slender bird-woman in a silver-grey armoured suit with a sleek bird-helm, a curved blade-crest and swept blue-and-gold wings"
BASE = {"silver": (200, 204, 216), "silver_dark": (110, 114, 130), "lilac": (190, 160, 230), "blue": (110, 160, 230),
        "blue_dark": (50, 80, 160), "gold": (230, 190, 90), "gold_dark": (160, 120, 30), "visor": (240, 80, 120),
        "claw": (240, 240, 236)}
SHINY = {"silver": (80, 70, 90), "silver_dark": (30, 26, 36), "blue": (240, 150, 90), "blue_dark": (180, 80, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = armour(P, "silver", "silver_dark", trim="lilac", trim_w=0.2)


def build():
    m = Model("shutumon")
    mats = {"skin": SUIT, "talon": solid(P, "claw"), "claw": solid(P, "claw")}
    a = humanoid(m, mats, bulk=0.75, arm_bulk=0.72, leg_bulk=0.8, talons=True, claws=True, digitigrade=True,
                 name="shutumon")
    bd = a["body"]
    for sx in (-1, 1):                                                                   # feathered shoulder ruffs
        for j in range(3):
            spike(m, bd, (sx * 6.0, 51.0, -1.0 + j), (sx * 1, -0.4, 0.2), 1.4, 5.0, feathers(P, "gold", "gold_dark"),
                  tip=0.8)
        feather_wing(m, bd, (sx * 3.0, 50.0, 3.0), 26.0, 14.0, 6, feathers(P, "blue", "gold"), side=sx, sweep=30,
                     droop=-12.0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.4, 3.0, 54.0, 60.0, metal(P, "silver", dark="silver_dark"), cut=1)
    spike(m, hd, (0, 57.0, -3.8), (0, -0.3, -1), 1.4, 3.0, metal(P, "silver"), tip=0.8)
    m.box(hd, -1.6, 57.6, -3.9, 1.6, 58.4, -3.7, solid(P, "visor", glow=True))
    pts = [(0, 60.0, -1.0), (0, 66.0, 2.0), (0, 68.0, 8.0), (0, 64.0, 12.0)]                # curved blade-crest
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, metal(P, "silver"), extend=0.2, t2=2)
    tl = m.bone("tail", bd, (0, 32, 3))                                                  # hooked tail-blade
    pts = [(0, 32.0, 3.0), (2.0, 20.0, 10.0), (4.0, 10.0, 12.0), (6.0, 6.0, 8.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, metal(P, "silver", dark="silver_dark"), extend=0.2, t2=2)
    return m
