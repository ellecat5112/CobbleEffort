"""Funbeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little bumblebee. A round amber-orange bee with a big round head, large green eyes, a grey muzzle, two long blue
antennae, a fluffy chubby body ringed in dark brown, a grey sting, six stubby legs ending in big brown tipped claws
and four smoky translucent wings. Child stage, 1 block tall.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, local, metal, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "floater"
K = 4
LOOK = ("a round amber bee with big green eyes, a grey muzzle, long blue antennae, a fluffy dark-ringed body, a grey "
        "sting, stubby legs with big brown claws and four smoky wings")
BASE = {"amber": (250, 180, 40), "amber_dark": (200, 120, 10), "amber_light": (255, 230, 140), "brown": (110, 60, 30),
        "claw": (190, 100, 40), "claw_tip": (110, 50, 20), "grey": (170, 174, 186), "grey_dark": (90, 94, 106),
        "eye": (60, 200, 110), "pupil": (16, 30, 20), "shine": (250, 250, 250), "blue": (40, 60, 180),
        "wing": (90, 90, 100, 130), "vein": (50, 50, 60, 200)}
SHINY = {"amber": (250, 140, 200), "amber_dark": (200, 80, 150), "amber_light": (255, 210, 240)}


def P(v):
    return pal(BASE, SHINY, v)


FLUFF = fur(P, "amber", "amber_dark", tip="amber_light", length=0.8, density=2.0)


def ringf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (z * 0.6) % 2.4 < 0.7:
        return tone(p["brown"], face), None
    return FLUFF(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west"):
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 14.6) if face == "north" else math.hypot(z + 4.0, y - 14.6)
            if face != "north" and (sx > 0) != (face == "east"):
                continue
            if d < 0.4:
                return tone(p["shine"], face), None
            if d < 0.9:
                return tone(p["pupil"], face), None
            if d < 1.6:
                return tone(p["eye"], face), None
    return FLUFF(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if (u % 2.2) < 0.25 or abs(v - H * 0.5) < 0.2:
        return p["vein"], None
    return p["wing"], None


def build():
    m = Model("funbeemon")
    top = m.bone("funbeemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 10.0, 4.0), 5.4, ringf, layers=5)                                    # chubby ringed body
    spike(m, bd, (0, 8.0, 9.0), (0, -0.4, 1), 1.0, 2.4, metal(P, "grey", dark="grey_dark"), tip=0.2)
    hd = m.bone("head", bd, (0, 14, -3))
    ball(m, hd, (0, 14.0, -3.0), 4.4, headf, layers=4)
    m.round_box(hd, 0, -7.2, 1.6, 1.0, 11.6, 13.6, metal(P, "grey", dark="grey_dark"), cut=0)   # grey muzzle
    for sx in (-1, 1):                                                                   # long blue antennae
        rod(m, hd, (sx * 1.4, 18.0, -4.0), (sx * 4.0, 22.0, -6.0), 1, solid(P, "blue"), extend=0.2, t2=1)
        rod(m, hd, (sx * 4.0, 22.0, -6.0), (sx * 7.0, 20.0, -8.0), 1, solid(P, "blue"), extend=0.2, t2=1)
    for side in (1, -1):                                                                 # four smoky wings
        for j, ang in enumerate((30, 0)):
            x0, x1 = sorted((side * 2.0, side * (12.0 - j * 3.0)))
            m.box(bd, x0, 14.0 - j * 1.6, 3.0 + j, x1, 18.0 - j * 1.6, 3.0 + j, wingf,
                  rotation=(0, side * 25, side * ang), pivot=(side * 2.0, 15.0, 3.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                  # stubby legs, big claws
        lg = m.bone(nm, bd, (sx * 3.0, 6.0, 1.0))
        for j, dz in enumerate((-2.0, 1.0, 4.0)):
            m.round_box(lg, sx * 3.6, dz, 1.2, 1.2, 3.0, 6.0, FLUFF, cut=0)
            spike(m, lg, (sx * 3.8, 3.0, dz - 0.6), (sx * 0.2, -1, -0.3), 1.4, 3.0, solid(P, "claw"), tip=0.3)
    return m
