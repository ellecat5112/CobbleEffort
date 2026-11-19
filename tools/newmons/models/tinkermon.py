"""Tinkermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net; built covered): a tiny fairy girl with a long blonde ponytail tied with a big green bow, a green
leaf tunic and shorts with leggings, brown laced boots and gauntlets, glittering translucent golden wings, and a red
trident spear longer than she is. 1 block.

Front is -z, y is up. 64 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, leather, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(1.0, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a tiny fairy girl with a blonde ponytail and green bow, a green leaf tunic, brown boots, golden wings and a red trident"
BASE = {"skin": (250, 220, 200), "skin_dark": (210, 170, 150), "green": (90, 170, 110), "green_dark": (40, 100, 60),
        "hair": (240, 220, 120), "hair_dark": (190, 160, 60), "brown": (150, 110, 60), "brown_dark": (90, 60, 30),
        "red": (210, 40, 50), "wing": (255, 230, 120, 140), "eye": (60, 120, 220), "legging": (230, 230, 210),
        "legging_dark": (180, 180, 160)}
SHINY = {"green": (220, 110, 160), "green_dark": (150, 50, 100), "hair": (200, 220, 250), "hair_dark": (130, 150, 200)}


def P(v):
    return pal(BASE, SHINY, v)


TUNIC = fabric(P, "green", "green_dark")
SKIN = skin(P, "skin", dark="skin_dark")


def faceF(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.2, y - 58.0) < 0.6:
                return p["eye"], None
    return SKIN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("tinkermon")
    mats = {"skin": SKIN, "chest": TUNIC, "abs": TUNIC, "pelvis": TUNIC, "deltoid": TUNIC, "upper_arm": SKIN,
            "forearm": leather(P, "brown", "brown_dark"), "hand": SKIN, "thigh": fabric(P, "legging", "legging_dark"),
            "knee": fabric(P, "legging", "legging_dark"), "shin": leather(P, "brown", "brown_dark"),
            "calf": leather(P, "brown", "brown_dark"), "foot": leather(P, "brown", "brown_dark"), "neck": SKIN}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name="tinkermon")
    bd = a["body"]
    for i in range(8):                                                                  # leaf hem
        ang = i * 2 * math.pi / 8
        cx, cz = 4.0 * math.sin(ang), 3.2 * math.cos(ang)
        spike(m, bd, (cx, 31.0, cz), (math.sin(ang) * 0.3, -1, math.cos(ang) * 0.3), 2.4, 5.0, TUNIC, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.0, 53.0, 61.0, faceF, cut=1)
    m.round_box(hd, 0, 0.8, 3.3, 2.6, 58.6, 62.0, strands(P, "hair", "hair_dark"), cut=1)
    pts = [(0, 61.0, 2.0), (3.0, 63.0, 4.0), (6.0, 60.0, 5.0), (7.0, 52.0, 5.0), (6.0, 44.0, 4.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # long ponytail
        rod(m, hd, p0, p1, 2, strands(P, "hair", "hair_dark"), extend=0.6)
    for sx in (-1, 1):                                                                  # green bow
        m.round_box(hd, sx * 2.0, 2.0, 1.6, 0.8, 61.4, 64.4, solid(P, "green"), cut=0)
    wb = m.bone("wings", bd, (0, 48, 3))
    for sx in (-1, 1):
        for j, (h, w, ang) in enumerate(((14.0, 9.0, 30), (9.0, 6.0, -20))):
            m.box(wb, min(sx * 1.0, sx * w), 48.0, 3.6, max(sx * 1.0, sx * w), 48.0 + h, 3.8, solid(P, "wing", glow=True),
                  rotation=(0, 0, sx * ang), pivot=(0, 48.0, 3.7))
    h = a["arm_right"]["hand"]                                                          # red trident
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0] - 14.0, h[1] - 10.0, h[2]), (h[0] + 14.0, h[1] + 10.0, h[2]), 1, solid(P, "red"), extend=0.0)
    for j in range(3):
        spike(m, rb, (h[0] - 14.0, h[1] - 10.0, h[2]), (-1 + (j - 1) * 0.2, -0.7 + (j - 1) * 0.3, 0), 1.0, 4.0,
              solid(P, "red"), tip=0.8)
    return m
