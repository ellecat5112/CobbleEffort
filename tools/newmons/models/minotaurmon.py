"""Minotaurmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the labyrinth's bull-man: a hulking brown bull-headed brute with great curved steel-grey horns,
a shaggy brown mane, a gold ring through its nose, stitched hide, huge clawed hands, green boots, and its left arm
ending in a massive steel piston drill. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fur, leather, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hulking brown bull-headed brute with curved steel horns, a shaggy mane, a gold nose ring, stitched hide, "
        "green boots and a massive steel piston-drill arm")
BASE = {"brown": (170, 100, 50), "brown_dark": (100, 54, 24), "brown_light": (220, 160, 110), "horn": (170, 174, 186),
        "horn_dark": (80, 84, 96), "gold": (240, 200, 70), "boot": (80, 110, 60), "boot_dark": (40, 60, 30),
        "steel": (200, 204, 214), "steel_dark": (100, 104, 116), "eye": (230, 40, 30), "stitch": (50, 30, 20),
        "mouth": (120, 30, 30), "claw": (240, 230, 210)}
SHINY = {"brown": (70, 70, 80), "brown_dark": (30, 30, 36), "brown_light": (140, 140, 150)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN0 = skin(P, "brown", dark="brown_dark", light="brown_light")


def skinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs((x * 0.8 + y * 0.3) % 6.0 - 3.0) < 0.12 and (int(y) % 3 == 0):
        return tone(p["stitch"], face), None
    return SKIN0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("minotaurmon")
    mats = {"skin": skinf, "claw": solid(P, "claw"), "shin": armour(P, "boot", "boot_dark"),
            "calf": armour(P, "boot", "boot_dark"), "foot": armour(P, "boot", "boot_dark"),
            "toe": armour(P, "boot", "boot_dark"), "pelvis": leather(P, "brown_dark", "brown_dark")}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.45, leg_bulk=1.3, claws=True, hand_pose="fist", name="minotaurmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 3.4, 3.4, 53.0, 60.0, skinf, cut=1)                            # bull head
    m.round_box(hd, 0, -5.4, 2.6, 1.8, 52.6, 56.4, SKIN0, cut=1)                            # muzzle
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 2.6), 57.6, -5.1, max(sx * 1.2, sx * 2.6), 58.4, -4.9, solid(P, "eye", glow=True))
        pts = [(sx * 3.0, 59.0, -1.0), (sx * 7.0, 61.0, -1.0), (sx * 9.0, 65.0, -2.0), (sx * 8.0, 68.0, -3.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # great curved horns
            rod(m, hd, p0, p1, 3 - j, metal(P, "horn", dark="horn_dark"), extend=0.3)
    for i in range(6):                                                                   # gold nose ring
        ang = 2 * math.pi * i / 6
        m.box(hd, 1.4 * math.cos(ang) - 0.35, 52.6 + 1.4 * math.sin(ang) - 0.35, -7.4, 1.4 * math.cos(ang) + 0.35,
              52.6 + 1.4 * math.sin(ang) + 0.35, -7.0, solid(P, "gold"))
    for i in range(8):                                                                   # shaggy mane
        spike(m, hd, ((i - 3.5) * 0.9, 60.0, 0.0), ((i - 3.5) * 0.2, 1, 0.6), 1.6, 5.0, strands(P, "brown_dark", "stitch"),
              tip=0.8)
    al = a["arm_left"]                                                                   # piston drill arm
    w = al["wrist"]
    m.round_box(al["bone"], w[0], w[2] - 1.0, 4.0, 4.0, w[1] - 6.0, w[1] + 2.0, metal(P, "steel", dark="steel_dark"),
                cut=1)
    for sx in (-1, 1):
        rod(m, al["bone"], (w[0] + sx * 3.0, w[1] + 2.0, w[2] - 1.0), (w[0] + sx * 3.0, w[1] - 6.0, w[2] - 1.0), 1,
            metal(P, "steel_dark"), extend=0.2)
    spike(m, al["bone"], (w[0], w[1] - 6.0, w[2] - 1.0), (0, -1, 0), 5.0, 7.0, metal(P, "steel", dark="steel_dark"),
          tip=0.8)
    return m
