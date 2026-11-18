"""Majiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the snake of the Twelve Devas: a long green dragon-serpent with a pale yellow banded belly, golden
antler horns, a long white beard and wild white mane, three-clawed arms on long serpentine limbs, a golden shell-plate
on its back, a long tasselled tail, and a violet sash knotted round its upper body. 25 blocks long.

Front is -z, y is up. 34 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
LOOK = "a long green dragon-serpent with golden antlers, a white beard and mane, long clawed serpentine arms, a golden shell plate and a violet sash"
BASE = {"green": (80, 160, 70), "green_dark": (30, 90, 30), "green_light": (160, 220, 130), "belly": (240, 220, 140),
        "belly_dark": (190, 160, 80), "gold": (240, 200, 70), "gold_dark": (160, 120, 20), "white": (246, 246, 246),
        "white_dark": (190, 190, 196), "violet": (150, 90, 190), "violet_dark": (80, 40, 110), "claw": (240, 236, 220),
        "eye": (240, 60, 40), "mouth": (180, 40, 50)}
SHINY = {"green": (70, 90, 170), "green_dark": (24, 34, 100), "green_light": (150, 170, 240)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "green", "green_dark", size=1.4, light="green_light", belly_key="belly", belly=lambda x, y, z, f: f == "down")


def build():
    m = Model("majiramon")
    top = m.bone("majiramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    pts = [(0, 22.0, -10.0), (0, 16.0, -4.0), (2.0, 8.0, 4.0), (-2.0, 5.0, 12.0), (2.0, 5.0, 20.0), (0, 8.0, 28.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                # serpent body
        rod(m, bd, p0, p1, 5 - j // 2, HIDE, extend=1.0)
    m.round_box(bd, 0, 2.0, 5.0, 6.0, 9.0, 15.0, armour(P, "gold", "gold_dark"), cut=2)       # golden shell plate
    m.round_box(bd, 0, -6.0, 5.4, 3.0, 14.0, 17.0, fabric(P, "violet", "violet_dark"), cut=1)  # violet sash
    hd = m.bone("head", bd, (0, 24, -12))
    m.round_box(hd, 0, -14.0, 3.0, 4.4, 22.0, 28.0, HIDE, cut=1)
    m.round_box(hd, 0, -16.0, 2.4, 3.0, 20.0, 22.0, solid(P, "mouth"), cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.9, sx * 3.2), 26.0, -16.0, max(sx * 2.9, sx * 3.2), 27.0, -14.6, solid(P, "eye", glow=True))
        pts2 = [(sx * 2.0, 28.0, -12.0), (sx * 5.0, 33.0, -11.0), (sx * 7.0, 35.0, -8.0)]       # golden antlers
        for p0, p1 in zip(pts2, pts2[1:]):
            rod(m, hd, p0, p1, 1, metal(P, "gold", dark="gold_dark"), extend=0.2, t2=1)
        spike(m, hd, (sx * 5.0, 33.0, -11.0), (sx * 0.4, 1, -0.4), 0.9, 2.4, metal(P, "gold", dark="gold_dark"), tip=0.8)
    for j in range(5):                                                               # white beard + mane
        rod(m, hd, ((j - 2) * 0.8, 20.6, -16.0), ((j - 2) * 1.2, 12.0, -16.0), 1, strands(P, "white", "white_dark"),
            extend=0.2, t2=1)
        spike(m, hd, ((j - 2) * 1.0, 28.0, -10.0 + j), (0, 0.8, 1), 1.4, 7.0, strands(P, "white", "white_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # long serpentine arms
        ab = m.bone(nm, bd, (sx * 4.0, 18.0, -6.0))
        pts3 = [(sx * 4.0, 18.0, -6.0), (sx * 12.0, 24.0, -10.0), (sx * 18.0, 32.0, -12.0)]
        for p0, p1 in zip(pts3, pts3[1:]):
            rod(m, ab, p0, p1, 2, HIDE, extend=0.4)
        for j in range(3):
            spike(m, ab, pts3[-1], (sx * 0.3 + (j - 1) * 0.5, 1, -0.4), 1.2, 4.0, solid(P, "claw"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # little hind legs
        lg = m.bone(nm, bd, (sx * 4.0, 6.0, 8.0))
        rod(m, lg, (sx * 4.0, 6.0, 8.0), (sx * 7.0, 1.0, 6.0), 2, HIDE, extend=0.4)
        for j in range(3):
            spike(m, lg, (sx * 7.0, 0.6, 6.0), ((j - 1) * 0.4, -0.2, -1), 1.0, 3.0, solid(P, "claw"), tip=0.8)
    tb = m.bone("tail", bd, (0, 8, 28))                                              # tasselled tail
    rod(m, tb, (0, 8.0, 28.0), (-4.0, 12.0, 34.0), 1, HIDE, extend=0.4, t2=2)
    for j in range(5):
        spike(m, tb, (-4.0, 12.0, 34.0), ((j - 2) * 0.3, 0.3, 1), 1.0, 5.0, strands(P, "white", "white_dark"),
              tip=0.8)
    return m
