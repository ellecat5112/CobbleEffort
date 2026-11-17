"""Bomber Nanimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a walking bomb with a mean right hook. A round black bomb body with a steel cap, a lit fuse
sparking on top, red-and-black goggles over angry eyes, a grimacing mouth, one enormous red boxing fist raised high
on a thick black arm, a small red-gloved left fist and short legs in red-and-yellow boots. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, leather, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 16}
LOOK = ("a walking black bomb with a lit fuse, red goggles, a grimace, one enormous raised red boxing fist and "
        "red-and-yellow boots")
BASE = {"black": (50, 50, 60), "black_dark": (16, 16, 22), "black_light": (130, 132, 150), "steel": (190, 194, 206),
        "steel_dark": (90, 94, 106), "red": (220, 40, 30), "red_dark": (120, 14, 10), "yellow": (250, 210, 40),
        "goggle": (240, 60, 30), "white": (255, 255, 255), "mouth": (20, 16, 18), "spark": (255, 240, 120),
        "fuse": (210, 180, 120)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 164), "black_light": (255, 255, 255),
         "red": (40, 110, 230), "red_dark": (14, 40, 130), "yellow": (240, 240, 250)}


def P(v):
    return pal(BASE, SHINY, v)


BOMB = skin(P, "black", dark="black_dark", light="black_light", var=0.03)
GLOVE = leather(P, "red", "red_dark", stitch="yellow")
STEEL = metal(P, "steel", dark="steel_dark")
HAIR = fur(P, "black", "black_dark", length=1.0)


def bombf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 12.0 < y < 14.4 and abs(x) < 3.6:                      # the grimace
        if abs(y - 13.2) < 0.25 or (x * 1.4) % 1.2 < 0.25:
            return tone(p["mouth"], face), None
        return tone(p["white"], face), None
    return BOMB(x, y, z, face, variant, box=box, **k)


def goggf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        u, v, W, H = local(x, y, z, face, box)
        if (u / max(W, 1e-6) * 5) % 1 < 0.3:
            return tone(p["black"], face), None
        return tone(p["goggle"], face), None
    return tone(p["red"], face), None


def build():
    m = Model("bombernanimon")
    top = m.bone("bombernanimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    ball(m, bd, (0, 17.0, 0), 8.0, bombf, layers=7)
    m.round_box(bd, 0, 0, 3.4, 3.4, 24.4, 27.0, STEEL, cut=1)                     # bomb cap
    rod(m, bd, (0, 26.6, 0), (1.6, 31.0, 1.0), 1, solid(P, "fuse"), extend=0)    # fuse
    for d in ((1, 1, 0), (-1, 1, 0.4), (0.4, 1, -1)):
        spike(m, bd, (1.6, 31.0, 1.0), d, 0.8, 1.6, solid(P, "spark", glow=True))
    m.box(bd, -7.0, 18.0, -7.6, 7.0, 20.8, -5.6, goggf, rotation=(-6, 0, 0), pivot=(0, 19, -6.6))   # goggles
    m.box(bd, -8.0, 18.4, -6.0, 8.0, 20.4, 5.6, solid(P, "red"))                 # goggle strap
    for i in range(4):                                                            # flames on the goggle rims
        spike(m, bd, (5.0 + i * 0.8, 20.6, -6.4), (0.5, 1, 0), 0.8, 1.8, solid(P, "yellow", glow=True))
    # the enormous raised right fist on a thick black arm
    ar = m.bone("arm_right", bd, (-7.0, 18.0, 0))
    rod(m, ar, (-7.0, 18.0, 0.0), (-11.0, 24.0, 0.6), 5, HAIR, extend=0.6)
    rod(m, ar, (-11.0, 24.0, 0.6), (-10.0, 29.0, -1.0), 5, HAIR, extend=0.6)
    m.round_box(ar, -10.0, -1.6, 5.6, 5.0, 28.6, 38.0, GLOVE, cut=2)
    m.box(ar, -14.0, 28.0, -4.6, -6.0, 30.0, 1.4, solid(P, "yellow"))           # cuff
    # small left fist
    al = m.bone("arm_left", bd, (7.4, 14.0, 0))
    rod(m, al, (7.4, 14.0, 0), (10.6, 9.4, -2.0), 3, HAIR, extend=0.4)
    m.round_box(al, 11.0, -2.6, 2.2, 2.2, 6.4, 10.4, GLOVE, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 10.0, 0))
        rod(m, lg, (sx * 3.4, 10.0, 0), (sx * 3.6, 4.0, 0), 3, HAIR, extend=0.4)
        m.box(lg, sx * 3.6 - 2.0, 0.0, -3.8, sx * 3.6 + 2.0, 5.6, 1.8, GLOVE)    # red boots
        m.box(lg, sx * 3.6 - 2.1, 4.0, -2.4, sx * 3.6 + 2.1, 5.8, 1.9, solid(P, "yellow"))
    return m
