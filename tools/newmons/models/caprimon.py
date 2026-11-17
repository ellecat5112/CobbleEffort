"""Caprimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little helmeted baby. A round silver-grey head shaped like a helmet with two tall pointed horn-
ears, a pale face with big brown eyes and a happy open mouth, and a big fluffy white tail banded in violet.
Baby II.

Front is -z, y is up. 24 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 24
SCALE, HITBOX = sized(0.5, HEIGHT, 0.55)
KIND = "floater"
K = 4
LOOK = "a round silver-grey helmet-headed baby with tall pointed ears, big brown eyes and a fluffy violet-banded tail"
BASE = {"silver": (196, 200, 214), "silver_dark": (110, 114, 130), "face": (236, 236, 244), "eye": (170, 110, 50),
        "pupil": (30, 20, 10), "white": (255, 255, 255), "mouth": (200, 60, 70), "violet": (100, 80, 180),
        "violet_dark": (50, 34, 110), "tail": (244, 244, 250), "tail_dark": (190, 190, 210)}
SHINY = {"silver": (230, 190, 90), "silver_dark": (160, 110, 30), "violet": (60, 160, 120), "violet_dark": (20, 90, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HELM = metal(P, "silver", dark="silver_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and y < 12.6 and abs(x) < 6.0:
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.6, y - 9.2, 1.5, "eye")
            if c is not None:
                return c, None
        if 5.6 < y < 7.0 and abs(x) < 1.2 - (7.0 - y) * 0.4:
            return tone(p["mouth"], face), None
        return tone(p["face"], face), None
    return HELM(x, y, z, face, variant, box=box, **k)


def tailf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (x * 0.8 + y * 0.6) % 3.0 < 1.0:
        return tone(p["violet"], face), None
    return fur(P, "tail", "tail_dark", length=0.8)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("caprimon")
    top = m.bone("caprimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 9.0, 0), 7.2, headf, layers=6, squash=0.9)
    hd = m.bone("head", bd, (0, 14, 0))
    for sx in (-1, 1):                                                   # tall pointed horn-ears
        spike(m, hd, (sx * 4.4, 13.6, 0.4), (sx * 0.7, 1, 0.1), 3.6, 8.0, HELM, tip=0.8)
    tl = m.bone("tail", bd, (5, 6, 4))
    pts = [(5.0, 6.0, 4.0), (10.0, 5.0, 6.0), (14.0, 8.0, 7.0), (15.0, 13.0, 6.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - j, tailf, extend=0.6)
    return m
