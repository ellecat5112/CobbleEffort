"""Bibimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a tiny
ball of bright yellow spikes. A round spiky yellow body, a green crystal visor across its face over round black eyes,
a jagged mouth and a white lightning-bolt horn on top. Tiny.

Front is -z, y is up. 26 units tall; Baby II stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import gem, local, plane, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(0.5, HEIGHT, 0.45)
KIND = "floater"
K = 4
LOOK = "a tiny ball of yellow spikes with a green crystal visor, round black eyes and a white lightning-bolt horn"
BASE = {"yellow": (250, 236, 60), "yellow_dark": (200, 170, 20), "green": (60, 200, 90), "green_light": (200, 255, 200),
        "black": (20, 20, 24), "white": (250, 250, 250)}
SHINY = {"yellow": (250, 140, 190), "yellow_dark": (200, 80, 140), "green": (60, 140, 240), "green_light": (200, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "yellow", dark="yellow_dark", var=0.03)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if math.hypot(a - sx * 2.0, b - 10.6) < 1.1:
                return (p["white"] if math.hypot(a - sx * 2.0 + 0.4, b - 11.0) < 0.35 else p["black"]), None
        if abs(b - 7.6 - 0.4 * abs(((a * 1.2) % 2) - 1)) < 0.25 and abs(a) < 2.6:
            return p["black"], None
    return BODY(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bibimon")
    top = m.bone("bibimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 10.0, 0), 7.0, bodyf, layers=6)
    for i in range(16):                                          # spikes
        ang = math.radians(i * 22.5)
        el = math.radians(-20 + (i % 3) * 30)
        d = (math.cos(ang) * math.cos(el), math.sin(el), math.sin(ang) * math.cos(el))
        if d[2] < -0.6 and abs(d[1]) < 0.5:
            continue                                             # keep the face clear
        spike(m, bd, (6.0 * d[0], 10.0 + 6.0 * d[1], 6.0 * d[2]), d, 2.0, 3.0, BODY, tip=0.8)
    m.box(bd, -5.0, 11.6, -7.2, 5.0, 13.6, -6.0, gem(P, "green", "green_light"))       # crystal visor
    for j, (p0, p1) in enumerate((((0, 16.0, -2.0), (1.6, 21.0, -2.0)), ((1.6, 21.0, -2.0), (-0.6, 22.0, -2.0)),
                                  ((-0.6, 22.0, -2.0), (1.0, 26.0, -2.0)))):
        rod(m, bd, p0, p1, 2, solid(P, "white"), extend=0.3, t2=1)   # lightning-bolt horn
    return m
