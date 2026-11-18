"""Pteromon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little bird-dragon: a green feathered body with a cream belly and white ruff, a white beaked head
with a long red-tipped horn and red-edged crest, violet eyes, green feathered wing-arms tipped red, a feathered tail
and yellow taloned feet, a little whirlwind spinning by its claw. 1 block.

Front is -z, y is up. 28 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, fan
from _digidetail import feathers, skin, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(1, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a green feathered bird-dragon with a white beaked head, a long red-tipped horn, red-tipped wing-arms and yellow talons"
BASE = {"green": (90, 180, 80), "green_dark": (30, 110, 40), "white": (246, 244, 236), "white_dark": (190, 186, 170),
        "cream": (240, 230, 190), "red": (210, 50, 40), "eye": (120, 70, 180), "pupil": (24, 20, 30),
        "yellow": (250, 200, 60), "black": (30, 30, 34), "wind": (170, 230, 240, 170)}
SHINY = {"green": (80, 140, 210), "green_dark": (30, 80, 150)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = feathers(P, "green", "green_dark", tip="red")
HEAD = skin(P, "white", dark="white_dark")


def build():
    m = Model("pteromon")
    top = m.bone("pteromon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0.6), 4.6, FEATH, layers=4, ry=5.4)
    m.round_box(bd, 0, -3.0, 2.6, 1.4, 8.0, 15.0, solid(P, "cream"), cut=1)
    m.round_box(bd, 0, 0, 4.2, 4.0, 16.0, 18.0, feathers(P, "white", "white_dark"), cut=1)          # white ruff
    hd = m.bone("head", bd, (0, 18, 0))
    ball(m, hd, (0, 21.0, -0.4), 3.6, HEAD, layers=3, ry=3.2)
    spike(m, hd, (0, 20.4, -3.4), (0, -0.3, -1), 1.6, 3.0, solid(P, "yellow"), tip=0.8)
    for sx in (-1, 1):
        m.box(hd, min(sx * 1.4, sx * 2.6), 21.4, -3.6, max(sx * 1.4, sx * 2.6), 22.4, -3.3, solid(P, "eye"))
    spike(m, hd, (0, 23.6, -1.0), (0, 1, -0.6), 1.8, 8.0, HEAD, tip=0.8)                   # long horn
    spike(m, hd, (0, 28.6, -4.0), (0, 0.8, -0.6), 1.0, 2.6, solid(P, "red"), tip=0.8)
    for j in range(3):
        spike(m, hd, (0, 23.0 - j, 2.0 + j), (0, 0.6, 1), 1.2, 4.0, FEATH, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 4.0, 15.0, 0))
        fan(m, ab, (sx * 4.0, 15.0, 0), 4, 7.0, 1.6, -20, -60, FEATH, plane="xy", side=sx)
        for f in range(3):
            spike(m, ab, (sx * 8.0, 11.0, -0.6 + f * 0.6), (sx * 0.2, -1, -0.4), 0.8, 2.2, solid(P, "black"), tip=0.8)
    tl = m.bone("tail", bd, (0, 9, 4))
    for j in range(3):
        spike(m, tl, (0, 9.0, 4.0), ((j - 1) * 0.4, -0.2, 1), 1.4, 6.0, FEATH, tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.0, 7.0, 0))
        rod(m, lg, (sx * 2.0, 7.0, 0), (sx * 2.4, 2.0, -0.4), 1, solid(P, "yellow"), extend=0.2, t2=2)
        for f in range(3):
            spike(m, lg, (sx * 2.4 + (f - 1) * 0.8, 0.8, -0.6), ((f - 1) * 0.3, -0.4, -1), 0.8, 2.4, solid(P, "black"),
                  tip=0.8)
    for j in range(4):                                                                   # whirlwind
        r = 1.0 + j * 0.8
        m.round_box("arm_right", -11.0, -2.0, r, r, 12.0 + j * 1.4, 13.0 + j * 1.4, solid(P, "wind"), cut=0)
    return m
