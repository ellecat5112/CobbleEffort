"""Pumpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a jack-o'-lantern head with glowing yellow eyes and a jagged grin, an axe buried in its crown, a
ragged green scarf and leafy collar streaming behind, on a lumpy white stitched cloth-doll body with stubby arms
and legs. 25 blocks.

Front is -z, y is up. 36 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, fabric, local, metal, noise2, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a jack-o'-lantern head with glowing eyes and an axe in its crown, a ragged green scarf, on a white stitched cloth-doll body"
BASE = {"pumpkin": (240, 140, 30), "pumpkin_dark": (180, 80, 10), "glow": (250, 220, 60), "cloth": (246, 244, 236),
        "cloth_dark": (190, 186, 170), "stitch": (130, 90, 50), "green": (80, 150, 60), "green_dark": (30, 90, 30),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 126), "wood": (150, 110, 70), "stem": (90, 120, 40)}
SHINY = {"pumpkin": (150, 90, 200), "pumpkin_dark": (90, 40, 140), "glow": (120, 250, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def pumpf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 2.4) < 1.2 - (y - 26.0) * 0.5 and 25.0 < y < 27.4:
                return p["glow"], p["glow"]
        if 21.0 < y < 23.4 and abs(x) < 4.0 and (y - 21.0) < 1.2 + 0.8 * abs(math.sin(x * 1.6)):
            return p["glow"], p["glow"]
    if face != "up" and abs(math.sin(math.atan2(z, x) * 5)) > 0.94:
        return tone(p["pumpkin_dark"], face), None
    return skin(P, "pumpkin", dark="pumpkin_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def clothf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y % 5.0) - 2.5) < 0.12 or abs(((x + z) % 6.0) - 3.0) < 0.12:
        if int((x + y + z) * 3) % 2:
            return tone(p["stitch"], face), None
    return fabric(P, "cloth", "cloth_dark", axis="y", period=2.0)(x, y, z, face, variant, box=box, **k)


def raggedf(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    f = (box.lo[0] + u) * 1.1
    return v / max(H, 1e-6) > 0.2 * noise2(f, 7) + 0.2 * abs(math.sin(f * 1.7))


def build():
    m = Model("pumpmon")
    top = m.bone("pumpmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0.6), 6.6, clothf, layers=5, ry=6.4)
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 25.0, -0.4), 7.4, pumpf, layers=6, ry=6.6)
    rod(m, hd, (0, 31.0, 0), (0.6, 33.0, 0.4), 2, solid(P, "stem"), extend=0.2)
    m.box(hd, -4.0, 30.0, -0.4, 1.0, 34.0, 0.4, metal(P, "steel", dark="steel_dark"),
          rotation=(0, 0, -20), pivot=(-1.0, 31.0, 0))                                    # the axe
    rod(m, hd, (0, 33.0, 0), (4.0, 36.0, 0.4), 1, solid(P, "wood"), extend=0.2)
    m.round_box(bd, 0, 0, 6.4, 6.0, 17.0, 19.0, fabric(P, "green", "green_dark", axis="x"), cut=2)   # scarf
    for j in range(6):                                                                   # ragged leaf collar
        x0 = -7.0 + j * 2.4
        m.box(bd, x0, 10.0, 6.0, x0 + 3.0, 19.0, 6.0, cutout(raggedf, fabric(P, "green", "green_dark", axis="y")),
              rotation=(30 + j * 4, 0, (j - 2.5) * 8), pivot=(x0 + 1.5, 19.0, 6.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 14.0, 0))
        rod(m, ab, (sx * 6.0, 14.0, 0), (sx * 10.0, 9.0, -2.0), 3, clothf, extend=0.4)
        ball(m, ab, (sx * 10.4, 8.4, -2.4), 2.0, clothf, layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 6.0, 0))
        m.round_box(lg, sx * 3.0, -0.4, 2.4, 2.8, 0.0, 6.6, clothf, cut=1)
    return m
