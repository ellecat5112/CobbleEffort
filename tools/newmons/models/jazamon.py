"""Jazamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little machine bird-dragon: a silver robot body with a navy face plate and red eyes under a crest of swept silver
spikes tipped with ice-blue, wide jointed silver wings of fanned blades with blue lights, blue-glowing joint lenses,
sturdy clawed legs with ice-blue talons and a short tail. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 2.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little silver robot bird-dragon with a navy face plate, red eyes, a crest of swept spikes and wide bladed wings"
BASE = {"silver": (210, 214, 224), "silver_dark": (90, 94, 110), "silver_light": (250, 252, 255), "navy": (30, 40, 90),
        "eye": (240, 40, 40), "ice": (120, 220, 255), "ice_light": (230, 250, 255), "black": (30, 30, 40)}
SHINY = {"silver": (220, 190, 110), "silver_dark": (130, 100, 40), "silver_light": (255, 240, 190)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "silver", "silver_dark", light="silver_light", trim="black", trim_w=0.2)
STEEL = metal(P, "silver", dark="silver_dark", light="silver_light")
ICE = solid(P, "ice", glow=True)


def build():
    m = Model("jazamon")
    top = m.bone("jazamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.4, 9.0, 17.0, ARM, cut=1)
    m.round_box(bd, 0, -3.0, 1.2, 0.6, 12.4, 14.6, gem(P, "ice", "ice_light"), cut=0)
    hd = m.bone("head", bd, (0, 17, -1))
    m.round_box(hd, 0, -1.0, 3.2, 3.6, 16.6, 23.0, ARM, cut=1)
    m.round_box(hd, 0, -4.4, 2.4, 1.0, 17.0, 20.6, solid(P, "navy"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 19.4, -5.5, max(sx * 0.8, sx * 2.4), 20.4, -5.3, solid(P, "eye", glow=True))
    for i in range(6):                                                               # crest of swept spikes
        ang = math.radians(-50 + i * 20)
        spike(m, hd, (2.2 * math.sin(ang), 22.6, -1.0 + i * 0.4), (math.sin(ang) * 0.6, 0.8, 0.8), 1.6,
              6.0 - abs(i - 2.5) * 0.5, STEEL, tip=0.8)
        spike(m, hd, (2.2 * math.sin(ang) + math.sin(ang) * 3.0, 26.0, 2.6 + i * 0.4), (math.sin(ang) * 0.6, 0.8, 0.8),
              0.8, 1.6, ICE, tip=0.8)
    for side in (1, -1):                                                             # bladed wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.4, 16.0, 2.0))
        rod(m, wb, (side * 3.4, 16.0, 2.0), (side * 8.0, 22.0, 3.0), 1, STEEL, extend=0.3, t2=1)
        m.round_box(wb, side * 8.0, 3.0, 1.0, 1.0, 21.0, 23.0, gem(P, "ice", "ice_light"), cut=0)
        rod(m, wb, (side * 8.0, 22.0, 3.0), (side * 14.0, 24.0, 4.0), 1, STEEL, extend=0.3, t2=1)
        for j in range(5):
            ang = math.radians(10 - j * 22)
            spike(m, wb, (side * (8.0 + j * 1.4), 22.0 + j * 0.4, 3.4), (side * math.cos(ang), math.sin(ang), 0.2), 1.6,
                  8.0 - j * 0.6, STEEL, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 15.0, -1.0))
        rod(m, ab, (sx * 3.6, 15.0, -1.0), (sx * 4.6, 11.0, -3.0), 1, STEEL, extend=0.3, t2=1)
        for j in range(3):
            spike(m, ab, (sx * 4.6 + (j - 1) * 0.6, 10.6, -3.6), (0, -0.6, -1), 0.8, 2.4, ICE, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 10.0, 0))
        rod(m, lg, (sx * 2.2, 10.0, 0), (sx * 2.8, 5.0, 1.0), 2, ARM, extend=0.4)
        m.round_box(lg, sx * 2.8, 1.0, 1.0, 1.0, 4.4, 6.0, gem(P, "ice", "ice_light"), cut=0)
        rod(m, lg, (sx * 2.8, 5.0, 1.0), (sx * 2.8, 1.0, 0), 1, STEEL, extend=0.3, t2=1)
        for j in range(3):
            spike(m, lg, (sx * 2.8 + (j - 1) * 0.8, 0.6, -0.6), ((j - 1) * 0.3, -0.2, -1), 0.8, 2.6, ICE, tip=0.8)
    rod(m, bd, (0, 10.0, 3.0), (0, 8.0, 8.0), 1, STEEL, extend=0.3, t2=2)
    return m
