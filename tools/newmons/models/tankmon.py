"""Tankmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a cyborg tank: an olive-green armoured hull on two heavy grey tread units, a fanged monster mouth with
an orange mane and a red tongue in front, a long main cannon for its left arm, a grey drill-tipped gun pod on the
right and a belt of brass shells slung across its back. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, eye, metal, riveted, solid, strands
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 3.4)
KIND = "biped"
K = 3
LOOK = "an olive-green cyborg tank with a fanged monster mouth and orange mane, a long main cannon and grey treads"
BASE = {"olive": (110, 130, 50), "olive_dark": (60, 74, 24), "grey": (120, 122, 130), "grey_dark": (50, 52, 58),
        "steel": (190, 194, 204), "orange": (230, 120, 40), "orange_dark": (150, 60, 14), "red": (200, 40, 50),
        "mouth": (80, 10, 20), "tooth": (250, 250, 244), "brass": (220, 170, 70), "eye": (250, 220, 60),
        "pupil": (20, 10, 10), "white": (255, 255, 255)}
SHINY = {"olive": (190, 170, 120), "olive_dark": (120, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "olive", "olive_dark", panel=(3.0, 3.0), rivets=True)
GREY = riveted(P, "grey", "grey_dark")
STEEL = metal(P, "steel", dark="grey_dark")


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and box is not None:
        cz = (z - box.lo[2]) % 3.0
        cy = y - box.lo[1]
        if 1.4 < cy < box.size[1] - 1.4 and abs(cz - 1.5) < 1.0:
            return tone(p["grey_dark"], face), None
    if face in ("up", "down", "north", "south") and (z % 1.6) < 0.5:
        return tone(p["grey_dark"], face), None
    return tone(p["grey"], face), None


def build():
    m = Model("tankmon")
    top = m.bone("tankmon", None, (0, 0, 0))
    for sx in (-1, 1):                                                                 # tread units
        tb = m.bone("tread_left" if sx > 0 else "tread_right", top, (sx * 6.0, 4.0, 0))
        m.round_box(tb, sx * 6.4, 0, 3.0, 10.0, 0.0, 8.0, treadf, cut=2)
        for j in range(4):
            ball(m, tb, (sx * 9.6, 3.0, -7.0 + j * 4.6), 1.6, STEEL, layers=1)
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 6.6, 9.0, 7.0, 16.0, HULL, cut=2)
    m.round_box(bd, 0, 1.0, 5.6, 7.0, 16.0, 22.0, HULL, cut=2)
    hd = m.bone("head", bd, (0, 14, -9))
    m.box(hd, -4.6, 8.0, -12.0, 4.6, 14.0, -9.0, solid(P, "mouth"))                      # monster mouth
    m.box(hd, -2.4, 8.4, -12.2, 2.4, 9.6, -10.0, solid(P, "red"))
    for j in range(7):
        x = -4.0 + j * 1.33
        spike(m, hd, (x, 14.0, -11.6), (0, -1, 0), 1.0, 2.6, solid(P, "tooth"), tip=0.8)
        spike(m, hd, (x, 8.0, -11.6), (0, 1, 0), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
    m.round_box(hd, 0, -10.6, 5.4, 1.6, 14.0, 17.4, HULL, cut=1)                         # brow
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.2, sx * 3.4), 15.0, -12.4, max(sx * 1.2, sx * 3.4), 16.4, -12.1, solid(P, "eye", glow=True))
    for j in range(6):                                                                 # orange mane
        spike(m, hd, (-4.0 + j * 1.6, 15.0, -11.0), ((j - 2.5) * 0.2, -1, -0.4), 1.4, 4.0, strands(P, "orange",
              "orange_dark"), tip=0.8)
    al = m.bone("arm_left", bd, (7.0, 17.0, 0))                                         # main cannon
    m.round_box(al, 9.0, 0, 2.6, 3.0, 14.0, 20.0, HULL, cut=1)
    rod(m, al, (9.0, 17.0, -2.0), (9.0, 18.0, -20.0), 3, STEEL, extend=0.0)
    m.round_box(al, 9.0, -20.0, 2.0, 0.8, 16.4, 19.6, GREY, cut=0)
    ar = m.bone("arm_right", bd, (-7.0, 17.0, 0))                                       # gun pod
    m.round_box(ar, -9.0, -1.0, 2.6, 3.4, 13.0, 21.0, GREY, cut=1)
    for j in range(3):
        rod(m, ar, (-9.6 + j * 0.6, 17.0 + (j - 1) * 1.2, -4.0), (-9.6 + j * 0.6, 17.0 + (j - 1) * 1.2, -11.0), 1,
            STEEL, extend=0.0)
    spike(m, ar, (-9.0, 21.0, -1.0), (0, 1, 0), 2.6, 4.0, STEEL, tip=0.8)
    for j in range(8):                                                                 # shell belt
        ang = -0.8 + j * 0.22
        m.box(bd, -6.0 + j * 1.6, 20.0 + 4.0 * math.sin(ang + 0.8), 7.4, -5.0 + j * 1.6, 23.0 + 4.0 * math.sin(ang + 0.8),
              8.4, solid(P, "brass"))
    return m
