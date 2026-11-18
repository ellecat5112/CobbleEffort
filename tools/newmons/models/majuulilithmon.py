"""Majuu Lilithmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the anime still on wikimon.net):
Lilithmon riding her demon beast: a hulking dark-red bear-like beast bristling with huge icy-blue crystal spikes, an
icy crystal mask over its face, a golden ring at its chest, thick clawed legs, and the robed Demon Lord herself seated
on its back in a dark gown with a horned headdress. 35 blocks tall (no level on wikimon: built as Ultimate, like
Lilithmon).

Front is -z, y is up. 50 units tall; Ultimate stage. The rider is fully robed.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, gem, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 7.0)
KIND = "quadruped"
K = 3
LOOK = "a hulking dark-red beast bristling with icy-blue crystal spikes and a crystal mask, ridden by a robed Demon Lord with a horned headdress"
BASE = {"red": (110, 30, 30), "red_dark": (50, 10, 10), "red_light": (170, 70, 60), "ice": (180, 210, 250),
        "ice_light": (240, 250, 255), "gold": (230, 160, 40), "gold_dark": (150, 90, 10), "black": (30, 28, 34),
        "black_dark": (10, 8, 12), "skin": (232, 214, 220), "skin_dark": (180, 150, 170), "claw": (60, 56, 60),
        "horn": (220, 150, 60)}
SHINY = {"red": (50, 50, 110), "red_dark": (16, 16, 50), "red_light": (110, 110, 180)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "red", "red_dark", tip="red_light", length=1.6)
ICE = gem(P, "ice", "ice_light", glow=False)


def build():
    m = Model("majuulilithmon")
    top = m.bone("majuulilithmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.round_box(bd, 0, 2.0, 10.0, 12.0, 10.0, 30.0, FUR, cut=4)
    m.round_box(bd, 0, -10.6, 2.0, 0.8, 18.0, 22.0, metal(P, "gold", dark="gold_dark"), cut=1)       # gold ring
    hd = m.bone("head", bd, (0, 22, -12))
    m.round_box(hd, 0, -12.0, 5.0, 3.0, 18.0, 28.0, FUR, cut=2)
    for j in range(5):                                                               # crystal mask
        ang = math.radians(-60 + j * 30)
        spike(m, hd, (2.0 * math.sin(ang), 24.0, -14.6), (math.sin(ang), math.cos(ang) * 0.6 + 0.2, -0.5), 1.6, 6.0, ICE, tip=0.8)
    for j, (px, py, pz, ln) in enumerate(((-8, 30, -4, 22.0), (8, 30, -4, 22.0), (-4, 32, 6, 16.0), (4, 32, 6, 16.0),
                                          (0, 30, 12, 12.0), (-10, 24, 8, 10.0), (10, 24, 8, 10.0))):   # crystal spikes
        spike(m, bd, (px, py, pz), (px * 0.06, 1, pz * 0.04), 2.4, ln, ICE, tip=0.8)
    for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                       (-1, 1, "leg_back_right")):
        lg = m.bone(nm, top, (sx * 7.0, 12.0, sz * 7.0))
        m.round_box(lg, sx * 8.0, sz * 7.0, 3.6, 4.0, 0.0, 14.0, FUR, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 8.0 + (j - 1) * 2.0, 1.0, sz * 7.0 - 4.0), (0, -0.2, -1), 1.4, 3.0, solid(P, "claw"), tip=0.8)
    rb = m.bone("rider", bd, (0, 30, 2))                                              # the seated Demon Lord
    m.round_box(rb, 0, 2.0, 2.4, 2.0, 30.0, 38.0, fabric(P, "black", "black_dark"), cut=1)
    m.round_box(rb, 0, 0.0, 3.0, 4.0, 30.0, 32.0, fabric(P, "black", "black_dark"), cut=1)
    m.round_box(rb, 0, 2.0, 1.6, 1.6, 38.0, 42.0, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(rb, 0, 2.6, 2.0, 1.6, 40.0, 43.0, strands(P, "black", "black_dark"), cut=1)
    for sx in (-1, 1):
        spike(m, rb, (sx * 1.4, 42.6, 2.0), (sx * 0.6, 1, 0), 1.0, 3.0, solid(P, "horn"), tip=0.8)
    return m
