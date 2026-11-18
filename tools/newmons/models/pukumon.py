"""Pukumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the pufferfish warrior: a great round steel-grey spiked puffer head with one fierce red eye and a
blue-lipped snarl, a squat blue scaled body with an anchor tattoo, frosty translucent fins flaring behind, and two
huge red-banded gauntlets ending in spiked steel fists. 35 blocks.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "a round spiked steel puffer head with one red eye, a squat blue scaled body, frosty fins and huge red-banded spiked fists"
BASE = {"steel": (170, 174, 186), "steel_dark": (80, 84, 96), "blue": (60, 100, 180), "blue_dark": (24, 44, 110),
        "red": (210, 40, 40), "red_dark": (120, 14, 14), "eye": (230, 40, 40), "white": (250, 250, 250),
        "lip": (110, 160, 230), "tooth": (250, 250, 240), "ice": (200, 236, 250, 190), "anchor": (240, 210, 60)}
SHINY = {"blue": (70, 160, 90), "blue_dark": (24, 90, 40), "red": (240, 180, 40), "red_dark": (150, 100, 10)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        d = math.hypot(x - 2.0, y - 26.0)
        if d < 0.7:
            return tone((20, 20, 24), face), None
        if d < 1.8:
            return tone(p["eye"] if d < 1.4 else p["white"], face), None
        if 19.0 < y < 21.4 and abs(x) < 4.0:
            if abs(y - 20.2) < 0.4:
                return tone(p["tooth"], face), None
            return tone(p["lip"], face), None
    return STEEL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("pukumon")
    top = m.bone("pukumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 6.0, 5.0, 8.0, 16.0, scales(P, "blue", "blue_dark", size=1.4), cut=2)
    m.box(bd, 1.0, 10.0, -5.3, 3.0, 13.0, -5.0, solid(P, "anchor"))
    hd = m.bone("head", bd, (0, 16, 0))
    ball(m, hd, (0, 24.0, 0), 9.0, headf, layers=7)                                        # puffer head
    for i in range(10):                                                                  # spikes
        th = math.pi * (i + 0.5) / 10
        for j in range(8):
            ph = 2 * math.pi * (j + 0.5 * (i % 2)) / 8
            d = (math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph))
            if d[2] < -0.55 and abs(d[1]) < 0.6:
                continue
            p0 = (9.0 * d[0], 24.0 + 9.0 * d[1], 9.0 * d[2])
            spike(m, hd, p0, d, 1.2, 3.6, STEEL, tip=0.8)
    fb = m.bone("fins", bd, (0, 22, 6))
    for j in range(5):                                                                   # frosty fins
        ang = math.radians(-40 + j * 20)
        m.box(fb, -2.0, 18.0, 8.0, 2.0, 34.0, 8.0, solid(P, "ice"),
              rotation=(20, 0, math.degrees(ang)), pivot=(0, 22.0, 8.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # gauntlets + fists
        ab = m.bone(nm, bd, (sx * 6.0, 14.0, 0))
        rod(m, ab, (sx * 6.0, 14.0, 0), (sx * 12.0, 12.0, -4.0), 3, scales(P, "blue", "blue_dark", size=1.2), extend=0.4)
        m.round_box(ab, sx * 13.0, -4.0, 3.2, 3.2, 6.0, 12.0, armour(P, "red", "red_dark"), cut=1)
        for j in range(3):
            m.round_box(ab, sx * 13.0, -4.0, 3.5, 3.5, 6.6 + j * 1.8, 7.4 + j * 1.8, solid(P, "red_dark"), cut=1)
        ball(m, ab, (sx * 13.0, 4.0, -4.6), 3.6, STEEL, layers=3)
        for f in range(4):
            spike(m, ab, (sx * 13.0 + (f - 1.5) * 1.6, 4.4, -8.0), (0, 0.2, -1), 1.0, 2.6, STEEL, tip=0.8)
    return m
