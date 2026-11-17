"""Beowolfmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the beast warrior of light. Silver-and-lilac plate armour with gold trim, a wolf-crest helm with
a visor and a short blond fringe, a cannon housing on its left forearm, a great double-ended gold blade (the Licht
Sieger) held in its right hand, and armoured boots with gold talons. 25 blocks tall.

Front is -z, y is up. 70 units tall; Perfect stage (a Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("the beast warrior of light: silver-and-lilac plate armour with gold trim, a wolf-crest helm, a forearm cannon "
        "and a great double-ended gold blade")
BASE = {"silver": (200, 206, 220), "silver_dark": (100, 106, 124), "silver_light": (246, 248, 255),
        "lilac": (150, 140, 200), "lilac_dark": (80, 70, 130), "gold": (236, 196, 60), "gold_dark": (160, 120, 30),
        "gold_light": (255, 240, 170), "hair": (240, 220, 120), "hair_dark": (190, 160, 60), "eye": (60, 200, 255),
        "black": (30, 30, 36), "green": (150, 200, 150)}
SHINY = {"silver": (60, 60, 74), "silver_dark": (24, 24, 30), "silver_light": (130, 130, 150), "lilac": (190, 60, 80),
         "lilac_dark": (110, 20, 40)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.4)
SILVER_PLAIN = armour(P, "silver", "silver_dark", light="silver_light", seams=(3.0,))
LILAC = armour(P, "lilac", "lilac_dark")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def blade(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    return abs(u / max(W, 1e-6) - 0.5) < 0.5 * min(1.0, min(t, 1 - t) * 6)


def build():
    m = Model("beowolfmon")
    mats = {"skin": LILAC, "chest": SILVER, "abs": LILAC, "pelvis": SILVER, "neck": LILAC, "deltoid": SILVER,
            "upper_arm": LILAC, "forearm": SILVER, "hand": SILVER_PLAIN, "finger": SILVER_PLAIN, "thigh": SILVER,
            "knee": GOLD, "shin": SILVER, "calf": SILVER_PLAIN, "foot": SILVER, "talon": GOLD}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.2, talons=True, name="beowolfmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.6, 60.6, SILVER, cut=1)
    m.box(hd, -2.0, 57.2, -3.4, 2.0, 58.2, -3.0, solid(P, "eye", glow=True))
    m.box(hd, -2.0, 60.4, -4.4, 2.0, 63.0, 2.0, SILVER_PLAIN)                         # wolf crest
    m.box(hd, -1.4, 60.6, -7.0, 1.4, 62.4, -4.4, SILVER_PLAIN)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 63.0, 0.0), (sx * 0.3, 1, 0.4), 1.4, 3.0, SILVER_PLAIN)
    for i in range(5):
        rod(m, hd, (-1.6 + i * 0.8, 58.6, -3.0), (-1.8 + i * 0.9, 56.6, -3.3), 1, strands(P, "hair", "hair_dark"),
            extend=0.2)
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, SILVER)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.6, 50.0, 0.3), 4.6, 4.2, SILVER, layers=4)
    al = a["arm_left"]                                           # forearm cannon housing
    el, wr = al["elbow"], al["wrist"]
    mid = tuple((e + w) / 2 for e, w in zip(el, wr))
    m.round_box(al["bone"], mid[0] + 1.0, mid[2], 3.2, 3.2, mid[1] - 5.0, mid[1] + 4.0, SILVER, cut=1)
    for j in range(3):
        m.box(al["bone"], mid[0] + 3.6, mid[1] - 4.0 + j * 2.6, mid[2] - 2.0, mid[0] + 4.4, mid[1] - 2.8 + j * 2.6,
              mid[2] + 2.0, solid(P, "green"))
    ar = a["arm_right"]                                          # the great double-ended blade
    h = ar["hand"]
    sb = m.bone("sword", ar["bone"], h)
    m.box(sb, h[0] - 0.8, h[1] - 1.6, h[2] - 0.8, h[0] + 0.8, h[1] + 1.6, h[2] + 0.8, solid(P, "black"))
    m.box(sb, h[0] - 2.6, h[1] + 1.6, h[2], h[0] + 2.6, h[1] + 30.0, h[2], cutout(blade, GOLD))
    m.box(sb, h[0] - 2.6, h[1] - 26.0, h[2], h[0] + 2.6, h[1] - 1.6, h[2], cutout(blade, GOLD))
    return m
