"""Angoramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a plump angora rabbit. Fluffy tan fur with a pale pink belly, a shaggy cream mane and beard round its
small face, long ears with green-banded tips, big brown paw pads, a strap across its shoulder and stubby feet.
1 block tall.

Front is -z, y is up. 34 units tall (the ears); Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, leather, local, plane, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(1.0, HEIGHT, 0.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 18}
LOOK = ("a plump angora rabbit: fluffy tan fur, a pale pink belly, a shaggy cream mane and beard, long ears with green "
        "tips, big brown paw pads and a shoulder strap")
BASE = {"tan": (226, 200, 150), "tan_dark": (170, 140, 90), "tan_light": (246, 230, 190), "cream": (246, 236, 200),
        "cream_dark": (210, 190, 140), "pink": (246, 210, 226), "pink_dark": (220, 170, 196), "green": (90, 170, 80),
        "green_dark": (40, 110, 40), "pad": (120, 80, 60), "pad_dark": (70, 44, 30), "strap": (60, 50, 50),
        "eye": (30, 24, 24), "nose": (120, 70, 60)}
SHINY = {"tan": (200, 200, 214), "tan_dark": (140, 140, 160), "tan_light": (236, 236, 246), "green": (200, 80, 140),
         "green_dark": (140, 30, 90)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "tan", "tan_dark", tip="tan_light", length=1.0)
MANE = fur(P, "cream", "cream_dark", length=1.2)
PAD = skin(P, "pad", dark="pad_dark", var=0.03)


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and ((x / 5.4) ** 2 + ((y - 11.0) / 6.0) ** 2) < 1:
        return tone(p["pink"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.5) < 0.45 and abs(y - 22.0) < 0.3:
                return p["eye"], None                            # sleepy closed eyes
        if abs(x) < 0.6 and abs(y - 20.8) < 0.4:
            return p["nose"], None
    return MANE(x, y, z, face, variant, box=box, **k)


def earf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
    if t > 0.6:
        u, v, W, H = local(x, y, z, face, box)
        stripe = abs(((u / max(W, 1e-6)) - 0.5) - (t - 0.8) * 0.8) < 0.12
        return tone(p["green_dark"] if stripe else p["green"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("angoramon")
    top = m.bone("angoramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 12.0, 0), 7.6, bellyf, layers=7, ry=8.0)
    hd = m.bone("head", bd, (0, 19, -1))
    ball(m, hd, (0, 21.0, -1.0), 4.4, facef, layers=5)
    for i in range(10):                                          # shaggy mane and beard
        ang = math.radians(-150 + i * 33)
        spike(m, hd, (3.6 * math.sin(ang), 20.0 + 1.6 * math.cos(ang), -1.0 - 3.6 * math.cos(ang) * 0.8),
              (math.sin(ang), -0.4, -0.5 * math.cos(ang)), 2.0, 2.8, MANE, tip=1.0)
    m.box(hd, -1.6, 15.6, -5.6, 1.6, 19.0, -4.0, MANE)                                   # the beard
    for sx in (-1, 1):                                           # long ears bent outward
        ear = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 2.0, 24.5, 0))
        rod(m, ear, (sx * 2.0, 24.5, 0), (sx * 5.0, 30.0, 0.6), 3, earf, extend=0.3, t2=2)
        rod(m, ear, (sx * 5.0, 30.0, 0.6), (sx * 11.0, 33.0, 1.0), 4, earf, extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # arms with big paw pads
        ab = m.bone(nm, bd, (sx * 6.6, 14.0, 0))
        hand = (sx * 9.6, 11.0, -3.0)
        rod(m, ab, (sx * 6.6, 14.0, 0), hand, 3, FUR, extend=0.4)
        m.round_box(ab, hand[0], hand[2], 2.2, 2.0, hand[1] - 2.0, hand[1] + 1.6, FUR, cut=1)
        m.box(ab, hand[0] - 1.6, hand[1] - 1.6, hand[2] - 2.2, hand[0] + 1.6, hand[1] + 1.2, hand[2] - 1.8, PAD)
    rod(m, bd, (6.0, 18.0, -4.6), (-6.0, 7.0, -6.0), 1, leather(P, "strap", "strap"), extend=0.2, t2=1)  # strap
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 5.0, 0))
        m.round_box(lg, sx * 3.6, -0.6, 2.4, 3.0, 0.0, 5.0, FUR, cut=1)
        m.box(lg, sx * 3.6 - 1.6, 0.4, -3.8, sx * 3.6 + 1.6, 3.0, -3.4, PAD)
    return m
