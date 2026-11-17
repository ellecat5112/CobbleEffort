"""Digitamamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the egg. A huge smooth white eggshell with fine cracks, a jagged hole in its front opening onto pure
darkness where two yellow eyes glow, and two stubby green scaly legs bursting from its underside, each with three big
pink-red claws. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import scales, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a huge white eggshell with fine cracks and a jagged hole onto darkness with two glowing yellow eyes, on stubby "
        "green scaly legs with pink-red claws")
BASE = {"shell": (246, 246, 250), "shell_dark": (180, 184, 200), "crack": (60, 60, 70), "dark": (16, 14, 20),
        "eye": (250, 230, 60), "green": (110, 200, 70), "green_dark": (40, 110, 30), "green_light": (180, 240, 140),
        "claw": (240, 70, 110), "claw_light": (255, 170, 190)}
SHINY = {"shell": (250, 240, 200), "shell_dark": (200, 180, 120), "green": (90, 140, 220), "green_dark": (30, 60, 140)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = skin(P, "shell", dark="shell_dark", var=0.02)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, (y - 27.0) * 1.2)
        a = math.atan2(y - 27.0, x)
        jag = 5.4 + 1.2 * abs(((a * 9 / math.pi) % 2.0) - 1.0)
        if r < jag:
            for sx in (-1, 1):
                if abs(x - sx * 1.8) < 0.5 and abs(y - 27.4) < 0.9:
                    return p["eye"], p["eye"]
            return tone(p["dark"], face), None
        if r < jag + 0.4:
            return tone(p["crack"], face), None
    if abs(((x * 0.8 + y * 0.5 + z * 0.3) % 9.0) - 4.5) < 0.1 and face != "down":
        return tone(p["crack"], face), None                           # fine cracks
    return SHELL(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("digitamamon")
    top = m.bone("digitamamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    ball(m, bd, (0, 22.0, 0), 13.0, shellf, layers=10, squash=0.95, ry=17.0)         # the egg
    hd = m.bone("head", bd, (0, 30, -10))
    LEG = scales(P, "green", "green_dark", size=1.2, light="green_light", rim_mix=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 8.0, 0))
        m.round_box(lg, sx * 7.0, -1.0, 4.4, 5.0, 0.0, 8.0, LEG, cut=2)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 2.6, 1.4, -5.6), ((j - 1) * 0.2, -0.3, -1), 2.0, 4.6,
                  solid(P, "claw"), tip=0.8)
    return m
