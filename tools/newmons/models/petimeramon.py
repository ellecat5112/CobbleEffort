"""Peti Meramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a little ball of flame: a blazing orange fireball with dark flickering edges, two big blue eyes and
a stitched grin, flames streaming back from it and two tiny flame-feet. 0.5 blocks tall.

Front is -z, y is up. 18 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, flame_inside, local, solid
from _route import pal, tone

HEIGHT = 18
SCALE, HITBOX = sized(0.5, HEIGHT, 1.4)
KIND = "floater"
K = 3
LOOK = "a little blazing orange fireball with big blue eyes, a stitched grin and flames streaming back from it"
BASE = {"orange": (250, 140, 40), "core": (255, 220, 120), "dark": (130, 40, 14), "eye": (80, 150, 240),
        "white": (250, 250, 255), "black": (30, 20, 20), "fire": (255, 150, 40, 210), "fire_core": (255, 240, 160, 235)}
SHINY = {"orange": (90, 160, 250), "core": (200, 230, 255), "dark": (20, 40, 120), "fire": (100, 170, 255, 210),
         "fire_core": (220, 240, 255, 235)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    c = p["core"] if face == "north" and y < 8.0 else p["orange"]
    return c, c


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("petimeramon")
    top = m.bone("petimeramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 8.0, 0), 5.0, bodyf, layers=5, ry=4.6)
    for sx in (-1, 1):
        ball(m, bd, (sx * 1.8, 9.0, -4.0), 1.2, solid(P, "white"), layers=2, squash=0.5)
        m.box(bd, sx * 1.8 - 0.6, 8.4, -4.75, sx * 1.8 + 0.6, 9.6, -4.6, solid(P, "eye"))
    m.box(bd, -2.4, 6.0, -4.9, 2.4, 6.4, -4.75, solid(P, "black"))
    for j in range(5):
        m.box(bd, -2.0 + j * 1.0, 5.6, -4.95, -1.8 + j * 1.0, 6.8, -4.8, solid(P, "black"))
    for i in range(5):                                                                   # streaming flames
        c = (-2.0 + i, 8.0 + (i % 2) * 2.0, 3.0)
        for ang in (0, 90):
            m.box(bd, c[0] - 1.6, c[1], c[2], c[0] + 1.6, c[1] + 7.0, c[2], cutout(flame_inside(3, 0.3, i), firef),
                  rotation=(-50, ang, 0), pivot=c)
    for sx in (-1, 1):
        spike(m, bd, (sx * 2.0, 3.6, -1.0), (0, -1, -0.3), 1.2, 2.6, solid(P, "orange"), tip=0.8)
    return m
