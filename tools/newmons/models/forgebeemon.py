"""Forgebeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the forge bee. A round golden armoured ball of a body banded with black-and-yellow hazard stripes and studded with
spikes, a small helmeted face with a gold visor, little brown wings, a huge steel drill-and-pincer arm on the right,
a giant glowing grabber claw on the left and a drill stinger beneath. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a round golden armoured ball banded with hazard stripes and spikes, a helmeted face, small wings, a huge steel "
        "drill-and-pincer arm, a giant glowing grabber claw and a drill stinger")
BASE = {"gold": (220, 180, 60), "gold_dark": (140, 100, 20), "gold_light": (255, 230, 140), "black": (40, 40, 46),
        "black_dark": (16, 16, 20), "yellow": (250, 220, 40), "steel": (170, 174, 186), "steel_dark": (70, 74, 86),
        "glow": (255, 240, 140), "wing": (140, 90, 50), "visor": (250, 200, 60), "red": (200, 40, 30)}
SHINY = {"gold": (180, 190, 210), "gold_dark": (100, 110, 130), "gold_light": (230, 240, 255), "yellow": (80, 220, 250)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.25, rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
DARK = riveted(P, "black", "black_dark")


def hazardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["yellow"] if ((x + y + z) * 0.6) % 2.0 < 1.0 else p["black"], face), None


def bodyf(x, y, z, face, variant, box=None, **k):
    if abs(y - 22.0) < 1.2 or abs(x) > 6.2 and abs(y - 18.0) < 3.0:
        return hazardf(x, y, z, face, variant, box=box, **k)
    return GOLD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("forgebeemon")
    top = m.bone("forgebeemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    ball(m, bd, (0, 18.0, 0), 8.0, bodyf, layers=6)
    for ang in (30, 90, 150, 210, 330):                                                  # spikes
        r = math.radians(ang)
        spike(m, bd, (7.0 * math.cos(r), 18.0 + 7.0 * math.sin(r), 2.0), (math.cos(r), math.sin(r), 0.3), 1.6, 3.6,
              STEEL, tip=0.3)
    hd = m.bone("head", bd, (0, 20, -7))
    m.round_box(hd, 0, -8.0, 2.6, 1.6, 16.0, 22.0, DARK, cut=1)                          # helmeted face
    m.box(hd, -1.8, 18.6, -9.8, 1.8, 19.6, -9.5, solid(P, "visor", glow=True))
    m.box(hd, -0.5, 16.4, -9.8, 0.5, 21.0, -9.5, solid(P, "visor"))
    rod(m, hd, (0, 26.0, -3.0), (0, 29.0, -3.0), 1, solid(P, "red", glow=True), extend=0.2, t2=1)   # beacon
    for sx in (-1, 1):                                                                   # small wings
        x0, x1 = sorted((sx * 3.0, sx * 9.0))
        m.box(bd, x0, 25.0, 6.0, x1, 29.0, 6.0, solid(P, "wing"), rotation=(0, sx * 30, sx * 25),
              pivot=(sx * 3.0, 26.0, 6.0))
    ar = m.bone("arm_right", bd, (-8.0, 18.0, 0))                                        # drill-and-pincer arm
    rod(m, ar, (-7.0, 18.0, 0), (-20.0, 20.0, 0), 4, DARK, extend=0.4)
    for j in range(3):
        m.round_box(ar, -12.0 - j * 3.0, 0, 1.0, 3.0, 17.0, 23.0, hazardf, cut=1)
    for sy in (-1, 1):
        spike(m, ar, (-20.0, 20.0 + sy * 1.4, 0), (-1, sy * 0.15, 0), 1.6, 6.0, STEEL, tip=0.3)
    al = m.bone("arm_left", bd, (8.0, 18.0, 0))                                          # giant grabber claw
    rod(m, al, (7.0, 18.0, 0), (16.0, 18.0, 0), 3, DARK, extend=0.4)
    m.round_box(al, 19.0, 0, 3.4, 5.0, 13.0, 23.0, STEEL, cut=2)
    m.round_box(al, 19.0, -5.2, 2.0, 0.4, 16.0, 20.0, solid(P, "glow", glow=True), cut=0)
    for sy in (-1, 1):
        spike(m, al, (21.0, 18.0 + sy * 4.0, -3.0), (0.3, -sy * 0.3, -1), 2.0, 4.0, DARK, tip=0.4)
    spike(m, bd, (0, 10.6, 0), (0, -1, 0.1), 2.6, 8.0, hazardf, tip=0.3)                  # drill stinger
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 4.0, 11.0, 0))
        spike(m, lg, (sx * 4.0, 12.0, -1.0), (sx * 0.3, -1, -0.4), 1.6, 5.0, DARK, tip=0.4)
    return m
