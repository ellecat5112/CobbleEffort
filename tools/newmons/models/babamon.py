"""Babamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): an ancient grandmother of a Digimon. A small hunched figure in a green hooded coat with a zigzag
trim and a red-and-cream sash, a pale stitched face-mask with a jagged red mouth, grey hair pinned up in two buns
with a red hairpin, a string of pink prayer beads and a long broom with a straw head. 35 blocks tall.

Front is -z, y is up. 50 units tall (the broom); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, local, metal, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("an ancient grandmother: a green hooded coat with zigzag trim, a pale stitched mask with a jagged red mouth, "
        "grey hair in two buns, pink prayer beads and a long straw broom")
BASE = {"green": (110, 180, 90), "green_dark": (50, 110, 40), "cream": (240, 226, 190), "red": (200, 50, 50),
        "mask": (220, 216, 220), "mask_dark": (150, 146, 160), "hair": (180, 180, 190), "hair_dark": (110, 110, 124),
        "bead": (240, 140, 180), "wood": (170, 110, 50), "straw": (240, 200, 60), "straw_dark": (190, 140, 30),
        "mouth": (120, 20, 30), "tooth": (250, 250, 246), "eye": (30, 30, 36), "boot": (140, 100, 60)}
SHINY = {"green": (150, 100, 190), "green_dark": (90, 50, 130), "bead": (120, 220, 200), "hair": (240, 240, 250)}


def P(v):
    return pal(BASE, SHINY, v)


COAT = fabric(P, "green", "green_dark", axis="y", period=2.4)
HAIR = strands(P, "hair", "hair_dark")


def trimf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    zig = abs(((u * 0.9) % 2.0) - 1.0)
    return tone(p["red"] if v / max(H, 1e-6) < zig else p["cream"], face), None


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if abs(a) < 3.0 and 26.0 < b < 28.6:
            jag = abs(((a * 1.2) % 2) - 1) * 1.0
            return (p["tooth"] if (b < 26.0 + jag * 0.8 or b > 28.6 - jag * 0.8) else p["mouth"]), None
        for sx in (-1, 1):
            if abs(a - sx * 1.4) < 0.4 and abs(b - 30.4) < 0.3:
                return p["eye"], None
        if abs(a) < 0.2 or abs(b - 31.6) < 0.18:
            return p["mask_dark"], None                          # stitch lines
    return skin(P, "mask", dark="mask_dark", var=0.02)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("babamon")
    top = m.bone("babamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    for i in range(6):                                           # the round coat, flaring at the hem
        r = 8.0 - abs(i - 1.5) * 0.7
        m.round_box(bd, 0, 0, r, r * 0.9, 4.0 + i * 3.4, 7.6 + i * 3.4, COAT, cut=2)
    m.round_box(bd, 0, 0, 8.4, 7.6, 3.0, 5.0, trimf, cut=2)
    m.box(bd, -6.0, 13.0, -7.6, 6.0, 15.0, -6.6, trimf)                                 # sash
    hd = m.bone("head", bd, (0, 24, -2))
    m.round_box(hd, 0, -2.0, 4.0, 3.6, 24.0, 33.0, maskf, cut=1)
    m.round_box(hd, 0, -0.6, 4.6, 4.2, 31.0, 35.0, COAT, cut=1)                        # hood
    for sx in (-1, 1):                                           # two hair buns
        ball(m, hd, (sx * 1.8, 37.0, 0.0), 2.4, HAIR, layers=3)
    rod(m, hd, (-1.0, 38.0, 0.0), (4.0, 39.0, 0.0), 1, solid(P, "wood"), extend=0.2)
    ball(m, hd, (4.4, 39.0, 0.0), 0.8, solid(P, "red"), layers=2)
    for i in range(12):                                          # prayer beads
        ang = math.radians(-90 + i * (180 / 11))
        c = (5.0 * math.sin(ang), 22.0 - 3.0 * math.cos(ang) ** 2, -6.6 * math.cos(ang) * 0.9)
        ball(m, bd, c, 0.9, solid(P, "bead"), layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 7.0, 20.0, 0))
        hand = (sx * 9.0, 16.0, -5.0)
        rod(m, ab, (sx * 7.0, 20.0, 0), hand, 4, COAT, extend=0.4)
        m.box(ab, hand[0] - 1.2, hand[1] - 1.4, hand[2] - 1.2, hand[0] + 1.2, hand[1] + 1.0, hand[2] + 1.2,
              skin(P, "mask", dark="mask_dark"))
    st = m.bone("staff", "arm_right", (-9.0, 16.0, -5.0))         # the broom
    rod(m, st, (-9.0, 2.0, -5.0), (-9.0, 44.0, -5.0), 1, solid(P, "wood"), extend=0)
    for i in range(8):
        ang = math.radians(i * 45)
        rod(m, st, (-9.0, 44.0, -5.0), (-9.0 + 1.6 * math.cos(ang), 50.0, -5.0 + 1.6 * math.sin(ang)), 1,
            strands(P, "straw", "straw_dark"), extend=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 3.0, 0))
        m.round_box(lg, sx * 3.0, -0.6, 2.0, 2.6, 0.0, 3.4, solid(P, "boot"), cut=1)
    return m
