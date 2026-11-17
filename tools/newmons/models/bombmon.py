"""Bombmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a baby bomb. A round navy-blue ball streaked with darker hatching, big round white eyes, a wide
toothy grin, and a short ribbed steel fuse on top sprouting a ragged orange spark. Baby I.

Front is -z, y is up. 22 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fbm, local, metal, solid
from _route import pal, tone

HEIGHT = 22
SCALE, HITBOX = sized(0.35, HEIGHT, 0.35)
KIND = "floater"
K = 4
LOOK = "a round navy-blue bomb with big white eyes, a toothy grin and a steel fuse sprouting an orange spark"
BASE = {"navy": (40, 70, 170), "navy_dark": (14, 24, 80), "navy_light": (90, 130, 230), "white": (250, 250, 250),
        "pupil": (16, 16, 24), "tooth": (240, 240, 236), "mouth": (20, 20, 40), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "spark": (250, 120, 40), "spark_light": (255, 220, 120)}
SHINY = {"navy": (170, 40, 50), "navy_dark": (80, 10, 16), "navy_light": (240, 110, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def ballf(x, y, z, face, variant, box=None, **k):
    """Navy with dark hatching; on the front, two big round eyes and a grin of teeth."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 3.6, y - 9.6)
            if d < 1.9:
                return tone(p["pupil"] if math.hypot(x - sx * 3.4, y - 9.6) < 0.9 else
                            p["white"] if d < 1.5 else p["pupil"], face), None
        if 4.4 < y < 6.6 and abs(x) < 5.0 - (6.6 - y) * 0.6:
            return tone(p["mouth"] if abs(y - 5.5) < 0.3 else p["tooth"] if (x * 1.3) % 1.3 > 0.25
                        else p["mouth"], face), None
    h = abs(((x + y * 0.7 + z * 0.3) * 1.6) % 1 - 0.5) < 0.1
    col = p["navy_dark"] if h and fbm(x * 0.5, y * 0.5, z * 0.5, 3) > 0.45 else p["navy"]
    if face == "up":
        col = p["navy_light"]
    return tone(col, face), None


def build():
    m = Model("bombmon")
    top = m.bone("bombmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 8.0, 0), 7.6, ballf, layers=7)
    m.round_box(bd, 0, 0, 1.4, 1.4, 15.0, 18.0, metal(P, "steel", dark="steel_dark"), cut=1)
    for y in (15.8, 17.0):
        m.round_box(bd, 0, 0, 1.6, 1.6, y, y + 0.5, solid(P, "steel_dark"), cut=1)
    for i in range(7):                                                           # the ragged spark
        ang = math.radians(i * 51)
        spike(m, bd, (0, 18.4, 0), (math.cos(ang), 1.2, math.sin(ang)), 1.0, 3.0,
              solid(P, "spark" if i % 2 else "spark_light", glow=True))
    return m
