"""Gerbemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
garbage-can Digimon: a lumpy pink creature with a grinning toothy face, blue eyes, spikes down its back and a mop of
yellow dreadlocks, sitting in a battered green rubbish bin stencilled "01" and hugging a spray-bottle bazooka.
25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fbm, metal, riveted, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a lumpy pink creature with a toothy grin and yellow dreadlocks sitting in a battered green rubbish bin with a "
        "spray-bottle bazooka")
BASE = {"pink": (240, 150, 190), "pink_dark": (190, 80, 130), "bin": (90, 120, 50), "bin_dark": (50, 70, 24),
        "rust": (130, 90, 50), "hair": (240, 230, 70), "hair_dark": (180, 160, 30), "eye": (60, 110, 220),
        "white": (250, 250, 250), "mouth": (100, 20, 30), "tooth": (250, 250, 240), "red": (210, 40, 40),
        "steel": (180, 184, 196), "steel_dark": (90, 94, 106)}
SHINY = {"pink": (150, 220, 160), "pink_dark": (80, 150, 90), "bin": (120, 100, 150), "bin_dark": (70, 50, 100)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = skin(P, "pink", dark="pink_dark")
BIN0 = riveted(P, "bin", "bin_dark")


def binf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if fbm(x * 0.4, y * 0.4, z * 0.4, seed=9) > 0.7:
        return tone(p["rust"], face), None
    if face in ("east", "west", "north", "south") and (abs(math.atan2(z, x) * 6 / math.pi % 1.0 - 0.5) < 0.08):
        return tone(p["bin_dark"], face), None
    return BIN0(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 24.0 < y < 26.4 and -1.0 < x < 4.6:
            return tone(p["tooth"] if (x * 1.4) % 1.4 < 0.9 else p["mouth"], face), None
        for sx in (-1, 1):
            d = math.hypot(x - 1.4 - sx * 1.6, y - 29.0)
            if d < 0.5:
                return tone(p["eye"], face), None
            if d < 1.0:
                return tone(p["white"], face), None
    return PINK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gerbemon")
    top = m.bone("gerbemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 7.0, 7.0, 0.0, 18.0, binf, cut=3)                              # the rubbish bin
    m.round_box(bd, 0, 0, 7.6, 7.6, 17.0, 19.0, metal(P, "bin", dark="bin_dark"), cut=3)
    hd = m.bone("head", bd, (0, 24, -1))
    m.round_box(hd, 1.0, -1.0, 5.6, 5.0, 18.0, 32.0, headf, cut=2)                         # lumpy pink body
    for j in range(5):
        spike(m, hd, (5.0, 30.0 - j * 3.0, 2.0), (1, 0.2, 0.4), 1.4, 3.0, PINK, tip=0.8)
    for i in range(12):                                                                    # yellow dreadlocks
        ang = math.radians(-150 + i * 26)
        spike(m, hd, (1.0 + 3.4 * math.cos(ang), 32.0, -1.0 + 3.4 * math.sin(ang)),
              (math.cos(ang), 0.4, math.sin(ang)), 1.2, 6.0, strands(P, "hair", "hair_dark"), tip=0.9)
    ab = m.bone("arm_right", bd, (-3.0, 24.0, -3.0))                                       # spray-bottle bazooka
    rod(m, ab, (4.0, 26.0, -4.0), (-10.0, 20.0, -8.0), 4, metal(P, "steel", dark="steel_dark"), extend=0)
    m.round_box(ab, -11.0, -8.4, 2.6, 2.6, 18.0, 22.0, solid(P, "red"), cut=1)
    m.round_box(ab, 1.0, -5.4, 1.6, 1.6, 26.0, 30.0, solid(P, "steel"), cut=0)
    return m
