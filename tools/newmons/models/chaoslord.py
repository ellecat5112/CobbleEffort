"""Chaos Lord (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): the lord of the chaos machines. A hulking red machine-dragon armoured in blocky crimson plates
with yellow trim, a fanged dragon head low between massive grey shoulder blocks, a grey turret tower with red lights
on its back, and four heavy grey limbs that end in great steel drill-spikes and claws. 35 blocks tall.

Front is -z, y is up. 44 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a hulking red machine-dragon in blocky crimson plates with yellow trim, a fanged head between massive grey "
        "shoulder blocks, a turret tower on its back and four drill-spiked grey limbs")
BASE = {"red": (210, 30, 30), "red_dark": (110, 10, 10), "red_light": (250, 120, 110), "yellow": (250, 210, 40),
        "grey": (150, 152, 162), "grey_dark": (70, 72, 82), "grey_light": (210, 212, 222), "steel": (220, 224, 234),
        "steel_dark": (110, 114, 126), "black": (24, 24, 30), "tooth": (240, 240, 240), "light": (255, 60, 40)}
SHINY = {"red": (40, 50, 70), "red_dark": (14, 16, 26), "red_light": (110, 130, 170), "yellow": (80, 230, 230)}


def P(v):
    return pal(BASE, SHINY, v)


RED = armour(P, "red", "red_dark", light="red_light", trim="yellow", trim_w=0.4)
GREY = riveted(P, "grey", "grey_dark", light="grey_light")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("chaoslord")
    top = m.bone("chaoslord", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.box(bd, -10.0, 14.0, -12.0, 10.0, 28.0, 14.0, RED)                              # blocky crimson body
    m.box(bd, -8.0, 28.0, -8.0, 8.0, 31.0, 10.0, RED)
    for sx in (-1, 1):                                                               # massive shoulder blocks
        m.box(bd, min(sx * 8.0, sx * 17.0), 20.0, -14.0, max(sx * 8.0, sx * 17.0), 33.0, -2.0, GREY)
        for j in range(3):
            spike(m, bd, (sx * 13.0, 33.0, -11.0 + j * 4.0), (sx * 0.3, 1, 0), 1.6, 3.0, STEEL)
    tw = m.bone("turret", bd, (0, 31, 4))                                            # turret tower
    m.box(tw, -5.0, 31.0, 0.0, 5.0, 42.0, 9.0, GREY)
    m.box(tw, -3.0, 42.0, 2.0, 3.0, 44.0, 7.0, GREY)
    for j in range(3):
        m.box(tw, -4.0 + j * 3.0, 38.0, -0.4, -2.6 + j * 3.0, 39.6, 0.0, solid(P, "light", glow=True))
    hd = m.bone("head", bd, (0, 22, -14))                                            # fanged dragon head
    m.box(hd, -5.0, 18.0, -26.0, 5.0, 26.0, -12.0, RED)
    m.box(hd, -4.0, 14.0, -25.0, 4.0, 18.0, -14.0, RED, rotation=(14, 0, 0), pivot=(0, 18.0, -14.0))
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.0, sx * 5.2), 23.0, -26.2, max(sx * 1.0, sx * 5.2), 24.0, -16.0, solid(P, "yellow"))
        for i in range(4):
            spike(m, hd, (sx * 3.6, 18.0, -25.0 + i * 2.4), (0, -1, 0), 1.0, 2.0, solid(P, "tooth"))
        spike(m, hd, (sx * 4.0, 26.0, -14.0), (sx * 0.4, 0.6, 1), 1.6, 5.0, STEEL)
    for sx, fz, nm in ((1, -8.0, "leg_front_left"), (-1, -8.0, "leg_front_right"), (1, 10.0, "leg_back_left"),
                       (-1, 10.0, "leg_back_right")):                               # four drill-spiked limbs
        lg = m.bone(nm, top, (sx * 12.0, 20.0, fz))
        m.box(lg, min(sx * 9.0, sx * 15.0), 6.0, fz - 4.0, max(sx * 9.0, sx * 15.0), 22.0, fz + 4.0, GREY)
        m.box(lg, min(sx * 9.4, sx * 14.6), 0.0, fz - 6.0, max(sx * 9.4, sx * 14.6), 6.0, fz + 3.0, GREY)
        for j in range(3):
            spike(m, lg, (sx * 12.0 + (j - 1) * 1.8, 1.4, fz - 6.0), (0, -0.2, -1), 1.4, 3.0, STEEL)
        spike(m, lg, (sx * 15.0, 14.0, fz), (sx, -0.2, -0.6 if fz < 0 else 0.6), 3.4, 12.0, STEEL, tip=1.0)
    return m
