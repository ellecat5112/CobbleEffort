"""Styracomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the armoured horned dragon-man: a hulking warrior in crimson plate cut with blue streaks, a
styracosaur helm crowned with long black horns and a glowing pink chest core, huge shoulder pods with drill tips, a
green scaled tail and green clawed feet, and steel-pointed fists. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking crimson-armoured dragon-man with a styracosaur helm of long black horns, a pink chest core, drill shoulder pods and a green tail"
BASE = {"red": (200, 40, 60), "red_dark": (110, 14, 26), "blue": (60, 90, 200), "black": (30, 28, 32),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 130), "green": (70, 150, 70), "green_dark": (24, 80, 24),
        "pink": (250, 100, 220), "claw": (246, 246, 240)}
SHINY = {"red": (60, 60, 70), "red_dark": (24, 24, 30), "pink": (90, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(math.sin(x * 0.8 + y * 0.7)) > 0.95:
        return tone(p["blue"], face), None
    return armour(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("styracomon")
    mats = {"skin": platef, "shin": scales(P, "green", "green_dark"), "foot": scales(P, "green", "green_dark"),
            "talon": solid(P, "claw"), "hand": platef, "finger": STEEL}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.4, leg_bulk=1.3, talons=True, digitigrade=True, name="styracomon")
    bd = a["body"]
    ball(m, bd, (0, 46.0, -6.0), 1.8, solid(P, "pink", glow=True), layers=2)
    for sx in (-1, 1):                                                                   # drill shoulder pods
        m.round_box(bd, sx * 11.0, 2.0, 4.6, 6.0, 44.0, 54.0, platef, cut=2)
        spike(m, bd, (sx * 11.0, 49.0, -4.0), (0, 0, -1), 3.0, 8.0, STEEL, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.0, 3.6, 54.0, 60.0, platef, cut=1)
    for j in range(5):                                                                   # long black horns
        ang = math.radians(-60 + j * 30)
        spike(m, hd, (2.6 * math.sin(ang), 60.0, 1.0), (math.sin(ang) * 0.6, 1, 0.4), 1.4, 12.0, solid(P, "black"),
              tip=0.8)
    spike(m, hd, (0, 57.0, -4.6), (0, 0.4, -1), 1.4, 5.0, solid(P, "black"), tip=0.8)
    for side in ("arm_left", "arm_right"):                                               # steel-pointed fists
        h = a[side]["hand"]
        spike(m, a[side]["bone"], (h[0], h[1], h[2] - 1.0), (0, -0.2, -1), 1.6, 5.0, STEEL, tip=0.8)
    tl = m.bone("tail", bd, (0, 32, 4))
    pts = [(0, 32.0, 4.0), (0, 22.0, 12.0), (2.0, 12.0, 20.0), (2.0, 6.0, 28.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 5 - i, scales(P, "green", "green_dark"), extend=0.6)
    return m
