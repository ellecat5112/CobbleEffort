"""Black King Numemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the king of the slugs, in grey. A glossy grey slug body with a sleepy proud face, a
drooping moustache, two eyestalks with red-ringed eyes, and a huge silver crown with gold-ball points and an engraved
crest resting on its back. 25 blocks tall.

Front is -z, y is up. 50 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, local, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("the king of the slugs: a glossy grey slug with a sleepy proud face, a moustache, red-ringed eyestalks and a "
        "huge silver crown with gold-ball points")
BASE = {"grey": (160, 160, 170), "grey_dark": (90, 90, 100), "grey_light": (220, 220, 230), "silver": (210, 214, 226),
        "silver_dark": (110, 114, 128), "gold": (250, 210, 60), "gold_dark": (180, 130, 20), "black": (30, 30, 36),
        "eye": (220, 40, 50), "pupil": (40, 10, 10), "white": (250, 250, 250)}
SHINY = {"grey": (90, 90, 100), "grey_dark": (40, 40, 48), "grey_light": (160, 160, 176), "silver": (240, 210, 120),
         "silver_dark": (170, 130, 40)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "grey", dark="grey_dark", light="grey_light", var=0.03)


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for sx in (-1, 1):
            if abs(b - 22.0 + 0.1 * (a - sx * 3.0) ** 2) < 0.3 and abs(a - sx * 3.0) < 2.0:
                return p["black"], None                          # half-closed eyes
            if abs(a - sx * 2.6) < 2.0 and abs(b - 18.0 - 0.5 * abs(a - sx * 2.6)) < 0.3:
                return p["black"], None                          # moustache
        if abs(b - 16.0) < 0.25 and abs(a) < 1.4:
            return p["black"], None
    return BODY(x, y, z, face, variant, box=box, **k)


def crownf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west", "south"):
        a, b = plane(x, y, z, face)
        if math.hypot(a % 8.0 - 4.0, b - 30.0) < 1.0:
            return tone(p["black"], face), None                  # engraved crest
    return metal(P, "silver", dark="silver_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("blackkingnumemon")
    top = m.bone("blackkingnumemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(7):                                           # slug foot, front rising into the head
        z0 = -12.0 + i * 4.0
        r = 7.0 - abs(i - 2) * 0.6
        m.round_box(bd, 0, z0 + 2.0, r, 2.4, 0.0, 6.0 + max(0, 4 - i) * 4.0, BODY, cut=2)
    hd = m.bone("head", bd, (0, 20, -8))
    ball(m, hd, (0, 20.0, -9.0), 7.0, facef, layers=6, ry=8.0)
    for sx in (-1, 1):                                           # eyestalks
        rod(m, hd, (sx * 2.4, 26.0, -8.0), (sx * 4.4, 36.0, -10.0), 1, BODY, extend=0.3)
        ball(m, hd, (sx * 4.6, 38.0, -10.4), 2.4, solid(P, "white"), layers=3)
        m.box(hd, sx * 4.6 - 1.0, 37.0, -12.9, sx * 4.6 + 1.0, 39.0, -12.6, solid(P, "eye"))
    cr = m.bone("cap", bd, (0, 22, 8))                            # the huge crown on its back
    for i in range(12):
        ang = math.radians(i * 30)
        c = (5.4 * math.cos(ang), 26.0, 9.0 + 5.4 * math.sin(ang))
        m.box(cr, c[0] - 1.6, 20.0, c[2] - 0.6, c[0] + 1.6, 32.0, c[2] + 0.6, crownf,
              rotation=(0, -math.degrees(ang) + 90, 0), pivot=c)
    for i in range(6):
        ang = math.radians(i * 60)
        c = (5.4 * math.cos(ang), 36.0, 9.0 + 5.4 * math.sin(ang))
        spike(m, cr, (c[0], 32.0, c[2]), (0, 1, 0), 2.4, 3.0, crownf)
        ball(m, cr, c, 1.6, metal(P, "gold", dark="gold_dark"), layers=2)
    return m
