"""Rebellimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a biker outlaw welded to its machine: a green reptile rider with a blazing orange mohawk and a
skull mask, steel bull horns and hoses, riding a single huge flame-painted wheel, a hazard-striped saw-blade launcher
on one arm and a spiked iron gauntlet on the other. 25 blocks.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, scales, solid, strands
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a green reptile biker with a blazing orange mohawk and skull mask on a huge flame-painted wheel, a saw-blade launcher and a spiked gauntlet"
BASE = {"green": (70, 160, 60), "green_dark": (24, 90, 20), "orange": (250, 140, 30), "yellow": (250, 210, 40),
        "black": (30, 28, 32), "steel": (180, 184, 196), "steel_dark": (80, 84, 96), "rust": (140, 80, 50),
        "rust_dark": (80, 40, 20), "bone": (236, 230, 214), "red": (220, 50, 30), "tyre": (36, 34, 38)}
SHINY = {"green": (60, 120, 200), "green_dark": (20, 60, 140), "orange": (200, 60, 220)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.2)
STEEL = metal(P, "steel", dark="steel_dark")
RUST = metal(P, "rust", dark="rust_dark")


def hazardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["yellow"] if (x + y) % 3.0 < 1.5 else p["black"], face), None


def wheelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 12.0) < 5.0 and abs(z) < 8.0:
        if (z + y * 0.6) % 3.0 < 1.4:
            return tone(p["orange"] if y < 12.0 else p["yellow"], face), None
        return tone(p["red"], face), None
    return tone(p["tyre"], face), None


def build():
    m = Model("rebellimon")
    top = m.bone("rebellimon", None, (0, 0, 0))
    wb = m.bone("wheel", top, (0, 12, 0))
    for i in range(18):                                                                  # huge single wheel
        ang = 2 * math.pi * i / 18
        y, z = 12.0 + 11.0 * math.sin(ang), 11.0 * math.cos(ang)
        m.box(wb, -3.0, y - 2.2, z - 2.2, 3.0, y + 2.2, z + 2.2, wheelf)
    m.round_box(wb, 0, 0, 2.6, 7.0, 6.0, 18.0, wheelf, cut=2)
    m.round_box(wb, 0, 0, 3.2, 1.6, 10.6, 13.4, STEEL, cut=0)
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats = {"skin": HIDE, "hand": RUST, "finger": RUST}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.95, leg_bulk=0.8, name="rider")
    m.boxes[:] = m.boxes[:i_box] + [b for b in m.boxes[i_box:] if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = m.bones[:i_bone] + [b for b in m.bones[i_bone:] if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.6, 3.0, 54.0, 60.0, HIDE, cut=1)
    m.round_box(hd, 0, -3.0, 2.4, 0.8, 54.0, 58.6, solid(P, "bone"), cut=0)                # skull mask
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.6, 56.6, -3.9, sx * 1.2 + 0.6, 57.6, -3.7, solid(P, "black"))
        spike(m, hd, (sx * 2.6, 58.0, 0), (sx * 1, 0.4, 0), 1.2, 6.0, STEEL, tip=0.8)       # bull horns
        rod(m, hd, (sx * 2.0, 55.0, -2.0), (sx * 4.0, 50.0, 2.0), 1, STEEL, extend=0.2)   # hoses
    for j in range(7):                                                                   # blazing mohawk
        spike(m, hd, (0, 59.6, -2.0 + j * 0.9), (0, 1, 0.3 + j * 0.06), 1.2, 4.0 + (3 - abs(j - 3)) * 1.4,
              strands(P, "orange", "yellow"), tip=0.8)
    w = a["arm_left"]["wrist"]                                                           # saw-blade launcher
    m.box(a["arm_left"]["bone"], w[0] - 2.0, w[1] - 4.0, w[2] - 4.0, w[0] + 3.0, w[1] + 8.0, w[2] + 4.0, hazardf)
    for i in range(12):
        ang = 2 * math.pi * i / 12
        spike(m, a["arm_left"]["bone"], (w[0] + 0.5, w[1] + 12.0 + 5.0 * math.sin(ang), w[2] + 5.0 * math.cos(ang)),
              (0, math.sin(ang), math.cos(ang)), 1.0, 2.4, RUST, tip=0.8)
    m.round_box(a["arm_left"]["bone"], w[0] + 0.5, w[2], 1.0, 5.0, w[1] + 7.0, w[1] + 17.0, RUST, cut=0)
    h = a["arm_right"]["hand"]                                                           # spiked gauntlet
    ball(m, a["arm_right"]["bone"], h, 3.4, RUST, layers=3)
    for j in range(5):
        ang = 2 * math.pi * j / 5
        spike(m, a["arm_right"]["bone"], (h[0] + 3.0 * math.cos(ang), h[1] + 3.0 * math.sin(ang), h[2]),
              (math.cos(ang), math.sin(ang), 0), 1.0, 2.6, STEEL, tip=0.8)
    mount(m, i_box, i_bone, -8.0, 0.0, top)
    return m
