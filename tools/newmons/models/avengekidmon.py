"""Avenge Kidmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a vengeful dragon-man gunslinger. Lean black-and-silver armour traced with crimson
lines, a narrow dragon helm, a long crimson sash trailing behind, huge black bat-wings, a long gun-blade in one hand
and crackling blue orbs of energy held in both claws. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, fabric, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a vengeful dragon-man gunslinger in lean black-and-silver armour with crimson lines, a long crimson sash, huge "
        "black bat-wings, a long gun-blade and crackling blue energy orbs")
BASE = {"black": (36, 36, 44), "black_dark": (12, 12, 16), "black_light": (110, 110, 130), "silver": (200, 204, 216),
        "silver_dark": (100, 104, 116), "red": (200, 30, 40), "red_dark": (110, 10, 20), "orb": (120, 140, 255),
        "orb_light": (220, 230, 255), "membrane": (30, 30, 38, 240), "eye": (255, 60, 60)}
SHINY = {"black": (220, 220, 230), "black_dark": (150, 150, 166), "black_light": (255, 255, 255),
         "red": (240, 180, 40), "red_dark": (170, 110, 20), "membrane": (200, 200, 214, 240)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.3)
BLACK_PLAIN = armour(P, "black", "black_dark", light="black_light")
SILVER = metal(P, "silver", dark="silver_dark")


def build():
    m = Model("avengekidmon")
    mats = {"skin": BLACK_PLAIN, "chest": BLACK, "abs": BLACK, "pelvis": BLACK, "neck": BLACK_PLAIN, "deltoid": BLACK,
            "upper_arm": SILVER, "forearm": BLACK, "hand": BLACK_PLAIN, "finger": SILVER, "claw": SILVER,
            "thigh": BLACK, "knee": SILVER, "shin": BLACK, "calf": BLACK_PLAIN, "foot": BLACK, "talon": SILVER}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="avengekidmon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.2, 2.8, 54.6, 60.4, BLACK, cut=1)
    m.box(hd, -1.4, 55.0, -6.8, 1.4, 57.6, -2.8, BLACK_PLAIN)
    for sx in (-1, 1):
        m.box(hd, sx * 1.1 - 0.5, 57.6, -3.6, sx * 1.1 + 0.5, 58.2, -3.4, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 60.0, 0.6), (sx * 0.3, 0.6, 1), 1.0, 4.0, SILVER)
    shell(m, bd, (0, 0, 0.6), 5.0, 42.0, 51.0, -85, 85, 9, 1.2, BLACK)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.0, 0.3), 3.8, 3.4, BLACK, layers=3)
        spike(m, ab, (sh[0] + sx * 3.0, 52.0, 0.0), (sx * 0.6, 1, 0.3), 1.4, 4.0, SILVER)
        h = a[nm]["hand"]
        ball(m, ab, (h[0], h[1] + 4.0 if sx > 0 else h[1] - 3.0, h[2] - 3.0), 2.2, gem(P, "orb", "orb_light"),
             layers=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # huge bat wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        bat_wing(m, wb, (sx * 3.0, 49.0, 3.0), 30.0, 20.0, 4, BLACK_PLAIN,
                 cutout(lambda *q: True, lambda x, y, z, f, variant=None, box=None, **k: (P(variant)["membrane"],
                                                                                          None)), side=sx)
    sk = m.bone("skirt", bd, (0, 32, 3))                         # crimson sash trailing
    for j in range(3):
        rod(m, sk, (-2.0 + j * 2.0, 32.0, 3.0), (-8.0 + j * 3.0, 20.0, 14.0 + j * 2), 1, fabric(P, "red", "red_dark"),
            extend=0.3, t2=2)
    ar = a["arm_right"]                                          # the long gun-blade
    h = ar["hand"]
    gb = m.bone("gun", ar["bone"], h)
    m.box(gb, h[0] - 1.0, h[1] - 2.0, h[2] - 1.4, h[0] + 1.0, h[1] + 3.0, h[2] + 1.4, SILVER)
    rod(m, gb, h, (h[0] + 2.0, h[1] - 26.0, h[2] + 4.0), 2, BLACK, extend=0, t2=3)
    spike(m, gb, (h[0] + 2.0, h[1] - 26.0, h[2] + 4.0), (0.08, -1, 0.15), 2.0, 4.0, SILVER)
    return m
