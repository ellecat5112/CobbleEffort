"""Atratusmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a dark swan-knight. Black armour with red seams and a bird-skull helm under a spray of blond
hair, long black feathered arms, steel-tipped talons, and great wings of glowing magenta feathers with two
translucent pink crystal shields hovering beside it. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, feathers, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a dark swan-knight: black armour with red seams, a bird-skull helm under blond hair, steel talons, great wings "
        "of glowing magenta feathers and two translucent pink crystal shields")
BASE = {"black": (36, 34, 44), "black_dark": (12, 12, 16), "black_light": (100, 98, 120), "red": (210, 30, 50),
        "hair": (240, 220, 120), "hair_dark": (180, 150, 60), "steel": (200, 204, 216), "steel_dark": (100, 104, 116),
        "pink": (240, 80, 210), "pink_dark": (170, 30, 150), "crystal": (250, 170, 240, 140),
        "crystal_rim": (255, 220, 250, 200), "eye": (255, 60, 80)}
SHINY = {"black": (230, 230, 240), "black_dark": (160, 160, 176), "black_light": (255, 255, 255),
         "pink": (90, 200, 255), "pink_dark": (30, 120, 220), "crystal": (170, 230, 255, 140)}


def P(v):
    return pal(BASE, SHINY, v)


BLACK = armour(P, "black", "black_dark", light="black_light", trim="red", trim_w=0.3)
BLACK_PLAIN = armour(P, "black", "black_dark", light="black_light")
STEEL = metal(P, "steel", dark="steel_dark")
HAIR = strands(P, "hair", "hair_dark")


def glowfeather(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["pink_dark"] if abs(u - W / 2) < 0.25 else p["pink"]
    return c, c


def crystalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if min(u, W - u, v, H - v) < 0.5:
        return p["crystal_rim"], None
    return p["crystal"], None


def build():
    m = Model("atratusmon")
    mats = {"skin": BLACK_PLAIN, "chest": BLACK, "abs": BLACK, "pelvis": BLACK, "neck": BLACK_PLAIN, "deltoid": BLACK,
            "upper_arm": BLACK_PLAIN, "forearm": BLACK, "hand": BLACK_PLAIN, "finger": STEEL, "claw": STEEL,
            "thigh": BLACK, "knee": BLACK, "shin": BLACK, "calf": BLACK_PLAIN, "foot": BLACK, "talon": STEEL}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="atratusmon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 2.8, 54.6, 60.4, BLACK, cut=1)
    m.box(hd, -1.0, 55.0, -7.4, 1.0, 57.6, -2.8, BLACK_PLAIN)                           # beak-like skull snout
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.6, 57.6, -3.6, sx * 1.2 + 0.6, 58.2, -3.4, solid(P, "eye", glow=True))
    hr = m.bone("mane", hd, (0, 60, 0))
    for i in range(10):                                          # blond hair spray
        ang = math.radians(-70 + i * 15)
        rod(m, hr, (1.6 * math.sin(ang), 60.0, 0.5), (6.0 * math.sin(ang), 66.0 + 2.0 * math.cos(ang), 4.0), 2, HAIR,
            extend=0.3, t2=1)
    shell(m, bd, (0, 0, 0.6), 5.0, 42.0, 51.0, -85, 85, 9, 1.2, BLACK)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.2, 50.0, 0.3), 3.8, 3.4, BLACK, layers=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # glowing magenta wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        for i in range(12):
            t = i / 11
            ang = math.radians(60 - 90 * t)
            ln = 18.0 + 10.0 * math.sin(math.pi * t)
            base = (sx * 3.0, 49.0, 3.0 + i * 0.3)
            x0, x1 = sorted((base[0], base[0] + sx * ln))
            m.box(wb, x0, base[1] - 1.2, base[2], x1, base[1] + 1.2, base[2], glowfeather,
                  rotation=(0, sx * 10, sx * math.degrees(ang)), pivot=base)
    for sx in (-1, 1):                                           # translucent crystal shields hovering
        sb = m.bone(f"shield_{'left' if sx > 0 else 'right'}", bd, (sx * 16.0, 40.0, -4.0))
        m.box(sb, sx * 16.0 - 4.0, 32.0, -4.0, sx * 16.0 + 4.0, 46.0, -2.0, crystalf, rotation=(0, sx * 30, 0),
              pivot=(sx * 16.0, 40.0, -3.0))
    return m
