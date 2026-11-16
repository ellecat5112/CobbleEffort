"""Arbormon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the warrior of wood, a wooden puppet-robot. A barrel chest of pale carved wood with brown inlay and a
round emblem, a dome head with a visor band, segmented wooden arms ending in big jointed hands, a spring waist,
segmented legs with brown panels and rounded clog feet. 15 blocks tall.

Front is -z, y is up. 56 units tall; Adult stage (a Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import dome
from _digidetail import local, metal, mix, plane, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(15, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a wooden puppet-robot: a carved pale wood barrel chest with brown inlay and a round emblem, a dome head with a "
        "visor band, segmented arms with big jointed hands, a spring waist and rounded clog feet")
BASE = {"wood": (236, 220, 180), "wood_dark": (180, 156, 110), "inlay": (140, 90, 50), "inlay_dark": (90, 56, 26),
        "steel": (180, 184, 196), "steel_dark": (90, 94, 106), "visor": (40, 40, 48), "eye": (255, 220, 80)}
SHINY = {"wood": (150, 110, 80), "wood_dark": (100, 66, 40), "inlay": (230, 210, 160), "inlay_dark": (180, 150, 100)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def woodf(x, y, z, face, variant, box=None, **k):
    """Carved pale wood with fine grain and a brown inlaid band pattern."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    u, v, W, H = local(x, y, z, face, box)
    if min(v, H - v) < 0.5 and face not in ("up", "down"):
        return tone(p["inlay"], face), None
    if face not in ("up", "down") and abs((a * 0.6) % 3 - 1.5) < 0.3 and abs(v - H / 2) < H * 0.2:
        return tone(p["inlay_dark"], face), None
    grain = math.sin(a * 3.0 + math.sin(b * 0.8) * 2.0) * 0.5 + 0.5
    return tone(mix(p["wood"], p["wood_dark"], 0.1 + 0.15 * grain), face), None


def emblemf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        d = math.hypot(a, b - 44.0)
        if d < 3.0:
            if d > 2.4 or (abs(b - 44.0 - abs(a) * 1.2 + 1.0) < 0.4 and abs(a) < 1.8):
                return tone(p["inlay_dark"], face), None
            return tone(p["steel"], face), None
    return woodf(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("arbormon")
    top = m.bone("arbormon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 32, 0))
    m.round_box(bd, 0, 0, 7.4, 5.4, 36.0, 50.0, emblemf, cut=2)                         # barrel chest
    for i in range(4):                                           # spring waist
        m.round_box(bd, 0, 0, 2.6, 2.6, 28.0 + i * 2.0, 29.2 + i * 2.0, STEEL, cut=1)
    m.round_box(bd, 0, 0, 5.0, 4.0, 24.0, 28.6, woodf, cut=2)                            # hips
    hd = m.bone("head", bd, (0, 50, 0))
    dome(m, hd, (0, 50.0, 0), 4.6, 6.0, woodf, layers=4)
    m.box(hd, -4.8, 52.0, -4.9, 4.8, 53.8, 4.9, solid(P, "visor"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.8 - 0.6, 52.4, -5.0, sx * 1.8 + 0.6, 53.4, -4.9, solid(P, "eye", glow=True))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):           # segmented arms raised, big hands
        ab = m.bone(nm, bd, (sx * 7.6, 47.0, 0))
        ball(m, ab, (sx * 8.4, 47.0, 0), 2.8, woodf, layers=3)
        pts = [(sx * 9.0, 47.0, 0), (sx * 14.0, 52.0, -1.0), (sx * 18.0, 58.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 3, woodf, extend=0.4)
            ball(m, ab, p1, 1.8, STEEL, layers=2)
        h = pts[-1]
        m.round_box(ab, h[0], h[2], 2.6, 1.8, h[1], h[1] + 4.0, woodf, cut=1)
        for f in range(4):                                       # jointed fingers spread
            fx = h[0] + (f - 1.5) * 1.3
            rod(m, ab, (fx, h[1] + 4.0, h[2]), (fx + (f - 1.5) * 0.6, h[1] + 7.0, h[2] - 0.6), 1, woodf, extend=0.3)
        rod(m, ab, (h[0] - sx * 2.6, h[1] + 1.5, h[2]), (h[0] - sx * 4.4, h[1] + 3.5, h[2] - 0.4), 1, woodf,
            extend=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):           # segmented legs, clog feet
        lg = m.bone(nm, top, (sx * 3.0, 24.0, 0))
        m.round_box(lg, sx * 3.0, 0, 2.6, 2.6, 15.0, 24.0, woodf, cut=1)
        ball(m, lg, (sx * 3.0, 14.0, 0), 2.2, STEEL, layers=2)
        m.round_box(lg, sx * 3.0, 0, 2.4, 2.4, 4.0, 13.0, woodf, cut=1)
        m.round_box(lg, sx * 3.0, -1.2, 3.0, 4.0, 0.0, 4.4, woodf, cut=1)
    return m
