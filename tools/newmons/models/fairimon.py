"""Fairimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Legendary Warrior of wind's human spirit. A slender fairy warrior in a pale-lilac armoured
suit with white and violet plates, a lilac visor-helm with long swept antenna-ribbons and long lavender hair, tall
lilac boots with green-and-red knee discs, white gauntlets with green rings, four translucent dragonfly wings and a
swirl of wind round her. Its official design is kept as drawn (a full armoured suit here). 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, gem, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender fairy warrior in a pale-lilac armoured suit with a visor-helm, long antenna-ribbons, lavender hair, tall "
        "boots, four translucent dragonfly wings and a swirl of wind")
BASE = {"lilac": (210, 190, 240), "lilac_dark": (130, 110, 180), "lilac_light": (245, 235, 255), "white": (246, 246, 250),
        "white_dark": (190, 190, 206), "violet": (120, 80, 170), "green": (90, 200, 110), "green_light": (200, 255, 210),
        "red": (220, 40, 40), "red_light": (255, 150, 150), "hair": (200, 180, 230), "hair_dark": (140, 110, 180),
        "skin": (246, 222, 206), "skin_dark": (200, 170, 150), "visor": (60, 50, 90), "wing": (220, 240, 255, 110),
        "vein": (170, 190, 230, 190), "wind": (220, 230, 255, 140)}
SHINY = {"lilac": (180, 230, 200), "lilac_dark": (100, 160, 120), "hair": (250, 220, 150), "hair_dark": (200, 160, 80)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = armour(P, "lilac", "lilac_dark", light="lilac_light", trim="violet", trim_w=0.3)
WHITE = armour(P, "white", "white_dark", trim="violet", trim_w=0.25)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 2.4) < 0.25 or abs(v - H / 2) < 0.2:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("fairimon")
    mats = {"skin": SUIT, "chest": WHITE, "abs": SUIT, "pelvis": WHITE, "neck": SUIT, "deltoid": WHITE,
            "upper_arm": SUIT, "forearm": WHITE, "hand": WHITE, "finger": WHITE, "thigh": SUIT, "knee": SUIT,
            "shin": SUIT, "calf": SUIT, "foot": SUIT, "toe": SUIT}
    a = humanoid(m, mats, bulk=0.78, arm_bulk=0.8, leg_bulk=0.85, name="fairimon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.2, 2.6, 54.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, 0.4, 2.6, 3.0, 57.4, 61.2, WHITE, cut=1)                         # visor-helm
    m.box(hd, -2.4, 57.4, -2.9, 2.4, 58.6, -2.5, solid(P, "visor"))
    for sx in (-1, 1):                                                                 # antenna-ribbons
        pts = [(sx * 1.6, 61.0, 0), (sx * 4.0, 66.0, 1.0), (sx * 7.0, 68.0, 3.0), (sx * 9.0, 64.0, 5.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "white"), extend=0.3, t2=2)
    for i in range(9):                                                                 # long lavender hair
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.2 * math.sin(ang), 59.0, 0.8 + math.cos(ang)), (3.4 * math.sin(ang), 46.0, 4.0), 2,
            strands(P, "hair", "hair_dark"), extend=0.3, t2=1)
    for nm in ("leg_left", "leg_right"):                                               # knee discs
        kn = a[nm]["knee"]
        m.round_box(a[nm]["bone"], kn[0], kn[2] - 1.6, 1.6, 0.6, kn[1] - 2.0, kn[1] + 1.0, gem(P, "red", "red_light"), cut=0)
    for nm in ("arm_left", "arm_right"):                                               # green rings
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 1.6, 1.6, w[1], w[1] + 1.2, gem(P, "green", "green_light"), cut=0)
    for side in (1, -1):                                                               # four dragonfly wings
        for j, (y, ang) in enumerate(((50.0, 25), (46.0, -15))):
            x0, x1 = sorted((side * 2.0, side * (20.0 - j * 4.0)))
            m.box(bd, x0, y - 2.4, 3.6 + j * 0.6, x1, y + 2.4, 3.6 + j * 0.6, wingf,
                  rotation=(0, side * 25, side * ang), pivot=(side * 2.0, y, 3.6))
    wb = m.bone("ring_wind", bd, (0, 20, 0))                                           # swirl of wind
    for i in range(14):
        a0, a1 = 2 * math.pi * i / 14, 2 * math.pi * (i + 1) / 14
        rod(m, wb, (10.0 * math.cos(a0), 10.0 + i * 0.8, 10.0 * math.sin(a0)),
            (10.0 * math.cos(a1), 10.8 + i * 0.8, 10.0 * math.sin(a1)), 1, solid(P, "wind"), extend=0.4, t2=2)
    return m
