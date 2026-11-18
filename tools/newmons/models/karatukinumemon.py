"""Karatuki Numemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
a Numemon wearing a shell: a lime-green slug with a big grimacing mouth full of square teeth, two stalk eyes with red
pupils and a great pale-orange spiral snail shell striped with violet on its back. 15 blocks long.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import armour, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.6)
KIND = "quadruped"
K = 3
LOOK = "a lime-green slug with a big grimacing square-toothed mouth, stalk eyes with red pupils and a pale-orange spiral shell"
BASE = {"lime": (190, 220, 60), "lime_dark": (120, 150, 20), "lime_light": (230, 250, 150), "shell": (250, 220, 180),
        "shell_dark": (200, 150, 110), "stripe": (150, 110, 190), "white": (250, 250, 250), "eye": (220, 40, 40),
        "mouth": (40, 40, 30), "tooth": (250, 250, 246), "lip": (240, 160, 160)}
SHINY = {"lime": (240, 160, 200), "lime_dark": (180, 90, 140), "lime_light": (255, 220, 240)}


def P(v):
    return pal(BASE, SHINY, v)


SLUG = skin(P, "lime", dark="lime_dark", light="lime_light")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 6.0 < y < 14.0 and abs(x) < 5.0:
        if abs(y - 10.0) < 0.3 or (x + 6.0) % 1.8 < 0.3:
            return tone(p["mouth"], face), None
        if 7.0 < y < 13.0 and abs(x) < 4.4:
            return tone(p["tooth"], face), None
        return tone(p["lip"], face), None
    return SLUG(x, y, z, face, variant, box=box, **k)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    ang = math.atan2(y - 20.0, z - 6.0)
    r = math.hypot(y - 20.0, z - 6.0)
    if face in ("east", "west") and ((r - ang * 1.2) % 3.6) < 0.7:
        return tone(p["stripe"], face), None
    return armour(P, "shell", "shell_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("karatukinumemon")
    top = m.bone("karatukinumemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 2.0, 6.0, 12.0, 0.0, 6.0, SLUG, cut=2)                          # foot
    hd = m.bone("head", bd, (0, 10, -6))
    m.round_box(hd, 0, -6.0, 6.0, 4.0, 2.0, 18.0, facef, cut=3)                        # tall head-body
    for sx in (-1, 1):                                                               # stalk eyes
        rod(m, hd, (sx * 2.4, 17.0, -6.0), (sx * 4.0, 24.0, -7.0), 1, SLUG, extend=0.3, t2=1)
        m.round_box(hd, sx * 4.4, -7.4, 2.2, 2.2, 23.0, 27.4, solid(P, "white"), cut=1)
        m.round_box(hd, sx * 4.4, -9.4, 1.0, 0.4, 24.4, 26.0, solid(P, "eye"), cut=0)
    sh = m.bone("shell", bd, (0, 14, 6))                                              # spiral shell
    for j, (r, cz, cy) in enumerate(((9.0, 6.0, 18.0), (7.0, 8.0, 22.0), (5.0, 9.0, 25.6), (3.0, 9.4, 28.0))):
        m.round_box(sh, 0, cz, 5.0 - j * 0.6, r, cy - r, cy + r, shellf, cut=max(1, int(r * 0.4)))
    return m
