"""Pidmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the fire angel: a lean angel with one white and one black wing, silver armour bound with pink cloth
streamers, a helmet with a crescent crest, long silver hair, white boots and a golden staff topped with a crescent.
15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean angel with one white and one black wing, silver armour bound with pink cloth streamers, long silver hair and a crescent staff"
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 116, 130), "pink": (220, 80, 150), "pink_dark": (140, 30, 90),
        "white": (246, 246, 250), "white_dark": (190, 190, 210), "black": (40, 40, 48), "black_dark": (14, 14, 18),
        "gold": (230, 190, 70), "hair": (220, 220, 230), "hair_dark": (160, 160, 176), "eye": (240, 60, 60)}
SHINY = {"pink": (90, 170, 240), "pink_dark": (40, 100, 180)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", trim="pink", trim_w=0.25)


def build():
    m = Model("pidmon")
    mats = {"skin": ARM, "abs": fabric(P, "pink", "pink_dark"), "pelvis": fabric(P, "pink", "pink_dark"),
            "foot": solid(P, "white"), "toe": solid(P, "white")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="pidmon")
    bd = a["body"]
    for j in range(4):                                                                   # pink cloth streamers
        m.box(bd, -2.0 + j * 1.4, 10.0 + j * 2.0, -4.0, -1.0 + j * 1.4, 32.0, -3.6, fabric(P, "pink", "pink_dark"),
              rotation=(-5, 0, (j - 1.5) * 5), pivot=(-1.5 + j * 1.4, 32.0, -3.8))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, ARM, cut=1)
    m.box(hd, -1.8, 57.2, -3.3, 1.8, 58.0, -3.1, solid(P, "eye", glow=True))
    for i in range(5):                                                                   # crescent crest
        ang = math.radians(-60 + i * 30)
        m.box(hd, 3.0 * math.sin(ang) - 0.5, 61.0 + 3.0 * math.cos(ang) - 0.5, -0.5, 3.0 * math.sin(ang) + 0.5,
              61.0 + 3.0 * math.cos(ang) + 0.5, 0.5, metal(P, "gold"))
    for i in range(7):                                                                   # long silver hair
        ang = math.radians(-60 + i * 20)
        rod(m, hd, (2.2 * math.sin(ang), 59.0, 1.0), (3.6 * math.sin(ang), 44.0, 4.0), 1, strands(P, "hair", "hair_dark"),
            extend=0.2, t2=2)
    wb = m.bone("wings", bd, (0, 48, 3))
    feather_wing(m, wb, (3.0, 48.0, 3.0), 20.0, 16.0, 6, feathers(P, "white", "white_dark"), side=1, sweep=25,
                 droop=-12.0)
    feather_wing(m, wb, (-3.0, 48.0, 3.0), 20.0, 16.0, 6, feathers(P, "black", "black_dark"), side=-1, sweep=25,
                 droop=-12.0)
    ar = a["arm_right"]                                                                  # crescent staff
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] - 24.0, h[2]), (h[0], h[1] + 18.0, h[2]), 1, metal(P, "gold"), extend=0.2)
    for i in range(5):
        ang = math.radians(-70 + i * 35)
        m.box(ar["bone"], h[0] + 2.4 * math.sin(ang) - 0.5, h[1] + 20.0 + 2.4 * math.cos(ang) - 0.5, h[2] - 0.5,
              h[0] + 2.4 * math.sin(ang) + 0.5, h[1] + 20.0 + 2.4 * math.cos(ang) + 0.5, h[2] + 0.5, metal(P, "gold"))
    return m
