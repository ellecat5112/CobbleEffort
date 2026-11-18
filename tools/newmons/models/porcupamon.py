"""Porcupamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a patched-up teddy bear gone wrong: violet plush body spotted pale and sewn with red stitches, a
tan patchwork snout and arm, an X-stitched eye, curled ram horns, a rusted gas-mask breather and hose, steel spikes
bristling from its back, elbows and feet, a belt with a buckle round one leg. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, leather, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a patched violet teddy bear sewn with red stitches, an X-stitched eye, ram horns, a gas-mask breather and steel spikes"
BASE = {"violet": (80, 60, 140), "violet_dark": (36, 24, 80), "spot": (220, 214, 240), "tan": (200, 180, 140),
        "tan_dark": (140, 120, 80), "stitch": (200, 40, 40), "horn": (150, 150, 160), "horn_dark": (80, 80, 90),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "black": (24, 22, 28), "heart": (230, 60, 90)}
SHINY = {"violet": (60, 120, 80), "violet_dark": (20, 60, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def plushf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(x * 0.9) * math.sin(y * 0.8 + z * 0.4)) > 0.92:
        return tone(p["spot"], face), None
    if abs((x * 0.7 + y) % 9.0 - 4.5) < 0.18 and int(y * 3) % 2:
        return tone(p["stitch"], face), None
    return fabric(P, "violet", "violet_dark", axis="y", period=1.6)(x, y, z, face, variant, box=box, **k)


def patchf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(x) < 0.2 or abs(y % 4.0 - 2.0) < 0.12:
        return tone(p["stitch"], face), None
    return fabric(P, "tan", "tan_dark", axis="x", period=1.6)(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("porcupamon")
    top = m.bone("porcupamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    ball(m, bd, (0, 20.0, 0.6), 7.0, plushf, layers=6, ry=9.0)
    m.box(bd, -2.0, 22.0, -6.6, 2.0, 25.0, -6.0, solid(P, "heart"))                       # stitched heart
    for j in range(5):                                                                   # back spikes
        for sx in (-1, 0, 1):
            spike(m, bd, (sx * 3.6, 15.0 + j * 2.6, 6.6), (sx * 0.4, 0.3, 1), 1.0, 3.6, STEEL, tip=0.8)
    hd = m.bone("head", bd, (0, 28, 0))
    ball(m, hd, (0, 33.0, 0), 5.6, plushf, layers=5, ry=5.0)
    m.round_box(hd, 0, -5.0, 3.0, 1.8, 29.6, 33.4, patchf, cut=1)                          # tan snout
    m.box(hd, -0.8, 32.4, -7.0, 0.8, 33.4, -6.6, solid(P, "black"))
    m.box(hd, -3.4, 34.4, -5.4, -1.4, 35.2, -5.2, solid(P, "stitch"), rotation=(0, 0, 45), pivot=(-2.4, 34.8, -5.3))
    m.box(hd, -3.4, 34.4, -5.4, -1.4, 35.2, -5.2, solid(P, "stitch"), rotation=(0, 0, -45), pivot=(-2.4, 34.8, -5.3))
    m.box(hd, 1.6, 34.0, -5.4, 3.2, 35.6, -5.2, solid(P, "black"))
    for sx in (-1, 1):                                                                   # curled ram horns
        pts = [(sx * 4.0, 36.0, 0), (sx * 6.6, 38.0, 1.0), (sx * 7.6, 35.0, 2.0), (sx * 6.0, 32.6, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, metal(P, "horn", dark="horn_dark"), extend=0.3)
        spike(m, hd, (sx * 2.0, 38.0, 0), (sx * 0.3, 1, 0), 1.0, 3.0, STEEL, tip=0.8)
    m.round_box(hd, 2.6, -5.0, 1.6, 1.4, 29.0, 31.4, metal(P, "steel", dark="steel_dark"), cut=0)  # breather
    pts = [(3.6, 30.0, -4.6), (6.0, 27.0, -2.0), (6.6, 23.0, 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, hd, p0, p1, 1, solid(P, "steel_dark"), extend=0.2, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.6, 24.0, 0))
        sh = patchf if sx < 0 else plushf
        rod(m, ab, (sx * 6.6, 24.0, 0), (sx * 9.6, 16.0, -1.0), 4, sh, extend=0.6)
        ball(m, ab, (sx * 10.0, 15.0, -1.4), 2.4, sh, layers=2)
        spike(m, ab, (sx * 8.6, 21.0, 2.0), (sx * 0.5, 0.2, 1), 1.0, 3.0, STEEL, tip=0.8)
        for f in range(3):
            spike(m, ab, (sx * 10.0 + (f - 1) * 1.0, 13.0, -2.6), ((f - 1) * 0.2, -1, -0.3), 0.8, 2.2, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.6, 13.0, 0))
        m.round_box(lg, sx * 3.6, 0, 3.0, 3.0, 3.0, 14.0, plushf, cut=1)
        m.round_box(lg, sx * 3.6, -1.0, 3.4, 4.2, 0.0, 3.4, plushf, cut=1)
        for f in range(3):
            spike(m, lg, (sx * 3.6 + (f - 1) * 1.6, 1.0, -5.0), (0, -0.2, -1), 0.9, 2.2, STEEL, tip=0.8)
        if sx > 0:
            m.round_box(lg, sx * 3.6, 0, 3.4, 3.4, 8.0, 9.4, leather(P, "black", "black"), cut=1)
            m.box(lg, sx * 3.6 - 1.0, 7.6, -3.8, sx * 3.6 + 1.0, 9.8, -3.4, STEEL)
    return m
