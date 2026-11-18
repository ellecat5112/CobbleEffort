"""Karakurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the clockwork puppet: a kimono doll in a violet hakama skirt and pink kimono with long black
hair and a pale shadowed face under a wide black-and-red straw hat, holding a green teacup, with four thin silver
mechanical arms spreading from its back, each ending in a cyan energy blade, on a dark rolling base. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import cutout, fabric, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a kimono puppet doll in a violet hakama under a wide black straw hat, holding a teacup, with four thin silver "
        "mechanical arms ending in cyan energy blades")
BASE = {"violet": (120, 70, 170), "violet_dark": (60, 24, 100), "pink": (220, 120, 170), "pink_dark": (150, 50, 110),
        "black": (30, 28, 34), "black_dark": (10, 10, 12), "red": (200, 40, 40), "face": (236, 230, 226),
        "face_dark": (170, 160, 160), "green": (60, 140, 70), "silver": (200, 204, 216), "silver_dark": (90, 94, 106),
        "blade": (120, 210, 255, 190), "blade_light": (230, 250, 255, 220), "gold": (220, 180, 60)}
SHINY = {"violet": (60, 140, 110), "violet_dark": (20, 70, 50), "pink": (240, 200, 90), "pink_dark": (170, 130, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def blade_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return abs(a - 0.5) < 0.5 * (1 - b) ** 0.6 + 0.04


def bladef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["blade_light"] if abs(u - W / 2) < 0.4 else p["blade"]
    return c, c[:3]


def build():
    m = Model("karakurumon")
    top = m.bone("karakurumon", None, (0, 0, 0))
    m.round_box(top, 0, 0, 6.0, 5.0, 0.0, 3.0, metal(P, "black", dark="black_dark"), cut=2)   # rolling base
    bd = m.bone("body", top, (0, 3, 0))
    HAK = fabric(P, "violet", "violet_dark", period=1.6)
    for j in range(5):                                                               # violet hakama
        r = 8.0 - j * 1.0
        m.round_box(bd, 0, 0.6, r, r * 0.8, 3.0 + j * 6.0, 9.4 + j * 6.0, HAK, cut=max(1, int(r * 0.3)))
    KIM = fabric(P, "pink", "pink_dark")
    m.round_box(bd, 0, 0.4, 4.2, 3.4, 33.0, 46.0, KIM, cut=1)                         # kimono top
    for sx in (-1, 1):
        m.round_box(bd, sx * 4.4, -1.8, 2.2, 3.0, 36.0, 45.0, KIM, cut=1)            # sleeves
    m.round_box(bd, 0, -4.4, 1.4, 1.4, 38.0, 40.6, solid(P, "green"), cut=0)          # teacup
    hd = m.bone("head", bd, (0, 47, 0))
    m.round_box(hd, 0, 0, 2.4, 2.4, 46.0, 52.0, skin(P, "face", dark="face_dark"), cut=1)
    for i in range(9):                                                               # long black hair
        ang = math.radians(-100 + i * 25)
        rod(m, hd, (2.2 * math.sin(ang), 51.6, 0.6 + 1.4 * math.cos(ang)), (3.0 * math.sin(ang), 36.0, 2.6), 1,
            strands(P, "black", "black_dark"), extend=0.3, t2=2)
    m.round_box(hd, 0, 0, 8.0, 8.0, 51.6, 52.6, solid(P, "black"), cut=3)                # wide straw hat
    m.round_box(hd, 0, 0, 3.6, 3.6, 52.6, 55.0, solid(P, "black"), cut=1)
    m.round_box(hd, 0, 0, 3.8, 3.8, 53.0, 53.8, solid(P, "red"), cut=1)
    S = metal(P, "silver", dark="silver_dark")
    for k_, (sx, up) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):            # four mechanical arms
        nm = ("arm_left", "arm_right", "arm2_left", "arm2_right")[k_]
        ab = m.bone(nm, bd, (sx * 3.0, 42.0, 3.0))
        pts = [(sx * 3.0, 42.0, 3.0), (sx * 10.0, 42.0 + up * 6.0, 4.0), (sx * 18.0, 40.0 + up * 4.0, 2.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 1, S, extend=0, t2=1)
            m.round_box(ab, p1[0], p1[2], 0.9, 0.9, p1[1] - 0.9, p1[1] + 0.9, metal(P, "gold", dark="silver_dark"), cut=0)
        e = pts[-1]
        m.box(ab, e[0] - 1.8, e[1], e[2], e[0] + 1.8, e[1] + 16.0, e[2], cutout(blade_in, bladef),
              rotation=(0, 0, -sx * 15 if up > 0 else sx * 165), pivot=e)
    return m
