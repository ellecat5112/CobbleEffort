"""Bulkmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the dragon-man bruiser. A hunched, heavily muscled lime-green dragon-man with neon green lightning
markings, a crest of jagged yellow and green spines down its head and back, a fanged black-armoured snout, a giant
black-and-yellow boxing glove on its right arm, a black wrist guard and long white claws, and thick legs ending in
taloned feet. 15 blocks tall.

Front is -z, y is up. 56 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import Bulge, armour, leather, skin, solid, torso_bulges
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hunched muscular lime-green dragon-man with neon lightning markings, a crest of jagged spines, a fanged "
        "black-armoured snout, a giant black-and-yellow boxing glove and long white claws")
BASE = {"lime": (190, 230, 40), "lime_dark": (110, 150, 10), "lime_light": (240, 255, 150), "neon": (60, 230, 80),
        "black": (30, 30, 36), "black_light": (90, 90, 104), "yellow": (240, 230, 50), "yellow_dark": (180, 160, 10),
        "claw": (240, 240, 244), "eye": (250, 60, 40), "mouth": (110, 20, 30), "tooth": (250, 250, 246),
        "vein": (150, 200, 30)}
SHINY = {"lime": (240, 140, 40), "lime_dark": (170, 80, 10), "lime_light": (255, 210, 140), "neon": (240, 60, 200),
         "yellow": (120, 220, 255), "yellow_dark": (40, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


CHEST = skin(P, "lime", dark="lime_dark", light="lime_light", bulges=torso_bulges(0, 51.0, 6.2, abs_rows=4),
             vein_key="vein", vein_rects=(((-6, 36, 6, 51), ("north",), 3),), var=0.03)
ARM = skin(P, "lime", dark="lime_dark", light="lime_light", var=0.03,
           bulges=[Bulge("north", sx * 9.6, 42.0, 2.0, 3.8, light=0.35, shadow=0.45) for sx in (-1, 1)])
GLOVE = leather(P, "black", "black_light", stitch="yellow")


def bolted(sh):
    """Neon green lightning markings zigzagging across the hide."""
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        zz = 1.4 * abs(((y * 0.35) % 2) - 1)
        if abs(x - 2.0 - zz * 2.0) < 0.35 or abs(z - 1.0 + zz * 2.0) < 0.3 and face in ("east", "west"):
            return p["neon"], p["neon"]
        return sh(x, y, z, face, variant, box=box, **k)
    return s


def build():
    m = Model("bulkmon")
    mats = {"skin": bolted(ARM), "chest": bolted(CHEST), "abs": bolted(CHEST), "hand": ARM, "finger": ARM,
            "claw": solid(P, "claw"), "foot": ARM, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.4, arm_bulk=1.5, leg_bulk=1.45, digitigrade=True, claws=True, talons=True,
                 name="bulkmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 52, -3))
    m.round_box(hd, 0, -3.0, 2.8, 3.0, 51.0, 57.4, ARM, cut=1)                          # head sunk forward
    m.box(hd, -2.2, 50.6, -9.4, 2.2, 54.0, -5.0, armour(P, "black", "black_light"))      # armoured snout
    m.box(hd, -1.8, 49.6, -8.8, 1.8, 50.6, -5.4, solid(P, "mouth"))
    for i in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.4, 50.8, -8.6 + i * 0.9), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.5, 55.0, -6.1, sx * 1.4 + 0.5, 55.6, -5.9, solid(P, "eye", glow=True))
    for i in range(12):                                                                # crest of jagged spines
        y = 57.0 - i * 2.0
        z = -2.0 + i * 1.0
        for sx in (-1, 0, 1):
            spike(m, bd if i > 2 else hd, (sx * 2.2, y, z + 2.4), (sx * 0.6, 0.8, 0.8), 2.0, 5.0 - abs(sx) * 1.6,
                  solid(P, "yellow" if (i + sx) % 2 else "neon"), tip=0.5)
    ar = a["arm_right"]                                                                # the giant boxing glove
    h = ar["hand"]
    m.round_box(ar["bone"], h[0] - 1.0, h[2] - 2.0, 6.0, 6.4, h[1] - 8.0, h[1] + 4.0, GLOVE, cut=2)
    m.box(ar["bone"], h[0] - 7.0, h[1] - 2.0, h[2] - 8.6, h[0] + 5.0, h[1] + 1.0, h[2] - 8.2, solid(P, "yellow"))
    m.round_box(ar["bone"], h[0], h[2], 3.6, 3.6, h[1] + 4.0, h[1] + 7.0, solid(P, "yellow"), cut=1)
    al = a["arm_left"]
    w = al["wrist"]
    rod(m, al["bone"], w, (w[0], w[1] + 4.0, w[2] + 0.4), 5, GLOVE, extend=0)          # wrist guard
    return m
