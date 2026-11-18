"""Kotemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little kendo fighter: a small reptile in full kendo armour: a dark indigo men helmet with a brass face grille and
glowing yellow eyes, two horn-like bands, a red-and-black do breastplate with a white bow, indigo hakama, mesh
sleeves and a bamboo shinai held high; a lizard tail and clawed violet feet poke out. Child stage, 1 block tall.

Front is -z, y is up. 28 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, scales, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little reptile in kendo armour with an indigo helmet and brass grille, a red breastplate, indigo hakama and a bamboo shinai"
BASE = {"indigo": (50, 40, 110), "indigo_dark": (20, 14, 50), "brass": (200, 160, 70), "brass_dark": (120, 90, 30),
        "red": (210, 40, 40), "red_dark": (120, 14, 18), "white": (246, 246, 246), "mesh": (150, 156, 176),
        "mesh_dark": (80, 84, 100), "bamboo": (240, 220, 160), "bamboo_dark": (170, 140, 80), "eye": (250, 220, 60),
        "violet": (140, 120, 200), "violet_dark": (80, 60, 140), "claw": (240, 240, 240), "steel": (130, 134, 146)}
SHINY = {"indigo": (40, 110, 70), "indigo_dark": (14, 50, 30), "red": (40, 90, 200), "red_dark": (14, 30, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def grillef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(y - 19.6) < 0.5 and 0.4 < abs(x) < 1.6:
            return tone(p["eye"], face), p["eye"]
        if (x + 3.0) % 1.0 < 0.25 or (y % 1.2) < 0.25:
            return tone(p["brass"], face), None
        return tone(p["indigo_dark"], face), None
    return fabric(P, "indigo", "indigo_dark")(x, y, z, face, variant, box=box, **k)


def meshf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["mesh_dark"] if (x + y) % 0.9 < 0.2 or (x - y) % 0.9 < 0.2 else p["mesh"], face), None


def build():
    m = Model("kotemon")
    top = m.bone("kotemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for j in range(5):                                                               # indigo hakama skirt
        ang = math.radians(-60 + j * 30)
        spike(m, bd, (2.6 * math.sin(ang), 9.0, -2.0 * math.cos(ang)), (math.sin(ang) * 0.4, -1, -math.cos(ang) * 0.3), 2.0,
              5.0, fabric(P, "indigo", "indigo_dark"), tip=0.8)
    m.round_box(bd, 0, 0, 3.2, 2.6, 8.6, 15.4, armour(P, "red", "red_dark", trim="steel", trim_w=0.25), cut=1)  # do
    m.round_box(bd, 0, -2.7, 0.8, 0.3, 12.0, 13.0, solid(P, "white"), cut=0)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 3.4, 3.2, 15.4, 22.6, grillef, cut=1)
    for sx in (-1, 1):                                                               # horn bands
        spike(m, hd, (sx * 2.6, 22.0, 0.4), (sx * 0.6, 1, 0.2), 1.6, 3.6, metal(P, "steel", dark="indigo_dark"), tip=0.8)
        m.round_box(hd, sx * 4.0, 0.4, 0.8, 2.6, 15.0, 19.0, fabric(P, "indigo", "indigo_dark"), cut=0)   # side flaps
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.2, 14.6, 0))
        rod(m, ab, (sx * 3.2, 14.6, 0), (sx * 4.6, 10.6, -1.0), 1, meshf, extend=0.3, t2=2)
        m.round_box(ab, sx * 4.8, -1.0, 1.2, 1.2, 9.0, 11.0, fabric(P, "indigo", "indigo_dark"), cut=0)
    rod(m, "arm_left", (4.8, 9.0, -1.0), (1.0, 26.0, -4.0), 1, fabric(P, "bamboo", "bamboo_dark", period=1.6), extend=0,
        t2=2)                                                                       # bamboo shinai
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 6.0, 0))
        rod(m, lg, (sx * 1.6, 6.0, 0), (sx * 1.8, 1.4, 0), 1, scales(P, "violet", "violet_dark"), extend=0.3, t2=2)
        for j in range(3):
            spike(m, lg, (sx * 1.8 + (j - 1) * 0.8, 0.6, -0.8), (0, -0.2, -1), 0.8, 2.0, solid(P, "claw"), tip=0.8)
    tb = m.bone("tail", bd, (0, 7, 2))
    rod(m, tb, (0, 7.0, 2.0), (2.0, 3.0, 7.0), 1, scales(P, "violet", "violet_dark"), extend=0.3, t2=2)
    return m
