"""Chibi Kiwimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a tiny kiwi bird. A round brown hatched-feather body under a white hood that sweeps forward into
a long pointed grey beak, one sharp red eye, a little three-fingered wing reaching out, and two thin black legs with
splayed toes. Child stage.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import feathers, metal, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a tiny round brown kiwi bird under a white hood that sweeps into a long grey beak, with one sharp red eye"
BASE = {"brown": (140, 96, 50), "brown_dark": (80, 50, 20), "hood": (236, 236, 240), "hood_dark": (170, 172, 184),
        "beak": (170, 174, 186), "beak_dark": (100, 104, 116), "eye": (220, 30, 40), "pupil": (40, 10, 10),
        "white": (255, 255, 255), "black": (24, 24, 28)}
SHINY = {"brown": (80, 120, 60), "brown_dark": (30, 70, 24), "hood": (250, 220, 120), "hood_dark": (200, 160, 60)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "brown", "brown_dark", size=(0.8, 1.4))


def hoodf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(y - 16.4) < 1.2 and abs(z + 2.0) < 1.6:
        d = math.hypot(y - 16.4, z + 2.0)
        if d < 1.2:
            return tone(p["pupil"] if d < 0.5 else p["eye"], face), None
    return metal(P, "hood", dark="hood_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chibikiwimon")
    top = m.bone("chibikiwimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 12.0, 1.0), 6.6, FEATH, layers=6)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0.0, 6.0, 5.6, 13.0, 19.6, hoodf, cut=2)                     # the white hood
    for i in range(5):                                                             # long pointed beak
        z0 = -5.0 - i * 2.4
        w = 3.0 - i * 0.55
        m.box(hd, -w, 14.6 - i * 0.3, z0 - 2.6, w, 17.6 - i * 0.5, z0, metal(P, "beak", dark="beak_dark"))
    for sx in (-1, 1):
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 2.0, 6.0, 1.0))
        rod(m, lg, (sx * 2.0, 6.4, 1.0), (sx * 2.4, 0.6, 0.6), 1, solid(P, "black"), extend=0.2)
        for d in ((-0.5, 0, -1), (0.5, 0, -1), (0, 0, 1)):
            rod(m, lg, (sx * 2.4, 0.4, 0.6), (sx * 2.4 + d[0] * 1.6, 0.4, 0.6 + d[2] * 1.8), 1, solid(P, "black"),
                extend=0)
    ab = m.bone("arm_left", bd, (5, 11, -1))                                       # the little wing hand
    rod(m, ab, (5.0, 11.0, -1.0), (9.0, 11.6, -3.0), 1, solid(P, "black"), extend=0.2)
    for j, d in enumerate(((1, 0.6, -0.4), (1, 0, -0.6), (1, -0.6, -0.4))):
        rod(m, ab, (9.0, 11.6, -3.0), (9.0 + d[0] * 2.0, 11.6 + d[1] * 2.0, -3.0 + d[2] * 2.0), 1, solid(P, "black"),
            extend=0)
    return m
