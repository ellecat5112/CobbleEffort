"""ShouCutemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little pink imp with two long pointed pink ears, big blue eyes with a cross scowl and a jagged
mouth, blue headphones, a magenta scarf blowing to both sides, pale-blue paws and red boots. 1 block. Child stage (no
level on wikimon; by analogy with Cutemon).

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a little pink imp with long pointed ears, a scowling face, blue headphones, a magenta scarf, pale-blue paws and red boots"
BASE = {"pink": (246, 180, 200), "pink_dark": (210, 120, 150), "blue": (90, 150, 230), "paleblue": (190, 220, 250),
        "magenta": (200, 50, 140), "magenta_dark": (130, 20, 80), "red": (210, 40, 50), "black": (30, 26, 30),
        "eye": (70, 140, 230), "white": (255, 255, 255)}
SHINY = {"pink": (200, 230, 190), "pink_dark": (130, 180, 120)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "pink", "pink_dark", length=1.0)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 20.4)
            if d < 0.5:
                return tone(p["black"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
            if abs(y - 21.8 - (x * sx - 1.6) * 0.4) < 0.15 and abs(x - sx * 1.6) < 1.0:
                return tone(p["black"], face), None
        if abs(y - 18.4 - 0.3 * abs(math.sin(x * 3))) < 0.15 and abs(x) < 1.6:
            return tone(p["black"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("shoucutemon")
    top = m.bone("shoucutemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 3.0, 2.6, 6.0, 15.0, FUR, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 20.0, -0.2), 3.8, facef, layers=4, ry=3.6)
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 23.0, 0), (sx * 0.5, 1, 0), 1.8, 9.0, FUR, tip=0.8)          # long pointed ears
        m.round_box(hd, sx * 3.8, 0, 1.0, 1.6, 19.0, 22.0, metal(P, "blue"), cut=0)           # headphones
    m.round_box(bd, 0, 0, 3.6, 3.2, 14.0, 16.0, fabric(P, "magenta", "magenta_dark", axis="x"), cut=1)   # scarf
    for sx in (-1, 1):
        rod(m, bd, (sx * 3.0, 15.0, 0), (sx * 9.0, 14.0, 0.6), 1, fabric(P, "magenta", "magenta_dark", axis="x"),
            extend=0.2, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.0, 13.0, 0))
        rod(m, ab, (sx * 3.0, 13.0, 0), (sx * 4.6, 9.0, -1.0), 2, FUR, extend=0.3)
        ball(m, ab, (sx * 4.8, 8.6, -1.2), 1.4, solid(P, "paleblue"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.0, 0), (sx * 1.8, 2.0, 0), 2, FUR, extend=0.3)
        m.round_box(lg, sx * 1.8, -0.6, 1.6, 2.0, 0.0, 2.8, solid(P, "red"), cut=0)
    return m
