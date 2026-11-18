"""Loogarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
demon wolf grown fierce: a hulking blue beast crouched low, its back a storm of navy-and-red feathered spikes, a
masked snarling head with fire burning in its jaws, black studded gauntlets on its forelegs and huge red claws.
15 blocks long.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import cutout, flame_inside, fur, leather, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
LOOK = "a hulking blue wolf-beast with a storm of navy-and-red feathered spikes, a fire-breathing masked head, studded gauntlets and red claws"
BASE = {"navy": (40, 50, 140), "navy_dark": (14, 18, 70), "red": (220, 40, 50), "red_dark": (130, 14, 20),
        "black": (30, 30, 36), "black_dark": (10, 10, 12), "silver": (210, 214, 224), "silver_dark": (100, 104, 116),
        "mask": (110, 110, 130), "fire": (255, 180, 40, 210), "fire_core": (255, 245, 190, 240), "eye": (250, 220, 60)}
SHINY = {"navy": (70, 70, 80), "navy_dark": (24, 24, 30), "red": (240, 180, 50), "red_dark": (170, 110, 10)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "navy", "navy_dark", length=1.6)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("loogarmon")
    GAUNT = leather(P, "black", "black_dark", stitch="silver")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": metal(P, "mask", dark="black"), "snout": FUR, "jaw": FUR,
            "mouth": solid(P, "red"), "tooth": solid(P, "silver"), "leg_upper": GAUNT, "leg_lower": GAUNT, "paw": FUR,
            "claw": solid(P, "red"), "tail": FUR}
    a = quadruped(m, mats, "loogarmon", length=26.0, body_y=12.0, body_rx=6.0, body_ry=5.6, chest_bulk=1.4,
                  neck=((0, 15, -12), (0, 15, -16)), head_len=8.0, head_w=3.4, head_h=3.4, snout=0.8, mouth_open=20,
                  teeth=4, leg_bulk=1.5, toes=3, tail=((0, 16, 13), (0, 20, 18)), tail_r=(2.0, 1.4))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.3, ez + 0.6,
              solid(P, "eye", glow=True))
    for i in range(14):                                                              # storm of feathered spikes
        ang = math.radians(-80 + (i % 7) * 27)
        zz = -8.0 + (i // 7) * 12.0
        key = "red" if (i % 3 == 0) else "navy"
        spike(m, bd, (5.0 * math.sin(ang), 16.0, zz), (math.sin(ang) * 0.8, 1, 0.6), 2.2, 10.0 + (i % 3) * 2.0,
              strands(P, key, "navy_dark"), tip=0.8)
    sn = (0, a["mouth_y"], a["snout_front"])
    for rot in (0, 90):                                                              # fire in its jaws
        m.box(hd, -2.0, sn[1] - 1.0, sn[2] - 1.0, 2.0, sn[1] + 4.0, sn[2] - 1.0, cutout(flame_inside(4, 0.2, 3), firef),
              rotation=(0, rot, 0), pivot=(0, sn[1], sn[2] - 1.0))
    for nm in ("leg_front_left", "leg_front_right"):                                 # studded gauntlets
        el = a[nm]["elbow"]
        for j in range(3):
            spike(m, a[nm]["bone"], (el[0], el[1] - 1.0 - j * 1.4, el[2]), (1 if el[0] > 0 else -1, 0, 0), 0.8, 1.4,
                  metal(P, "silver", dark="silver_dark"), tip=0.8)
    return m
