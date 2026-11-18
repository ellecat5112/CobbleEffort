"""Kaiser Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Hybrid of flame united: a towering dragon warrior in crimson-and-gold armour, a
dragon-headed helm with a gold crest and a blue visor, great dragon-head pauldrons with gaping jaws, a flowing red
tabard, clawed gauntlets and greaves, and the giant flaming sword Ryuuko Souzanken held high. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering dragon warrior in crimson-and-gold armour with a dragon helm, dragon-head pauldrons, a red tabard and "
        "a giant flaming sword")
BASE = {"red": (200, 30, 30), "red_dark": (110, 10, 12), "red_light": (250, 120, 100), "gold": (250, 200, 60),
        "gold_dark": (170, 120, 20), "gold_light": (255, 240, 170), "blue": (60, 120, 220), "black": (30, 28, 34),
        "eye": (250, 220, 60), "tooth": (250, 248, 236), "blade": (230, 236, 246), "blade_dark": (120, 130, 150),
        "fire": (255, 170, 40, 210), "fire_core": (255, 245, 190, 240)}
SHINY = {"red": (40, 40, 50), "red_dark": (14, 14, 20), "red_light": (110, 110, 130), "fire": (120, 190, 255, 210)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="gold", trim_w=0.3, rivets=True)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def dragon_head(m, bone, c, sx, s=1.0):
    x, y, z = c
    m.round_box(bone, x, z - 2.0 * s, 3.0 * s, 4.4 * s, y - 2.0 * s, y + 2.4 * s, RED, cut=1)
    m.round_box(bone, x, z - 3.0 * s, 2.6 * s, 3.4 * s, y - 4.0 * s, y - 2.4 * s, RED, cut=1)          # jaw
    for j in range(3):
        spike(m, bone, (x + (j - 1) * 1.2 * s, y - 2.2 * s, z - 6.0 * s), (0, -1, 0), 0.8, 1.6 * s, solid(P, "tooth"), tip=0.8)
    m.box(bone, min(x + sx * 2.8 * s, x + sx * 3.2 * s), y + 0.6 * s, z - 4.0 * s, max(x + sx * 2.8 * s, x + sx * 3.2 * s),
          y + 1.6 * s, z - 2.6 * s, solid(P, "eye", glow=True))
    spike(m, bone, (x, y + 2.0 * s, z), (sx * 0.3, 0.6, 1), 1.4, 5.0 * s, GOLD, tip=0.8)


def build():
    m = Model("kaisergreymon")
    mats = {"skin": RED, "chest": RED, "abs": RED, "pelvis": RED, "neck": GOLD, "deltoid": RED, "upper_arm": RED,
            "forearm": RED, "hand": RED, "finger": GOLD, "claw": GOLD, "thigh": RED, "knee": GOLD, "shin": RED,
            "calf": RED, "foot": RED, "talon": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.2, leg_bulk=1.2, claws=True, talons=True, digitigrade=True,
                 name="kaisergreymon")
    bd = a["body"]
    m.round_box(bd, 0, -4.4, 2.4, 0.6, 44.0, 48.0, GOLD, cut=0)
    for sx in (-1, 1):                                                               # flowing tabard flaps
        m.round_box(bd, sx * 2.0, -3.6, 1.8, 0.6, 18.0, 32.0, fabric(P, "red", "red_dark"), cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.2, 54.0, 60.6, RED, cut=1)
    m.round_box(hd, 0, -4.0, 1.8, 1.8, 54.4, 57.4, RED, cut=1)                        # dragon snout helm
    m.round_box(hd, 0, -3.4, 2.2, 0.3, 57.4, 58.4, solid(P, "blue", glow=True), cut=0)
    for j in range(5):                                                               # gold crest
        spike(m, hd, (0, 60.4, -2.0 + j * 1.0), (0, 1, 0.4 + j * 0.2), 1.4, 6.0 - j * 0.6, GOLD, tip=0.8)
    for sx in (-1, 1):                                                               # dragon-head pauldrons
        pb = a["arm_left" if sx > 0 else "arm_right"]["bone"]
        dragon_head(m, pb, (sx * 9.0, 51.0, -1.0), sx, 1.2)
    hr = a["arm_right"]                                                              # giant flaming sword held high
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx, hz, 1.0, 1.0, hy - 2.0, hy + 3.0, GOLD, cut=0)
    m.round_box(hr["bone"], hx, hz, 4.0, 1.6, hy + 3.0, hy + 4.6, GOLD, cut=0)
    m.round_box(hr["bone"], hx, hz, 2.0, 0.6, hy + 4.6, hy + 40.0, metal(P, "blade", dark="blade_dark"), cut=0)
    spike(m, hr["bone"], (hx, hy + 40.0, hz), (0, 1, 0), 2.4, 4.0, metal(P, "blade", dark="blade_dark"), tip=0.8)
    for j in range(3):
        for ang in (0, 90):
            m.box(hr["bone"], hx - 3.0, hy + 8.0 + j * 10.0, hz, hx + 3.0, hy + 16.0 + j * 10.0, hz,
                  cutout(flame_inside(4, 0.1, j), firef), rotation=(0, ang, 0), pivot=(hx, hy + 8.0 + j * 10.0, hz))
    tb = m.bone("tail", bd, (0, 32, 3))
    rod(m, tb, (0, 32.0, 3.0), (0, 22.0, 14.0), 3, RED, extend=0.6)
    rod(m, tb, (0, 22.0, 14.0), (0, 14.0, 22.0), 2, RED, extend=0.4)
    return m
