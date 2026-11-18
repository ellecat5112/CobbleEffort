"""Metamormon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a mutant of shifting data: a round pale-green egg of a body with a steel knight's visor for a
face, a spiky violet crest, two small red eyes on stalks, a thin forked tail, two steel arms ending in great hooked
claws, and a crown of long red-and-green tentacle petals flaring out above it. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a round pale-green egg of a body with a steel knight's visor face, a violet crest, two steel arms with hooked "
        "claws and a crown of long red-and-green tentacle petals")
BASE = {"green": (180, 220, 140), "green_dark": (100, 150, 70), "steel": (170, 176, 200), "steel_dark": (70, 74, 96),
        "red": (200, 50, 70), "red_dark": (110, 20, 30), "petal_g": (120, 160, 90), "violet": (110, 60, 160),
        "eye": (200, 30, 40), "black": (24, 22, 30)}
SHINY = {"green": (230, 170, 200), "green_dark": (170, 100, 140), "red": (60, 120, 210), "red_dark": (24, 60, 130)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "green", dark="green_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def petalf(x, y, z, face, variant, box=None, **k):
    """Tentacle petals: green at the root shading into red at the bulbous tip."""
    p = P(variant)
    t = min(1.0, max(0.0, (y - 28.0) / 14.0 + abs(x) / 24.0))
    c = tuple(int(p["petal_g"][i] * (1 - t) + p["red"][i] * t) for i in range(3))
    return tone(c, face), None


def build():
    m = Model("metamormon")
    top = m.bone("metamormon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 20.0, 0), 9.0, BODY, layers=6, ry=10.0, squash=0.9)                   # egg body
    hd = m.bone("head", bd, (0, 20, -7))
    m.round_box(hd, 0, -7.8, 5.0, 1.2, 14.0, 24.0, armour(P, "steel", "steel_dark"), cut=1)   # knight's visor
    for j in range(3):
        m.box(hd, -4.0, 17.0 + j * 2.0, -9.1, 4.0, 17.6 + j * 2.0, -8.9, solid(P, "black"))
    for sx in (-1, 1):                                                                   # stalk eyes
        ball(m, hd, (sx * 6.0, 12.0, -6.0), 1.0, solid(P, "eye", glow=True), layers=2)
    for i in range(6):                                                                   # spiky violet crest
        spike(m, hd, ((i - 2.5) * 0.6, 29.0, -2.0 + i * 0.6), (0, 1, 0.3), 1.0, 4.0, solid(P, "violet"), tip=0.8)
    pb = m.bone("petals", bd, (0, 26, 2))                                                # tentacle petal crown
    for i in range(6):
        sx = 1 if i < 3 else -1
        j = i % 3
        ang = math.radians(25 + j * 30)
        root = (sx * 3.0, 26.0, 2.0)
        mid = (sx * (3.0 + 9.0 * math.cos(ang)), 26.0 + 9.0 * math.sin(ang) + 3.0, 2.0 + j)
        tip = (sx * (3.0 + 18.0 * math.cos(ang)), 26.0 + 16.0 * math.sin(ang) - 2.0, 3.0 + j)
        rod(m, pb, root, mid, 2, petalf, extend=0.4)
        rod(m, pb, mid, tip, 3, petalf, extend=0.4)
        ball(m, pb, tip, 2.2, petalf, layers=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # steel hooked claws
        ab = m.bone(nm, bd, (sx * 8.0, 20.0, 0))
        rod(m, ab, (sx * 8.0, 20.0, 0), (sx * 13.0, 18.0, -3.0), 2, STEEL, extend=0.4)
        ball(m, ab, (sx * 14.0, 17.0, -3.0), 2.4, STEEL, layers=3)
        for f in range(3):
            pts = [(sx * 14.0 + (f - 1) * 1.2, 15.0, -4.0), (sx * 15.0 + (f - 1) * 1.6, 11.0, -6.0),
                   (sx * 13.0 + (f - 1) * 1.6, 8.0, -5.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, STEEL, extend=0.2)
    tb = m.bone("tail", bd, (0, 10, 2))                                                  # thin forked tail
    rod(m, tb, (0, 11.0, 2.0), (1.0, 4.0, 1.0), 1, BODY, extend=0.2)
    for s in (-1, 1):
        rod(m, tb, (1.0, 4.0, 1.0), (1.0 + s * 1.2, 1.0, 0.0), 1, BODY, extend=0.2)
    return m
