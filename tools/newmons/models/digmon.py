"""Digmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the armoured drill beetle. A stocky yellow armoured insect painted with purple swirls, a drill for a
nose, a drill on each forearm and drills on its knees, small dark clawed hands, a crest of spiky yellow horns and two
little clear wings on its back. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a stocky yellow armoured beetle painted with purple swirls, with a drill nose, drills on its forearms and knees, "
        "spiky yellow horns and little clear wings")
BASE = {"yellow": (250, 200, 40), "yellow_dark": (180, 120, 10), "yellow_light": (255, 240, 150), "purple": (90, 50, 150),
        "steel": (210, 214, 226), "steel_dark": (100, 104, 116), "black": (40, 40, 46), "eye": (40, 180, 60),
        "wing": (220, 240, 255, 140)}
SHINY = {"yellow": (240, 120, 60), "yellow_dark": (160, 50, 10), "yellow_light": (255, 200, 150), "purple": (40, 120, 70)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "yellow", "yellow_dark", light="yellow_light")
DARK = metal(P, "black", dark="black")


def swirlf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = (x, y) if face in ("north", "south") else (z, y)
    r = math.hypot(a % 8.0 - 4.0, b % 8.0 - 4.0)
    if abs(r - 2.2) < 0.4 and (a % 8.0 - 4.0) > -1.0:
        return tone(p["purple"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def drill(m, bone, base, d, length, r0):
    """A conical drill with spiral grooves (shrinking steel boxes along d)."""
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    steps = 4
    for j in range(steps):
        t0, t1 = j / steps, (j + 1) / steps
        p0 = tuple(b + u_ * length * t0 for b, u_ in zip(base, u))
        p1 = tuple(b + u_ * length * t1 for b, u_ in zip(base, u))
        rod(m, bone, p0, p1, max(1, round(r0 * 2 * (1 - t0))), metal(P, "steel", dark="steel_dark", streak=1.2),
            extend=0.2)


def build():
    m = Model("digmon")
    top = m.bone("digmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 22.0, 1.0), 8.0, swirlf, layers=7, squash=1.0)                     # armoured body
    hd = m.bone("head", bd, (0, 30, -4))
    m.round_box(hd, 0, -4.0, 3.6, 3.6, 27.0, 33.0, swirlf, cut=1)
    drill(m, hd, (0, 29.0, -7.6), (0, -0.2, -1), 8.0, 1.8)                             # drill nose
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.6, sx * 3.0), 31.0, -7.7, max(sx * 1.6, sx * 3.0), 31.8, -7.5, solid(P, "eye", glow=True))
    for i in range(4):                                                                 # spiky horn crest
        spike(m, hd, ((i - 1.5) * 1.2, 33.0, -2.0 + i), ((i - 1.5) * 0.3, 1, 0.5), 1.2, 7.0 - abs(i - 1.5), ARM,
              tip=0.3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 26.0, -2.0))
        rod(m, ab, (sx * 7.0, 26.0, -2.0), (sx * 11.0, 20.0, -5.0), 3, ARM, extend=0.5)
        m.round_box(ab, sx * 11.0, -5.0, 2.6, 2.6, 17.0, 22.0, swirlf, cut=1)
        drill(m, ab, (sx * 11.0, 18.0, -7.0), (sx * 0.2, -0.6, -1), 9.0, 1.8)          # forearm drill
        for j in range(3):
            spike(m, ab, (sx * 12.6, 17.0, -4.0 + j), (sx, -0.6, 0), 0.8, 2.4, DARK, tip=0.25)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 14.0, 1.0))
        rod(m, lg, (sx * 4.0, 15.0, 1.0), (sx * 5.0, 8.0, -1.0), 4, ARM, extend=0.6)
        rod(m, lg, (sx * 5.0, 8.0, -1.0), (sx * 5.0, 1.0, 0.0), 3, ARM, extend=0.6)
        drill(m, lg, (sx * 5.0, 8.0, -3.0), (0, 0.3, -1), 5.0, 1.4)                    # knee drill
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 1.4, 0.8, -1.4), ((j - 1) * 0.3, -0.1, -1), 1.2, 3.4, ARM, tip=0.3)
    for sx in (-1, 1):                                                                 # little clear wings
        x0, x1 = sorted((sx * 1.0, sx * 9.0))
        m.box(bd, x0, 24.0, 8.4, x1, 34.0, 8.4, solid(P, "wing"), rotation=(20, sx * 20, sx * 20),
              pivot=(sx * 1.0, 26.0, 8.4))
    return m
