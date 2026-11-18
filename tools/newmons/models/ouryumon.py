"""Ouryumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the king dragon: a mighty long-bodied dragon armoured in gold plates over dark scales, a horned
golden dragon helm with a violet mane, clawed golden gauntlets, a great black wing edged with a golden crescent blade,
a long armoured tail, and storm clouds crackling with blue lightning about it. 35 blocks long.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import armour, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a mighty long-bodied dragon in gold plate over dark scales, a horned golden helm with a violet mane, a great "
        "black wing edged with a golden crescent blade and storm clouds crackling with lightning")
BASE = {"gold": (230, 190, 80), "gold_dark": (150, 110, 30), "scale": (70, 60, 50), "scale_dark": (30, 24, 20),
        "violet": (140, 90, 180), "black": (30, 30, 36), "eye": (240, 60, 40), "cloud": (230, 236, 250),
        "bolt": (140, 200, 255), "tooth": (250, 250, 240), "mouth": (130, 20, 30)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 140), "violet": (220, 80, 80)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", trim="scale_dark", trim_w=0.25, rivets=True)
SC = scales(P, "scale", "scale_dark", size=1.4)


def build():
    m = Model("ouryumon")
    top = m.bone("ouryumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    pts = [(0, 36.0, -8.0), (0, 30.0, -2.0), (0, 24.0, 2.0), (2.0, 18.0, 6.0), (6.0, 12.0, 10.0), (10.0, 8.0, 16.0),
           (12.0, 6.0, 24.0), (10.0, 8.0, 30.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(2, 7 - j), GOLD if j % 2 == 0 else SC, extend=0.7)
    spike(m, bd, pts[-1], (-0.4, 0.2, 1), 1.6, 6.0, metal(P, "gold"), tip=0.8)
    hd = m.bone("head", bd, pts[0])
    h = pts[0]
    m.round_box(hd, h[0], h[2] - 3.0, 3.4, 5.0, h[1] - 1.0, h[1] + 3.6, GOLD, cut=1)      # golden dragon helm
    m.round_box(hd, h[0], h[2] - 7.0, 2.4, 3.0, h[1] - 2.4, h[1] - 0.6, SC, cut=0)
    m.box(hd, h[0] - 2.0, h[1] - 0.8, h[2] - 10.0, h[0] + 2.0, h[1] - 0.4, h[2] - 4.0, solid(P, "mouth"))
    for sx in (-1, 1):
        m.box(hd, h[0] + min(sx * 3.4, sx * 3.6), h[1] + 1.4, h[2] - 6.0, h[0] + max(sx * 3.4, sx * 3.6), h[1] + 2.2,
              h[2] - 4.6, solid(P, "eye", glow=True))
        pts_h = [(h[0] + sx * 2.0, h[1] + 3.4, h[2] - 1.0), (h[0] + sx * 4.0, h[1] + 8.0, h[2] + 2.0),
                 (h[0] + sx * 3.0, h[1] + 12.0, h[2] + 5.0)]
        for j, (p0, p1) in enumerate(zip(pts_h, pts_h[1:])):
            rod(m, hd, p0, p1, 2 - j, metal(P, "gold"), extend=0.3)
        spike(m, hd, (h[0] + sx * 1.8, h[1] - 0.4, h[2] - 9.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
    for i in range(8):                                                                   # violet mane
        spike(m, hd, (h[0] + (i - 3.5) * 0.7, h[1] + 3.6, h[2] + 1.0), ((i - 3.5) * 0.2, 0.6, 1), 1.4, 7.0,
              strands(P, "violet", "black"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # golden gauntlets
        ab = m.bone(nm, bd, (sx * 4.0, 30.0, -2.0))
        rod(m, ab, (sx * 4.0, 30.0, -2.0), (sx * 9.0, 24.0, -6.0), 3, GOLD, extend=0.4)
        for f in range(3):
            spike(m, ab, (sx * 9.0, 24.0, -6.0), (sx * 0.2 + (f - 1) * 0.4, -0.6, -1), 1.0, 4.0, metal(P, "gold"),
                  tip=0.8)
    wb = m.bone("wing_left", bd, (4.0, 32.0, 2.0))                                       # great black wing
    bat_wing(m, wb, (4.0, 32.0, 2.0), 28.0, 22.0, 4, metal(P, "gold"), solid(P, "black"), side=1, sweep=15)
    for j in range(7):                                                                   # golden crescent blade
        ang = math.radians(-20 + j * 20)
        c = (4.0 + 20.0 * math.cos(ang), 40.0 + 14.0 * math.sin(ang), 4.0)
        m.box(wb, c[0] - 2.0, c[1] - 0.6, c[2] - 0.4, c[0] + 2.0, c[1] + 0.6, c[2] + 0.4, metal(P, "gold"),
              rotation=(0, 0, math.degrees(ang) + 90), pivot=c)
    for i in range(5):                                                                   # storm clouds + lightning
        ang = 2 * math.pi * i / 5
        c = (14.0 * math.cos(ang), 10.0 + 4.0 * math.sin(ang * 2), 14.0 * math.sin(ang) + 4.0)
        ball(m, bd, c, 3.0, solid(P, "cloud"), layers=2, ry=2.0)
        rod(m, bd, c, (c[0] + 2.0, c[1] + 6.0, c[2]), 1, solid(P, "bolt", glow=True), extend=0.1)
    return m
