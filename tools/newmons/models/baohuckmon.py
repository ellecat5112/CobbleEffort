"""Bao Huckmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a white armoured dragon-knight on the prowl. A sleek white-and-silver armoured body crouched low
on clawed limbs, a narrow fanged dragon head with red-fringed crests, a great tattered crimson cape-mane streaming
from its neck and back, burning gold thrusters at its shoulders and a long armoured tail with a red-edged blade tip.
15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digibody import cape
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a white armoured dragon-knight crouched on clawed limbs: a narrow fanged dragon head with red crests, a "
        "tattered crimson cape-mane, burning gold thrusters and a long tail with a red-edged blade tip")
BASE = {"white": (240, 242, 248), "white_dark": (170, 174, 190), "silver": (200, 204, 216), "silver_dark": (100, 104, 116),
        "red": (200, 30, 40), "red_dark": (110, 10, 20), "gold": (240, 200, 60), "flame": (255, 170, 50, 220),
        "flame_core": (255, 240, 160, 235), "mouth": (100, 14, 24), "tooth": (250, 250, 246), "tongue": (200, 60, 80),
        "eye": (255, 60, 60)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "red": (240, 180, 40), "red_dark": (170, 110, 16)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="silver", trim_w=0.4)
SILVER = metal(P, "silver", dark="silver_dark")
CAPE = fabric(P, "red", "red_dark", axis="y", period=2.6)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.16 * abs(math.sin((box.lo[0] + u) * 2.3)) + 0.04


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
    return c, c[:3]


def build():
    m = Model("baohuckmon")
    mats = {"skin": WHITE, "belly": SILVER, "neck": WHITE, "head": WHITE, "snout": WHITE, "jaw": SILVER,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": WHITE, "leg_lower": SILVER,
            "paw": WHITE, "claw": SILVER, "tail": WHITE}
    a = quadruped(m, mats, "baohuckmon", length=24.0, body_y=16.0, body_rx=5.6, body_ry=5.6, chest_bulk=1.25,
                  neck=((0, 22, -13), (0, 25, -17)), head_len=11.0, head_w=3.6, head_h=4.0, snout=0.7,
                  mouth_open=18, teeth=5, leg_bulk=1.3, toes=3,
                  tail=((0, 20, 16), (0, 22, 24), (0, 20, 32), (0, 16, 38)), tail_r=(2.0, 1.6, 1.2, 0.9))
    hd = a["head"]
    for sx in (-1, 1):
        m.box(hd, sx * 2.0 - 0.6, 27.0, -22.2, sx * 2.0 + 0.6, 27.8, -22.0, solid(P, "eye", glow=True))
        for j in range(3):
            spike(m, hd, (sx * 2.6, 28.0 - j * 1.4, -18.0 + j * 2.0), (sx * 0.5, 0.5, 1), 1.0, 4.0 - j,
                  solid(P, "red"))
    bd = a["body"]
    cb = m.bone("cap", bd, (0, 24, -10))                         # the crimson cape-mane
    cape(m, cb, 27.0, 18.0, 30.0, cutout(torn, CAPE), z=-6.0, flare=1.2, panels=8, sweep=(0, 55))
    for sx in (-1, 1):                                           # gold thrusters with flames
        m.round_box(bd, sx * 6.0, -6.0, 1.6, 1.6, 20.0, 25.0, metal(P, "gold", dark="red_dark"), cut=1)
        m.box(bd, sx * 6.0 - 2.0, 24.0, -6.0, sx * 6.0 + 2.0, 34.0, -6.0, cutout(flame_inside(3, 0.0, 2), flamef),
              rotation=(30, 0, 0), pivot=(sx * 6.0, 24.0, -6.0))
    tl = a["tail"]
    e = a["tail_pts"][-1]
    m.box(tl, e[0] - 0.3, e[1] - 6.0, e[2] - 1.0, e[0] + 0.3, e[1] + 1.0, e[2] + 3.0, solid(P, "red"))
    return m
