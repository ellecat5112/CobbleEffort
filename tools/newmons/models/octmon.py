"""Octmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the pirate octopus: a red octopus with a brown rounded head shell riveted like an old diving helmet,
crowned with a gold crown, dark eye-holes with yellow eyes, red-and-black striped horns, red tentacles ending in black
claws, a cutlass, a hook and an old pistol held in its curling arms. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, riveted, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a red pirate octopus with a riveted brown helmet shell, a gold crown, striped horns, black-clawed tentacles, a "
        "cutlass, a hook and an old pistol")
BASE = {"red": (220, 50, 40), "red_dark": (130, 20, 14), "shell": (160, 120, 70), "shell_dark": (90, 64, 30),
        "gold": (240, 200, 60), "black": (30, 26, 30), "eye": (250, 220, 60), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126)}
SHINY = {"red": (80, 120, 220), "red_dark": (30, 50, 140), "shell": (200, 200, 210), "shell_dark": (120, 120, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "red", dark="red_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def hornf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["black"] if (y + abs(x)) % 2.4 < 1.0 else p["red"], face), None


def build():
    m = Model("octmon")
    top = m.bone("octmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    hd = m.bone("head", bd, (0, 22, 0))
    ball(m, hd, (0, 24.0, 0), 8.0, riveted(P, "shell", "shell_dark", spacing=2.6), layers=6, ry=7.0)   # helmet shell
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.0, -7.4, 1.8, 0.4, 20.4, 24.0, solid(P, "black"), cut=0)
        m.box(hd, sx * 3.0 - 0.8, 21.6, -7.9, sx * 3.0 + 0.8, 23.0, -7.75, solid(P, "eye", glow=True))
        pts = [(sx * 6.0, 26.0, 0), (sx * 10.0, 30.0, 0), (sx * 10.0, 34.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):                                                 # striped horns
            rod(m, hd, p0, p1, 2, hornf, extend=0.3)
    m.round_box(hd, 0, 0, 3.6, 3.6, 30.6, 32.0, metal(P, "gold"), cut=1)                  # gold crown
    for i in range(5):
        ang = 2 * math.pi * i / 5
        spike(m, hd, (3.0 * math.cos(ang), 32.0, 3.0 * math.sin(ang)), (0, 1, 0), 1.0, 2.4, metal(P, "gold"), tip=0.8)
    tb = m.bone("tentacles", bd, (0, 16, 0))
    for i in range(8):                                                                   # tentacles
        ang = 2 * math.pi * i / 8
        pts = [(4.0 * math.cos(ang), 16.0, 4.0 * math.sin(ang)), (9.0 * math.cos(ang), 10.0, 9.0 * math.sin(ang)),
               (12.0 * math.cos(ang + 0.3), 3.0, 12.0 * math.sin(ang + 0.3))]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 3, SKIN, extend=0.4)
        e = pts[-1]
        spike(m, tb, e, (math.cos(ang + 0.3), -0.6, math.sin(ang + 0.3)), 1.4, 3.0, solid(P, "black"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                  # curling weapon arms
        ab = m.bone(nm, bd, (sx * 6.0, 18.0, -3.0))
        pts = [(sx * 6.0, 18.0, -3.0), (sx * 12.0, 22.0, -5.0), (sx * 14.0, 28.0, -6.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 2, SKIN, extend=0.3)
        e = pts[-1]
        if sx < 0:                                                                       # cutlass
            m.box(ab, e[0] - 0.4, e[1], e[2] - 1.0, e[0] + 0.4, e[1] + 14.0, e[2] + 1.0, STEEL,
                  rotation=(0, 0, 15), pivot=e)
        else:                                                                            # pistol
            rod(m, ab, e, (e[0] + 1.0, e[1] + 1.0, e[2] - 6.0), 2, STEEL, extend=0.2)
    return m
