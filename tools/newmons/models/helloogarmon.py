"""Helloogarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the hell-wolf: a gaunt dark wolf-beast wreathed in red-orange hellfire from muzzle to tail, black
spiked fur showing through the flames, huge black claws, a burning fan of a tail and glowing ember spots. 25 blocks.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, fur, local, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a gaunt dark wolf-beast wreathed in red-orange hellfire with black spiked fur, huge black claws and a burning tail"
BASE = {"black": (40, 30, 30), "black_dark": (14, 10, 10), "red": (230, 70, 40), "red_dark": (150, 20, 14),
        "fire": (255, 120, 40, 215), "fire_core": (255, 230, 150, 240), "claw": (24, 22, 26), "eye": (255, 220, 60),
        "mouth": (90, 14, 14), "tooth": (250, 240, 220)}
SHINY = {"fire": (120, 90, 255, 215), "red": (120, 80, 230), "red_dark": (60, 30, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FUR0 = fur(P, "red", "red_dark", tip="black", length=1.4, density=2.0)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def flame(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, 0.2, seed), firef), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("helloogarmon")
    mats = {"skin": FUR0, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "claw"),
            "leg_lower": fur(P, "black", "black_dark"), "paw": fur(P, "black", "black_dark")}
    a = quadruped(m, mats, "helloogarmon", length=30.0, body_y=16.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.3,
                  neck=((0, 20, -13), (0, 23, -17)), head_len=11.0, head_w=3.0, head_h=3.4, snout=0.9, mouth_open=18,
                  teeth=6, leg_bulk=1.2, toes=4, tail=((0, 19, 15), (4, 24, 20), (9, 27, 21)), tail_r=(2.4, 2.4, 2.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye", glow=True))
    for j, at in enumerate(((0, 21.0, -10.0), (0, 21.0, -2.0), (0, 21.0, 6.0), (0, 21.0, 12.0))):
        flame(m, bd, at, 6.0, 7.0, j + 2)
    flame(m, a["tail"], a["tail_pts"][-1], 7.0, 10.0, 8)
    flame(m, hd, (0, ey + 2.0, ez + 2.0), 4.0, 6.0, 11)
    return m
