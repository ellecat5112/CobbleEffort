"""Vortexdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a sky dragon of the vortex: a long pale-blue serpentine body coiled in a loop and banded with
red, a spiked crowned dragon head with streaming whiskers, dark armour blades along its neck, fans of white and
crimson feathers, and great translucent rainbow wings like a dragonfly's. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import feathers, metal, scales, solid
from _route import pal, tone

HEIGHT = 54
SCALE, HITBOX = sized(35, HEIGHT, 10.0)
KIND = "floater"
K = 3
LOOK = "a long pale-blue serpentine sky dragon coiled in a loop, with a spiked crowned head, white-and-crimson feather fans and translucent rainbow wings"
BASE = {"blue": (170, 210, 230), "blue_dark": (90, 140, 180), "red": (210, 50, 60), "dark": (50, 60, 70),
        "dark_light": (130, 140, 150), "white": (246, 246, 250), "white_dark": (190, 194, 210), "eye": (255, 220, 80)}
WING = [(150, 220, 255, 140), (180, 255, 200, 140), (255, 240, 150, 140), (255, 190, 220, 140)]
SHINY = {"blue": (230, 200, 160), "blue_dark": (170, 130, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y + z) % 7.0 < 0.9:
        return tone(p["red"], face), None
    return scales(P, "blue", "blue_dark", size=1.0)(x, y, z, face, variant, box=box, **k)


def _wing(i):
    col = WING[i % len(WING)]

    def f(x, y, z, face, variant, box=None, **k):
        return col, col[:3]
    return f


def build():
    m = Model("vortexdramon")
    top = m.bone("vortexdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 28, 0))
    for i in range(18):                                                                 # coiled loop body
        a0 = i * 2 * math.pi / 18
        a1 = (i + 1) * 2 * math.pi / 18
        p0 = (0.0, 24.0 + 12.0 * math.sin(a0), 12.0 * math.cos(a0))
        p1 = (0.0, 24.0 + 12.0 * math.sin(a1), 12.0 * math.cos(a1))
        rod(m, bd, p0, p1, 3, bodyf, extend=0.6)
    nk = m.bone("neck", bd, (0, 36, -4))
    pts = [(0, 34.0, -8.0), (0, 42.0, -12.0), (0, 48.0, -16.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, nk, p0, p1, 3, bodyf, extend=0.6)
        spike(m, nk, p1, (0, 0.6, 1), 1.6, 6.0, metal(P, "dark", dark="dark"), tip=0.8)
    hd = m.bone("head", nk, (0, 49, -17))
    m.round_box(hd, 0, -21.0, 2.0, 4.6, 47.4, 51.0, bodyf, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.1), 49.6, -23.4, max(sx * 1.0, sx * 2.1), 50.4, -22.8, solid(P, "eye", glow=True))
        pts = [(sx * 1.6, 48.0, -24.0), (sx * 5.0, 46.0, -22.0), (sx * 9.0, 47.0, -18.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "red"), extend=0.2)
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.8, 51.0, -18.0), ((j - 2) * 0.3, 1, 0.6), 1.0, 5.0, metal(P, "dark_light"), tip=0.8)
    for sx in (-1, 1):                                                                  # rainbow wings + feather fans
        for i in range(4):
            wb = m.bone("wing_%s_%d" % ("left" if sx > 0 else "right", i), bd, (sx * 2.0, 38.0, -2.0))
            x0, x1 = sorted((sx * 2.0, sx * (22.0 - i * 2.0)))
            m.box(wb, x0, 38.0, -2.0 + i * 1.6, x1, 44.0, -1.8 + i * 1.6, _wing(i),
                  rotation=(0, 0, sx * (40 - i * 20)), pivot=(sx * 2.0, 40.0, -1.9 + i * 1.6))
        fb = m.bone("fan_left" if sx > 0 else "fan_right", bd, (sx * 3.0, 20.0, 0))
        feather_wing(m, fb, (sx * 3.0, 20.0, 0), 12.0, 8.0, 2, feathers(P, "white", "red"), side=sx, sweep=60,
                     droop=10.0)
    return m
