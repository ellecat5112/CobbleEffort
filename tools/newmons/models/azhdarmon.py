"""Azhdarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a pterosaur with blades for a crest. A slate-blue body with a shaggy spined ruff, huge pale
blue membrane wings, a long beaked head crowned with a great steel axe-blade crest, steel blades at its wing
joints, a long red-banded tail ending in a bladed tip and red clawed feet. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import cutout, eye, fur, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a pterosaur with a great steel axe-blade crest, a slate-blue body with a spined ruff, huge pale-blue "
        "membrane wings with blades at the joints, a red-banded bladed tail and red clawed feet")
BASE = {"blue": (90, 100, 190), "blue_dark": (40, 46, 110), "blue_light": (160, 170, 240), "wing": (150, 170, 240, 235),
        "wing_dark": (100, 120, 210, 240), "steel": (220, 226, 240), "steel_dark": (110, 116, 134), "red": (200, 50, 50),
        "red_dark": (120, 20, 20), "eye": (250, 60, 60), "pupil": (20, 10, 10), "white": (250, 250, 250)}
SHINY = {"blue": (60, 130, 90), "blue_dark": (20, 70, 40), "blue_light": (140, 210, 160), "wing": (170, 230, 190, 235),
         "wing_dark": (110, 190, 140, 240)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.04)
STEEL = metal(P, "steel", dark="steel_dark")
RUFF = fur(P, "blue", "blue_dark", tip="blue_light")


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["wing_dark"] if (u * 0.5) % 2.0 < 0.2 else p["wing"]), None


def axe(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return abs(v / max(H, 1e-6) - 0.5) < 0.12 + 0.38 * t ** 1.5


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 12.0, y - 27.0, 0.9, "eye")
        if c is not None:
            return c, None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("azhdarmon")
    top = m.bone("azhdarmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    for i in range(5):                                           # the body, leaning forward
        r = 5.0 - abs(i - 2) * 0.6
        m.round_box(bd, 0, 2.0 - i * 2.0, r, r * 0.9, 12.0 + i * 2.6, 15.0 + i * 2.6, HIDE, cut=1)
    for i in range(12):                                          # spined ruff round the neck
        ang = math.radians(i * 30)
        spike(m, bd, (3.6 * math.sin(ang), 24.0, -6.0 + 3.6 * math.cos(ang)), (math.sin(ang), 0.2, math.cos(ang)),
              1.4, 2.6, RUFF)
    hd = m.bone("head", bd, (0, 26, -8))
    m.round_box(hd, 0, -10.0, 2.4, 2.6, 25.0, 29.4, headf, cut=1)
    m.box(hd, -1.4, 25.4, -22.0, 1.4, 28.0, -12.0, HIDE)                                 # long beak
    spike(m, hd, (0, 26.4, -22.0), (0, -0.2, -1), 2.0, 3.0, HIDE)
    m.box(hd, -0.4, 28.0, -12.0, 0.4, 32.0, 2.0, STEEL)                                   # crest base
    for sx in (-1, 1):                                           # the axe-blade crest: two curved blades
        pts = [(0, 31.0, -6.0), (0, 38.0, -2.0), (0, 42.0, 4.0), (sx * 0.0, 40.0, 10.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 1, STEEL, extend=0.3, t2=4 - j)
    rod(m, hd, (0, 29.0, -12.0), (0, 36.0, -18.0), 1, STEEL, extend=0.3, t2=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # huge membrane wings with blades at the joints
        wb = m.bone(nm, bd, (sx * 4.0, 22.0, -3.0))
        wrist, tips = bat_wing(m, wb, (sx * 4.0, 22.0, -3.0), 36.0, 20.0, 4, HIDE, cutout(lambda *q: True, wingf),
                               side=sx)
        spike(m, wb, wrist, (sx * 0.3, 1, -0.6), 2.0, 8.0, STEEL, tip=0.8)
    tl = m.bone("tail", bd, (0, 14, 4))
    pts = [(0, 14.0, 4.0), (0, 12.0, 10.0), (0, 11.0, 16.0), (0, 11.0, 22.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 2, solid(P, "red") if j % 2 else HIDE, extend=0.3)
    for d in ((0, 1, 0.4), (0, -1, 0.4), (0, 0, 1)):
        spike(m, tl, pts[-1], d, 1.4, 4.0, STEEL)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 12.0, 2.0))
        rod(m, lg, (sx * 3.0, 12.0, 2.0), (sx * 3.6, 6.0, 0.0), 2, HIDE, extend=0.3)
        rod(m, lg, (sx * 3.6, 6.0, 0.0), (sx * 3.6, 1.0, -1.0), 2, solid(P, "red"), extend=0.3)
        for d in ((sx * 0.3, -0.3, -1), (0, -0.3, -1), (-sx * 0.3, -0.3, -1)):
            spike(m, lg, (sx * 3.6, 1.0, -1.0), d, 0.9, 2.6, solid(P, "red_dark"))
    return m
