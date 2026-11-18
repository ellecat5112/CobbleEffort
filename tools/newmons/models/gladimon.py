"""Gladimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
gladiator ball: a round bronze-and-steel helmet-body with a barred visor showing big green eyes, a flaming orange
plume, little steel legs, and two long curved sabres swung on black hoses from its sides. Adult stage, 15 blocks.

Front is -z, y is up. 34 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, flame_inside, leather, local, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a round bronze-and-steel helmet-body with a barred visor and big green eyes, a flaming plume and two long "
        "curved sabres on black hoses")
BASE = {"bronze": (150, 100, 50), "bronze_dark": (90, 56, 20), "steel": (214, 218, 228), "steel_dark": (110, 114, 126),
        "eye": (60, 200, 150), "pupil": (16, 30, 24), "black": (30, 28, 32), "black_dark": (10, 10, 12),
        "fire": (255, 140, 40, 215), "fire_core": (255, 240, 170, 240), "gold": (240, 200, 70)}
SHINY = {"bronze": (60, 70, 110), "bronze_dark": (24, 30, 60), "fire": (90, 180, 255, 215)}


def P(v):
    return pal(BASE, SHINY, v)


BRONZE = metal(P, "bronze", dark="bronze_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 14.0 < y < 22.0 and abs(x) < 5.0:
        if abs((x * 0.8) % 2.0 - 1.0) < 0.25:
            return tone(p["steel"], face), None
        for sx in (-1, 1):
            d = math.hypot(x - sx * 2.0, y - 17.0)
            if d < 0.6:
                return tone(p["pupil"], face), None
            if d < 1.6:
                return tone(p["eye"], face), None
        return tone(p["black"], face), None
    if y > 20.0:
        return STEEL(x, y, z, face, variant, box=box, **k)
    return BRONZE(x, y, z, face, variant, box=box, **k)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def build():
    m = Model("gladimon")
    top = m.bone("gladimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 17.0, 0), 8.0, bodyf, layers=6)
    hd = m.bone("head", bd, (0, 25, 0))
    for ang in (0, 90):                                                                # flaming plume
        m.box(hd, -2.5, 24.0, 2.0, 2.5, 33.0, 2.0, cutout(flame_inside(4, 0.3, 4), firef), rotation=(0, ang, 0),
              pivot=(0, 24.0, 2.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                 # hoses + sabres
        ab = m.bone(nm, bd, (sx * 8.0, 16.0, 0))
        pts = [(sx * 7.6, 16.0, 0), (sx * 11.0, 22.0, 2.0), (sx * 14.0, 26.0, -2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, leather(P, "black", "black_dark"), extend=0.3, t2=1)
        m.round_box(ab, sx * 14.0, -2.0, 1.2, 1.2, 25.0, 27.6, STEEL, cut=0)
        blade = [(sx * 14.0, 27.0, -2.0), (sx * 18.0, 31.0, -4.0), (sx * 24.0, 31.0, -6.0), (sx * 29.0, 27.0, -7.0)]
        for p0, p1 in zip(blade, blade[1:]):
            rod(m, ab, p0, p1, 1, STEEL, extend=0.3, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 10.0, 0))
        rod(m, lg, (sx * 2.6, 10.0, 0), (sx * 3.4, 2.0, 0), 2, STEEL, extend=0.3)
        spike(m, lg, (sx * 3.4, 1.0, 0), (0, -0.4, -1), 2.0, 3.0, STEEL, tip=0.8)
    return m
