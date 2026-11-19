"""Skull Seadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): an undead sea serpent: a long whipping spine of grey-silver vertebrae trimmed with dark
teal ridges and translucent violet fin-membranes, a fanged dragon skull with a long blade-horn and a green-gem eye,
a glowing green core in its ribs, and a tail fin of ghostly blue. 25 blocks.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 7.0)
KIND = "floater"
K = 3
LOOK = "an undead sea serpent of grey-silver vertebrae with teal ridges, violet fin-membranes, a fanged blade-horned skull and a green core"
BASE = {"bone": (210, 214, 220), "bone_dark": (110, 114, 124), "teal": (40, 110, 110), "fin": (200, 170, 240, 150),
        "green": (90, 240, 140), "white": (240, 255, 250), "ghost": (150, 220, 250, 160), "tooth": (250, 250, 240)}
SHINY = {"bone": (230, 200, 150), "bone_dark": (150, 120, 70), "teal": (140, 40, 60)}


def P(v):
    return pal(BASE, SHINY, v)


BONE = armour(P, "bone", "bone_dark")


def build():
    m = Model("skullseadramon")
    top = m.bone("skullseadramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    pts = [(0, 28.0, -8.0), (4.0, 24.0, 0.0), (8.0, 20.0, 8.0), (4.0, 16.0, 14.0), (-4.0, 12.0, 14.0), (-8.0, 8.0, 8.0),
           (-4.0, 4.0, 2.0), (4.0, 4.0, -2.0), (10.0, 6.0, -4.0)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        b = m.bone(f"coil_{i}", bd, p0)
        rod(m, b, p0, p1, 2, BONE, extend=0.4)
        for j in range(2):
            q = tuple(p0[c] + (p1[c] - p0[c]) * (0.25 + 0.5 * j) for c in range(3))
            m.round_box(b, q[0], q[2], 1.8, 1.8, q[1] - 0.5, q[1] + 0.5, metal(P, "teal"), cut=0)
            spike(m, b, q, (0, 1, 0.3), 1.2, 3.0, BONE, tip=0.8)
        if i < 3:
            for sx in (-1, 1):
                rp = [p0, (p0[0] + sx * 4.0, p0[1] - 3.0, p0[2]), (p0[0] + sx * 2.0, p0[1] - 6.0, p0[2])]
                for a_, b_ in zip(rp, rp[1:]):
                    rod(m, b, a_, b_, 1, BONE, extend=0.2)
                m.box(b, min(p0[0], p0[0] + sx * 8.0), p0[1] - 2.0, p0[2], max(p0[0], p0[0] + sx * 8.0), p0[1] + 6.0,
                      p0[2], solid(P, "fin"), rotation=(0, 0, sx * 20), pivot=p0)
    ball(m, "coil_0", (2.0, 24.0, -4.0), 2.0, gem(P, "green", "white"), layers=2)          # green core
    tl = m.bone("tail_fin", "coil_7", pts[-1])
    m.box(tl, pts[-1][0], pts[-1][1] - 3.0, pts[-1][2] - 0.2, pts[-1][0] + 6.0, pts[-1][1] + 3.0, pts[-1][2] + 0.2,
          solid(P, "ghost", glow=True))
    hd = m.bone("head", bd, pts[0])
    m.round_box(hd, 0, -14.0, 3.0, 5.0, 26.0, 32.0, BONE, cut=1)                             # dragon skull
    m.round_box(hd, 0, -20.0, 2.0, 2.6, 25.0, 28.0, BONE, cut=0)
    jb = m.bone("jaw", hd, (0, 25, -10))
    m.round_box(jb, 0, -17.0, 2.0, 5.0, 22.6, 24.6, BONE, cut=0)
    for j in range(6):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.8, 25.0, -21.0 + j * 1.6), (0, -1, 0), 0.9, 2.0, solid(P, "tooth"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.9, sx * 3.2), 29.0, -15.0, max(sx * 2.9, sx * 3.2), 30.4, -13.4, gem(P, "green", "white"))
    spike(m, hd, (0, 32.0, -10.0), (0, 0.3, 1), 1.6, 16.0, BONE, tip=0.8)                    # long blade-horn
    return m
