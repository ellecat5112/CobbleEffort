"""Great King Scumon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): the king of the sludge: a big yellow slime with a gaping mouth of square teeth and a long lolling pink
tongue, two thin clawed arms bound in iron cuffs, a little crown of grey castle turrets on its head and a cloud of
sparkles around it. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "floater"
K = 3
LOOK = ("a big yellow slime king with a gaping mouth of square teeth, a long pink tongue, thin clawed arms in iron cuffs "
        "and a crown of grey castle turrets")
BASE = {"yellow": (250, 214, 50), "yellow_dark": (200, 150, 20), "yellow_light": (255, 245, 170), "mouth": (40, 14, 20),
        "tooth": (250, 250, 240), "tongue": (220, 60, 90), "tongue_dark": (150, 20, 50), "grey": (170, 170, 180),
        "grey_dark": (90, 90, 100), "iron": (60, 60, 66), "iron_dark": (24, 24, 30), "claw": (240, 236, 220),
        "spark": (255, 240, 140)}
SHINY = {"yellow": (180, 230, 120), "yellow_dark": (110, 170, 60), "yellow_light": (230, 255, 190)}


def P(v):
    return pal(BASE, SHINY, v)


SLIME = skin(P, "yellow", dark="yellow_dark", light="yellow_light")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 9.0 and 10.0 < y < 20.0:
        if y > 17.6 and (x % 2.6) < 2.0:
            return tone(p["tooth"], face), None
        if y < 12.4 and (x % 2.6) < 2.0:
            return tone(p["tooth"], face), None
        return tone(p["mouth"], face), None
    return SLIME(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("greatkingscumon")
    top = m.bone("greatkingscumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 15.0, 0), 11.0, bodyf, layers=6, ry=10.0)
    rod(m, bd, (2.0, 11.0, -10.0), (4.0, 2.0, -16.0), 4, skin(P, "tongue", dark="tongue_dark"), extend=0.4, t2=2)
    hd = m.bone("head", bd, (0, 25, 0))
    m.round_box(hd, 0, 0, 5.0, 4.0, 24.0, 27.0, riveted(P, "grey", "grey_dark"), cut=1)       # castle-turret crown
    for j in range(4):
        x = -3.6 + j * 2.4
        m.box(hd, x - 0.8, 27.0, -1.0, x + 0.8, 30.0 + (j % 2), 1.0, metal(P, "grey", dark="grey_dark"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 9.0, 18.0, 0))
        pts = [(sx * 9.0, 18.0, 0), (sx * 15.0, 24.0, -2.0), (sx * 20.0, 12.0, -4.0), (sx * 22.0, 4.0, -6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, SLIME, extend=0.4)
        m.round_box(ab, sx * 20.0, -4.0, 2.0, 2.0, 11.0, 14.0, riveted(P, "iron", "iron_dark"), cut=1)  # iron cuffs
        for j in range(4):
            spike(m, ab, (sx * 22.0 + (j - 1.5) * 0.9, 3.0, -6.0), (sx * 0.3 * (j - 1.5), -1, -0.4), 0.8, 3.0,
                  solid(P, "claw"), tip=0.8)
    for c in ((-12.0, 28.0, -4.0), (12.0, 30.0, -2.0), (-16.0, 20.0, 2.0), (6.0, 34.0, 2.0)):
        spike(m, bd, c, (0, 1, 0), 1.0, 2.0, solid(P, "spark", glow=True))
    return m
