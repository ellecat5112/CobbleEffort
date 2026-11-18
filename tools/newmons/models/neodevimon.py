"""Neo Devimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the artificial fallen angel: a tall gaunt grey-white figure with red gem studs down its chest, a
golden horned mask over its face, long white hair, a dark crimson bat-wing cape, black trousers with gold-banded
greaves and heavy spiked black boots, and very long arms ending in great golden claws. 25 blocks tall.

Front is -z, y is up. 70 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, fabric, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall gaunt grey-white fallen angel with red gem studs, a golden horned mask, long white hair, crimson bat "
        "wings, spiked black boots and very long arms with great golden claws")
BASE = {"grey": (200, 204, 214), "grey_dark": (120, 124, 140), "red": (200, 30, 40), "red_dark": (100, 10, 16),
        "gold": (230, 190, 70), "gold_dark": (150, 110, 30), "black": (36, 34, 40), "hair": (236, 236, 240),
        "hair_dark": (170, 170, 180), "wing": (130, 30, 30), "eye": (240, 40, 40)}
SHINY = {"grey": (80, 80, 96), "grey_dark": (36, 36, 46), "wing": (40, 40, 130), "red": (60, 160, 230)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "grey", dark="grey_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 3.0 and abs(((y + abs(x) * 0.5) % 3.0) - 1.5) < 0.4 and abs(abs(x) - 1.6) < 0.5:
        return p["red"], p["red"]
    return SKIN0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("neodevimon")
    mats = {"skin": SKIN0, "chest": chestf, "abs": chestf, "pelvis": fabric(P, "black", "black"),
            "thigh": fabric(P, "black", "black"), "knee": metal(P, "gold"), "shin": leather(P, "black", "black"),
            "calf": leather(P, "black", "black"), "foot": solid(P, "black"), "toe": solid(P, "black"),
            "claw": metal(P, "gold", dark="gold_dark")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.9, claws=True, name="neodevimon")
    bd = a["body"]
    for nm in ("arm_left", "arm_right"):                                                 # very long golden claws
        anc = a[nm]
        h = anc["hand"]
        sx = 1 if h[0] > 0 else -1
        for f in range(4):
            spike(m, anc["bone"], (h[0] + (f - 1.5) * 0.8, h[1] - 2.0, h[2] - 0.6), (sx * 0.2, -1, -0.3), 0.9, 9.0,
                  metal(P, "gold", dark="gold_dark"), tip=0.8)
    for nm in ("leg_left", "leg_right"):                                                 # spiked boots
        ank = a[nm]["ankle"]
        sx = 1 if ank[0] > 0 else -1
        spike(m, a[nm]["bone"], (ank[0] + sx * 2.0, 5.0, ank[2]), (sx, 0.3, 0), 1.4, 4.0, metal(P, "gold"), tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SKIN0, cut=1)
    m.round_box(hd, 0, -2.4, 2.2, 0.6, 56.4, 59.8, armour(P, "gold", "gold_dark"), cut=0)   # golden mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.6), 57.6, -3.05, max(sx * 0.6, sx * 1.6), 58.4, -2.95, solid(P, "eye", glow=True))
        pts = [(sx * 1.6, 59.6, -1.0), (sx * 4.0, 62.0, -1.0), (sx * 4.6, 66.0, 0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # horns
            rod(m, hd, p0, p1, 2 - j, metal(P, "gold", dark="gold_dark"), extend=0.3)
    for i in range(9):                                                                   # long white hair
        ang = math.radians(-80 + i * 20)
        rod(m, hd, (2.4 * math.sin(ang), 59.6, 1.0), (4.0 * math.sin(ang), 46.0, 5.0), 1,
            strands(P, "hair", "hair_dark"), extend=0.2, t2=2)
    wb = m.bone("wings", bd, (0, 50, 3))
    for side in (1, -1):                                                                 # crimson bat wings
        bat_wing(m, wb, (side * 3.0, 50.0, 3.0), 22.0, 30.0, 4, solid(P, "red_dark"), fabric(P, "wing", "red_dark"),
                 side=side, sweep=15)
    return m
