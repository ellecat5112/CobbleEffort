"""Bearmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a scrappy black bear cub. Thick black fur with a pale muzzle and belly, a backwards blue cap with
"BEARS" across it, blue bandage wraps on its right paw, a belt of blue buckled straps round its middle, a pink
scratch mark on its cheek and stubby clawed feet. 1 block tall.

Front is -z, y is up. 34 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fabric, fur, leather, local, plane, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 0.9)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a scrappy black bear cub with a pale muzzle, a backwards blue cap, blue bandage wraps on its paw, blue "
        "buckled straps round its middle and a pink cheek scratch")
BASE = {"fur": (40, 40, 48), "fur_dark": (16, 16, 20), "fur_light": (110, 110, 124), "pale": (230, 226, 216),
        "blue": (60, 80, 180), "blue_dark": (24, 34, 110), "pink": (240, 100, 140), "eye": (90, 160, 240),
        "pupil": (16, 20, 30), "white": (250, 250, 250), "nose": (20, 20, 24), "claw": (230, 230, 236),
        "tooth": (250, 250, 246)}
SHINY = {"fur": (140, 90, 50), "fur_dark": (80, 46, 20), "fur_light": (200, 150, 100), "blue": (200, 50, 50),
         "blue_dark": (120, 20, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=1.0)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            c = eye(p, a - sx * 1.8, b - 24.6, 1.0, "eye")
            if c is not None:
                return c, None
        if 2.4 < a < 4.0 and 22.4 < b < 23.4 and abs(b - 22.9 - (a - 3.2) * 0.3) < 0.2:
            return p["pink"], None
    return FUR(x, y, z, face, variant, box=box, **k)


def capf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 29.6) < 0.4 and (z * 1.5) % 1.0 < 0.6:
        return p["white"], None                                  # the "BEARS" lettering, as a dashed line
    return fabric(P, "blue", "blue_dark", axis="x")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bearmon")
    top = m.bone("bearmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 12.0, 0), 6.4, FUR, layers=5, ry=6.0)
    m.box(bd, -4.0, 7.0, -6.6, 4.0, 15.0, -5.4, skin(P, "pale"))                        # pale belly
    for j in range(3):                                           # blue buckled straps
        m.round_box(bd, 0, 0, 6.6, 6.0, 9.0 + j * 2.2, 10.0 + j * 2.2, leather(P, "blue", "blue_dark", stitch="white"),
                    cut=2)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 23.0, 0), 5.4, headf, layers=5)
    m.round_box(hd, 0, -4.8, 2.4, 1.6, 19.6, 22.6, skin(P, "pale"), cut=1)              # muzzle
    m.box(hd, -0.8, 21.6, -6.6, 0.8, 22.6, -6.2, solid(P, "nose"))
    spike(m, hd, (1.0, 19.8, -6.2), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"))
    for sx in (-1, 1):
        ball(m, hd, (sx * 4.0, 27.4, 0.6), 1.6, FUR, layers=2)                          # ears
    m.round_box(hd, 0, 0.4, 5.2, 5.0, 27.0, 31.0, capf, cut=2)                          # cap
    m.box(hd, -3.0, 27.0, 5.0, 3.0, 28.0, 8.0, capf)                                    # brim backwards
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 15.0, 0))
        h = (sx * 7.6, 18.0 if sx < 0 else 10.0, -4.0)
        rod(m, ab, (sx * 6.0, 15.0, 0), h, 3, FUR, extend=0.4)
        m.round_box(ab, h[0], h[2], 2.0, 2.0, h[1] - 1.6, h[1] + 1.6, fabric(P, "blue", "blue_dark") if sx < 0
                    else FUR, cut=1)
        for f in range(3):
            spike(m, ab, (h[0] + (f - 1) * 0.8, h[1] + 1.4, h[2] - 1.4), (0, 1, -0.5), 0.6, 1.2, solid(P, "claw"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 6.0, 0))
        m.round_box(lg, sx * 3.6, -0.6, 2.4, 3.0, 0.0, 6.0, FUR, cut=1)
        for f in range(3):
            spike(m, lg, (sx * 3.6 + (f - 1) * 1.2, 0.6, -3.4), (0, -0.2, -1), 0.7, 1.2, solid(P, "claw"))
    return m
