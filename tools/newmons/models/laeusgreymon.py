"""Laeus Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the berserk winged dragon: a lean crimson dragon streaked with black and glowing blue scars, a
dark grey horned skull-helm with a fanged maw, great tattered crimson bat wings, curved talons, spines down its back
and a long tail ending in a black spiked mace with a glowing orange core. 35 blocks tall.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, theropod
from _digidetail import cutout, gem, local, metal, noise2, scales, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean crimson dragon with glowing blue scars, a dark horned skull-helm, tattered crimson bat wings and a spiked mace tail"
BASE = {"red": (190, 40, 50), "red_dark": (100, 10, 20), "red_light": (240, 120, 120), "grey": (70, 70, 80),
        "grey_dark": (30, 30, 36), "blue": (90, 200, 255), "membrane": (200, 120, 110), "membrane_dark": (120, 60, 60),
        "claw": (240, 230, 210), "mouth": (160, 30, 40), "tooth": (250, 248, 236), "eye": (250, 220, 60),
        "core": (255, 140, 40), "core_light": (255, 230, 160)}
SHINY = {"red": (60, 60, 70), "red_dark": (20, 20, 26), "red_light": (140, 140, 160), "membrane": (130, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north") and abs(math.sin(y * 0.8 + z * 0.5)) > 0.97:
        return tone(p["blue"], face), p["blue"]
    if abs(math.sin(y * 0.5 - z * 0.7)) > 0.95:
        return tone(p["grey_dark"], face), None
    return scales(P, "red", "red_dark", size=1.2, light="red_light")(x, y, z, face, variant, box=box, **k)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.14 * abs(math.sin(u * 0.8)) + 0.06 * noise2(u, 0.0, 2)


def build():
    m = Model("laeusgreymon")
    HELM = metal(P, "grey", dark="grey_dark")
    mats = {"skin": hidef, "belly": hidef, "neck": hidef, "head": HELM, "snout": HELM, "jaw": HELM,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": hidef, "hand": hidef, "claw": solid(P, "claw"),
            "thigh": hidef, "shin": hidef, "foot": hidef, "talon": solid(P, "claw"), "tail": hidef, "tail_tip": hidef}
    a = theropod(m, mats, "laeusgreymon", hip_y=18.0, chest=(0, 28.0, -4.0), body_r=5.0, chest_r=5.4,
                 neck_top=(0, 34.0, -10.0), head_len=10.0, head_w=3.4, head_h=3.8, mouth_open=26, teeth=6, arm_len=10.0,
                 arm_bulk=1.0, leg_bulk=1.2, stance=4.6,
                 tail=((0, 16, 8), (0, 12, 16), (2, 9, 24), (4, 8, 32)), tail_r=(3.0, 2.2, 1.6, 1.2))
    hd, bd = a["head"], a["body"]
    st = a["skull_top"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.6, st - 0.6, -10.0), (sx * 0.8, 0.4, 0.8), 1.4, 5.0, HELM, tip=0.8)       # swept horns
    for i in range(8):                                                              # back spines
        spike(m, bd, (0, 26.0 - i * 1.2, -4.0 + i * 2.6), (0, 1, 0.5), 1.2, 3.0, HELM, tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 30.0, 0.0))
        bat_wing(m, wb, (side * 3.0, 30.0, 0.0), 28.0, 22.0, 4, hidef, cutout(tatter, scales(P, "membrane", "membrane_dark")),
                 side=side, sweep=25)
    tp = a["tail_pts"][-1]                                                           # spiked mace tail
    m.round_box(a["tail"], tp[0], tp[2] + 1.0, 2.4, 2.4, tp[1] - 2.0, tp[1] + 2.0, gem(P, "core", "core_light"), cut=1)
    for j in range(6):
        ang = 2 * math.pi * j / 6
        spike(m, a["tail"], (tp[0] + 2.0 * math.cos(ang), tp[1] + 2.0 * math.sin(ang), tp[2] + 1.0),
              (math.cos(ang), math.sin(ang), 0.2), 1.0, 2.6, HELM, tip=0.8)
    spike(m, a["tail"], (tp[0], tp[1], tp[2] + 3.0), (0.2, -0.2, 1), 1.4, 5.0, HELM, tip=0.8)
    return m
