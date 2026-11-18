"""Owlmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of knowledge: a stocky owl armoured in white plate with red-lit eye lenses behind a
grey visor, a violet swirl on its helm, two horn-like white crest plumes, a brown-and-white feathered breast, broad
brown wings and yellow talons tipped silver. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult (Armor) stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, feather_wing
from _digidetail import armour, feathers, metal, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a stocky owl in white plate armour with red eye lenses behind a grey visor, white crest plumes, a brown "
        "feathered breast, broad brown wings and yellow talons")
BASE = {"white": (240, 242, 248), "white_dark": (160, 164, 184), "brown": (130, 80, 40), "brown_dark": (70, 40, 16),
        "grey": (120, 124, 136), "red": (230, 40, 40), "violet": (130, 90, 190), "yellow": (240, 200, 50),
        "steel": (210, 214, 226)}
SHINY = {"brown": (70, 70, 80), "brown_dark": (30, 30, 36), "white": (240, 220, 160)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "white", "white_dark", trim="grey", trim_w=0.3)
FEATH = feathers(P, "brown", "brown_dark", tip="white")


def build():
    m = Model("owlmon")
    top = m.bone("owlmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 18.0, 0.4), 7.0, PLATE, layers=5, ry=8.0)
    ball(m, bd, (0, 16.0, -4.0), 4.6, FEATH, layers=4, ry=6.0, squash=0.5)                 # feathered breast
    hd = m.bone("head", bd, (0, 25, 0))
    m.round_box(hd, 0, -0.4, 5.0, 4.6, 25.0, 34.0, PLATE, cut=2)                          # helm
    m.box(hd, -4.0, 28.0, -5.1, 4.0, 31.0, -4.9, solid(P, "grey"))                        # visor
    for sx in (-1, 1):
        ball(m, hd, (sx * 1.8, 29.6, -5.2), 1.0, solid(P, "red", glow=True), layers=1)
        spike(m, hd, (sx * 3.4, 34.0, 0), (sx * 0.4, 1, 0.2), 1.8, 6.0, PLATE, tip=0.8)     # crest plumes
    m.box(hd, -1.2, 31.6, -4.85, 1.2, 33.2, -4.7, solid(P, "violet"))
    spike(m, hd, (0, 27.6, -5.0), (0, -0.6, -1), 1.0, 1.6, solid(P, "yellow"), tip=0.8)
    for side in (1, -1):                                                                 # broad brown wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 22.0, 0))
        feather_wing(m, wb, (side * 6.0, 22.0, 0), 18.0, 12.0, 6, FEATH, side=side, sweep=20, droop=-6.0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 10.0, 0))
        rod(m, lg, (sx * 3.0, 11.0, 0), (sx * 3.4, 4.0, 0), 2, PLATE, extend=0.3)
        m.round_box(lg, sx * 3.4, -0.4, 1.6, 1.6, 2.0, 4.0, solid(P, "yellow"), cut=0)
        for f in range(3):
            spike(m, lg, (sx * 3.4 + (f - 1) * 0.9, 2.0, -1.0), (0, -0.8, -0.6), 0.9, 2.6, metal(P, "steel"), tip=0.8)
    return m
