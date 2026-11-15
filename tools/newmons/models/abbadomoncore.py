"""Abbadomon Core (a Digimon of the CobbleEffort: Digital crossover, built after the official art on wikimon.net): a
tall cloaked knight of tattered navy eye-ribbons, red eyes staring from the folds, crimson armour beneath and a long
crimson blade for its right arm. 45 blocks tall.

Front is -z, y is up. 46 units tall; Ultimate stage, one step past Abbadomon.
"""
from __future__ import annotations

import math

from _boxmodel import rod, spike
from _digi import sized
from _digiwar import make_palette, warrior
from _route import tone

HEIGHT = 46
SCALE, HITBOX = sized(45, HEIGHT, 1.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a tall cloaked knight of tattered navy eye-ribbons with red eyes staring from the folds, crimson armour beneath and a long crimson blade for an arm"

BASE = {"suit": (30, 30, 44), "armour": (180, 30, 50), "armour_dark": (110, 16, 30), "skin": (20, 20, 28),
        "boot": (30, 30, 44), "eye": (255, 40, 40), "ribbon": (34, 40, 72), "ribbon_dark": (20, 24, 44),
        "blade": (210, 30, 60)}
SHINY = {"ribbon": (220, 222, 236), "ribbon_dark": (170, 174, 190), "armour": (120, 40, 180), "armour_dark": (70, 20, 110),
         "blade": (150, 60, 220)}
P = make_palette(BASE, SHINY)


def ribbonf(x, y, z, face, variant, box=None, **k):
    """A tattered eye-ribbon of the cloak (a cut-out plane): ragged hem, red eyes along it."""
    p = P(variant)
    lx = x - box.lo[0]
    hem = 2.0 + 3.0 * abs(math.sin(lx * 1.1)) + 2.0 * abs(math.sin(lx * 0.37))
    if y - box.lo[1] < hem:
        return (0, 0, 0, 0), None
    if (int(lx * 0.8) + int(y * 0.25)) % 5 == 0 and (y % 4) < 0.9 and (lx % 2.5) < 0.9:
        return p["eye"], p["eye"]
    return tone(p["ribbon"] if int(lx / 1.6) % 2 else p["ribbon_dark"], face), None


def build():
    m, b, solid = warrior("abbadomoncore", P, {"suit": "suit", "armour": "armour", "armour_dark": "armour_dark",
                                               "skin": "skin", "boot": "boot"}, bulk=1.1)
    hd = b["head"]
    m.box(hd, -2.8, 33.0, -2.4, 2.8, 40.0, 3.0, solid("ribbon"))           # the hood
    cp = m.bone("cape", b["body"], (0, 33, 2))
    for i, ang in enumerate((-40, -20, 0, 20, 40)):                      # cloak panels, fanned round the back
        m.box(cp, -4.5, 2.0, 3.2, 4.5, 34.0, 3.2, ribbonf, rotation=(0, ang, 0), pivot=(0, 33, 0))
    a = b["arm_right"]
    rod(m, a, (-6.0, 19.0, -1.0), (-8.0, 2.0, -12.0), 2.0, solid("blade", glow=True), extend=0.3, t2=0.8)
    spike(m, a, (-8.0, 2.0, -12.0), (-0.1, -0.85, -0.55), 2.0, 4.0, solid("blade", glow=True), tip=0.3)
    return m
