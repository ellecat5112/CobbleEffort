"""Amon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a spirit
of living crimson flame with a demon's face: slanted glowing yellow eyes, a jagged fanged mouth, horn-like flame
points and a long flickering tail of fire rising from its crown. 15 blocks tall.

Front is -z, y is up. 46 units tall; no level known (Adult used).
"""
from __future__ import annotations

import math

from _boxmodel import Model
from _digi import sized
from _digidetail import cutout, flame_inside, local, mix, plane
from _route import pal, tone

HEIGHT = 46
SCALE, HITBOX = sized(15, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "a spirit of crimson flame with a demon's face: glowing yellow eyes, a jagged fanged mouth and a tail of fire"
BASE = {"flame": (230, 50, 50, 230), "flame_core": (255, 120, 110, 240), "flame_dark": (150, 20, 30, 230),
        "eye": (255, 230, 60), "mouth": (90, 10, 20, 240), "fang": (255, 200, 190, 240)}
SHINY = {"flame": (60, 120, 240, 230), "flame_core": (140, 200, 255, 240), "flame_dark": (20, 50, 150, 230),
         "eye": (255, 255, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    c = mix(p["flame_core"], p["flame"], min(1.0, t * 1.6 + abs(u / max(W, 1e-6) - 0.5)))
    return c, c[:3]


def facef(x, y, z, face, variant, box=None, **k):
    """The demon face on the front of its core: slanted yellow eyes, a jagged mouth with fangs."""
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            du, dv = a - sx * 3.2, (b - 17.0) - 0.5 * sx * (a - sx * 3.2)
            if abs(du) < 2.0 and abs(dv) < 0.8 - 0.3 * abs(du):
                return p["eye"], p["eye"]
        jag = 0.8 * abs(((a * 0.9) % 2) - 1)
        if abs(a) < 5.0 and 9.0 + jag < b < 13.0 - jag:
            return (p["fang"] if (b < 9.9 + jag or b > 12.1 - jag) else p["mouth"]), None
    return flamef(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("amon")
    top = m.bone("amon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(5):                                           # the core: a rounded mass of flame
        r = 7.0 - abs(i - 2) * 1.3
        m.round_box(bd, 0, 0, r, r * 0.7, 6.0 + i * 4.0, 10.6 + i * 4.0, facef, cut=2)
    fl = m.bone("cap", bd, (0, 24, 0))
    shape = cutout(flame_inside(4, 0.15, 3), flamef)
    for ang in (0, 60, 120):                                     # tongues of fire licking up from it
        m.box(fl, -8.0, 14.0, 0, 8.0, 46.0, 0, shape, rotation=(0, ang, 0), pivot=(0, 24, 0))
    for sx in (-1, 1):                                           # flame horns and side spikes
        m.box(fl, sx * 4.0 - 3.0, 20.0, -1.0, sx * 4.0 + 3.0, 32.0, -1.0, cutout(flame_inside(2, sx * 0.3, 5), flamef),
              rotation=(0, 0, -sx * 20), pivot=(sx * 4.0, 22.0, -1.0))
        m.box(bd, sx * 6.0, 8.0, -1.0, sx * 12.0, 20.0, -1.0, cutout(flame_inside(3, sx * 0.4, 7), flamef),
              rotation=(0, 0, -sx * 50), pivot=(sx * 6.0, 12.0, -1.0))
    m.box(bd, -4.0, 0.0, 0, 4.0, 8.0, 0, cutout(flame_inside(3, 0.0, 9), flamef), rotation=(180, 0, 0),
          pivot=(0, 6.0, 0))                                     # wisps trailing below
    return m
