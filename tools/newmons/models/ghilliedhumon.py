"""Ghilliedhumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the sniper in the moss: a hulking shape draped in a shaggy ghillie suit of green and brown moss
and vines, two curved horns, a dark face with glowing orange eyes, big grey gloved hands with red claws cradling a
long scoped rifle hung with little skull charms, and red-spiked boots. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, leather, metal, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hulking shape in a shaggy green-and-brown ghillie suit with curved horns, glowing orange eyes, grey gloves "
        "with red claws and a long scoped rifle hung with skull charms")
BASE = {"moss": (70, 110, 50), "moss_dark": (30, 60, 20), "moss_light": (140, 170, 80), "brown": (120, 90, 50),
        "face": (24, 22, 26), "eye": (250, 160, 40), "glove": (150, 150, 160), "glove_dark": (80, 80, 90),
        "claw": (210, 40, 40), "horn": (200, 190, 150), "gun": (60, 60, 66), "gun_dark": (24, 24, 30),
        "stock": (130, 90, 50), "skull": (240, 220, 120)}
SHINY = {"moss": (180, 170, 150), "moss_dark": (110, 100, 80), "moss_light": (230, 220, 200)}


def P(v):
    return pal(BASE, SHINY, v)


MOSS = fur(P, "moss", "moss_dark", tip="moss_light", length=2.0, density=1.8)
GLOVE = leather(P, "glove", "glove_dark")
GUN = metal(P, "gun", dark="gun_dark")


def build():
    m = Model("ghilliedhumon")
    top = m.bone("ghilliedhumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 22.0, 2.0), 13.0, MOSS, layers=7, ry=14.0)                          # shaggy ghillie mass
    for i in range(10):                                                                 # trailing moss strands
        ang = 2 * math.pi * i / 10
        spike(m, bd, (11.0 * math.cos(ang), 10.0, 2.0 + 10.0 * math.sin(ang)), (math.cos(ang) * 0.3, -1, math.sin(ang) * 0.3),
              2.4, 6.0, MOSS, tip=1.0)
    hd = m.bone("head", bd, (0, 32, -6))
    m.box(hd, -4.0, 28.0, -11.2, 4.0, 34.0, -10.6, solid(P, "face"))                    # dark face
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 2.6), 31.0, -11.4, max(sx * 1.0, sx * 2.6), 32.2, -11.2, solid(P, "eye", glow=True))
        pts = [(sx * 6.0, 36.0, -2.0), (sx * 10.0, 42.0, 0.0), (sx * 9.0, 47.0, 2.0)]   # curved horns
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, solid(P, "horn"), extend=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 24.0, -6.0))
        rod(m, ab, (sx * 10.0, 24.0, -6.0), (sx * 6.0, 18.0, -14.0), 4, MOSS, extend=0.6)
        m.round_box(ab, sx * 5.0, -15.0, 3.0, 3.0, 15.0, 21.0, GLOVE, cut=1)
        for j in range(3):
            spike(m, ab, (sx * 5.0 + (j - 1) * 1.6, 15.0, -17.0), (0, -0.4, -1), 0.9, 2.6, solid(P, "claw"), tip=0.8)
    rb = m.bone("rifle", bd, (0, 20, -14))                                               # long scoped rifle
    rod(m, rb, (14.0, 22.0, -12.0), (-22.0, 30.0, -16.0), 2, GUN, extend=0)
    m.round_box(rb, 8.0, -12.0, 3.0, 1.4, 18.0, 22.0, metal(P, "stock", dark="brown"), cut=0)
    rod(m, rb, (2.0, 24.4, -14.0), (-6.0, 26.2, -14.6), 2, GUN, extend=0)
    for j in range(2):
        m.round_box(rb, -2.0 + j * 4.0, -14.6, 1.2, 1.0, 19.0, 21.4, solid(P, "skull"), cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 10.0, 0))
        m.round_box(lg, sx * 5.0, -1.0, 3.0, 3.6, 0.0, 10.0, MOSS, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 1.6, 0.6, -4.6), (0, -0.4, -1), 1.2, 3.0, solid(P, "claw"), tip=0.8)
    return m
