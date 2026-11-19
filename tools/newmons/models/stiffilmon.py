"""Stiffilmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a feral beast-man of blades: a hulking white-furred wolf-man with a wild golden mane streaked
black, a snarling fanged face, a rope belt and ragged dark trousers, scarred brown boots, and long black-and-red blade
spikes bristling from its shoulders, arms and legs, with huge red-tipped claws. 25 blocks.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking white-furred wolf-man with a wild golden mane, a snarling face and long black-and-red blade spikes bristling all over"
BASE = {"white": (240, 236, 230), "white_dark": (180, 176, 170), "gold": (240, 190, 50), "gold_dark": (170, 110, 20),
        "black": (30, 28, 32), "red": (200, 30, 40), "dark": (50, 44, 44), "dark2": (20, 18, 18), "brown": (120, 80, 50),
        "brown_dark": (70, 44, 24), "rope": (200, 170, 120), "eye": (90, 200, 120), "mouth": (130, 30, 40)}
SHINY = {"white": (60, 56, 66), "white_dark": (24, 22, 28), "gold": (200, 210, 230), "gold_dark": (120, 130, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["red"] if (x + y + z) % 3.0 < 0.8 else p["black"], face), None


FUR = fur(P, "white", "white_dark", length=1.6)


def build():
    m = Model("stiffilmon")
    mats = {"skin": FUR, "pelvis": fabric(P, "dark", "dark2", axis="y"), "thigh": fabric(P, "dark", "dark2", axis="y"),
            "knee": fabric(P, "dark", "dark2"), "shin": leather(P, "brown", "brown_dark"),
            "foot": leather(P, "brown", "brown_dark"), "claw": solid(P, "red"), "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.35, leg_bulk=1.2, claws=True, talons=True, digitigrade=True,
                 name="stiffilmon")
    bd = a["body"]
    m.round_box(bd, 0, 0, 6.0, 4.6, 31.0, 33.0, solid(P, "rope"), cut=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.2, 3.0, 3.4, 53.4, 60.0, FUR, cut=1)
    m.round_box(hd, 0, -4.4, 1.8, 1.6, 53.6, 56.6, FUR, cut=0)
    m.box(hd, -1.4, 53.8, -6.1, 1.4, 54.6, -5.9, solid(P, "mouth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -4.7, max(sx * 0.8, sx * 2.2), 58.2, -4.5, solid(P, "eye"))
    for j in range(14):                                                                  # wild golden mane
        ang = math.radians(-110 + j * 17)
        spike(m, hd, (3.0 * math.sin(ang), 58.0 + 2.6 * math.cos(ang), 1.6), (math.sin(ang), math.cos(ang) + 0.3, 0.8),
              2.0, 8.0 + (j % 3) * 3.0, strands(P, "gold", "black"), tip=0.8)
    for sx in (-1, 1):                                                                   # blade spikes everywhere
        for j in range(4):
            spike(m, bd, (sx * 8.0, 50.0 - j * 2.0, -1.0 + j * 1.4), (sx * 1, 0.3 - j * 0.15, 0.2), 1.6, 14.0 - j * 2.0,
                  bladef, tip=0.8)
    for side in ("arm_left", "arm_right", "leg_left", "leg_right"):
        p0 = a[side]["elbow" if side.startswith("arm") else "knee"]
        sx = 1 if side.endswith("left") else -1
        spike(m, a[side]["bone"], p0, (sx * 1, 0.2, 0.4), 1.4, 9.0, bladef, tip=0.8)
    return m
