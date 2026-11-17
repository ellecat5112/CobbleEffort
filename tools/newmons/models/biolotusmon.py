"""Bio Lotusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a Bio Hybrid lotus fairy, in her official outfit: a violet bodysuit and leggings, a white frilled
lotus-petal skirt and sleeves edged with green beads, short blond hair under a lotus-seed-pod helm crowned with
yellow petals, and a tall pink staff topped with a lotus pod and a golden wheat-sheaf whip. 35 blocks tall.

Front is -z, y is up. 72 units tall; Ultimate stage. Official outfit only.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lotus fairy in a violet bodysuit, a white frilled lotus-petal skirt and sleeves with green beads, a "
        "lotus-pod helm with yellow petals and a pink lotus staff")
BASE = {"violet": (150, 60, 170), "violet_dark": (80, 24, 100), "white": (250, 250, 250), "white_dark": (200, 200, 214),
        "green": (90, 180, 90), "green_dark": (40, 110, 40), "yellow": (250, 220, 60), "pink": (240, 160, 210),
        "pink_dark": (190, 100, 160), "skin": (246, 222, 206), "hair": (250, 220, 120), "hair_dark": (200, 160, 60),
        "gold": (236, 196, 70), "eye": (60, 140, 90)}
SHINY = {"violet": (60, 110, 190), "violet_dark": (24, 50, 120), "pink": (160, 220, 250), "pink_dark": (90, 160, 210)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT = fabric(P, "violet", "violet_dark", axis="y", period=2.8)
FRILL = fabric(P, "white", "white_dark", axis="x", period=1.4)


def podf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if face in ("north", "up") and math.hypot((a % 1.6) - 0.8, (b % 1.6) - 0.8) < 0.45:
        return tone(p["green_dark"], face), None                 # seed holes
    return tone(p["green"], face), None


def build():
    m = Model("biolotusmon")
    mats = {"skin": SUIT, "hand": skin(P, "skin"), "finger": skin(P, "skin"), "foot": SUIT, "toe": SUIT,
            "neck": skin(P, "skin")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.78, leg_bulk=0.85, name="biolotusmon", hand_pose="open",
                 chest_depth=0.9)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.2, 2.4, 54.5, 60.5, skin(P, "skin"), cut=1)
    for i in range(7):
        rod(m, hd, (-2.0 + i * 0.66, 60.0, -1.0), (-2.6 + i * 0.86, 55.6, -1.4 + (i % 2) * 2), 2,
            strands(P, "hair", "hair_dark"), extend=0.2)
    m.round_box(hd, 0, 0, 3.0, 3.0, 59.6, 63.4, podf, cut=1)                           # lotus-pod helm
    for i in range(8):                                           # yellow petals round it
        ang = math.radians(i * 45)
        spike(m, hd, (2.8 * math.cos(ang), 62.0, 2.8 * math.sin(ang)), (math.cos(ang), 0.8, math.sin(ang)), 1.6,
              3.0, solid(P, "yellow"))
    sk = m.bone("skirt", bd, (0, 32, 0))
    for layer, (y0, r) in enumerate(((32.0, 5.6), (24.0, 8.4))):   # frilled lotus-petal skirt in two tiers
        for i in range(14):
            ang = math.radians(i * (360 / 14))
            c = (r * math.sin(ang), y0, -r * math.cos(ang) * 0.9)
            m.box(sk, c[0] - 2.2, y0 - 10.0, c[2], c[0] + 2.2, y0, c[2] + 0.6, FRILL,
                  rotation=(-28 * math.cos(ang), -math.degrees(ang), -28 * math.sin(ang)), pivot=c)
    for i in range(10):                                          # green bead belt
        ang = math.radians(-90 + i * 20)
        ball(m, bd, (4.4 * math.sin(ang), 31.0, -4.0 * math.cos(ang)), 0.7, solid(P, "green"), layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # frilled sleeves
        el = a[nm]["elbow"]
        m.box(a[nm]["bone"], el[0] - 3.0, el[1] - 10.0, el[2] - 3.0, el[0] + 3.0, el[1] + 2.0, el[2] + 3.0, FRILL)
    h = a["arm_right"]["hand"]                                   # the pink lotus staff
    st = m.bone("staff", a["arm_right"]["bone"], h)
    rod(m, st, (h[0], h[1] - 26.0, h[2]), (h[0], h[1] + 36.0, h[2]), 1, metal(P, "pink", dark="pink_dark"), extend=0)
    m.round_box(st, h[0], h[2], 2.0, 2.0, h[1] + 36.0, h[1] + 39.0, podf, cut=1)
    for j in range(5):                                           # golden wheat-sheaf
        rod(m, st, (h[0], h[1] + 30.0, h[2]), (h[0] + (j - 2) * 1.2, h[1] + 38.0, h[2] + 2.0), 1,
            metal(P, "gold", dark="pink_dark"), extend=0.1)
    return m
