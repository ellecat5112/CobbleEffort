"""Oboromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the phantom samurai: a skeletal warrior in tattered red armour and a conical straw hat with a
horn, a grinning skull face bound with talismans, an arrow stuck through it, bony arms, a long katana, and below the
waist a great blue ghost-skull of spirit fire trailing violet flame. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a skeletal phantom samurai in tattered red armour and a horned straw hat, a grinning skull bound with "
        "talismans, a long katana and a great blue ghost-skull of spirit fire below its waist")
BASE = {"bone": (220, 218, 226), "bone_dark": (140, 136, 150), "red": (190, 40, 40), "red_dark": (100, 14, 14),
        "straw": (200, 170, 110), "straw_dark": (140, 110, 60), "talisman": (240, 220, 140), "blue": (110, 190, 255),
        "blue_dark": (40, 100, 200), "violet": (170, 110, 250, 200), "violet_core": (230, 210, 255, 230),
        "steel": (220, 224, 236), "steel_dark": (110, 114, 126), "eye": (250, 250, 160), "black": (24, 22, 28)}
SHINY = {"blue": (120, 255, 160), "blue_dark": (40, 160, 80), "violet": (255, 140, 120, 200), "red": (60, 60, 70)}


def P(v):
    return pal(BASE, SHINY, v)


BONE = armour(P, "bone", "bone_dark")
RED = armour(P, "red", "red_dark", trim="black", trim_w=0.3)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["violet_core"] if v / max(H, 1e-6) < 0.3 else p["violet"]
    return c, c[:3]


def skullf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and ((abs(abs(x) - 3.4) < 1.6 and abs(y - 22.0) < 1.6) or (abs(x) < 3.0 and abs(y - 15.0) < 0.6)):
        return tone(p["blue_dark"], face), None
    return p["blue"], p["blue"]


def build():
    m = Model("oboromon")
    mats = {"skin": BONE, "chest": RED, "abs": BONE, "pelvis": RED, "neck": BONE, "deltoid": RED, "upper_arm": BONE,
            "forearm": RED, "hand": BONE, "finger": BONE}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.75, leg_bulk=0.8, name="oboromon")
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]          # a ghost-skull below
    m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
    bd = a["body"]
    ball(m, bd, (0, 20.0, -1.0), 8.0, skullf, layers=6, ry=8.0)
    for i in range(6):                                                                   # trailing violet flame
        ang = math.radians(-150 + i * 60)
        c = (7.0 * math.cos(ang), 12.0, 5.0 + 4.0 * math.sin(ang))
        for rot in (0, 90):
            m.box(bd, c[0] - 2.0, c[1] - 8.0, c[2], c[0] + 2.0, c[1], c[2], cutout(flame_inside(3, 0.1, i), firef),
                  rotation=(180, rot, 0), pivot=(c[0], c[1] - 4.0, c[2]))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.4, BONE, cut=1)                           # grinning skull
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 56.8, -2.9, max(sx * 0.6, sx * 1.8), 58.0, -2.8, solid(P, "black"))
        m.box(hd, min(sx * 1.0, sx * 1.4), 57.2, -2.95, max(sx * 1.0, sx * 1.4), 57.6, -2.9, solid(P, "eye", glow=True))
    for j in range(5):
        m.box(hd, -1.8 + j * 0.8, 54.6, -2.9, -1.4 + j * 0.8, 55.6, -2.8, solid(P, "bone"))
    m.box(hd, 1.0, 54.0, -2.95, 2.4, 59.0, -2.85, solid(P, "talisman"))                   # talisman
    m.round_box(hd, 0, 0, 6.0, 6.0, 59.4, 60.4, fabric(P, "straw", "straw_dark"), cut=2)  # conical straw hat
    m.round_box(hd, 0, 0, 3.6, 3.6, 60.4, 62.0, fabric(P, "straw", "straw_dark"), cut=1)
    spike(m, hd, (0, 62.0, 0), (0, 1, 0), 2.0, 4.0, BONE, tip=0.8)
    rod(m, bd, (-6.0, 50.0, 6.0), (6.0, 46.0, -6.0), 1, solid(P, "straw_dark"), extend=0.2)   # arrow through it
    ar = a["arm_right"]                                                                  # long katana
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1] + 2.0, h[2]), (h[0] + 3.0, h[1] - 28.0, h[2] - 8.0), 1,
        metal(P, "steel", dark="steel_dark"), extend=0.2, t2=2)
    for j in range(4):                                                                   # tattered red cloth
        m.box(bd, -5.0 + j * 2.6, 34.0, 3.6, -3.0 + j * 2.6, 48.0, 3.8, fabric(P, "red", "red_dark"),
              rotation=(10, 0, -10 + j * 6), pivot=(-4.0 + j * 2.6, 48.0, 3.7))
    return m
