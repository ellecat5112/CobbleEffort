"""Omekamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a boxy grey cardboard puppet decorated like a child's craft: a square head with angry yellow eyes and
a jagged red mouth, coloured paper cones taped on as horns and spikes (cyan, yellow, red, blue), a painted character on
its chest, stubby legs, and a giant rainbow-banded crayon slung on its back with a marker for one hand. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, local, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a boxy grey cardboard puppet with angry yellow eyes, a jagged red mouth, coloured paper-cone horns and spikes and "
        "a giant rainbow crayon on its back")
BASE = {"grey": (200, 204, 210), "grey_dark": (130, 134, 140), "yellow": (250, 220, 50), "red": (220, 40, 40),
        "cyan": (80, 200, 230), "blue": (40, 70, 190), "black": (30, 28, 30), "green": (80, 180, 70),
        "orange": (240, 140, 40), "violet": (130, 80, 190)}
SHINY = {"grey": (230, 200, 160), "grey_dark": (170, 140, 100)}


def P(v):
    return pal(BASE, SHINY, v)


CARD = fabric(P, "grey", "grey_dark", axis="x", period=3.0)


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 4.0 and 14.0 < y < 22.0:
        if abs(abs(x) - 3.2) < 0.4:
            return tone(p["blue"], face), None
        if abs(x) < 2.0 and (abs(y - 18.0) < 0.5 or abs(x - (y - 18.0) * 0.5) < 0.4):
            return tone(p["red"], face), None
    return CARD(x, y, z, face, variant, box=box, **k)


def crayonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    bands = ["red", "orange", "yellow", "green", "cyan", "blue", "violet"]
    return tone(p[bands[int(((x + y) * 0.5) % 7)]], face), None


def build():
    m = Model("omekamon")
    top = m.bone("omekamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.box(bd, -6.0, 8.0, -4.0, 6.0, 24.0, 4.0, chestf)                                   # box body
    hd = m.bone("head", bd, (0, 24, 0))
    m.box(hd, -6.0, 24.0, -4.4, 6.0, 36.0, 4.4, CARD)                                    # square head
    for sx in (-1, 1):
        m.box(hd, sx * 2.6 - 1.4, 30.0, -4.6, sx * 2.6 + 1.4, 32.0, -4.4, solid(P, "yellow"))
        m.box(hd, sx * 2.6 - 0.5, 30.4, -4.65, sx * 2.6 + 0.5, 31.4, -4.6, solid(P, "black"))
    m.box(hd, -4.0, 26.0, -4.6, 4.0, 28.0, -4.4, solid(P, "red"))
    for i, (cx, key, d) in enumerate(((-5.0, "cyan", (-0.6, 1, 0)), (5.0, "yellow", (0.6, 1, 0)))):   # paper-cone horns
        spike(m, hd, (cx, 36.0, 0), d, 3.0, 6.0, solid(P, key), tip=0.8)
    for j, (pos, key, d) in enumerate((((-6.0, 18.0, -2.0), "red", (-1, 0.2, -0.3)), ((-6.0, 12.0, 0), "blue", (-1, -0.2, 0)),
                                       ((6.0, 14.0, -2.0), "yellow", (1, -0.2, -0.3)))):
        spike(m, bd, pos, d, 2.6, 5.0, solid(P, key), tip=0.8)
    rod(m, bd, (-4.0, 14.0, 5.0), (8.0, 40.0, 5.0), 4, crayonf, extend=0.6)              # giant crayon
    spike(m, bd, (8.6, 41.4, 5.0), (0.4, 1, 0), 2.6, 3.0, solid(P, "red"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 20.0, 0))
        rod(m, ab, (sx * 6.0, 20.0, 0), (sx * 9.0, 14.0, -2.0), 3, CARD, extend=0.4)
        if sx > 0:                                                                       # marker hand
            rod(m, ab, (9.0, 14.0, -2.0), (11.0, 8.0, -4.0), 2, solid(P, "grey"), extend=0.3)
            spike(m, ab, (11.0, 8.0, -4.0), (0.3, -1, -0.3), 1.6, 2.0, solid(P, "blue"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 8.0, 0))
        m.box(lg, sx * 3.0 - 2.0, 0.0, -3.0, sx * 3.0 + 2.0, 8.0, 3.0, CARD)
    return m
