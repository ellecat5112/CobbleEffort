"""Necromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the lord of the dead: a towering skeletal king of icy blue spirit-flame in a black-and-violet robe
trimmed gold with red runic stoles, a crown of blue candle-flames on a horned headdress, a great anchor-hilted sword
planted before it, and pale ghosts swirling about its arms. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a towering skeletal king of icy blue spirit-flame in a black-and-violet robe with red runic stoles, a crown of "
        "blue candle-flames, a great planted sword and swirling ghosts")
BASE = {"spirit": (130, 200, 255), "spirit_dark": (40, 100, 200), "robe": (50, 40, 80), "robe_dark": (20, 14, 34),
        "gold": (230, 190, 70), "red": (190, 30, 40), "bone": (220, 230, 245), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 108), "flame": (110, 170, 255, 210), "flame_core": (230, 245, 255, 235),
        "ghost": (210, 236, 255, 160), "eye": (250, 250, 160)}
SHINY = {"spirit": (150, 255, 170), "spirit_dark": (40, 160, 80), "flame": (120, 255, 150, 210),
         "flame_core": (230, 255, 235, 235), "robe": (90, 30, 30), "robe_dark": (40, 10, 10)}


def P(v):
    return pal(BASE, SHINY, v)


ROBE = fabric(P, "robe", "robe_dark", seam="gold")


def spiritf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["spirit"] if (y * 0.8 + x * 0.3) % 2.6 > 0.7 else p["spirit_dark"]
    return c, c


def stolef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs((y % 4.0) - 2.0) < 0.5:
        return tone(p["gold"], face), None
    return tone(p["red"], face), None


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.35 else p["flame"]
    return c, c[:3]


def build():
    m = Model("necromon")
    mats = {"skin": spiritf, "chest": ROBE, "abs": ROBE, "pelvis": ROBE, "neck": spiritf, "deltoid": armour(P, "gold",
            "robe_dark"), "upper_arm": ROBE, "forearm": ROBE, "hand": spiritf, "finger": spiritf}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.1, leg_bulk=1.0, name="necromon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]          # a robe to the ground
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    for j in range(6):
        r = 5.6 + j * 1.0
        m.round_box(bd, 0, 0.6, r, r * 0.8, 33.0 - (j + 1) * 5.4, 33.4 - j * 5.4, ROBE, cut=max(1, int(r * 0.3)))
    for sx in (-1, 1):                                                                   # red runic stoles
        x0, x1 = sorted((sx * 1.2, sx * 3.4))
        m.box(bd, x0, 6.0, -9.0, x1, 48.0, -8.4, stolef, rotation=(-8, 0, 0), pivot=(sx * 2.3, 48.0, -4.0))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.0, 60.0, spiritf, cut=1)                        # skull of spirit-flame
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 57.0, -3.3, max(sx * 0.6, sx * 1.8), 58.0, -3.1, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.0, 60.0, 0), (sx * 1, 0.5, 0), 1.6, 6.0, metal(P, "gold"), tip=0.8)   # horned headdress
    m.round_box(hd, 0, 0, 4.0, 3.4, 59.6, 61.0, metal(P, "gold"), cut=1)
    for i in range(7):                                                                   # crown of candle-flames
        x = (i - 3) * 1.6
        rod(m, hd, (x, 61.0, 0.6), (x, 64.0, 0.6), 1, solid(P, "bone"), extend=0.1)
        for ang in (0, 90):
            m.box(hd, x - 0.8, 64.0, 0.6, x + 0.8, 67.0, 0.6, cutout(flame_inside(2, 0.0, i), firef),
                  rotation=(0, ang, 0), pivot=(x, 64.0, 0.6))
    rod(m, bd, (0, 2.0, -12.0), (0, 44.0, -12.0), 2, metal(P, "steel", dark="steel_dark"), extend=0.4, t2=4)   # sword
    m.box(bd, -6.0, 40.0, -13.0, 6.0, 42.0, -11.0, metal(P, "gold"))
    for sx in (-1, 1):
        rod(m, bd, (0, 4.0, -12.0), (sx * 6.0, 6.0, -12.0), 2, metal(P, "steel"), extend=0.3)   # anchor flukes
    for i in range(4):                                                                   # swirling ghosts
        ang = 2 * math.pi * i / 4 + 0.4
        c = (14.0 * math.cos(ang), 34.0 + 8.0 * math.sin(ang * 2), 4.0 * math.sin(ang))
        ball(m, bd, c, 2.4, solid(P, "ghost", glow=True), layers=3)
        spike(m, bd, (c[0], c[1] - 2.0, c[2]), (0, -1, 0.3), 2.0, 4.0, solid(P, "ghost", glow=True), tip=0.8)
    return m
