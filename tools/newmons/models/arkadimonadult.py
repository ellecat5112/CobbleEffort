"""Arkadimon Adult (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a gaunt crouching beast-man. Peach skin stretched over lean muscle with crimson muscle
lines showing through, mint collar plates on its shoulders, a narrow face and spiky crest, very long arms with huge
hands and black nails knuckling the ground, and long clawed feet. 15 blocks tall.

Front is -z, y is up. 48 units tall (crouching); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _arkadi import MINT, P
from _digidetail import Bulge, local, plane, skin, solid, torso_bulges
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a gaunt crouching beast-man: peach skin with crimson muscle lines, mint collar plates, a narrow face with a "
        "spiky crest, very long arms with huge black-nailed hands and long clawed feet")
SKIN = skin(P, "peach", dark="peach_dark", light="peach_light", bulges=torso_bulges(0, 50.5, 4.6, abs_rows=4),
            vein_key="muscle", vein_rects=(((-14, 20, 14, 52), ("north", "east", "west"), 5),), vein_count=4,
            vein_width=0.35, var=0.03)


def build():
    m = Model("arkadimonadult")
    mats = {"skin": SKIN, "hand": SKIN, "finger": SKIN, "claw": solid(P, "nail"), "talon": solid(P, "nail")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, digitigrade=True, claws=True, talons=True,
                 name="arkadimonadult", hand_pose="open", fingers=4)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 1.8, 2.6, 54.0, 61.0, SKIN, cut=1)                         # narrow face
    m.box(hd, -0.9, 55.0, -5.0, 0.9, 58.0, -3.0, SKIN)
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.4, 58.6, -3.7, sx * 0.9 + 0.4, 59.2, -3.5, solid(P, "eye", glow=True))
    for i in range(7):                                           # spiky crest
        ang = math.radians(-60 + i * 20)
        spike(m, hd, (1.6 * math.sin(ang), 60.6, 0.0), (math.sin(ang), 1, 0.5), 1.0, 4.0 + (i % 2) * 2,
              solid(P, "crimson"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # mint collar plates, arms stretched long
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        m.box(ab, min(sh[0], sh[0] + sx * 6.0), 49.0, -3.0, max(sh[0], sh[0] + sx * 6.0), 53.0, 3.0, MINT,
              rotation=(0, 0, sx * 18), pivot=sh)
        wr = a[nm]["wrist"]
        rod(m, ab, wr, (wr[0] + sx * 1.5, 6.0, wr[2] - 4.0), 2, SKIN, extend=0.4)       # forearm extension
        h = (wr[0] + sx * 1.5, 4.0, wr[2] - 5.0)
        m.box(ab, h[0] - 2.0, 2.4, h[2] - 2.6, h[0] + 2.0, 5.4, h[2] + 1.0, SKIN)       # the huge hand
        for f in range(4):
            fx = h[0] + (f - 1.5) * 1.1
            rod(m, ab, (fx, 3.0, h[2] - 2.6), (fx, 0.6, h[2] - 6.0), 1, SKIN, extend=0.3)
            spike(m, ab, (fx, 0.6, h[2] - 6.0), (0, -0.4, -1), 0.9, 1.4, solid(P, "nail"))
    return m
