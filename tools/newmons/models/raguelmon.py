"""Raguelmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a fallen angel of a beast-man: a crouching hunter in gold-and-black banded armour, a wild mane
of tawny fur and a golden fur ruff round a feral masked face with a violet eye-gem, one smoky grey feathered wing and
one black wing trailing ash, long violet crystal claws on its hands and feet. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a crouching fallen-angel beast-man in gold-and-black banded armour with a tawny mane, a smoky grey wing and violet crystal claws"
BASE = {"gold": (230, 190, 70), "gold_dark": (150, 100, 20), "black": (36, 32, 36), "black_dark": (12, 10, 12),
        "tawny": (220, 170, 90), "tawny_dark": (150, 100, 40), "grey": (170, 170, 180), "grey_dark": (90, 90, 100),
        "ash": (50, 48, 54), "violet": (200, 90, 240), "white": (240, 240, 246)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (140, 144, 160), "tawny": (200, 200, 214), "tawny_dark": (130, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def bandf(x, y, z, face, variant, box=None, **k):
    if (y % 3.6) < 1.2:
        return armour(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)
    return armour(P, "gold", "gold_dark")(x, y, z, face, variant, box=box, **k)


MANE = fur(P, "tawny", "tawny_dark", length=1.6)
CLAW = solid(P, "violet", glow=True)


def build():
    m = Model("raguelmon")
    mats = {"skin": bandf, "neck": MANE, "hand": bandf, "finger": bandf, "claw": CLAW, "talon": CLAW}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.05, claws=True, talons=True, digitigrade=True,
                 name="raguelmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.6, 5.0, 48.0, 53.0, MANE, cut=2)                               # golden ruff
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.8, 3.2, 54.0, 60.0, bandf, cut=1)
    m.round_box(hd, 0, -3.8, 1.8, 1.2, 54.0, 56.6, metal(P, "gold", dark="gold_dark"), cut=0)   # feral muzzle
    m.box(hd, -0.8, 57.4, -4.1, 0.8, 58.6, -3.8, gem(P, "violet", "white"))
    for j in range(9):                                                                   # wild mane
        ang = math.radians(-80 + j * 20)
        spike(m, hd, (2.6 * math.sin(ang), 58.0 + 1.6 * math.cos(ang), 1.6), (math.sin(ang), math.cos(ang) + 0.2, 0.8),
              1.6, 6.0 + (j % 3) * 1.6, MANE, tip=0.8)
    for side, key, dark in ((1, "grey", "grey_dark"), (-1, "ash", "black_dark")):        # mismatched wings
        feather_wing(m, bd, (side * 3.0, 50.0, 3.0), 22.0, 14.0, 5, feathers(P, key, dark), side=side, sweep=30,
                     droop=-6.0)
    for side in ("arm_left", "arm_right"):                                               # long crystal claws
        h = a[side]["hand"]
        sx = 1 if side == "arm_left" else -1
        for f in range(3):
            spike(m, a[side]["bone"], (h[0] + (f - 1) * 0.8, h[1], h[2]), (sx * 0.3, -1, -0.4), 0.9, 7.0, CLAW, tip=0.8)
    return m
