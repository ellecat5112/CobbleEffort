"""Rasielmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Ophan of knowledge: a slender angel in white-and-gold ceremonial armour with a long white
coat lined pink, a huge white fur collar about a pale masked face with golden ram-curl horns, golden clawed gauntlets
each holding a glowing golden rune circle, a golden plated chest like a book's spine, and pink-tipped talons. 35 blocks.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a slender angel in white-and-gold armour with a huge white fur collar, golden ram-curl horns and glowing golden rune circles"
BASE = {"white": (246, 244, 236), "white_dark": (190, 186, 176), "gold": (240, 200, 70), "gold_dark": (160, 110, 20),
        "pink": (240, 120, 170), "pink_dark": (170, 60, 110), "face": (250, 236, 230), "eye": (220, 60, 120),
        "rune": (255, 230, 120, 190)}
SHINY = {"white": (60, 56, 80), "white_dark": (24, 22, 36), "gold": (200, 204, 216), "gold_dark": (110, 114, 130)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "white", "white_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark")
FUR = fur(P, "white", "white_dark", length=1.6)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["pink"] if face == "north" else p["white"], face), None


def build():
    m = Model("rasielmon")
    mats = {"skin": ARM, "chest": GOLD, "hand": GOLD, "finger": GOLD, "claw": GOLD, "talon": solid(P, "pink"),
            "neck": FUR}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.8, claws=True, talons=True, digitigrade=True,
                 name="rasielmon")
    bd = a["body"]
    cape(m, bd, 52.0, 18.0, 40.0, coatf, z=4.0, flare=2.0, panels=7, seed=6)                 # long coat
    for sx in (-1, 1):
        m.box(bd, min(sx * 4.0, sx * 9.0), 14.0, -3.0, max(sx * 4.0, sx * 9.0), 40.0, -2.6, coatf,
              rotation=(0, sx * 20, sx * 8), pivot=(sx * 4.0, 40.0, -2.8))
    m.round_box(bd, 0, 0.6, 8.0, 6.0, 48.0, 56.0, FUR, cut=3)                              # huge fur collar
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 2.6, 54.0, 60.0, solid(P, "face"), cut=1)
    m.box(hd, -1.6, 57.0, -3.3, -0.6, 57.8, -3.1, solid(P, "eye"))
    m.box(hd, 0.6, 57.0, -3.3, 1.6, 57.8, -3.1, solid(P, "eye"))
    for sx in (-1, 1):                                                                   # ram-curl horns
        pts = [(sx * 2.4, 59.0, 0), (sx * 5.0, 62.0, 1.0), (sx * 7.0, 59.0, 1.6), (sx * 5.6, 56.0, 0.6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, GOLD, extend=0.3)
    for side in ("arm_left", "arm_right"):                                               # glowing rune circles
        h = a[side]["hand"]
        sx = 1 if side == "arm_left" else -1
        for i in range(12):
            ang = 2 * math.pi * i / 12
            m.box(a[side]["bone"], h[0] + sx * 3.0 - 0.4, h[1] + 5.0 * math.sin(ang) - 0.8, h[2] + 5.0 * math.cos(ang) - 0.8,
                  h[0] + sx * 3.0 + 0.4, h[1] + 5.0 * math.sin(ang) + 0.8, h[2] + 5.0 * math.cos(ang) + 0.8,
                  solid(P, "rune", glow=True))
    return m
