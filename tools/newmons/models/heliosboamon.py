"""Helios Boamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the sun serpent: a huge white boa coiled in loops, edged with violet scales, its head armoured in a gold crested helm
with red eyes, a gold ring-blade orbiting its coils and a streak of cyan light behind it. 25 blocks long.

Front is -z, y is up. 30 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(25, HEIGHT, 4.6)
KIND = "floater"
K = 3
LOOK = "a huge white boa coiled in loops edged with violet scales, a gold crested helm, red eyes and a gold ring-blade"
BASE = {"white": (246, 246, 250), "white_dark": (190, 192, 206), "violet": (130, 90, 190), "gold": (230, 190, 80),
        "gold_dark": (150, 110, 20), "eye": (230, 40, 50)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "violet": (240, 160, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and box is not None and (min(y - box.lo[1], box.lo[1] + box.size[1] - y) < 0.6):
        return tone(p["violet"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("heliosboamon")
    top = m.bone("heliosboamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    pts = []
    for i in range(34):                                                                 # coiled loops
        t = i / 33
        ang = t * 4.6 * math.pi
        r = 13.0 - 5.0 * t
        pts.append((r * math.cos(ang), 4.0 + 3.0 * math.sin(ang * 0.5) + 14.0 * t, r * math.sin(ang)))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bd, p0, p1, max(3, 6 - j // 8), bodyf, extend=0.6)
    h = pts[-1]
    hd = m.bone("head", bd, h)
    m.round_box(hd, h[0], h[2] - 3.0, 2.6, 4.4, h[1] - 1.0, h[1] + 3.0, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):
        m.box(hd, h[0] + min(sx * 2.6, sx * 2.8), h[1] + 1.0, h[2] - 5.0, h[0] + max(sx * 2.6, sx * 2.8), h[1] + 2.0,
              h[2] - 3.0, solid(P, "eye", glow=True))
    spike(m, hd, (h[0], h[1] + 3.0, h[2] - 1.0), (0, 0.8, 1), 1.6, 6.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    rb = m.bone("ring_blade", bd, (0, 12, 0))                                             # gold ring-blade
    for i in range(16):
        a0, a1 = 2 * math.pi * i / 16, 2 * math.pi * (i + 1) / 16
        rod(m, rb, (16.0 * math.cos(a0), 12.0 + 3.0 * math.sin(a0), 16.0 * math.sin(a0)),
            (16.0 * math.cos(a1), 12.0 + 3.0 * math.sin(a1), 16.0 * math.sin(a1)), 1, metal(P, "gold", dark="gold_dark"),
            extend=0.3, t2=2)
    return m
