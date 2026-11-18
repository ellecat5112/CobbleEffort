"""Gigantic Pumpmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): a giant grinning jack-o'-lantern with a glowing triangular eye, carrying on its head a woven basket
overflowing with Halloween treats (a candy cane, lollipops, a teddy, a ribbon bow) under a smaller pumpkin wearing a
little hat, with a purple witch's hat and a tiny green pumpkin at its side. 35 blocks tall.

Front is -z, y is up. 56 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, skin, solid, twisted
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a giant grinning jack-o'-lantern with a glowing eye carrying a basket overflowing with Halloween treats and a "
        "smaller pumpkin on top")
BASE = {"orange": (240, 150, 40), "orange_dark": (180, 90, 14), "face": (60, 30, 10), "glow": (255, 220, 60),
        "stem": (90, 120, 50), "basket": (150, 100, 50), "basket_dark": (90, 56, 20), "red": (220, 40, 40),
        "white": (250, 250, 250), "pink": (240, 150, 220), "violet": (90, 70, 200), "violet_dark": (40, 30, 120),
        "teddy": (230, 200, 120), "green": (170, 200, 60), "green_dark": (110, 140, 20), "bow": (250, 110, 40)}
SHINY = {"orange": (200, 200, 220), "orange_dark": (130, 130, 150), "glow": (120, 220, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def pumpkinf(cy, scale, eye_glow=True):
    SK = skin(P, "orange", dark="orange_dark")

    def f(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            u, v = x / scale, (y - cy) / scale
            if abs(u) < 7.0 and -5.0 < v < -1.6 and abs(v + 3.3 + 0.08 * u * u) < 1.3 and (abs(u * 1.3) % 2.6) > 0.5:
                return tone(p["face"], face), None
            for su in (-1, 1):
                if 0.6 < v < 4.4 and abs(u - su * 3.4) < (4.4 - v) * 0.6:
                    if su > 0 and eye_glow and abs(u - 3.4) < (4.4 - v) * 0.3 and v < 2.6:
                        return p["glow"], p["glow"]
                    return tone(p["face"], face), None
        if face in ("east", "west", "north", "south") and abs((math.atan2(z, x) * 8 / math.pi) % 2.0 - 1.0) < 0.12:
            return tone(p["orange_dark"], face), None
        return SK(x, y, z, face, variant, box=box, **k)
    return f


def build():
    m = Model("giganticpumpmon")
    top = m.bone("giganticpumpmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    ball(m, bd, (0, 14.0, 0), 14.0, pumpkinf(14.0, 1.6), layers=7, ry=12.0)          # the giant jack-o'-lantern
    hd = m.bone("head", bd, (0, 26, 0))
    m.round_box(hd, 0, 0, 10.0, 8.0, 25.0, 34.0, twisted(P, "basket", "basket_dark", period=1.4, angle=0.8), cut=3)
    rod(m, hd, (-8.0, 34.0, 0), (8.0, 34.0, 0), 1, twisted(P, "basket", "basket_dark"), extend=0)
    ball(m, hd, (1.0, 40.0, 0), 6.0, pumpkinf(40.0, 0.7, eye_glow=False), layers=4, ry=5.0)     # smaller pumpkin
    rod(m, hd, (1.0, 45.0, 0), (1.6, 48.0, 0.4), 1, solid(P, "stem"), extend=0, t2=2)
    rod(m, hd, (-8.0, 30.0, 0), (-10.0, 42.0, -1.0), 1, solid(P, "red"), extend=0, t2=1)        # candy cane
    rod(m, hd, (-10.0, 42.0, -1.0), (-12.0, 44.0, -1.0), 1, solid(P, "white"), extend=0, t2=1)
    rod(m, hd, (7.0, 32.0, -2.0), (8.0, 44.0, -2.0), 1, solid(P, "white"), extend=0, t2=1)       # lollipop
    m.round_box(hd, 8.0, -2.0, 2.4, 0.6, 43.0, 47.8, solid(P, "pink"), cut=0)
    m.round_box(hd, -4.0, -4.0, 2.0, 1.6, 33.0, 37.0, solid(P, "teddy"), cut=1)                 # teddy
    m.round_box(hd, 6.0, -8.4, 2.4, 0.8, 30.0, 33.0, solid(P, "bow"), cut=0)                    # ribbon bow
    hat = m.bone("hat", bd, (14, 16, -2))                                                        # witch's hat
    m.round_box(hat, 14.0, -2.0, 5.0, 5.0, 14.0, 15.0, fabric(P, "violet", "violet_dark"), cut=2)
    spike(m, hat, (14.0, 15.0, -2.0), (0.4, 1, 0), 4.0, 8.0, fabric(P, "violet", "violet_dark"), tip=1.6)
    ball(m, bd, (18.0, 3.0, -4.0), 3.0, skin(P, "green", dark="green_dark"), layers=3)           # little green pumpkin
    return m
