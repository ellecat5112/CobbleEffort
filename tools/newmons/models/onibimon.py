"""Onibimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little will-o'-the-wisp: a pale-blue teardrop of ghost-fire with one big magenta eye, a wide grin of
sharp teeth, and a wispy tail curling off into dark flame. 0.5 blocks tall.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a pale-blue teardrop of ghost-fire with one big magenta eye, a wide toothy grin and a wispy tail"
BASE = {"blue": (150, 210, 250, 230), "blue_dark": (80, 150, 220), "eye": (230, 60, 150), "white": (250, 250, 255),
        "pupil": (20, 10, 20), "tooth": (250, 250, 250), "mouth": (30, 40, 80), "dark": (30, 40, 60)}
SHINY = {"blue": (180, 250, 170, 230), "blue_dark": (100, 200, 110), "eye": (240, 180, 40)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["blue"]
    return c, c[:3]


def build():
    m = Model("onibimon")
    top = m.bone("onibimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 10.0, 0), 5.0, bodyf, layers=5, ry=4.6)
    spike(m, bd, (0, 14.0, 0.6), (0.3, 1, 0.4), 3.0, 4.0, bodyf, tip=0.8)
    ball(m, bd, (0, 11.0, -4.0), 2.0, solid(P, "white"), layers=2, squash=0.5)
    m.box(bd, -1.2, 10.0, -5.15, 1.2, 12.2, -5.0, solid(P, "eye"))
    m.box(bd, -0.5, 10.6, -5.2, 0.5, 11.6, -5.15, solid(P, "pupil"))
    m.box(bd, -3.0, 7.0, -5.0, 3.0, 8.0, -4.8, solid(P, "mouth"))
    for j in range(6):
        spike(m, bd, (-2.6 + j * 1.04, 8.0, -4.9), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
    pts = [(0, 6.0, 1.0), (1.0, 3.0, 2.0), (-1.0, 1.0, 2.6), (0.6, 0.0, 3.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bd, p0, p1, 1, solid(P, "dark"), extend=0.2, t2=2)
    return m
