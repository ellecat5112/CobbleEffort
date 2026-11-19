"""Tesla Jellymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a jellyfish girl: a big striped lilac-and-blue jelly dome hat with little cat ears worn
low over her face, a ragged pink jelly frill skirt over a dark bodysuit, dark armoured boots with pink soles, ragged
green frills at the shoulders, and long black ribbon tentacles fading to magenta, crackling with yellow sparks. 15
blocks.

Front is -z, y is up. 66 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, skin, solid
from _jellyhat import ribbon, spark
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a jellyfish girl in a striped lilac jelly dome hat with cat ears, a ragged pink frill skirt and long black ribbon tentacles crackling with sparks"
BASE = {"suit": (40, 40, 70), "suit_dark": (16, 16, 30), "pink": (240, 150, 190), "pink_dark": (190, 90, 140),
        "lilac": (210, 200, 250), "blue": (110, 140, 230), "green": (90, 140, 90), "green_dark": (40, 80, 50),
        "ribbon": (30, 28, 40), "magenta": (220, 80, 200), "spark": (255, 240, 80), "skin": (250, 220, 210),
        "skin_dark": (210, 170, 160), "sole": (230, 70, 140)}
SHINY = {"pink": (150, 230, 200), "pink_dark": (80, 170, 140), "magenta": (60, 200, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def domef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    ang = math.atan2(x, z)
    c = p["lilac"] if int((ang + math.pi) / (math.pi / 6)) % 2 else p["blue"]
    return tone(c, face), None


def ribbonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["magenta"] if y < 22.0 else p["ribbon"], face), None


SUIT = fabric(P, "suit", "suit_dark")


def build():
    m = Model("teslajellymon")
    mats = {"skin": SUIT, "chest": SUIT, "abs": SUIT, "pelvis": SUIT, "deltoid": SUIT, "upper_arm": SUIT,
            "forearm": SUIT, "hand": skin(P, "skin", dark="skin_dark"), "thigh": SUIT, "knee": armour(P, "suit",
            "suit_dark"), "shin": armour(P, "suit", "suit_dark", trim="sole"), "foot": armour(P, "suit", "suit_dark",
            trim="sole"), "neck": skin(P, "skin", dark="skin_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, name="teslajellymon")
    bd = a["body"]
    for i in range(10):                                                                 # ragged frill skirt
        ang = i * 2 * math.pi / 10
        cx, cz = 5.0 * math.sin(ang), 4.0 * math.cos(ang)
        m.box(bd, cx - 1.8, 22.0 + (i % 3) * 1.6, cz - 0.4, cx + 1.8, 34.0, cz + 0.4, fabric(P, "pink", "pink_dark"),
              rotation=(0, math.degrees(ang), 0), pivot=(cx, 34.0, cz))
    for sx in (-1, 1):                                                                  # green shoulder frills
        for j in range(3):
            spike(m, bd, (sx * 5.6, 50.0, (j - 1) * 1.6), (sx, -0.4, (j - 1) * 0.3), 1.6, 5.0,
                  fabric(P, "green", "green_dark"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 53.0, 60.0, skin(P, "skin", dark="skin_dark"), cut=1)
    ball(m, hd, (0, 61.0, 0), 6.0, domef, layers=5, squash=0.85)                        # jelly dome hat
    m.round_box(hd, 0, 0, 6.6, 6.6, 56.4, 58.0, domef, cut=2)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.4, 65.0, 0), (sx * 0.4, 1, 0), 2.0, 3.0, domef, tip=0.8)
    rb = m.bone("ribbons", bd, (0, 50, 2))                                              # ribbon tentacles
    for i, sx in enumerate((-1, 1, -1, 1)):
        hi = i < 2
        pts = [(sx * 4.0, 50.0 if hi else 40.0, 2.0), (sx * 12.0, 58.0 if hi else 36.0, 4.0),
               (sx * 18.0, 52.0 if hi else 26.0, 6.0), (sx * 20.0, 40.0 if hi else 16.0, 4.0),
               (sx * 18.0, 28.0 if hi else 6.0, 2.0)]
        ribbon(m, rb, pts, 2.4, ribbonf)
        spark(m, rb, (sx * 9.0, 46.0 - i * 6.0, -1.0), 2.0, solid(P, "spark", glow=True), seed=i)
    return m
