"""Flaremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the lion of the sun. A powerful orange lion-man with an enormous blazing golden mane round his
head, a red-and-gold chest harness with a sun emblem, golden bracers and greaves edged with flame motifs, bare
muscular arms, a white sash and a lion's tail tipped with fire. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, fur, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a powerful orange lion-man with an enormous blazing golden mane, a red-and-gold harness with a sun emblem, "
        "golden flame-edged bracers and greaves, a white sash and a fire-tipped tail")
BASE = {"orange": (240, 130, 40), "orange_dark": (160, 70, 14), "orange_light": (255, 200, 130), "gold": (250, 200, 60),
        "gold_dark": (190, 130, 20), "red": (210, 40, 30), "red_dark": (120, 14, 10), "white": (246, 244, 236),
        "white_dark": (190, 186, 170), "eye": (40, 150, 220), "nose": (90, 40, 30), "fire": (255, 170, 40, 210),
        "fire_core": (255, 245, 180, 235)}
SHINY = {"orange": (240, 240, 246), "orange_dark": (170, 172, 190), "gold": (120, 220, 250), "gold_dark": (40, 140, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "orange", dark="orange_dark", light="orange_light")
MANE = strands(P, "gold", "gold_dark")
GOLD = armour(P, "gold", "gold_dark", trim="red", trim_w=0.3)


def harnessf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x, y - 46.0) < 2.4:
        return tone(p["gold"], face), None
    return armour(P, "red", "red_dark", trim="gold", trim_w=0.3)(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("flaremon")
    mats = {"skin": SKIN, "chest": harnessf, "abs": SKIN, "pelvis": fabric(P, "white", "white_dark"), "neck": SKIN,
            "deltoid": GOLD, "upper_arm": SKIN, "forearm": GOLD, "hand": SKIN, "finger": SKIN, "claw": solid(P, "white"),
            "thigh": SKIN, "knee": GOLD, "shin": GOLD, "calf": GOLD, "foot": SKIN, "talon": solid(P, "white")}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                 name="flaremon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 3.0, 3.0, 53.6, 60.4, SKIN, cut=1)
    m.round_box(hd, 0, -3.6, 1.8, 1.4, 54.0, 57.0, SKIN, cut=1)                          # muzzle
    m.box(hd, -0.7, 56.0, -5.1, 0.7, 57.0, -4.9, solid(P, "nose"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.9, sx * 2.2), 58.0, -3.5, max(sx * 0.9, sx * 2.2), 58.8, -3.3, solid(P, "eye"))
    for ring, (r, n, ln) in enumerate(((4.0, 16, 7.0), (5.6, 20, 9.0))):                 # enormous golden mane
        for i in range(n):
            ang = 2 * math.pi * (i + ring * 0.5) / n
            spike(m, hd, (r * math.cos(ang) * 0.8, 57.0 + r * math.sin(ang) * 0.9, 1.0 + ring * 1.2),
                  (math.cos(ang), math.sin(ang), 0.5), 2.4 - ring * 0.4, ln, MANE, tip=0.5)
    tb = m.bone("tail", bd, (0, 32, 3))                                                  # lion's tail
    pts = [(0, 32.0, 3.0), (2.0, 24.0, 10.0), (4.0, 20.0, 16.0), (5.0, 22.0, 21.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, SKIN, extend=0.4, t2=1)
    for ang in (0, 90):
        m.box(tb, 3.0, 22.0, 21.0, 7.0, 28.0, 21.0, cutout(flame_inside(4, 0.1, 7), firef), rotation=(0, ang, 0),
              pivot=(5.0, 22.0, 21.0))
    return m
