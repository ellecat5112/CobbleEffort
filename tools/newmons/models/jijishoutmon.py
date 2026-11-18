"""Jiji Shoutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
an old Shoutmon: a red dragon-imp with a long snout, a bushy white beard and wild grey hair, a green earphone on its
head, big blue eyes, a cream belly, white-furred cuffs, black claws, a red tail and a wooden staff topped with a yellow
horned paw. Child stage (no level on wikimon), 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fur, skin, solid, strands
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "an old red dragon-imp with a bushy white beard, wild grey hair, a green earphone and a horned yellow paw staff"
BASE = {"red": (220, 50, 50), "red_dark": (140, 20, 24), "red_light": (250, 140, 130), "white": (246, 246, 246),
        "white_dark": (180, 180, 186), "grey": (190, 190, 200), "grey_dark": (120, 120, 130), "green": (60, 160, 70),
        "eye": (60, 120, 220), "pupil": (16, 16, 24), "black": (30, 30, 34), "yellow": (250, 210, 60),
        "yellow_dark": (200, 150, 20), "wood": (140, 100, 60), "mouth": (220, 120, 140)}
SHINY = {"red": (60, 110, 210), "red_dark": (20, 50, 140), "red_light": (150, 190, 250)}


def P(v):
    return pal(BASE, SHINY, v)


RED = skin(P, "red", dark="red_dark", light="red_light")
BEARD = fur(P, "white", "white_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot(x - sx * 1.6, y - 22.4)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["eye"], face), None
    return RED(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("jijishoutmon")
    top = m.bone("jijishoutmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0, 3.4, 2.8, 6.0, 15.0, RED, cut=1)
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 3.6, 3.4, 15.0, 24.6, headf, cut=1)
    m.round_box(hd, 0, -4.2, 2.6, 1.6, 17.0, 20.6, RED, cut=1)                             # long snout
    m.round_box(hd, 0, -5.0, 1.8, 0.6, 17.4, 18.6, solid(P, "mouth"), cut=0)
    for i in range(9):                                                               # bushy beard
        ang = math.radians(-80 + i * 20)
        spike(m, hd, (3.0 * math.sin(ang), 16.4, -3.0 * math.cos(ang) - 1.0), (math.sin(ang) * 0.3, -1, -0.3), 1.8, 4.0,
              BEARD, tip=0.8)
    for i in range(9):                                                               # wild grey hair
        ang = math.radians(-100 + i * 25)
        spike(m, hd, (3.0 * math.sin(ang), 24.0, 1.0 + 2.0 * math.cos(ang)), (math.sin(ang) * 0.7, 0.7, 0.6), 1.6, 4.0,
              strands(P, "grey", "grey_dark"), tip=0.8)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.8, 0, 0.6, 1.4, 21.0, 23.6, solid(P, "green"), cut=0)          # earphone
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 13.0, 0))
        rod(m, ab, (sx * 3.4, 13.0, 0), (sx * 5.4, 9.0, -1.0), 1, RED, extend=0.3, t2=2)
        m.round_box(ab, sx * 5.6, -1.0, 1.4, 1.4, 7.6, 9.4, BEARD, cut=0)
    rod(m, "arm_right", (-5.6, 1.0, -2.0), (-7.0, 27.0, -2.6), 1, solid(P, "wood"), extend=0, t2=1)   # paw staff
    m.round_box("arm_right", -7.2, -2.6, 2.4, 1.6, 26.0, 30.0, skin(P, "yellow", dark="yellow_dark"), cut=1)
    for sx in (-1, 1):
        spike(m, "arm_right", (-7.2 + sx * 1.8, 29.6, -2.6), (sx * 0.4, 1, 0), 0.9, 2.4, skin(P, "yellow", dark="yellow_dark"),
              tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 6.0, 0))
        rod(m, lg, (sx * 2.0, 6.4, 0), (sx * 2.4, 1.6, 0), 2, RED, extend=0.3)
        m.round_box(lg, sx * 2.4, -1.0, 1.6, 2.4, 0.0, 1.8, RED, cut=0)
        for j in range(3):
            spike(m, lg, (sx * 2.4 + (j - 1) * 0.9, 0.6, -3.2), (0, -0.2, -1), 0.8, 1.2, solid(P, "black"), tip=0.8)
    tb = m.bone("tail", bd, (0, 7, 2))
    rod(m, tb, (0, 7.0, 2.4), (2.0, 4.0, 7.0), 2, RED, extend=0.3, t2=1)
    return m
