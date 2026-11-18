"""Golem Jiji Kamemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Jiji Kamemon riding inside a golem: an old green turtle with a grey fur mane and a blue cap sitting in a
hulking body of olive stone wrapped in bandages, with a red shell front marked by an orange disc, huge stone fists and
a big orange paw-print mitten on its tail. 15 blocks tall.

Front is -z, y is up. 40 units tall (no level on wikimon: sized as an Adult).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("an old green turtle with a grey fur mane and a blue cap riding in a hulking olive stone golem with a red shell "
        "front, huge stone fists and a paw mitten on its tail")
BASE = {"stone": (140, 130, 70), "stone_dark": (80, 74, 36), "band": (190, 180, 150), "turtle": (90, 160, 90),
        "turtle_dark": (40, 100, 40), "fur": (190, 186, 180), "fur_dark": (130, 126, 120), "cap": (60, 70, 140),
        "red": (190, 50, 40), "orange": (240, 150, 40), "eye": (24, 22, 26), "mitt": (220, 140, 50)}
SHINY = {"stone": (120, 120, 140), "stone_dark": (60, 60, 76), "turtle": (180, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


STONE0 = skin(P, "stone", dark="stone_dark")


def stonef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((y * 0.6 + x * 0.2) % 4.0 - 2.0) < 0.3:
        return tone(p["band"], face), None
    return STONE0(x, y, z, face, variant, box=box, **k)


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x - 1.0, y - 20.0) < 3.0:
        return tone(p["orange"], face), None
    return tone(p["red"], face), None


def build():
    m = Model("golemjijikamemon")
    top = m.bone("golemjijikamemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 1.0, 8.0, 6.6, 12.0, 30.0, stonef, cut=3)                          # golem body
    m.round_box(bd, 0, -5.0, 5.4, 1.6, 14.0, 26.0, chestf, cut=1)                          # red shell front
    hd = m.bone("head", bd, (0, 30, -2))                                                      # Jiji Kamemon
    m.round_box(hd, 0, -3.0, 4.6, 4.0, 28.0, 34.0, fur(P, "fur", "fur_dark", length=1.4), cut=2)
    m.round_box(hd, 0, -6.4, 2.4, 2.0, 30.0, 34.0, skin(P, "turtle", dark="turtle_dark"), cut=1)
    m.box(hd, -1.6, 32.6, -8.5, -0.6, 33.4, -8.3, solid(P, "eye"))
    m.box(hd, 0.6, 32.6, -8.5, 1.6, 33.4, -8.3, solid(P, "eye"))
    m.round_box(hd, 0, -4.4, 2.8, 2.6, 34.0, 36.0, solid(P, "cap"), cut=1)
    for sx in (-1, 1):
        spike(m, bd, (sx * 6.0, 30.0, 2.0), (sx * 0.3, 1, 0.4), 2.6, 7.0, stonef, tip=1.0)    # golem horn-crests
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 26.0, 0))
        rod(m, ab, (sx * 8.0, 26.0, 0), (sx * 13.0, 14.0, -4.0), 5, stonef, extend=0.6)
        m.round_box(ab, sx * 13.0, -5.0, 4.0, 4.0, 4.0, 12.0, stonef, cut=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 12.0, 0))
        rod(m, lg, (sx * 4.0, 12.0, 0), (sx * 4.6, 3.0, 0), 4, skin(P, "turtle", dark="turtle_dark"), extend=0.4)
        m.round_box(lg, sx * 4.6, -1.0, 2.6, 3.4, 0.0, 3.0, skin(P, "turtle", dark="turtle_dark"), cut=1)
    tb = m.bone("tail", bd, (0, 14, 6))
    rod(m, tb, (0, 14.0, 6.0), (6.0, 16.0, 14.0), 2, skin(P, "turtle", dark="turtle_dark"), extend=0.4)
    m.round_box(tb, 7.0, 15.0, 3.0, 2.0, 14.0, 20.0, solid(P, "mitt"), cut=1)
    return m
