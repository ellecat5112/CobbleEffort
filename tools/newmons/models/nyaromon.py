"""Nyaromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a round pale-yellow cat head with no body, two pointed ears, big red-brown eyes, a little zigzag
mouth and a long curling tail banded yellow and violet. 0.5 blocks tall.

Front is -z, y is up. 16 units tall; Baby II stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 16
SCALE, HITBOX = sized(0.5, HEIGHT, 1.2)
KIND = "floater"
K = 3
LOOK = "a round pale-yellow cat head with pointed ears, big red-brown eyes, a zigzag mouth and a long yellow-and-violet tail"
BASE = {"yellow": (250, 226, 110), "yellow_dark": (210, 170, 50), "violet": (140, 110, 200), "eye": (170, 60, 40),
        "white": (250, 250, 250), "black": (30, 26, 26)}
SHINY = {"yellow": (240, 200, 220), "yellow_dark": (200, 140, 170), "violet": (90, 170, 200)}


def P(v):
    return pal(BASE, SHINY, v)


HEAD = skin(P, "yellow", dark="yellow_dark", var=0.02)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["violet"] if (y + z) % 3.0 < 1.2 else p["yellow"], face), None


def build():
    m = Model("nyaromon")
    top = m.bone("nyaromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 5.0, 0), 5.6, HEAD, layers=5, ry=4.4, squash=0.8)
    for sx in (-1, 1):
        spike(m, bd, (sx * 3.4, 8.0, 0), (sx * 0.4, 1, 0), 2.4, 4.0, HEAD, tip=0.8)
        m.box(bd, sx * 2.0 - 1.0, 4.6, -4.55, sx * 2.0 + 1.0, 6.8, -4.4, solid(P, "eye"))
        m.box(bd, sx * 2.0 - 0.4, 6.0, -4.6, sx * 2.0 + 0.2, 6.6, -4.55, solid(P, "white"))
    for j in range(4):
        m.box(bd, -1.6 + j * 0.8, 3.0 + 0.4 * (j % 2), -4.5, -1.0 + j * 0.8, 3.4 + 0.4 * (j % 2), -4.4,
              solid(P, "black"))
    tb = m.bone("tail", bd, (3.0, 4.0, 3.0))
    pts = [(3.0, 4.0, 3.0), (6.0, 5.0, 5.0), (8.0, 9.0, 6.0), (7.0, 13.0, 6.0), (5.0, 14.0, 5.4)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, tailf, extend=0.3)
    return m
