"""Coronamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the little sun lion. A red-orange lion cub with a mane of licking flames, a steel ring set in its
brow, blue eyes, a yellow fluffy chest tuft, black-and-gold gauntlets with yellow claws, and a tail ending in a
glowing ball of sunfire. Child stage.

Front is -z, y is up. 30 units tall.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import cutout, eye, flame_inside, fur, gem, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = ("a red-orange lion cub with a mane of flames, a steel ring in its brow, blue eyes, a yellow chest tuft, "
        "black-and-gold gauntlets and a sunfire tail tip")
BASE = {"red": (230, 70, 40), "red_dark": (160, 30, 14), "red_light": (255, 140, 100), "yellow": (250, 210, 60),
        "yellow_dark": (220, 160, 20), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "black": (30, 28, 32),
        "gold": (240, 200, 70), "eye": (60, 160, 230), "pupil": (16, 30, 60), "white": (255, 255, 255),
        "flame": (255, 150, 40, 220), "flame_core": (255, 240, 160, 240), "sun": (255, 240, 180), "sun2": (255, 200, 80)}
SHINY = {"red": (240, 230, 120), "red_dark": (200, 170, 40), "red_light": (255, 250, 190), "flame": (120, 200, 255, 220),
         "flame_core": (230, 250, 255, 240)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "red", "red_dark", tip="red_light", length=0.9)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 2.0, y - 19.4, 1.1, "eye")
            if c is not None:
                return c, None
    return FUR(x, y, z, face, variant, box=box, **k)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def build():
    m = Model("coronamon")
    top = m.bone("coronamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0.6, 3.6, 3.0, 7.0, 14.6, FUR, cut=1)
    for j in range(4):                                                         # yellow chest tuft
        spike(m, bd, ((j - 1.5) * 1.0, 13.6, -2.6), ((j - 1.5) * 0.3, -1, -0.4), 1.4, 3.0,
              fur(P, "yellow", "yellow_dark", length=0.8), tip=0.4)
    hd = m.bone("head", bd, (0, 15, 0))
    ball(m, hd, (0, 19.0, 0), 4.6, headf, layers=5)
    m.box(hd, -1.6, 16.4, -5.2, 1.6, 18.6, -3.8, FUR)                          # muzzle
    for i in range(8):                                                         # steel brow ring
        ang = i * math.pi / 4
        p0 = (1.2 * math.cos(ang), 22.0 + 1.2 * math.sin(ang), -4.4)
        p1 = (1.2 * math.cos(ang + math.pi / 4), 22.0 + 1.2 * math.sin(ang + math.pi / 4), -4.4)
        rod(m, hd, p0, p1, 1, metal(P, "steel", dark="steel_dark"), extend=0.3)
    mane = m.bone("mane", hd, (0, 21, 1))
    for j, (ang, h) in enumerate(((-50, 6.0), (-20, 8.0), (10, 9.0), (40, 7.0), (70, 6.0))):  # mane of flames
        m.box(mane, -2.6, 21.0, 1.0, 2.6, 21.0 + h, 1.0, cutout(flame_inside(3, 0.0, j), flamef),
              rotation=(-20, 0, ang), pivot=(0, 21.0, 1.0))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 3.6, 13.0, 0))
        rod(m, ab, (sx * 3.6, 13.0, 0), (sx * 5.4, 9.0, -1.4), 2, FUR, extend=0.4)
        m.round_box(ab, sx * 5.8, -1.8, 2.2, 2.2, 6.6, 10.0, solid(P, "black"), cut=1)       # gauntlets
        m.round_box(ab, sx * 5.8, -1.8, 2.4, 2.4, 9.2, 10.2, metal(P, "gold", dark="yellow_dark"), cut=1)
        for j in range(3):
            spike(m, ab, (sx * 5.8 + (j - 1) * 1.0, 6.6, -3.6), (0, -0.6, -1), 0.8, 1.4, solid(P, "yellow"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 8.0, 0))
        m.round_box(lg, sx * 2.4, 0.4, 2.0, 2.2, 1.0, 8.4, FUR, cut=1)
        m.box(lg, sx * 2.4 - 2.0, 0.0, -3.0, sx * 2.4 + 2.0, 2.0, 1.4, solid(P, "black"))
    tl = m.bone("tail", bd, (0, 9, 3))
    pts = [(0, 9.0, 3.0), (2.0, 6.0, 7.0), (3.0, 4.0, 10.0)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, FUR, extend=0.3)
    m.round_box(tl, 3.0, 11.0, 1.8, 1.8, 2.2, 5.8, gem(P, "sun", "sun2"), cut=1)       # the sunfire ball
    return m
