"""Vulturemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a vulture bounty hunter: a bald grey hooked-beak head under a skull-marked bandana and a white
fur ruff, a ragged brown hooded cloak with a spiked green shoulder guard, ammo belts, baggy cream trousers bearing a
skull, grey taloned feet, wings of black and crimson feathers, and a long scoped sniper rifle. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import cape, humanoid
from _digidetail import fabric, feathers, fur, leather, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a vulture bounty hunter with a hooked-beak grey head, a ragged brown cloak, a spiked green shoulder guard, crimson-black wings and a long sniper rifle"
BASE = {"grey": (130, 130, 140), "grey_dark": (70, 70, 80), "white": (236, 236, 240), "white_dark": (180, 180, 190),
        "cloak": (110, 80, 60), "cloak_dark": (60, 40, 26), "green": (60, 200, 90), "cream": (230, 220, 190),
        "cream_dark": (180, 166, 130), "black": (30, 28, 32), "red": (190, 30, 40), "steel": (180, 184, 196),
        "steel_dark": (80, 84, 96), "skull": (240, 236, 226), "eye": (250, 220, 60), "brass": (220, 170, 70)}
SHINY = {"cloak": (60, 80, 110), "cloak_dark": (24, 34, 60), "red": (220, 160, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def trouserf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and box is not None and math.hypot(x - (box.lo[0] + box.size[0] / 2), y - 20.0) < 1.4:
        return tone(p["skull"], face), None
    return fabric(P, "cream", "cream_dark")(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) > 14.0:
        return tone(p["red"], face), None
    return feathers(P, "black", "black")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vulturemon")
    CLOAK = fabric(P, "cloak", "cloak_dark")
    mats = {"skin": CLOAK, "chest": CLOAK, "abs": leather(P, "black", "black"), "pelvis": trouserf, "deltoid": CLOAK,
            "upper_arm": CLOAK, "forearm": CLOAK, "hand": skin(P, "grey", dark="grey_dark"), "thigh": trouserf,
            "knee": trouserf, "shin": skin(P, "grey", dark="grey_dark"), "calf": skin(P, "grey", dark="grey_dark"),
            "foot": skin(P, "grey", dark="grey_dark"), "talon": solid(P, "black"), "neck": fur(P, "white", "white_dark")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, digitigrade=True, talons=True, name="vulturemon")
    bd = a["body"]
    for j in range(8):                                                                  # ammo belt
        t = j / 7
        m.box(bd, -5.0 + t * 10.0 - 0.5, 50.0 - t * 14.0 - 1.0, -4.6, -5.0 + t * 10.0 + 0.5, 50.0 - t * 14.0 + 1.0,
              -3.8, solid(P, "brass"))
    m.round_box(bd, 7.6, 0, 3.6, 3.8, 47.0, 54.0, metal(P, "green"), cut=1)                  # spiked shoulder guard
    for j in range(5):
        ang = j * 0.6 - 1.2
        spike(m, bd, (7.6 + 3.0 * math.sin(ang), 52.0, 3.0 * math.cos(ang)), (math.sin(ang), 0.6, math.cos(ang)), 1.0,
              2.6, metal(P, "green"), tip=0.8)
    m.round_box(bd, 0, 0.4, 5.6, 4.4, 50.0, 54.0, fur(P, "white", "white_dark", length=1.6), cut=2)   # fur ruff
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.6, 3.4, 54.0, 60.0, skin(P, "grey", dark="grey_dark"), cut=1)
    spike(m, hd, (0, 57.0, -4.4), (0, -0.6, -1), 1.6, 4.0, metal(P, "steel"), tip=0.8)        # hooked beak
    m.round_box(hd, 0, 0, 2.9, 3.6, 59.0, 61.6, fabric(P, "black", "black"), cut=1)         # bandana
    m.box(hd, -1.0, 59.6, -3.8, 1.0, 61.0, -3.5, solid(P, "skull"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.4), 58.0, -4.3, max(sx * 1.0, sx * 2.4), 58.8, -4.0, solid(P, "eye", glow=True))
        wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 46.0, 4.0))
        feather_wing(m, wb, (sx * 3.0, 46.0, 4.0), 20.0, 12.0, 3, wingf, side=sx, sweep=50, droop=10.0)
    cb = m.bone("cape", bd, (0, 52, 4))
    cape(m, cb, 52.0, 13.0, 30.0, CLOAK, z=4.6, flare=0.6, panels=6, seed=4)
    h = a["arm_right"]["hand"]                                                          # sniper rifle
    rb = a["arm_right"]["bone"]
    rod(m, rb, (h[0] + 6.0, h[1] + 2.0, h[2] + 2.0), (h[0] - 22.0, h[1] + 4.0, h[2] - 2.0), 1, metal(P, "steel",
        dark="steel_dark"), extend=0.0)
    m.box(rb, h[0] - 4.0, h[1] + 3.0, h[2] - 0.6, h[0] + 2.0, h[1] + 4.4, h[2] + 0.6, metal(P, "black"))
    m.box(rb, h[0] + 2.0, h[1] - 0.6, h[2] + 0.8, h[0] + 7.0, h[1] + 2.4, h[2] + 2.6, leather(P, "cloak", "cloak_dark"))
    m.box(rb, h[0] - 23.0, h[1] + 3.4, h[2] - 2.6, h[0] - 21.0, h[1] + 4.6, h[2] - 1.4, solid(P, "red"))
    return m
