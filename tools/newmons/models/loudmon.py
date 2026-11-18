"""Loudmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the rock-concert dragon: a hulking grey mecha frame packed with big black speakers on its shoulders
and chest, twin exhaust pipes on its back, a little violet dragon head with a green mohawk peeking out, violet legs,
big white claws, and a guitar cable with a jack plug swinging from its arm. 25 blocks tall.

Front is -z, y is up. 48 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, metal, scales, solid, strands
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking grey mecha frame packed with big speakers and exhaust pipes, a little violet dragon head with a green mohawk and big white claws"
BASE = {"grey": (150, 154, 166), "grey_dark": (70, 74, 86), "grey_light": (210, 214, 224), "black": (30, 30, 34),
        "violet": (110, 80, 170), "violet_dark": (50, 30, 100), "green": (80, 220, 90), "green_dark": (30, 130, 40),
        "white": (240, 240, 244), "gold": (230, 190, 60), "red": (210, 40, 40), "eye": (240, 40, 40)}
SHINY = {"grey": (210, 180, 90), "grey_dark": (130, 100, 30), "grey_light": (250, 230, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "grey", "grey_dark", light="grey_light", trim="black", trim_w=0.25, rivets=True)


def speakerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and box is not None:
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        r = math.hypot(x - cx, y - cy)
        R = min(box.size[0], box.size[1]) / 2
        if r < R * 0.2:
            return tone(p["gold"], face), None
        if r < R * 0.85:
            return tone(p["black"] if (r * 3.0) % 1.0 < 0.8 else p["grey_dark"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("loudmon")
    top = m.bone("loudmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 16, 0))
    m.round_box(bd, 0, 1.0, 8.0, 6.0, 16.0, 36.0, ARM, cut=2)
    for sx in (-1, 1):                                                               # speakers
        m.box(bd, sx * 7.0 - 4.0, 30.0, -5.6, sx * 7.0 + 4.0, 38.0, 2.0, speakerf)
        m.box(bd, sx * 3.0 - 3.0, 20.0, -5.4, sx * 3.0 + 3.0, 26.0, -1.0, speakerf)
        rod(m, bd, (sx * 3.0, 34.0, 5.0), (sx * 3.0, 46.0, 6.0), 2, metal(P, "grey_light", dark="grey_dark"), extend=0)  # exhausts
    hd = m.bone("head", bd, (2, 30, -6))                                              # little dragon head
    m.round_box(hd, 2.0, -7.0, 2.4, 3.0, 27.0, 32.0, scales(P, "violet", "violet_dark"), cut=1)
    m.box(hd, 0.6, 30.0, -10.1, 1.4, 30.8, -9.9, solid(P, "eye", glow=True))
    m.box(hd, 2.6, 30.0, -10.1, 3.4, 30.8, -9.9, solid(P, "eye", glow=True))
    for j in range(5):
        spike(m, hd, (2.0, 31.6, -8.0 + j * 1.0), (0.3, 1, 0.4), 1.0, 3.6, strands(P, "green", "green_dark"), tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                              # clawed arms
        ab = m.bone(nm, bd, (sx * 10.0, 32.0, 0))
        rod(m, ab, (sx * 10.0, 32.0, 0), (sx * 13.0, 22.0, -3.0), 3, ARM, extend=0.6)
        for j in range(3):
            spike(m, ab, (sx * 13.0 + (j - 1) * 1.4, 19.0, -3.6), (0, -1, -0.6), 1.4, 5.0, solid(P, "white"), tip=0.8)
    pts = [(-13.0, 22.0, -3.0), (-15.0, 14.0, -6.0), (-12.0, 8.0, -8.0)]               # guitar cable + jack
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, "arm_right", p0, p1, 1, solid(P, "black"), extend=0.2, t2=1)
    rod(m, "arm_right", pts[-1], (-12.0, 4.0, -8.0), 1, metal(P, "gold", dark="grey_dark"), extend=0, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.6, 16.0, 0))
        rod(m, lg, (sx * 4.6, 17.0, 0), (sx * 5.0, 6.0, -1.0), 4, scales(P, "violet", "violet_dark"), extend=0.8)
        m.round_box(lg, sx * 5.0, -2.0, 3.4, 4.6, 0.0, 6.0, ARM, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 5.0 + (j - 1) * 2.0, 1.0, -6.4), (0, -0.3, -1), 1.4, 4.0, solid(P, "white"), tip=0.8)
    return m
