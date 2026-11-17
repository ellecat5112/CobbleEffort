"""Bancho Lilimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the delinquent boss fairy, in her official outfit: a long crimson coat lined in black over a
white top and black trousers with straps, a black-and-red domino mask, black hair, fingerless gloves, pink arm wraps,
four petal-wings of violet and green behind her and a thorned vine whip ending in a spiked green flail-bud.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, leather, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("the delinquent boss fairy: a long crimson coat over a white top and black trousers, a black domino mask, black "
        "hair, violet-and-green petal wings and a thorned vine whip with a spiked flail-bud")
BASE = {"red": (180, 30, 40), "red_dark": (100, 10, 20), "white": (246, 246, 250), "white_dark": (190, 190, 206),
        "black": (34, 32, 40), "black_light": (90, 88, 104), "skin": (246, 222, 206), "skin_dark": (200, 160, 150),
        "pink": (240, 100, 170), "violet": (170, 90, 210, 230), "green": (90, 180, 80), "green_dark": (40, 110, 30),
        "hair": (30, 28, 34), "hair_light": (90, 86, 100), "thorn": (220, 230, 200), "eye": (240, 60, 120)}
SHINY = {"red": (40, 60, 160), "red_dark": (16, 24, 90), "violet": (90, 210, 190, 230), "pink": (90, 200, 250)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "red", "red_dark", axis="y", period=3.0)
TOP = fabric(P, "white", "white_dark", axis="x", period=2.0)
TROUSER = leather(P, "black", "black_light")
SKIN = skin(P, "skin", dark="skin_dark", var=0.02)
VINE = skin(P, "green", dark="green_dark")


def petal(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return abs(v / max(H, 1e-6) - 0.5) < 0.5 * math.sin(math.pi * t) ** 0.7


def petalf(key):
    def s(x, y, z, face, variant, box=None, **k):
        if not petal(x, y, z, face, box):
            return (0, 0, 0, 0), None
        c = P(variant)[key]
        return (c if len(c) == 4 else tuple(c) + (230,)), None
    return s


def build():
    m = Model("bancholilimon")
    mats = {"skin": SKIN, "chest": TOP, "abs": TOP, "pelvis": TROUSER, "neck": SKIN, "deltoid": COAT,
            "upper_arm": COAT, "forearm": solid(P, "pink"), "hand": solid(P, "black"), "finger": SKIN,
            "thigh": TROUSER, "knee": TROUSER, "shin": TROUSER, "calf": TROUSER, "foot": solid(P, "black"),
            "toe": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="bancholilimon", hand_pose="open",
                 chest_depth=0.9)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, SKIN, cut=1)
    m.box(hd, -2.4, 57.2, -2.7, 2.4, 58.8, -2.2, solid(P, "black"))                     # domino mask
    for sx in (-1, 1):
        m.box(hd, sx * 0.9 - 0.4, 57.6, -2.8, sx * 0.9 + 0.4, 58.2, -2.7, solid(P, "eye", glow=True))
    hr = m.bone("mane", hd, (0, 59, 1))
    for i in range(10):                                          # black hair
        ang = math.radians(-120 + i * 26)
        rod(m, hr, (2.0 * math.sin(ang), 60.0, 0.4), (3.0 * math.sin(ang), 53.0, 2.6), 2,
            strands(P, "hair", "hair", tip="hair_light"), extend=0.3)
    cb = m.bone("cap", bd, (0, 51, 3))                           # the long crimson coat
    cape(m, cb, 52.0, 16.0, 48.0, COAT, z=4.4, flare=1.0, panels=8, sweep=(0, 8))
    for sx in (-1, 1):
        m.box(bd, min(sx * 3.6, sx * 5.4), 8.0, -3.4, max(sx * 3.6, sx * 5.4), 50.0, -2.8, COAT,
              rotation=(-6, sx * 25, 0), pivot=(sx * 4.4, 50.0, -3.0))
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # petal wings
        wb = m.bone(nm, bd, (sx * 3.0, 47.0, 3.0))
        for j, ang in enumerate((30, -20)):
            x0, x1 = sorted((sx * 3.0, sx * 18.0))
            m.box(wb, x0, 42.0, 4.0 + j, x1, 52.0, 4.0 + j, petalf("violet" if j == 0 else "green"),
                  rotation=(0, 0, sx * ang), pivot=(sx * 3.0, 47.0, 4.0 + j))
    al = a["arm_left"]                                           # vine whip with a spiked flail-bud
    h = al["hand"]
    vb = m.bone("whip", al["bone"], h)
    pts = [h, (h[0] + 4.0, h[1] + 14.0, h[2] - 2.0), (h[0] + 10.0, h[1] + 22.0, h[2] - 1.0),
           (h[0] + 18.0, h[1] + 20.0, h[2]), (h[0] + 22.0, h[1] + 12.0, h[2] - 1.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, vb, p0, p1, 1, VINE, extend=0.2)
        spike(m, vb, p1, (0, 1, 0), 0.6, 1.0, solid(P, "thorn"))
    e = pts[-1]
    ball(m, vb, (e[0], e[1] - 4.0, e[2]), 3.4, VINE, layers=3)
    for j in range(8):
        ang = math.radians(j * 45)
        spike(m, vb, (e[0] + 3.0 * math.cos(ang), e[1] - 4.0 + 3.0 * math.sin(ang), e[2]),
              (math.cos(ang), math.sin(ang), 0), 0.8, 1.6, solid(P, "thorn"))
    return m
