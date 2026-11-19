"""Slash Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the blade angel: a lean warrior in silver plate and a long sky-blue tabard trimmed gold
with a holy cross, a silver mask-helm with spiky blue hair, and great wings made of long curved silver blades sweeping
up and down, its arms ending in blade gauntlets. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a lean blade angel in silver plate and a long sky-blue tabard, a silver mask-helm with spiky blue hair and wings of long curved silver blades"
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 124, 140), "blue": (100, 180, 240), "blue_dark": (40, 100, 170),
        "gold": (236, 196, 70), "hair": (90, 140, 220), "hair_dark": (40, 70, 150), "visor": (40, 40, 60)}
SHINY = {"blue": (240, 120, 160), "blue_dark": (170, 50, 90), "hair": (240, 200, 90)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = metal(P, "silver", dark="silver_dark")


def tabardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and ((abs(x) < 0.5 and 18.0 < y < 30.0) or (abs(y - 26.0) < 0.5 and abs(x) < 2.4)):
        return tone(p["gold"], face), None
    return fabric(P, "blue", "blue_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("slashangemon")
    mats = {"skin": armour(P, "silver", "silver_dark"), "talon": SILVER}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=0.9, talons=True, name="slashangemon")
    bd = a["body"]
    m.box(bd, -4.0, 4.0, -4.6, 4.0, 46.0, -4.0, tabardf)                                      # long tabard
    m.box(bd, -4.0, 4.0, 4.0, 4.0, 46.0, 4.6, tabardf)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.0, SILVER, cut=1)
    m.box(hd, -1.8, 56.6, -3.3, 1.8, 58.0, -3.1, solid(P, "visor"))
    for j in range(7):                                                                   # spiky blue hair
        spike(m, hd, ((j - 3) * 0.8, 60.0, 0.6), ((j - 3) * 0.2, 1, 0.6), 1.2, 5.0, strands(P, "hair", "hair_dark"), tip=0.8)
    wb = m.bone("wings", bd, (0, 50, 4))                                                 # wings of curved blades
    for sx in (-1, 1):
        for j in range(5):
            ang = math.radians(-50 + j * 30)
            d = (sx * math.cos(ang) * 0.6, math.sin(ang), 0.5)
            spike(m, wb, (sx * 3.0, 50.0, 4.0 + j * 0.3), d, 2.0, 30.0, SILVER, tip=0.8)
    for side in ("arm_left", "arm_right"):                                               # blade gauntlets
        w = a[side]["wrist"]
        sx = 1 if side == "arm_left" else -1
        spike(m, a[side]["bone"], w, (sx * 0.2, -1, -0.3), 1.6, 18.0, SILVER, tip=0.8)
    return m
