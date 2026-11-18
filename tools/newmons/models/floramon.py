"""Floramon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
flower child. A little green-legged plant Digimon whose head is a big flower of five red, white-edged petals round a
yellow face with green eyes, its hands two lavender bell-flowers with petal claws, its body yellow, its feet green
leaf-boots with red claws. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import local, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = ("a little plant Digimon whose head is a big flower of five red white-edged petals round a yellow face, lavender "
        "bell-flower hands and green leaf-boot feet")
BASE = {"red": (220, 40, 60), "red_dark": (140, 14, 30), "edge": (250, 240, 240), "yellow": (250, 210, 60),
        "yellow_dark": (200, 150, 20), "green": (80, 170, 70), "green_dark": (30, 100, 30), "lav": (190, 150, 230),
        "lav_dark": (120, 80, 170), "eye": (40, 160, 70), "pupil": (16, 16, 20), "claw": (220, 40, 40)}
SHINY = {"red": (250, 160, 200), "red_dark": (200, 90, 140), "lav": (120, 200, 250), "lav_dark": (50, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


YELLOW = skin(P, "yellow", dark="yellow_dark")
GREEN = skin(P, "green", dark="green_dark")


def petalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if min(u, W - u) < 0.5 or v > H - 0.6:
        return tone(p["edge"], face), None
    return tone(p["red"] if v > H * 0.3 else p["red_dark"], face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.5, y - 22.6)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
    return YELLOW(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("floramon")
    top = m.bone("floramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 2.6, 2.2, 7.0, 15.0, YELLOW, cut=1)
    hd = m.bone("head", bd, (0, 16, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 16.0, 26.0, facef, cut=2)
    for i in range(5):                                                                 # five petals
        ang = math.radians(90 + i * 72)
        cx, cy = 5.0 * math.cos(ang), 21.0 + 5.0 * math.sin(ang)
        m.box(hd, cx - 3.0, cy - 3.0, 0.4, cx + 3.0, cy + 3.0, 1.4, petalf,
              rotation=(0, 0, math.degrees(ang) - 90), pivot=(cx, cy, 0.9))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                # bell-flower hands
        ab = m.bone(nm, bd, (sx * 2.6, 14.0, 0))
        rod(m, ab, (sx * 2.6, 14.0, 0), (sx * 5.0, 10.0, -1.0), 1, GREEN, extend=0.3, t2=1)
        m.round_box(ab, sx * 5.6, -1.2, 2.0, 2.0, 6.0, 10.4, skin(P, "lav", dark="lav_dark"), cut=1)
        for j in range(3):
            spike(m, ab, (sx * 5.6 + (j - 1) * 1.2, 6.2, -1.2), (0, -1, -0.2), 1.0, 1.8, solid(P, "lav_dark"), tip=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.4, 7.0, 0))
        rod(m, lg, (sx * 1.4, 7.0, 0), (sx * 1.6, 2.4, 0), 1, GREEN, extend=0.3, t2=1)
        m.round_box(lg, sx * 1.8, -0.6, 1.6, 2.4, 0.0, 2.6, GREEN, cut=1)
        for j in range(2):
            spike(m, lg, (sx * 1.8 + (j - 0.5) * 1.4, 0.6, -3.0), (0, 0, -1), 0.8, 1.2, solid(P, "claw"))
    return m
