"""Sunflare, the Blaze Bloom Pokémon (Grass/Fire), Sunflora evolved, after the art the user shared (artist and name
not given; the name, sunflower + solar flare, is ours): a great sunflower whose petals have caught fire. Its round
face is a dark seed-head with closed, happy eyes and a little open mouth, ringed with yellow tiles studded with black
seeds; round it burn flame-shaped orange-red petals with yellow tips, yellow petals behind. Its green stem rises
behind the flower and hooks over the top into it, with leaves tipped orange like embers and two little green feet.

Shiny: blue flames round a pale ring, on a lime stem.

Front is -z, y is up. 33 units tall to the top of its stem; baseScale 0.72 (1.5 m).
"""
from __future__ import annotations

import math

from _afake import solid_of
from _boxmodel import Model, mix, rod, spike
from _route import along, pal, tone

SCALE = 0.72
HITBOX = [1.4, 2.05]
KIND = "biped"
K = 4
HEIGHT = 33
LOOK = ("a great sunflower with flame-shaped orange-red petals, a dark seed-head face with closed happy eyes, a "
        "yellow ring of seeds, a hooked green stem, ember-tipped leaves and little green feet")
C = (0.0, 20.0)                                                                  # centre of the flower's face
R = 8.6

BASE = {"brown": (62, 44, 34), "brown_line": (40, 28, 22), "yellow": (246, 214, 92), "yellow_dark": (214, 172, 60),
        "seed": (36, 30, 28), "flame": (232, 96, 40), "flame_tip": (250, 178, 60), "petal": (248, 220, 96),
        "green": (104, 182, 112), "green_dark": (70, 140, 86), "ember": (240, 150, 50), "mouth": (196, 110, 130)}
SHINY = {"flame": (60, 120, 230), "flame_tip": (150, 220, 255), "petal": (210, 236, 250), "yellow": (236, 236, 214),
         "yellow_dark": (200, 200, 176), "green": (150, 210, 70), "green_dark": (110, 170, 50), "ember": (100, 180, 250)}


def P(v):
    return pal(BASE, SHINY, v)


solid = solid_of(P)


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face != "north":
        return tone(p["yellow_dark"] if face != "south" else p["green_dark"], face), None
    dx, dy = x - C[0], y - C[1]
    r, a = math.hypot(dx, dy), math.atan2(dy, dx)
    if r < 4.4:
        for sx in (-1, 1):                                                    # closed, happy eyes
            ex, ey = dx - sx * 1.6, dy - 0.8
            if abs(math.hypot(ex, ey + 0.5) - 0.8) < 0.18 and ey > -0.2:
                return p["brown_line"], None
        if (dx / 0.8) ** 2 + ((dy + 1.4) / 0.5) ** 2 < 1:
            return p["mouth"], None                                           # a little open mouth
        return p["brown"], None
    seg = (a / (2 * math.pi) * 10) % 1.0
    if r < 4.8 or seg < 0.05:
        return p["yellow_dark"], None                                         # lines between the tiles
    sa = (math.floor(a / (2 * math.pi) * 10) + 0.5) * 2 * math.pi / 10
    if math.hypot(dx - 6.4 * math.cos(sa), dy - 6.4 * math.sin(sa)) < 0.55:
        return p["seed"], None                                                # a black seed on each tile
    return p["yellow"], None


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = along(z, box)
    c = mix(p["flame"], p["flame_tip"], max(0.0, (t - 0.35) / 0.65))
    return tone(c, face), (c if t > 0.55 else None)


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = along(z, box)
    return tone(p["ember"] if t > 0.72 else p["green"], face), None


def disc(m, bone, cx, cy, r, z0, z1, shader):
    """A round disc facing front (-z): four crossed boxes."""
    for w, h in ((1.0, 0.42), (0.93, 0.7), (0.7, 0.93), (0.42, 1.0)):
        m.box(bone, cx - r * w, cy - r * h, z0, cx + r * w, cy + r * h, z1, shader)


def build() -> Model:
    m = Model("sunflare")
    top = m.bone("sunflare", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 4))
    stem = [(0, 3.0, 4.0), (0, 10.0, 6.0), (0, 18.0, 7.0), (0, 26.0, 7.0), (0, 31.0, 5.0), (0, 32.0, 2.0),
            (0, 29.0, 0.4)]
    for a, b in zip(stem, stem[1:]):
        rod(m, bd, a, b, 3.0, solid("green"), extend=0.8)                       # the hooked stem

    hd = m.bone("head", bd, (0, 26, 0))
    disc(m, hd, C[0], C[1], R, -3.4, -0.4, facef)                               # the flower's face
    for i in range(12):                                                         # yellow petals behind
        a = 2 * math.pi * (i + 0.5) / 12
        spike(m, hd, (C[0] + (R - 0.6) * math.cos(a), C[1] + (R - 0.6) * math.sin(a), -0.6),
              (math.cos(a), math.sin(a), 0.1), 2.4, 3.4, solid("petal"), tip=1.0)
    for i in range(12):                                                         # burning petals in front
        a = 2 * math.pi * i / 12
        spike(m, hd, (C[0] + (R - 1.0) * math.cos(a), C[1] + (R - 1.0) * math.sin(a), -2.4),
              (math.cos(a), math.sin(a), -0.15), 3.0, 4.6, flamef, tip=1.4)

    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.0, 3.0, 4.0))
        rod(m, lb, (sx * 1.0, 3.4, 4.0), (sx * 2.6, 1.0, 2.6), 1.8, solid("green"), extend=0.4)
        m.round_box(lb, sx * 2.6, 2.0, 1.4, 1.8, 0.0, 1.4, solid("green_dark"), cut=0.6)   # little feet
        ar = m.bone(f"arm_{side}", bd, (sx * 1.0, 12, 6))                       # ember-tipped leaves
        rod(m, ar, (sx * 1.0, 12.0, 6.0), (sx * 7.6, 15.0, 5.0), 3.2, leaff, extend=0.3, t2=0.8)
        rod(m, ar, (sx * 1.0, 19.0, 7.0), (sx * 6.6, 23.0, 8.0), 2.8, leaff, extend=0.3, t2=0.8)
    rod(m, bd, (0.6, 27.0, 7.0), (5.0, 30.0, 8.0), 2.4, leaff, extend=0.3, t2=0.8)
    return m
