"""Culumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the little holy beast. A small round white creature with big green eyes and an open happy smile, a
red triangle on its brow, two huge flared ears trimmed in violet zigzags spread like wings, tiny arms and feet tipped
violet. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, eye, gem, local, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.0)
KIND = "floater"
K = 4
LOOK = ("a small round white creature with big green eyes, a happy smile, a red triangle on its brow and two huge "
        "flared violet-trimmed ears spread like wings")
BASE = {"white": (250, 250, 252), "white_dark": (200, 204, 220), "violet": (130, 100, 210), "violet_dark": (70, 50, 150),
        "eye": (90, 200, 90), "pupil": (16, 40, 16), "mouth": (220, 80, 90), "red": (220, 40, 40), "red_light": (255, 160, 150)}
SHINY = {"white": (250, 236, 190), "white_dark": (220, 196, 130), "violet": (90, 170, 230), "eye": (230, 120, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", var=0.02)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.4, y - 15.2, 1.6, "eye")
            if c is not None:
                return c, None
        if 11.6 < y < 13.0 and abs(x) < 1.6 - (13.0 - y) * 0.6:
            return tone(p["mouth"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def ear(flip):
    """A flared ear (inside test + shader): wide at the tip with a violet zigzag edge; flip for the ear on -x."""
    def frac(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        a, b = u / max(W, 1e-6), v / max(H, 1e-6)
        return (1 - a if flip else a), b

    def inside(x, y, z, face, box):
        a, b = frac(x, y, z, face, box)
        return abs(b - 0.5) * 2 < 0.25 + 0.65 * a + 0.08 * abs(((a * 8) % 2) - 1)

    def shader(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = frac(x, y, z, face, box)
        if abs(b - 0.5) * 2 > 0.25 + 0.65 * a - 0.18 or a > 0.85:
            return tone(p["violet"], face), None
        return tone(p["white"], face), None
    return cutout(inside, shader)


def build():
    m = Model("culumon")
    top = m.bone("culumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 14.0, 0), 5.6, bodyf, layers=5)
    m.round_box(bd, 0, 0.2, 3.4, 3.0, 4.0, 9.6, SKIN, cut=1)                       # little body
    m.box(bd, -0.9, 18.4, -5.3, 0.9, 19.8, -4.9, gem(P, "red", "red_light"))       # brow triangle
    hd = m.bone("head", bd, (0, 18, 0))
    for sx in (-1, 1):                                                             # huge flared ears
        x0, x1 = sorted((sx * 4.0, sx * 16.0))
        m.box(hd, x0, 15.0, 0.0, x1, 25.0, 0.0, ear(sx < 0), rotation=(0, sx * 15, -sx * 25),
              pivot=(sx * 4.0, 18.0, 0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.4, 8.0, 0))
        spike(m, ab, (sx * 3.2, 8.0, -0.6), (sx, -0.6, -0.4), 1.4, 2.4, SKIN, tip=0.6)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 4.0, 0))
        m.box(lg, sx * 1.8 - 1.2, 0.0, -1.6, sx * 1.8 + 1.2, 4.6, 1.2, SKIN)
        m.box(lg, sx * 1.8 - 1.2, 0.0, -1.8, sx * 1.8 + 1.2, 1.0, -1.2, solid(P, "violet"))
    return m
