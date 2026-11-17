"""Burgamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the burger kid. A cheerful cream-coloured little creature wearing a big glossy hamburger-bun cap
with a dark brown brim, one eye winking and pink cheeks, a bib printed with a hamburger, little winglike ears, a
thumbs-up, a curling tail, and a tray in its other hand. Child stage.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, skin, solid
from _route import pal, tone

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a cheerful cream creature in a big hamburger-bun cap, winking with pink cheeks, a burger bib, a thumbs-up and "
        "a curling tail")
BASE = {"cream": (250, 226, 190), "cream_dark": (210, 170, 130), "bun": (170, 96, 40), "bun_dark": (110, 56, 20),
        "bun_light": (220, 150, 80), "seed": (250, 240, 210), "brim": (90, 50, 26), "cheek": (250, 140, 160),
        "eye": (30, 20, 20), "mouth": (210, 60, 70), "bib": (250, 246, 236), "bib_edge": (220, 190, 120),
        "lettuce": (110, 190, 60), "patty": (110, 60, 30), "tray": (160, 110, 60)}
SHINY = {"cream": (220, 236, 250), "cream_dark": (160, 186, 214), "bun": (100, 60, 30), "bun_dark": (60, 30, 14),
         "bun_light": (150, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


CREAM = skin(P, "cream", dark="cream_dark", var=0.03)


def bunf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and ((x * 1.7 + z * 1.3) % 3.0 < 0.35 and (x * 0.9 - z * 1.9 + y) % 2.6 < 0.4):
        return tone(p["seed"], face), None
    g = min(1.0, max(0.0, (y - 18.0) / 6.0))
    col = p["bun_light"] if g > 0.7 else p["bun"] if g > 0.2 else p["bun_dark"]
    return tone(col, face), None


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if math.hypot(x - 2.4, y - 15.4) < 0.8:                                    # open eye
            return tone(p["eye"], face), None
        if abs(y - 15.4 + 0.3 * abs(x + 2.4)) < 0.2 and abs(x + 2.4) < 1.0:       # winking eye
            return tone(p["eye"], face), None
        for sx in (-1, 1):
            if math.hypot(x - sx * 3.6, y - 13.8) < 0.8:
                return tone(p["cheek"], face), None
        if 12.0 < y < 13.6 and abs(x) < 1.4 - (13.6 - y) * 0.5:
            return tone(p["mouth"], face), None
    return CREAM(x, y, z, face, variant, box=box, **k)


def bibf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for y0, y1, key in ((9.4, 10.2, "bun"), (8.8, 9.4, "lettuce"), (8.0, 8.8, "patty"), (7.4, 8.0, "bun")):
            if y0 < y < y1 and abs(x) < 1.6:
                return tone(p[key], face), None
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["bib_edge"] if v < 0.4 else p["bib"], face), None


def build():
    m = Model("burgamon")
    top = m.bone("burgamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 3.6, 3.0, 4.0, 10.4, CREAM, cut=1)
    m.box(bd, -3.0, 6.8, -3.4, 3.0, 10.6, -2.8, bibf)                                  # the bib
    hd = m.bone("head", bd, (0, 10, 0))
    ball(m, hd, (0, 15.0, 0), 5.4, facef, layers=5)
    m.round_box(hd, 0, -0.6, 6.4, 6.0, 17.4, 18.6, solid(P, "brim"), cut=2)            # cap brim
    ball(m, hd, (0, 19.4, 0.2), 6.2, bunf, layers=5, squash=0.7)                        # the bun cap
    for sx in (-1, 1):                                                                  # little winglike ears
        for j in range(3):
            spike(m, hd, (sx * 5.0, 15.0 - j * 0.6, 0.6), (sx, 0.4 - j * 0.4, 0.2), 1.2, 2.6 - j * 0.4, CREAM)
    al = m.bone("arm_left", bd, (3.4, 9.0, 0))                                         # thumbs-up
    rod(m, al, (3.4, 9.0, 0), (6.4, 11.4, -1.0), 2, CREAM, extend=0.3)
    m.round_box(al, 6.8, -1.2, 1.4, 1.4, 10.6, 13.0, CREAM, cut=1)
    rod(m, al, (6.8, 13.0, -1.2), (6.8, 15.0, -1.4), 1, CREAM, extend=0.2)
    ar = m.bone("arm_right", bd, (-3.4, 9.0, 0))                                       # the tray
    rod(m, ar, (-3.4, 9.0, 0), (-6.4, 7.6, -2.0), 2, CREAM, extend=0.3)
    m.box(ar, -10.0, 7.0, -5.0, -4.6, 7.6, 0.4, solid(P, "tray"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 4.0, 0))
        rod(m, lg, (sx * 1.8, 4.4, 0), (sx * 2.2, 0.8, -0.6), 2, CREAM, extend=0.3)
        m.box(lg, sx * 2.2 - 1.2, 0.0, -2.6, sx * 2.2 + 1.2, 1.2, 0.6, CREAM)
    tl = m.bone("tail", bd, (0, 6, 3))
    pts = [(0, 6.0, 2.8), (2.0, 5.0, 6.0), (4.0, 7.0, 8.0), (4.6, 10.0, 7.4)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, CREAM, extend=0.3)
    return m
