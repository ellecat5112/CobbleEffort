"""Gawappamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
punk kappa: a chubby mint-green kappa with a cream belly patched with stitches, an orange-brown turtle shell, a yellow
beak, a ring of orange dreadlocks round a shiny compact disc on its head, headphones, big webbed yellow feet and
clawed green hands. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a chubby mint-green kappa with a stitched cream belly, a turtle shell, a yellow beak, orange dreadlocks round "
        "a compact disc, headphones and big webbed feet")
BASE = {"green": (110, 200, 160), "green_dark": (50, 130, 100), "belly": (240, 230, 200), "belly_dark": (190, 180, 150),
        "stitch": (160, 40, 60), "shell": (190, 110, 50), "shell_dark": (120, 60, 20), "beak": (250, 200, 40),
        "dread": (220, 90, 30), "dread_dark": (150, 50, 14), "disc": (210, 220, 240), "disc_dark": (120, 140, 180),
        "black": (30, 28, 32), "eye": (20, 20, 24), "white": (246, 246, 246)}
SHINY = {"green": (200, 140, 220), "green_dark": (130, 70, 160)}


def P(v):
    return pal(BASE, SHINY, v)


GREEN = skin(P, "green", dark="green_dark")


def bellyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x * 0.9, y - 16.0)
        if 5.2 < r < 5.8 and (math.atan2(y - 16.0, x) * 6) % 1.0 < 0.5:
            return tone(p["stitch"], face), None
        if r < 5.6:
            return skin(P, "belly", dark="belly_dark")(x, y, z, face, variant, box=box, **k)
    return GREEN(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gawappamon")
    top = m.bone("gawappamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.0, 7.0, 6.0, 8.0, 24.0, bellyf, cut=3)
    m.round_box(bd, 0, 6.0, 6.6, 2.6, 9.0, 23.0, armour(P, "shell", "shell_dark", trim="green_dark"), cut=2)  # shell
    hd = m.bone("head", bd, (0, 24, -1))
    m.round_box(hd, 0, -1.0, 4.4, 4.2, 23.0, 31.0, GREEN, cut=2)
    m.round_box(hd, 0, -5.6, 2.4, 1.6, 24.4, 26.4, solid(P, "beak"), cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.8, -5.0, 1.0, 0.3, 27.0, 29.0, solid(P, "white"), cut=0)
        m.box(hd, sx * 1.8 - 0.3, 27.4, -5.5, sx * 1.8 + 0.3, 28.4, -5.3, solid(P, "eye"))
        m.round_box(hd, sx * 4.6, 0, 0.8, 1.6, 26.0, 29.0, solid(P, "black"), cut=0)          # headphones
    m.round_box(hd, 0, -0.4, 3.2, 3.2, 30.8, 31.6, metal(P, "disc", dark="disc_dark"), cut=1)  # compact disc
    for i in range(14):                                                                         # dreadlocks
        ang = 2 * math.pi * i / 14
        rod(m, hd, (4.0 * math.cos(ang), 31.0, 4.0 * math.sin(ang) - 0.4),
            (5.6 * math.cos(ang), 27.6, 5.6 * math.sin(ang) - 0.4), 1, strands(P, "dread", "dread_dark"),
            extend=0.3, t2=1)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.6, 20.0, -1.0))
        rod(m, ab, (sx * 6.6, 20.0, -1.0), (sx * 11.0, 22.0, -4.0), 2, GREEN, extend=0.4)
        rod(m, ab, (sx * 11.0, 22.0, -4.0), (sx * 13.0, 18.0, -6.0), 2, GREEN, extend=0.4)
        for j in range(3):
            spike(m, ab, (sx * 13.0 + (j - 1) * 0.9, 17.0, -6.6), (sx * 0.2, -1, -0.4), 0.8, 2.6, GREEN, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 10.0, 0))
        rod(m, lg, (sx * 3.4, 10.0, 0), (sx * 4.0, 3.0, -1.0), 3, GREEN, extend=0.4)
        m.round_box(lg, sx * 4.4, -3.0, 3.4, 4.6, 0.0, 2.0, skin(P, "beak", dark="dread"), cut=1)  # webbed feet
    return m
