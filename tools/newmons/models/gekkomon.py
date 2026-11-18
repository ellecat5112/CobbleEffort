"""Gekkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
cheeky gecko: a lime-green lizard with a spiky crest edged magenta, a crescent moon on its brow, big round eyes, a
long lolling pink tongue, a yellow-plated belly, blue padded paws with pink suction pads and a very long, zig-zag
tail striped pink and black. Child stage, 1 block tall.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a lime-green gecko with a magenta-edged spiky crest, a crescent moon on its brow, a pink tongue, blue padded "
        "paws and a long zig-zag pink-striped tail")
BASE = {"green": (120, 230, 60), "green_dark": (60, 160, 20), "magenta": (220, 40, 140), "belly": (250, 230, 70),
        "belly_dark": (200, 170, 20), "blue": (60, 130, 230), "blue_dark": (20, 60, 150), "pink": (250, 120, 180),
        "black": (30, 28, 32), "white": (250, 250, 250), "eye": (40, 40, 44), "moon": (250, 200, 40)}
SHINY = {"green": (250, 140, 60), "green_dark": (200, 80, 20), "blue": (140, 60, 200), "blue_dark": (70, 20, 120)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")
BLUE = skin(P, "blue", dark="blue_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.0:
        return tone(p["belly"] if (y % 1.6) > 0.3 else p["belly_dark"], face), None
    return GREEN(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 18.0)
            if d < 0.7:
                return tone(p["eye"], face), None
            if d < 1.6:
                return tone(p["white"], face), None
        if abs(math.hypot(x, y - 21.6) - 1.0) < 0.3 and y > 21.4:
            return tone(p["moon"], face), None
    return GREEN(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = (x + y + z) % 3.0
    return tone(p["pink"] if t < 0.8 else p["black"] if t < 1.1 else p["green"], face), None


def build():
    m = Model("gekkomon")
    top = m.bone("gekkomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.4, 3.4, 3.0, 4.0, 13.0, bodyf, cut=1)
    hd = m.bone("head", bd, (0, 13, -1))
    m.round_box(hd, 0, -1.0, 4.4, 3.6, 12.6, 22.0, headf, cut=2)
    rod(m, hd, (0, 14.6, -4.8), (1.0, 10.0, -7.0), 2, skin(P, "pink", dark="magenta"), extend=0.3, t2=1)   # tongue
    for j in range(6):                                                                 # spiky crest
        ang = math.radians(-70 + j * 28)
        spike(m, hd, (3.0 * math.sin(ang), 21.6, 0.6 + 1.6 * math.cos(ang)), (math.sin(ang) * 0.6, 1, 0.6), 1.4,
              4.0 + (j % 2) * 2.0, solid(P, "magenta" if j % 2 else "green"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 11.0, -1.0))
        rod(m, ab, (sx * 3.4, 11.0, -1.0), (sx * 6.4, 9.0, -2.4), 1, GREEN, extend=0.3, t2=2)
        m.round_box(ab, sx * 7.4, -2.6, 1.8, 1.8, 7.4, 11.0, BLUE, cut=1)
        m.round_box(ab, sx * 7.4, -4.5, 1.0, 0.2, 8.6, 9.8, solid(P, "pink"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 5.0, 0))
        rod(m, lg, (sx * 2.4, 5.0, 0), (sx * 4.0, 2.0, -3.0), 2, GREEN, extend=0.3)
        m.round_box(lg, sx * 4.4, -4.0, 2.0, 2.0, 0.0, 3.0, BLUE, cut=1)
        m.round_box(lg, sx * 4.4, -6.1, 1.0, 0.2, 0.8, 2.2, solid(P, "pink"), cut=0)
    tb = m.bone("tail", bd, (0, 5, 3))                                                  # long zig-zag tail
    pts = [(0, 5.0, 3.0), (4.0, 3.0, 8.0), (10.0, 10.0, 12.0), (6.0, 18.0, 14.0), (12.0, 26.0, 14.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 2, tailf, extend=0.4)
    return m
