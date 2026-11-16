"""Archelomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an ancient sea turtle. A domed green shell ridged with tall green spikes, a yellow body, a beaked
head with a pink crest and a pink hooked beak, two long yellow horns sweeping back, and four flippers edged with
steel blades. 15 blocks tall.

Front is -z, y is up. 32 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, slab_z
from _digidetail import armour, cutout, eye, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("an ancient sea turtle: a domed green shell ridged with tall spikes, a yellow body, a beaked head with a pink "
        "crest, two long yellow horns and flippers edged with steel blades")
BASE = {"shell": (60, 150, 60), "shell_dark": (24, 80, 24), "shell_light": (140, 210, 120), "yellow": (240, 220, 90),
        "yellow_dark": (180, 150, 40), "pink": (230, 60, 140), "pink_dark": (160, 30, 90), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 126), "eye": (250, 200, 40), "pupil": (20, 16, 10), "white": (250, 250, 250)}
SHINY = {"shell": (60, 110, 190), "shell_dark": (24, 50, 120), "shell_light": (140, 180, 240), "yellow": (240, 180, 200),
         "yellow_dark": (190, 120, 150)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "shell", "shell_dark", light="shell_light", panel=(3.0, 2.6))
SPIKE = armour(P, "shell", "shell_dark", light="shell_light")
BODY = skin(P, "yellow", dark="yellow_dark")
BLADE = metal(P, "steel", dark="steel_dark")
HORN = metal(P, "yellow", dark="yellow_dark")


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 19.0, y - 15.6, 1.0, "eye")
        if c is not None:
            return c, None
    return BODY(x, y, z, face, variant, box=box, **k)


def flipper(m, bone, root, sx, back=False):
    ln = 11.0 if not back else 7.0
    x0, x1 = sorted((root[0], root[0] + sx * ln))
    m.box(bone, x0, root[1] - 0.8, root[2] - 3.0, x1, root[1] + 0.8, root[2] + 1.0, BODY,
          rotation=(0, sx * (-25 if not back else 30), sx * -10), pivot=root)
    m.box(bone, x0, root[1] - 0.3, root[2] - 4.6, x1, root[1] + 0.3, root[2] - 3.0, BLADE,
          rotation=(0, sx * (-25 if not back else 30), sx * -10), pivot=root)


def build():
    m = Model("archelomon")
    top = m.bone("archelomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for i in range(6):                                           # yellow body under the shell
        slab_z(m, bd, 0, 9.0, -10 + i * 3.4, -6.4 + i * 3.4, 7.4 - abs(i - 2.5) * 0.5, 3.0, BODY)
    for i in range(6):                                           # the domed shell
        z0 = -11 + i * 3.8
        r = 9.0 - abs(i - 2.5) * 0.8
        slab_z(m, bd, 0, 13.0, z0, z0 + 4.0, r, 4.4 - abs(i - 2.5) * 0.4, SHELL)
    for i, z in enumerate((-7.0, -2.0, 3.0, 8.0)):              # tall green spikes along the ridge
        spike(m, bd, (0, 16.6, z), (0, 1, 0.5), 2.4, 8.0 - abs(i - 1.5), SPIKE, tip=1.2)
        for sx in (-1, 1):
            spike(m, bd, (sx * 4.0, 15.4, z), (sx * 0.4, 1, 0.5), 1.8, 4.6, SPIKE, tip=0.8)
    hd = m.bone("head", bd, (0, 13, -11))
    ball(m, hd, (0, 14.0, -16.0), 3.4, headf, layers=4)
    m.box(hd, -1.6, 11.4, -21.4, 1.6, 14.4, -18.0, metal(P, "pink", dark="pink_dark"))   # pink hooked beak
    spike(m, hd, (0, 12.6, -21.4), (0, -1, -0.3), 2.0, 2.0, metal(P, "pink", dark="pink_dark"))
    for j in range(5):                                           # pink crest
        spike(m, hd, (0, 17.0, -17.0 + j * 0.8), (0, 1, 0.3 + j * 0.2), 1.0, 3.0 - j * 0.3, solid(P, "pink"))
    for sx in (-1, 1):                                           # long yellow horns sweeping back
        rod(m, hd, (sx * 2.4, 16.0, -14.0), (sx * 8.0, 20.0, -4.0), 2, HORN, extend=0.3)
        spike(m, hd, (sx * 8.0, 20.0, -4.0), (sx * 0.4, 0.4, 1), 1.4, 6.0, HORN)
    for front, zz in ((True, -7.0), (False, 7.0)):
        for sx in (1, -1):
            nm = f"leg_{'front' if front else 'back'}_{'left' if sx > 0 else 'right'}"
            lg = m.bone(nm, top, (sx * 6.0, 9.0, zz))
            flipper(m, lg, (sx * 6.0, 9.0, zz), sx, back=not front)
    return m
