"""Gokumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the hell-prison warden: a tall cyborg in gold and gunmetal armour hung with skulls, a horned skull
helm, great golden scythe-blades curving from its forearms and shins, one arm a heavy cannon, a red sash and long
golden talons. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall cyborg in gold and gunmetal armour hung with skulls, a horned skull helm, golden scythe-blades on its "
        "arms and shins, a cannon arm and golden talons")
BASE = {"gold": (230, 190, 70), "gold_dark": (150, 110, 20), "gold_light": (255, 240, 160), "gun": (110, 114, 126),
        "gun_dark": (50, 54, 64), "bone": (240, 230, 200), "bone_dark": (170, 160, 130), "red": (200, 30, 40),
        "eye": (230, 40, 40), "black": (24, 22, 26)}
SHINY = {"gold": (200, 60, 60), "gold_dark": (120, 20, 20), "gold_light": (250, 140, 140)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.25)
GUN = riveted(P, "gun", "gun_dark")
BONE = metal(P, "bone", dark="bone_dark")


def skull(m, bone, c, s=1.0):
    m.round_box(bone, c[0], c[2], 1.4 * s, 1.0 * s, c[1] - 1.2 * s, c[1] + 1.2 * s, BONE, cut=0)
    for sx in (-1, 1):
        m.box(bone, c[0] + sx * 0.5 * s - 0.25 * s, c[1], c[2] - 1.05 * s, c[0] + sx * 0.5 * s + 0.25 * s, c[1] + 0.5 * s,
              c[2] - 0.95 * s, solid(P, "black"))


def build():
    m = Model("gokumon")
    mats = {"skin": GUN, "chest": GOLD, "deltoid": GOLD, "forearm": GOLD, "thigh": GUN, "knee": GOLD, "shin": GOLD,
            "calf": GOLD, "foot": GOLD, "talon": metal(P, "gold", dark="gold_dark"), "claw": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.05, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                 name="gokumon")
    bd = a["body"]
    m.round_box(bd, 0, -0.2, 5.2, 4.0, 33.4, 35.4, solid(P, "red"), cut=1)                  # red sash
    skull(m, bd, (0, 46.0, -4.4), 1.6)
    for sx in (-1, 1):
        m.round_box(bd, sx * 8.4, 0.4, 3.6, 4.2, 46.0, 53.0, GOLD, cut=1)
        spike(m, bd, (sx * 9.6, 52.6, 0), (sx * 0.3, 1, 0), 1.8, 7.0, GOLD, tip=0.9)       # shoulder horns
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 53.6, 60.0, BONE, cut=1)                              # skull helm
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.0, -3.5, max(sx * 0.6, sx * 1.8), 58.0, -3.3, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 59.6, 0), (sx * 0.4, 1, 0.2), 1.4, 7.0, GOLD, tip=0.9)
    for nm in ("arm_left", "leg_left", "leg_right"):                                          # golden scythe-blades
        jt = a[nm].get("elbow") or a[nm].get("knee")
        sx = 1 if jt[0] > 0 else -1
        pts = [(jt[0] + sx * 1.0, jt[1], jt[2] + 1.0), (jt[0] + sx * 5.0, jt[1] - 6.0, jt[2] + 4.0),
               (jt[0] + sx * 6.0, jt[1] - 14.0, jt[2] + 2.0), (jt[0] + sx * 4.0, jt[1] - 19.0, jt[2] - 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, a[nm]["bone"], p0, p1, 1, metal(P, "gold", dark="gold_dark"), extend=0.3, t2=3)
        skull(m, a[nm]["bone"], (jt[0], jt[1] - 4.0, jt[2] - 2.6), 1.0)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["wrist"]                                   # cannon arm
    rod(m, ar, (h[0], h[1] + 4.0, h[2]), (h[0] - 2.0, h[1] + 4.0, h[2] - 12.0), 6, GUN, extend=0)
    m.round_box(ar, h[0] - 2.0, h[2] - 12.4, 2.0, 0.6, h[1] + 2.0, h[1] + 6.0, solid(P, "black"), cut=0)
    return m
