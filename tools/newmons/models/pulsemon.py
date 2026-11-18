"""Pulsemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a lightning-charged beast cub: a spiky electric-yellow mane and fur zigzagged with black bolts, a
white muzzle with a fang, big green eyes, silver horn-spikes on its shoulders and tail, black-and-green bolt-marked
gauntlet paws and boots with silver claws, and a lightning-bolt tail. 1 block.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a spiky electric-yellow beast cub zigzagged with black bolts, big green eyes, silver spikes and black-and-green bolt gauntlets"
BASE = {"yellow": (230, 230, 40), "yellow_dark": (170, 170, 10), "black": (30, 30, 36), "white": (250, 250, 250),
        "eye": (60, 200, 80), "pupil": (20, 30, 20), "green": (80, 230, 80), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126), "mouth": (200, 60, 80)}
SHINY = {"yellow": (90, 200, 240), "yellow_dark": (30, 130, 190), "green": (240, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((y + abs(x) * 0.8) % 5.0) - 2.5 - math.sin(abs(x) * 2.0) * 0.6) < 0.35:
        return tone(p["black"], face), None
    return fur(P, "yellow", "yellow_dark", length=1.2)(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.8, (y - 21.4) * 0.8)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.2:
                return tone(p["eye"], face), None
        if abs(x) < 2.0 and y < 20.0:
            return tone(p["white"], face), None
    return furf(x, y, z, face, variant, box=box, **k)


def gauntf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(((y + x) % 3.0) - 1.5) < 0.25:
        return tone(p["green"], face), p["green"]
    return armour(P, "black", "black")(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("pulsemon")
    top = m.bone("pulsemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 7, 0))
    m.round_box(bd, 0, 0, 3.6, 3.0, 9.0, 17.0, furf, cut=1)
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 21.0, -0.2), 4.0, headf, layers=4, ry=3.8)
    m.round_box(hd, 0, -3.6, 1.8, 1.2, 18.4, 20.4, headf, cut=0)
    m.box(hd, -1.6, 18.4, -4.9, 0.6, 19.0, -4.7, solid(P, "mouth"))
    spike(m, hd, (0.8, 18.6, -4.8), (0, -1, 0), 0.8, 1.0, solid(P, "white"), tip=0.8)
    for j in range(8):                                                                   # spiky mane
        ang = math.radians(-80 + j * 23)
        spike(m, hd, (3.6 * math.sin(ang), 22.0 + 2.6 * math.cos(ang), 1.0), (math.sin(ang), math.cos(ang) + 0.3, 0.5),
              1.8, 5.0 + (j % 2) * 2.0, furf, tip=0.8)
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 24.0, 0), (sx * 0.6, 1, 0), 1.8, 5.0, furf, tip=0.8)       # ears
        spike(m, bd, (sx * 4.0, 16.4, 1.0), (sx * 1, 0.4, 0.2), 1.2, 4.0, STEEL, tip=0.8)  # shoulder spikes
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 16.0, 0))
        rod(m, ab, (sx * 3.6, 16.0, 0), (sx * 6.0, 12.0, -1.6), 2, furf, extend=0.2)
        m.round_box(ab, sx * 6.6, -2.0, 2.0, 2.0, 8.6, 12.0, gauntf, cut=1)
        for f in range(3):
            spike(m, ab, (sx * 6.6 + (f - 1) * 1.0, 8.6, -3.4), (0, -0.4, -1), 0.8, 2.2, STEEL, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
        m.round_box(lg, sx * 2.0, 0, 1.6, 1.6, 4.0, 9.0, furf, cut=0)
        m.round_box(lg, sx * 2.0, -0.8, 2.2, 3.0, 0.0, 4.4, gauntf, cut=1)
        for f in range(3):
            spike(m, lg, (sx * 2.0 + (f - 1) * 1.2, 0.8, -3.8), (0, -0.2, -1), 0.8, 2.0, STEEL, tip=0.8)
    tl = m.bone("tail", bd, (0, 10, 3))                                                  # bolt tail
    pts = [(0, 10.0, 3.0), (0, 13.0, 7.0), (0, 11.0, 9.0), (0, 16.0, 13.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 2, furf, extend=0.3)
    spike(m, tl, pts[-1], (0, 0.6, 1), 1.4, 4.0, STEEL, tip=0.8)
    return m
