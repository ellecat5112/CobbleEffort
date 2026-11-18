"""Firamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
flaming lion cub. A sturdy red-orange lion with a blazing golden mane, a red-and-gold helmet with a black crest,
flame-feathered red wings, black bands on its legs, golden claws, tongues of fire licking off its shoulders, mane
and tail. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, quadruped
from _digidetail import armour, cutout, feathers, flame_inside, fur, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a sturdy red-orange lion with a blazing golden mane, a red-and-gold helmet, flame-feathered red wings, black "
        "leg bands, golden claws and tongues of fire")
BASE = {"orange": (230, 90, 40), "orange_dark": (150, 40, 14), "orange_light": (255, 170, 110), "gold": (250, 200, 60),
        "gold_dark": (190, 130, 20), "red": (210, 40, 30), "red_dark": (120, 14, 10), "black": (30, 28, 30),
        "fire": (255, 170, 40, 210), "fire_core": (255, 245, 180, 235), "eye": (60, 140, 220), "mouth": (130, 20, 30),
        "tooth": (250, 250, 246)}
SHINY = {"orange": (70, 130, 220), "orange_dark": (20, 60, 150), "orange_light": (160, 200, 255), "red": (40, 80, 200)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fur(P, "orange", "orange_dark", tip="orange_light", length=1.2, density=2.4)
MANE = strands(P, "gold", "gold_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def flame(m, bone, at, w, h, seed):
    for ang in (0, 90):
        m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
              cutout(flame_inside(4, 0.1, seed), firef), rotation=(0, ang, 0), pivot=at)


def build():
    m = Model("firamon")
    mats = {"skin": COAT, "belly": COAT, "neck": MANE, "head": COAT, "snout": COAT, "jaw": COAT,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": COAT, "leg_lower": COAT, "paw": COAT,
            "claw": solid(P, "gold"), "tail": COAT}
    a = quadruped(m, mats, "firamon", length=26.0, body_y=13.0, body_rx=6.0, body_ry=5.6, chest_bulk=1.3,
                  neck=((0, 17, -12), (0, 20, -15)), head_len=8.0, head_w=4.4, head_h=4.6, snout=0.4, mouth_open=6,
                  teeth=2, leg_bulk=1.6, toes=4, tail=((0, 15, 13), (2, 19, 18), (4, 22, 21)), tail_r=(1.4, 1.2, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    m.round_box(hd, 0, ez + 1.0, 4.0, 3.0, ey + 1.0, ey + 4.0, armour(P, "red", "red_dark", trim="gold"), cut=1)   # helmet
    spike(m, hd, (0, ey + 4.0, ez + 1.0), (0, 1, 0.3), 1.4, 4.0, solid(P, "black"), tip=0.4)
    for i in range(14):                                                           # blazing golden mane
        ang = 2 * math.pi * i / 14
        spike(m, hd, (4.4 * math.cos(ang), ey + 4.4 * math.sin(ang), ez + 3.0), (math.cos(ang), math.sin(ang), 0.8),
              2.0, 6.0, MANE, tip=0.5)
    for side in (1, -1):                                                          # flame-feathered wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 18.0, -4.0))
        feather_wing(m, wb, (side * 4.0, 18.0, -4.0), 12.0, 7.0, 2, feathers(P, "red", "red_dark", tip="gold"),
                     side=side, sweep=30, droop=-6.0)
        flame(m, bd, (side * 5.0, 18.0, -8.0), 3.0, 6.0, side + 3)                # shoulder fire
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.4, 2.4, 4.0, 5.4, solid(P, "black"), cut=1)
    flame(m, a["tail"], a["tail_pts"][-1], 4.0, 7.0, 9)
    flame(m, hd, (0, ey + 6.0, ez + 2.0), 4.0, 7.0, 12)
    return m
