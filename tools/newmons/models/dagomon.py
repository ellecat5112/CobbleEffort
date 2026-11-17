"""Dagomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the deep-sea demon god. A towering pale-blue figure whose lower body and arms dissolve into masses of
writhing tentacles, a fanged leering head with small horns, black flame-shaped crest and red markings, a great finned
crest of orange membrane, strings of violet prayer beads, gold and leather bands and steel chains round its arms.
25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import leather, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a towering pale-blue deep-sea demon whose lower body and arms dissolve into writhing tentacles, a fanged "
        "horned head, an orange fin crest, violet prayer beads and chained bands")
BASE = {"blue": (140, 160, 210), "blue_dark": (70, 86, 140), "blue_light": (210, 220, 250), "red": (200, 50, 50),
        "black": (30, 30, 36), "fin": (240, 150, 100), "fin_dark": (190, 90, 50), "bead": (130, 90, 170),
        "gold": (230, 186, 60), "gold_dark": (160, 120, 20), "brown": (110, 80, 50), "brown_dark": (60, 40, 20),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "horn": (240, 236, 220), "mouth": (130, 20, 40),
        "tooth": (250, 250, 246), "eye": (240, 60, 40)}
SHINY = {"blue": (140, 200, 150), "blue_dark": (70, 130, 80), "blue_light": (210, 250, 220), "fin": (180, 120, 230),
         "fin_dark": (110, 60, 170)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.05)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.4) < 0.7 and abs(y - 52.6) < 0.35:
                return p["eye"], p["eye"]
            if abs(x - sx * 2.2) < 0.25 and 53.4 < y < 55.6:
                return tone(p["red"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def tentacle(m, bone, start, d, n, length, r0, curl):
    pts = [start]
    for j in range(1, n + 1):
        t = j / n
        ang = curl * t * 2.4
        pts.append((start[0] + d[0] * length * t + math.sin(ang) * 2.0, start[1] + d[1] * length * t,
                    start[2] + d[2] * length * t + math.cos(ang) * 2.0 - 2.0))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, max(1, round(r0 * (1 - j / (n + 1)))), SKIN, extend=0.6)


def build():
    m = Model("dagomon")
    top = m.bone("dagomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 30.0, 48.0, SKIN, cut=2)                          # torso
    hd = m.bone("head", bd, (0, 48, -1))
    m.round_box(hd, 0, -1.0, 3.6, 3.6, 48.0, 57.0, headf, cut=1)
    m.box(hd, -3.0, 48.0, -6.0, 3.0, 51.0, -3.0, SKIN)                                 # jaw
    m.box(hd, -2.6, 50.4, -6.2, 2.6, 51.2, -3.0, solid(P, "mouth"))
    for i in range(4):
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.2, 51.2, -6.0 + i * 0.9), (0, -1, 0), 0.7, 1.4, solid(P, "tooth"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 56.0, 0), (sx * 0.6, 1, 0.3), 1.4, 3.0, solid(P, "horn"), tip=0.3)
    for i in range(4):                                                                 # black flame crest
        spike(m, hd, (-1.0 + i * 0.6, 56.6, 1.0), (-0.8, 1, 0.3), 1.6, 6.0 - i, solid(P, "black"), tip=0.3)
    fin = m.bone("fin", bd, (3, 50, 2))                                                # orange fin crest
    for j in range(5):
        m.box(fin, 3.0, 50.0, 2.0 + j * 0.3, 14.0 - j * 1.4, 52.0, 2.4 + j * 0.3, skin(P, "fin", dark="fin_dark"),
              rotation=(0, -20, 20 + j * 14), pivot=(3.0, 51.0, 2.0))
    for i in range(14):                                                                # prayer beads
        ang = math.radians(-100 + i * 15)
        m.round_box(bd, 5.8 * math.sin(ang), -1.0 - 4.6 * math.cos(ang), 1.0, 1.0, 45.0 - 3.0 * math.cos(ang) ** 2,
                    47.0 - 3.0 * math.cos(ang) ** 2, solid(P, "bead"), cut=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # tentacle arms
        ab = m.bone(nm, bd, (sx * 6.0, 44.0, 0))
        for k in range(4):
            tentacle(m, ab, (sx * 6.0, 44.0, -1.0 + k * 0.6), (sx * 0.8, -0.6 - k * 0.1, -0.2), 5, 20.0, 3, k)
        m.round_box(ab, sx * 10.0, -1.0, 3.2, 3.2, 38.0, 41.0, metal(P, "gold", dark="gold_dark"), cut=1)
        m.round_box(ab, sx * 13.0, -1.6, 3.0, 3.0, 34.0, 36.4, leather(P, "brown", "brown_dark", stitch="steel"), cut=1)
    for k in range(10):                                                                # tentacle lower body
        ang = math.radians(k * 36)
        tentacle(m, bd, (3.0 * math.cos(ang), 31.0, 3.0 * math.sin(ang)),
                 (0.5 * math.cos(ang), -1.0, 0.5 * math.sin(ang)), 6, 28.0, 4, k * 0.7)
    return m
