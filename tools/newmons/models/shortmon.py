"""Shortmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the strawberry-shortcake cat: a little gentleman in a brown waistcoat and white shirt with brown
breeches and boots, a pink fluffy tail, his head a slice of strawberry shortcake with cream frosting, sponge layers,
a green cat eye peering out, cat ears and a big red strawberry on top. 15 blocks.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, fur, leather, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a little cat gentleman in a brown waistcoat whose head is a slice of strawberry shortcake with a green cat eye and a big strawberry"
BASE = {"cream": (252, 246, 236), "sponge": (250, 220, 150), "jam": (230, 70, 90), "pink": (246, 190, 206),
        "pink_dark": (220, 140, 170), "brown": (130, 80, 50), "brown_dark": (80, 46, 24), "white": (250, 250, 250),
        "red": (220, 30, 50), "green": (60, 160, 60), "eye": (90, 200, 90), "black": (24, 20, 20)}
SHINY = {"sponge": (140, 90, 60), "jam": (250, 210, 230), "red": (120, 60, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def cakef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and math.hypot(x - 1.0, y - 22.0) < 1.6:
        d = math.hypot(x - 1.0, y - 22.0)
        return tone(p["black"] if d < 0.6 else p["eye"], face), None
    if face == "up" or y > 27.0:
        return tone(p["cream"], face), None
    band = (y - 17.0) % 4.0
    if band < 0.8:
        return tone(p["cream"], face), None
    if band < 1.6:
        return tone(p["jam"], face), None
    return tone(p["sponge"], face), None


def build():
    m = Model("shortmon")
    top = m.bone("shortmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 3.4, 2.8, 8.0, 16.0, leather(P, "brown", "brown_dark", stitch="white"), cut=1)   # waistcoat
    m.box(bd, -1.0, 9.0, -2.9, 1.0, 16.0, -2.7, solid(P, "white"))
    hd = m.bone("head", bd, (0, 16, 0))
    m.box(hd, -5.0, 16.0, -4.0, 5.0, 28.0, 4.0, cakef, rotation=(0, 0, 8), pivot=(0, 22, 0))  # shortcake head
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.4, 27.0, 0), (sx * 0.4, 1, 0), 1.6, 3.0, solid(P, "pink"), tip=0.8)
    ball(m, hd, (-1.0, 30.6, 0), 2.6, solid(P, "red"), layers=2)                              # strawberry
    spike(m, hd, (-1.0, 33.0, 0), (0, 1, 0), 1.6, 1.4, solid(P, "green"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 14.0, 0))
        rod(m, ab, (sx * 3.4, 14.0, 0), (sx * 6.0, 10.0, -1.6), 2, fabric(P, "white", "cream", axis="x"), extend=0.3)
        ball(m, ab, (sx * 6.4, 9.4, -2.0), 1.4, solid(P, "white"), layers=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 7.0, 0))
        m.round_box(lg, sx * 1.8, 0, 1.6, 1.6, 3.0, 8.0, fabric(P, "brown", "brown_dark", axis="y"), cut=0)
        m.round_box(lg, sx * 1.8, -0.8, 1.6, 2.4, 0.0, 3.4, leather(P, "brown_dark", "black"), cut=0)
    tl = m.bone("tail", bd, (0, 8, 3))
    pts = [(0, 8.0, 3.0), (4.0, 6.0, 8.0), (8.0, 8.0, 10.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 3, fur(P, "pink", "pink_dark", length=1.2), extend=0.5)
    return m
