"""Blucomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little ice dragon. A crouching cobalt-blue dragon with a pale belly, a thick white fur mane round
its neck and down its back, a head crowned with jagged ice crystals, pink eyes, ice-crystal claws and a long tail
ending in a translucent icy blade. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import eye, fur, gem, scales, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a crouching cobalt-blue ice dragon with a white fur mane, a crown of jagged ice crystals, pink eyes, "
        "ice-crystal claws and a tail ending in an icy blade")
BASE = {"blue": (40, 70, 200), "blue_dark": (16, 30, 110), "blue_light": (110, 150, 240), "belly": (150, 180, 240),
        "fur": (244, 246, 252), "fur_dark": (180, 186, 204), "ice": (180, 226, 250), "ice_light": (240, 252, 255),
        "eye": (240, 90, 140), "pupil": (40, 10, 30), "white": (255, 255, 255), "mouth": (130, 30, 50),
        "tooth": (250, 250, 250)}
SHINY = {"blue": (90, 50, 170), "blue_dark": (40, 16, 90), "blue_light": (170, 130, 240), "belly": (200, 180, 240),
         "ice": (250, 200, 230), "ice_light": (255, 240, 250), "eye": (90, 220, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.4, light="blue_light", rim_mix=0.4)
BELLY = skin(P, "belly", var=0.03)
FUR = fur(P, "fur", "fur_dark", length=1.2)
ICE = gem(P, "ice", "ice_light", glow=False)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 16.6, y - 19.6, 1.1, "eye")
        if c is not None:
            return c, None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("blucomon")
    mats = {"skin": HIDE, "belly": BELLY, "neck": FUR, "head": headf, "snout": HIDE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": HIDE,
            "paw": HIDE, "claw": ICE, "tail": HIDE}
    a = quadruped(m, mats, "blucomon", length=14.0, body_y=10.0, body_rx=5.0, body_ry=5.0, chest_bulk=1.25,
                  neck=((0, 15, -7), (0, 18, -11)), head_len=10.0, head_w=4.2, head_h=4.4, snout=0.45,
                  mouth_open=14, teeth=4, leg_bulk=1.4, toes=3,
                  tail=((0, 14, 10), (0, 19, 14), (0, 25, 15)), tail_r=(2.0, 1.4, 1.0))
    bd, hd = a["body"], a["head"]
    # the white fur mane round the neck and down the back
    mane = m.bone("mane", bd, (0, 15, -6))
    for i in range(16):
        ang = math.radians(i * 22.5)
        base = (4.6 * math.cos(ang), 14.5 + 4.0 * math.sin(ang), -6.0)
        spike(m, mane, base, (math.cos(ang) * 0.7, 0.4 + 0.5 * math.sin(ang), 0.6), 2.4, 4.2, FUR, tip=1.0)
    for j in range(5):
        spike(m, bd, (0, 15.0 - j * 0.3, -3.0 + j * 2.6), (0, 1, 0.5), 3.0 - j * 0.3, 3.4, FUR, tip=1.0)
    # the crown of jagged ice crystals
    st = a["skull_top"]
    for sx, dz, ln in ((-1, 0, 6.0), (1, 0, 6.0), (-1, 2, 4.4), (1, 2, 4.4), (0, 1, 3.6)):
        spike(m, hd, (sx * 2.2, st - 0.4, -13.0 + dz), (sx * 0.5, 1, 0.7), 1.6, ln, ICE, tip=0.6)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.6, st - 2.6, -12.0), (sx, 0.2, 0.6), 1.2, 3.0, ICE, tip=0.4)
    # the icy tail blade
    e = a["tail_pts"][-1]
    m.box(a["tail"], -0.2, e[1] - 1.0, e[2] - 1.0, 0.2, e[1] + 9.0, e[2] + 3.0, ICE,
          rotation=(-20, 0, 0), pivot=e)
    spike(m, a["tail"], e, (0, 1, -0.4), 1.6, 5.0, ICE, tip=0.4)
    return m
