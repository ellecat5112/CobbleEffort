"""Chrysalimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the data-eating chrysalis. A segmented violet armoured cocoon body tapering to a spike, studded
with yellow spines and a red horn, with long black cable tentacles looping round it and ending in violet-and-gold
claw blades. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage (floats).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "floater"
K = 3
LOOK = ("a segmented violet armoured cocoon studded with yellow spines and a red horn, with long black cable tentacles "
        "ending in violet-and-gold claw blades")
BASE = {"violet": (130, 100, 200), "violet_dark": (60, 40, 120), "violet_light": (200, 180, 250), "gold": (240, 210, 90),
        "gold_dark": (170, 130, 30), "red": (210, 40, 40), "black": (30, 30, 38), "eye": (250, 220, 60)}
SHINY = {"violet": (90, 170, 110), "violet_dark": (30, 100, 50), "violet_light": (170, 230, 180)}


def P(v):
    return pal(BASE, SHINY, v)


VIOLET = armour(P, "violet", "violet_dark", light="violet_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark")


def build():
    m = Model("chrysalimon")
    top = m.bone("chrysalimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    for i in range(7):                                                      # segmented cocoon, tapering down
        y0 = 22.0 + i * 3.6
        r = 2.0 + 3.4 * math.sin(min(1.0, (i + 0.5) / 6) * math.pi * 0.85)
        m.round_box(bd, 0, 0, r, r * 0.86, y0, y0 + 3.8, VIOLET, cut=max(1, round(r * 0.3)))
        if i % 2:
            for sx in (-1, 1):
                spike(m, bd, (sx * r, y0 + 1.8, 0), (sx, 0.3, -0.2), 1.0, 2.6, solid(P, "gold"))
    spike(m, bd, (0, 22.0, 0), (0, -1, 0), 2.6, 6.0, VIOLET, tip=0.5)
    hd = m.bone("head", bd, (0, 46, 0))
    m.round_box(hd, 0, -0.6, 3.4, 3.0, 46.0, 50.4, VIOLET, cut=1)
    spike(m, hd, (2.0, 49.0, -1.6), (0.8, 0.6, -0.4), 1.4, 4.0, solid(P, "red"), tip=0.3)
    m.box(hd, -1.6, 47.6, -3.7, 1.6, 48.4, -3.5, solid(P, "eye", glow=True))
    # long black cable tentacles looping out to claw blades
    for k in range(6):
        ang = math.radians(k * 60 + 30)
        tb = m.bone(f"tentacle_{k}", bd, (0, 40, 0))
        pts = [(3.0 * math.cos(ang), 40.0, 3.0 * math.sin(ang))]
        for j in range(1, 6):
            rr = 3.0 + j * 3.0
            pts.append((rr * math.cos(ang + 0.4 * math.sin(j)), 40.0 + 6.0 * math.sin(j * 1.1 + k) - j * 3.0,
                        rr * math.sin(ang + 0.4 * math.sin(j))))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 1, solid(P, "black"), extend=0.3)
        e = pts[-1]
        spike(m, tb, e, (math.cos(ang), -0.6, math.sin(ang)), 2.0, 6.0, VIOLET, tip=0.4)
        spike(m, tb, e, (math.cos(ang) * 0.6, -1, math.sin(ang) * 0.6), 1.2, 3.0, GOLD, tip=0.3)
    return m
