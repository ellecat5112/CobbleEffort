"""Gigadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the cyborg dragon twin of Megadramon: a dark green armoured dragon head with yellow eyes and a
toothed jaw, great dark-green swept-back jet wings, violet hide, two huge mechanical arms ending in grey drill-claw
cannons, and a long violet serpentine tail coiled beneath. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "floater"
K = 3
LOOK = ("a cyborg dragon with a dark green armoured head, great swept-back jet wings, violet hide, mechanical arms "
        "ending in drill-claw cannons and a coiled violet tail")
BASE = {"green": (60, 90, 70), "green_dark": (24, 40, 30), "green_light": (120, 160, 130), "violet": (130, 90, 170),
        "violet_dark": (70, 40, 110), "steel": (190, 196, 210), "steel_dark": (90, 96, 110), "eye": (250, 220, 40),
        "mouth": (120, 20, 30), "tooth": (250, 250, 240), "red": (200, 40, 40)}
SHINY = {"green": (170, 60, 50), "green_dark": (90, 20, 14), "green_light": (230, 130, 110), "violet": (60, 90, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "green", "green_dark", light="green_light", trim="steel", trim_w=0.25)
HIDE = scales(P, "violet", "violet_dark", size=1.4)
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("gigadramon")
    top = m.bone("gigadramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    m.round_box(bd, 0, 0, 6.0, 7.0, 22.0, 34.0, ARM, cut=2)                            # armoured torso
    hd = m.bone("head", bd, (0, 34, -6))
    m.round_box(hd, 0, -10.0, 4.0, 7.0, 32.0, 39.0, ARM, cut=2)                        # long dragon head
    m.box(hd, -3.0, 32.6, -17.2, 3.0, 34.0, -16.9, solid(P, "mouth"))
    for j in range(6):
        spike(m, hd, (-2.6 + j * 1.04, 34.0, -16.6), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 4.0, sx * 4.2), 36.4, -12.0, max(sx * 4.0, sx * 4.2), 37.4, -10.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 39.0, -5.0), (sx * 0.3, 0.6, 1), 1.6, 7.0, ARM, tip=0.9)       # swept horns
    for side in (1, -1):                                                                     # jet wings
        for j in range(4):
            x0, x1 = sorted((side * 5.0, side * (30.0 - j * 3.0)))
            m.box(bd, x0, 34.0 - j * 3.0, 4.0 + j * 0.8, x1, 35.6 - j * 3.0, 9.0 + j * 0.8, ARM,
                  rotation=(0, side * 12, side * (14 - j * 5)), pivot=(side * 5.0, 35.0 - j * 3.0, 6.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                      # drill-claw cannons
        ab = m.bone(nm, bd, (sx * 6.0, 30.0, -2.0))
        rod(m, ab, (sx * 6.0, 30.0, -2.0), (sx * 12.0, 22.0, -6.0), 3, STEEL, extend=0.6)
        rod(m, ab, (sx * 12.0, 22.0, -6.0), (sx * 12.0, 14.0, -12.0), 4, ARM, extend=0.6)
        for j in range(3):
            ang = math.radians(j * 120)
            spike(m, ab, (sx * 12.0 + 1.6 * math.cos(ang), 13.0 + 1.6 * math.sin(ang), -14.0), (0, -0.3, -1), 1.2,
                  4.0, STEEL, tip=0.8)
    tb = m.bone("tail", bd, (0, 22, 2))                                                       # coiled violet tail
    pts = [(0, 22.0, 2.0), (2.0, 14.0, 6.0), (6.0, 8.0, 2.0), (4.0, 4.0, -4.0), (-2.0, 3.0, -2.0), (-4.0, 6.0, 4.0),
           (-2.0, 2.0, 10.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, max(2, 5 - j // 2), HIDE, extend=0.6)
    return m
