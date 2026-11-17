"""Belial Vamdemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the final form of Vamdemon's ambition, a hulking pale demon beast. A grey-white armoured
body on clawed legs, two snarling heads (a red-crested face on its shoulders and a second face in its chest), huge
dark blue wings lined in crimson membrane, red claws and a long segmented tail. 35 blocks tall.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import armour, cutout, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hulking pale demon beast: grey-white armour, two snarling heads (one on its shoulders, one in its chest), "
        "huge dark blue wings lined in crimson, red claws and a long segmented tail")
BASE = {"pale": (220, 220, 230), "pale_dark": (140, 140, 156), "pale_light": (250, 250, 255), "blue": (40, 50, 120),
        "blue_dark": (16, 20, 60), "crimson": (170, 20, 40, 235), "red": (200, 30, 40), "red_dark": (110, 10, 20),
        "mouth": (90, 10, 20), "tooth": (250, 248, 240), "tongue": (200, 60, 80), "eye": (255, 220, 60)}
SHINY = {"pale": (60, 56, 70), "pale_dark": (24, 22, 30), "pale_light": (130, 126, 150), "blue": (120, 30, 40),
         "blue_dark": (60, 10, 16), "crimson": (40, 120, 200, 235)}


def P(v):
    return pal(BASE, SHINY, v)


PALE = armour(P, "pale", "pale_dark", light="pale_light", seams=(3.0,))
RED = metal(P, "red", dark="red_dark", streak=2.0)


def build():
    m = Model("belialvamdemon")
    mats = {"skin": PALE, "belly": PALE, "neck": PALE, "head": PALE, "snout": PALE, "jaw": PALE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "tongue": solid(P, "tongue"), "arm": PALE,
            "hand": PALE, "claw": RED, "thigh": PALE, "shin": PALE, "foot": PALE, "talon": RED, "tail": PALE,
            "tail_tip": PALE}
    a = theropod(m, mats, "belialvamdemon", hip_y=18.0, hip_z=4.0, chest=(0, 30.0, -4.0), body_r=8.0, chest_r=8.6,
                 neck_top=(0, 38.0, -8.0), head_len=10.0, head_w=4.4, head_h=4.6, mouth_open=22, teeth=5,
                 arm_len=16.0, arm_bulk=1.9, leg_bulk=1.7, stance=6.4,
                 tail=((0, 16, 14), (3, 12, 22), (7, 8, 29), (10, 6, 35), (12, 6, 40)), tail_r=(4, 3.2, 2.4, 1.6, 1))
    hd = a["head"]
    for j in range(4):                                           # red crest
        spike(m, hd, (0, a["skull_top"], a["skull_z"][0] + j * 1.6), (0, 1, 0.6), 1.4, 3.4 - j * 0.4,
              solid(P, "red"))
    for sx in (-1, 1):
        m.box(hd, sx * 2.4 - 0.6, 40.4, -12.4, sx * 2.4 + 0.6, 41.2, -12.2, solid(P, "eye", glow=True))
    bd = a["body"]
    m.box(bd, -4.0, 22.0, -14.0, 4.0, 28.0, -11.6, solid(P, "mouth"))                  # the face in its chest
    for i in range(5):
        spike(m, bd, (-3.2 + i * 1.6, 28.0, -13.6), (0, -1, -0.2), 1.0, 2.0, solid(P, "tooth"))
        spike(m, bd, (-2.4 + i * 1.2, 22.0, -13.6), (0, 1, -0.2), 0.9, 1.6, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(bd, sx * 3.0 - 0.8, 29.0, -13.0, sx * 3.0 + 0.8, 30.0, -12.6, solid(P, "eye", glow=True))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # huge dark blue wings
        wb = m.bone(nm, bd, (sx * 6.0, 34.0, 2.0))
        bat_wing(m, wb, (sx * 6.0, 34.0, 2.0), 40.0, 22.0, 5, armour(P, "blue", "blue_dark"),
                 cutout(lambda *q: True, lambda x, y, z, f, variant=None, box=None, **k: (P(variant)["crimson"],
                                                                                          None)), side=sx)
    return m
