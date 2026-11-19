"""Trailmon Ball (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the art on
wikimon.net): the little rail-cart Trailmon: a round yellow ball with one droopy blue eye and its tongue poking out,
riding a small grey rail cart with jointed mechanical arms ending in orange grippers, an orange gas cylinder on its
back, and a pink parasol raised over it. 15 blocks tall.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fabric, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = "a round yellow ball with one droopy blue eye and its tongue out, riding a little rail cart with mechanical arms under a pink parasol"
BASE = {"yellow": (240, 230, 60), "yellow_dark": (180, 160, 20), "eye": (60, 150, 230), "pupil": (10, 20, 40),
        "white": (255, 255, 255), "tongue": (220, 60, 70), "grey": (170, 174, 186), "grey_dark": (80, 84, 96),
        "orange": (240, 130, 50), "pink": (240, 160, 200), "pink_dark": (190, 100, 150), "black": (30, 30, 34)}
SHINY = {"yellow": (120, 220, 200), "yellow_dark": (60, 150, 130), "pink": (170, 160, 250), "pink_dark": (110, 100, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def ballf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        c = eye(p, a, b - 17.6, 2.4, "eye", lid="yellow")
        if c is not None:
            if b > 18.6:
                return tone(p["yellow"], face), None
            return c, None
    return skin(P, "yellow", dark="yellow_dark")(x, y, z, face, variant, box=box, **k)


GREY = metal(P, "grey", dark="grey_dark")


def build():
    m = Model("trailmonball")
    top = m.bone("trailmonball", None, (0, 0, 0))
    m.box(top, -4.0, 1.6, -3.0, 4.0, 3.0, 3.0, GREY)                                    # rail cart
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.round_box(top, sx * 3.0, sz * 2.4, 1.4, 1.4, 0.0, 1.6, solid(P, "black"), cut=0)
    bd = m.bone("body", top, (0, 10, 0))
    rod(m, bd, (0, 3.0, 0), (0, 8.0, 0), 1, GREY, extend=0.2)
    ball(m, bd, (0, 15.0, 0), 7.0, ballf, layers=6)
    m.box(bd, -1.4, 10.0, -7.4, 1.4, 12.6, -6.4, solid(P, "tongue"), rotation=(30, 0, 0), pivot=(0, 12.0, -6.6))
    m.round_box(bd, 0, 7.0, 2.0, 2.0, 11.0, 19.0, solid(P, "orange"), cut=1)             # gas cylinder
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 12.0, 0))
        pts = [(sx * 6.0, 12.0, 0), (sx * 10.0, 10.0, -1.0), (sx * 10.0, 6.0, -3.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, GREY, extend=0.3)
        m.round_box(ab, sx * 10.0, -3.6, 1.6, 1.6, 4.0, 6.4, solid(P, "orange"), cut=1)
    pb = m.bone("parasol", bd, (2.0, 22, 2))                                            # pink parasol
    rod(m, pb, (2.0, 14.0, 4.0), (2.0, 34.0, 4.0), 1, GREY, extend=0.0)
    for i in range(8):
        ang = i * 2 * math.pi / 8
        cx, cz = 2.0 + 6.0 * math.cos(ang), 4.0 + 6.0 * math.sin(ang)
        m.box(pb, cx - 3.4, 32.0, cz - 3.4, cx + 3.4, 33.2, cz + 3.4, fabric(P, "pink", "pink_dark"),
              rotation=(math.degrees(math.sin(ang)) * 0.3, 0, -math.degrees(math.cos(ang)) * 0.3), pivot=(cx, 32.6, cz))
    m.round_box(pb, 2.0, 4.0, 4.0, 4.0, 33.0, 35.6, fabric(P, "pink", "pink_dark"), cut=2)
    return m
