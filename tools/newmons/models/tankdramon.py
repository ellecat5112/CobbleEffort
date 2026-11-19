"""Tankdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a dragon fused with a heavy tank: a dark green tracked hull bristling with steel drill spikes, a
grey armoured shark-dragon head with a gold-rimmed jaw full of teeth at the front, a blue muscled dragon rider riding
in the turret, twin cannons, a missile rack and a bulldozer blade. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
LOOK = "a dark green tracked tank bristling with drill spikes, a grey shark-dragon head with a toothed jaw and a blue dragon rider in the turret"
BASE = {"green": (50, 90, 80), "green_dark": (20, 44, 40), "grey": (140, 144, 154), "grey_dark": (60, 62, 70),
        "steel": (200, 206, 218), "gold": (220, 170, 60), "blue": (70, 110, 200), "blue_dark": (30, 50, 120),
        "mouth": (120, 20, 30), "tooth": (250, 250, 244), "eye": (250, 200, 40), "red": (200, 40, 40),
        "brown": (110, 90, 70), "brown_dark": (60, 46, 34)}
SHINY = {"green": (120, 60, 40), "green_dark": (60, 26, 14), "blue": (200, 70, 60), "blue_dark": (120, 30, 20)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "green", "green_dark", panel=(4.0, 4.0), rivets=True)
GREY = armour(P, "grey", "grey_dark", trim="gold", panel=(3.0, 3.0))
STEEL = metal(P, "steel", dark="grey_dark")


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z % 2.0) < 0.7 or (face in ("east", "west") and (y % 2.0) < 0.5):
        return tone(p["grey_dark"], face), None
    return tone(p["grey"], face), None


def build():
    m = Model("tankdramon")
    top = m.bone("tankdramon", None, (0, 0, 0))
    for sx in (-1, 1):
        tb = m.bone("tread_left" if sx > 0 else "tread_right", top, (sx * 9.0, 5.0, 0))
        m.round_box(tb, sx * 10.0, 0, 3.4, 15.0, 0.0, 9.0, treadf, cut=3)
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 0, 9.4, 14.0, 7.0, 16.0, HULL, cut=2)
    for i in range(5):                                                                 # drill spikes on the flanks
        for sx in (-1, 1):
            spike(m, bd, (sx * 9.4, 12.0, -10.0 + i * 5.0), (sx, 0.1, -0.4), 2.0, 5.0, STEEL, tip=0.8)
    blade = m.bone("blade", bd, (0, 8, 14))                                             # bulldozer blade at the back
    m.box(blade, -9.0, 4.0, 14.0, 9.0, 14.0, 16.0, riveted(P, "brown", "brown_dark"), rotation=(-20, 0, 0),
          pivot=(0, 4.0, 15.0))
    hd = m.bone("head", bd, (0, 14, -14))                                               # shark-dragon head
    m.round_box(hd, 0, -17.0, 5.4, 4.0, 12.0, 20.0, GREY, cut=2)
    m.box(hd, -4.4, 10.0, -24.0, 4.4, 14.0, -14.0, solid(P, "mouth"))
    m.round_box(hd, 0, -22.0, 4.6, 3.0, 14.0, 17.4, GREY, cut=1)
    for j in range(8):
        z = -23.0 + j * 1.2
        for sx in (-1, 1):
            spike(m, hd, (sx * 4.2, 14.0, z), (0, -1, 0), 1.0, 2.4, solid(P, "tooth"), tip=0.8)
            spike(m, hd, (sx * 4.2, 10.0, z), (0, 1, 0), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
    m.box(hd, -4.8, 9.0, -24.4, 4.8, 10.0, -14.0, metal(P, "gold"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 4.0), 18.0, -20.4, max(sx * 2.4, sx * 4.0), 19.0, -20.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 20.0, -16.0), (0, 1, 0.6), 1.6, 5.0, solid(P, "red"), tip=0.8)          # head fin
    rd = m.bone("rider", bd, (0, 18, 2))                                                # the blue dragon rider
    m.round_box(rd, 0, 2.0, 6.0, 5.0, 16.0, 19.0, HULL, cut=1)
    m.round_box(rd, 0, 2.0, 4.0, 3.0, 19.0, 27.0, skin(P, "blue", dark="blue_dark"), cut=1)
    m.round_box(rd, 0, 0.6, 2.6, 3.0, 27.0, 31.4, skin(P, "blue", dark="blue_dark"), cut=1)
    for sx in (-1, 1):
        m.box(rd, min(sx * 0.6, sx * 2.0), 29.4, -2.5, max(sx * 0.6, sx * 2.0), 30.2, -2.3, solid(P, "eye", glow=True))
        rod(m, rd, (sx * 4.0, 25.0, 2.0), (sx * 7.0, 20.0, -2.0), 2, skin(P, "blue", dark="blue_dark"), extend=0.4)
        spike(m, rd, (sx * 1.6, 31.0, 1.0), (sx * 0.3, 1, 0.5), 1.0, 4.0, solid(P, "grey"), tip=0.8)
    for sx in (-1, 1):                                                                 # twin cannons
        rod(m, rd, (sx * 3.0, 24.0, 6.0), (sx * 3.6, 34.0, 4.0), 2, STEEL, extend=0.0)
    for j in range(3):                                                                 # missile rack
        m.box(rd, 4.0 + j * 1.4, 19.0, 4.0, 5.0 + j * 1.4, 27.0, 5.0, STEEL)
        spike(m, rd, (4.5 + j * 1.4, 27.0, 4.5), (0, 1, 0), 1.0, 2.0, solid(P, "red"), tip=0.8)
    return m
