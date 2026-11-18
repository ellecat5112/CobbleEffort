"""Lunamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
moon bunny: a small white-and-lavender rabbit with a yellow crescent moon on its brow, big pink eyes, a pale pink
moon-patterned body with a ribbon and a dark moon charm, and four long translucent blue ear-fins shaped like leaves
(two up, two out to the sides). Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, gem, local, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 2.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a small white-and-lavender moon bunny with a yellow crescent on its brow, big pink eyes and four long translucent blue ear-fins"
BASE = {"white": (250, 248, 252), "white_dark": (200, 196, 220), "lav": (240, 220, 240), "lav_dark": (200, 170, 210),
        "yellow": (250, 220, 70), "eye": (220, 60, 120), "pupil": (40, 20, 30), "fin": (150, 180, 250, 200),
        "fin_light": (230, 240, 255, 220), "navy": (50, 60, 110), "pink": (250, 190, 210)}
SHINY = {"fin": (250, 190, 120, 200), "fin_light": (255, 240, 210, 220), "lav": (220, 240, 220), "lav_dark": (160, 200, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, y - 16.6)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.3:
                return tone(p["eye"], face), None
        if abs(math.hypot(x + 0.4, y - 20.0) - 1.1) < 0.3 and x > -0.6:
            return tone(p["yellow"], face), None
    return skin(P, "white", dark="white_dark")(x, y, z, face, variant, box=box, **k)


def fin_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6)
    return abs(a) < 0.5 * math.sin(math.pi * min(1.0, b)) + 0.02


def finf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["fin_light"] if v / max(H, 1e-6) > 0.6 else p["fin"]), None


def build():
    m = Model("lunamon")
    top = m.bone("lunamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    ball(m, bd, (0, 7.0, 0), 4.6, skin(P, "lav", dark="lav_dark"), layers=4, squash=1.0)
    m.round_box(bd, 0, -4.6, 1.0, 0.4, 7.0, 9.0, gem(P, "navy", "white", glow=False), cut=0)      # moon charm
    rod(m, bd, (-2.0, 9.6, -4.0), (2.0, 9.6, -4.0), 1, solid(P, "pink"), extend=0, t2=1)
    hd = m.bone("head", bd, (0, 12, 0))
    m.round_box(hd, 0, 0, 4.0, 3.4, 11.6, 21.0, headf, cut=2)
    F = cutout(fin_in, finf)
    for sx in (-1, 1):                                                               # four ear-fins
        m.box(hd, sx * 1.6 - 1.6, 20.6, 0.4, sx * 1.6 + 1.6, 31.0, 0.4, F, rotation=(0, 0, -sx * 12), pivot=(sx * 1.6, 20.6, 0.4))
        x0, x1 = sorted((sx * 3.6, sx * 13.0))
        m.box(hd, x0, 16.0, 0.6, x1, 21.0, 0.6, F, rotation=(0, 0, sx * -20), pivot=(sx * 3.6, 18.0, 0.6))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 8.0, 0))
        spike(m, ab, (sx * 4.0, 8.0, 0), (sx, -0.2, -0.3), 1.2, 2.0, skin(P, "white", dark="white_dark"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 3.0, 0))
        m.round_box(lg, sx * 1.8, -0.6, 1.4, 2.0, 0.0, 3.0, skin(P, "white", dark="white_dark"), cut=0)
    return m
