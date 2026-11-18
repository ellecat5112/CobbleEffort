"""Ragnamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a war satellite with a beast's body: a silver-and-violet armoured core like a space station, its
red-lensed head flanked by long gun barrels and striped gold solar vanes, clawed violet limbs, a long coiling purple
tail, and two glowing rings of blue light crossing round it. 35 blocks.

Front is -z, y is up. 60 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "a war satellite with a beast's body: a silver-violet armoured core, long gun barrels, gold solar vanes, a coiling tail and rings of light"
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 114, 130), "violet": (110, 70, 180), "violet_dark": (50, 26, 100),
        "gold": (220, 180, 80), "gold_dark": (140, 100, 30), "red": (220, 30, 50), "ring": (130, 210, 255, 180),
        "claw": (240, 220, 140)}
SHINY = {"violet": (200, 60, 70), "violet_dark": (110, 20, 30), "ring": (255, 180, 100, 180)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "silver", dark="silver_dark")
VIOLET = armour(P, "violet", "violet_dark", trim="silver", trim_w=0.2)


def vanef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["gold"] if (abs(x) % 2.0) < 1.2 else p["gold_dark"], face), None


def build():
    m = Model("ragnamon")
    top = m.bone("ragnamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    ball(m, bd, (0, 36.0, 0), 8.0, VIOLET, layers=6)                                       # core
    m.round_box(bd, 0, 0, 9.0, 9.0, 35.0, 37.0, STEEL, cut=3)
    ball(m, bd, (0, 36.0, -7.6), 2.4, solid(P, "red", glow=True), layers=2)
    hd = m.bone("head", bd, (0, 46, -2))
    m.round_box(hd, 0, -2.0, 3.0, 4.0, 44.0, 50.0, STEEL, cut=1)
    m.box(hd, -1.6, 47.0, -6.1, 1.6, 48.0, -5.9, solid(P, "red", glow=True))
    for sx in (-1, 1):                                                                   # long gun barrels
        rod(m, hd, (sx * 3.0, 48.0, 0), (sx * 4.0, 60.0, -4.0), 2, STEEL, extend=0.4)
        m.box(bd, min(sx * 9.0, sx * 32.0), 40.0, -1.0, max(sx * 9.0, sx * 32.0), 41.0, 3.0, vanef,
              rotation=(0, 0, sx * 10), pivot=(sx * 9.0, 40.0, 1.0))                     # solar vanes
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # clawed limbs
        ab = m.bone(nm, bd, (sx * 7.0, 32.0, -2.0))
        rod(m, ab, (sx * 7.0, 32.0, -2.0), (sx * 13.0, 24.0, -6.0), 3, VIOLET, extend=0.4)
        rod(m, ab, (sx * 13.0, 24.0, -6.0), (sx * 12.0, 16.0, -8.0), 2, VIOLET, extend=0.4)
        for f in range(3):
            spike(m, ab, (sx * 12.0 + (f - 1) * 1.2, 16.0, -8.0), ((f - 1) * 0.3, -1, -0.5), 1.0, 4.0,
                  solid(P, "claw"), tip=0.8)
    tl = m.bone("tail", bd, (0, 30, 4))                                                  # coiling tail
    pts = [(0, 30.0, 4.0)]
    for i in range(1, 10):
        a = i * 0.7
        pts.append((9.0 * math.sin(a), 30.0 - i * 2.8, 4.0 + 9.0 * (1 - math.cos(a))))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(2, 6 - i // 2), VIOLET, extend=0.6)
    for k_, tilt in enumerate((30, -30)):                                                # crossing rings of light
        rb = m.bone(f"ring_{k_}", bd, (0, 36, 0))
        for i in range(24):
            ang = 2 * math.pi * i / 24
            x, y = 22.0 * math.cos(ang), 22.0 * math.sin(ang)
            m.box(rb, x - 1.0, 36.0 + y - 1.0, -0.4, x + 1.0, 36.0 + y + 1.0, 0.4, solid(P, "ring", glow=True),
                  rotation=(0, 60 if k_ else -60, 0), pivot=(0, 36.0, 0))
    return m
