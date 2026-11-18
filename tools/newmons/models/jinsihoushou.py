"""Jinsihoushou (a Digimon of the CobbleEffort: Digital crossover; hand-built after the art on wikimon.net, a manga
panel): a young golden-haired monkey warrior: a lean simian with a shaggy mane of pale fur, a serious face with a pale
muzzle and big eyes, long arms with knuckles that brush the ground, a pale belly and a long curling tail. Child stage,
1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a lean golden-haired monkey with a shaggy pale mane, a serious pale-muzzled face, long knuckle-walking arms and a curling tail"
BASE = {"fur": (210, 180, 120), "fur_dark": (140, 110, 60), "pale": (246, 230, 200), "pale_dark": (200, 180, 150),
        "eye": (40, 30, 24), "white": (250, 250, 250), "nose": (90, 60, 50)}
SHINY = {"fur": (190, 190, 200), "fur_dark": (110, 110, 124)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.3, y - 22.6)
            if d < 0.45:
                return tone(p["eye"], face), None
            if d < 0.8:
                return tone(p["white"], face), None
        if abs(y - 20.6) < 0.3 and abs(x) < 0.5:
            return tone(p["nose"], face), None
    return skin(P, "pale", dark="pale_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jinsihoushou")
    top = m.bone("jinsihoushou", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.4, 3.0, 2.6, 9.0, 18.0, FUR, cut=1)
    m.round_box(bd, 0, -2.0, 2.0, 0.8, 10.0, 16.0, skin(P, "pale", dark="pale_dark"), cut=0)
    hd = m.bone("head", bd, (0, 18, 0))
    m.round_box(hd, 0, 0, 3.0, 2.8, 18.0, 25.0, FUR, cut=1)
    m.round_box(hd, 0, -2.4, 2.2, 0.8, 19.0, 24.0, facef, cut=0)
    for i in range(11):                                                              # shaggy mane
        ang = math.radians(-110 + i * 22)
        spike(m, hd, (2.8 * math.sin(ang), 24.0, 0.6 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.7, 0.6, 0.6), 1.6, 4.0,
              strands(P, "fur", "fur_dark"), tip=0.8)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.4, 0.4, 0.6, 1.0, 21.0, 23.0, skin(P, "pale", dark="pale_dark"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # long knuckle-walking arms
        ab = m.bone(nm, bd, (sx * 3.4, 17.0, 0))
        rod(m, ab, (sx * 3.4, 17.0, 0), (sx * 5.0, 9.0, -1.0), 1, FUR, extend=0.3, t2=2)
        rod(m, ab, (sx * 5.0, 9.0, -1.0), (sx * 5.4, 2.0, -2.0), 1, FUR, extend=0.3, t2=2)
        m.round_box(ab, sx * 5.4, -2.0, 1.2, 1.2, 0.0, 2.2, skin(P, "pale", dark="pale_dark"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 9.0, 0))
        rod(m, lg, (sx * 1.8, 9.4, 0), (sx * 2.2, 2.0, -0.6), 2, FUR, extend=0.3)
        m.round_box(lg, sx * 2.2, -1.2, 1.4, 2.2, 0.0, 1.6, skin(P, "pale", dark="pale_dark"), cut=0)
    tb = m.bone("tail", bd, (0, 10, 2))
    pts = [(0, 10.0, 2.4), (1.0, 8.0, 7.0), (3.0, 11.0, 10.0), (3.0, 15.0, 9.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, FUR, extend=0.3, t2=1)
    return m
