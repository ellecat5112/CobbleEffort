"""Coelamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the armoured ancient fish. A great coelacanth whose head and front are cased in a white bone-armour
shell with a big round blue eye and a toothy open jaw, a pink scaly body, lobed fins tipped in violet claws, and a
ragged white tail fin. 15 blocks long.

Front is -z, y is up. 30 units tall; Adult stage (swims).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import slab_z
from _digidetail import armour, cutout, eye, local, noise2, scales, solid
from _route import pal, tone

HEIGHT = 30
SCALE, HITBOX = sized(15 * 30 / 56, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a great coelacanth cased in white bone armour with a big blue eye and a toothy jaw, a pink scaly body, "
        "violet-clawed lobed fins and a ragged tail fin")
BASE = {"bone": (240, 240, 246), "bone_dark": (170, 174, 190), "pink": (230, 170, 170), "pink_dark": (170, 100, 110),
        "violet": (120, 80, 170), "eye": (60, 140, 240), "pupil": (16, 20, 40), "white": (255, 255, 255),
        "mouth": (200, 40, 60), "tooth": (250, 250, 246), "fin": (200, 220, 240)}
SHINY = {"pink": (130, 190, 230), "pink_dark": (70, 120, 180), "bone": (70, 70, 80), "bone_dark": (30, 30, 36)}


def P(v):
    return pal(BASE, SHINY, v)


BONE = armour(P, "bone", "bone_dark", rivets=True)
BODY = scales(P, "pink", "pink_dark", size=1.4)
CY = 14.0


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 14.0, y - CY - 3.0, 2.2, "eye")
        if c is not None:
            return c, None
    return BONE(x, y, z, face, variant, box=box, **k)


def ragged(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return u / max(W, 1e-6) < 0.75 + 0.25 * noise2(v * 1.3, 4.0)


def build():
    m = Model("coelamon")
    top = m.bone("coelamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    for i in range(9):                                                      # the body, tapering back
        z0 = -10.0 + i * 3.4
        r = 7.0 * (1 - i / 11)
        slab_z(m, bd, 0, CY, z0 - 0.2, z0 + 3.6, r * 0.8, r, BODY)
    hd = m.bone("head", bd, (0, CY, -10))                                   # bone-armour head shell
    slab_z(m, hd, 0, CY + 1.0, -22.0, -9.0, 6.4, 7.6, headf)
    jw = m.bone("jaw", hd, (0, CY - 3, -12))
    m.box(jw, -4.6, CY - 7.0, -21.0, 4.6, CY - 3.0, -12.0, BONE, rotation=(18, 0, 0), pivot=(0, CY - 3.0, -12.0))
    m.box(hd, -4.4, CY - 3.4, -21.6, 4.4, CY - 2.8, -12.4, solid(P, "mouth"))
    for i in range(5):
        for sx in (-1, 1):
            spike(m, hd, (sx * 4.0, CY - 3.0, -21.0 + i * 1.8), (0, -1, 0), 1.0, 1.8, solid(P, "tooth"))
    for i in range(4):                                                      # spines down its back
        spike(m, bd, (0, CY + 6.0 - i, -6.0 + i * 5.0), (0, 1, 0.4), 1.6, 3.0, BONE)
    for sx in (-1, 1):                                                      # lobed fins with violet claws
        for zz in (-4.0, 8.0):
            fb = (sx * 5.0, CY - 4.0, zz)
            rod(m, bd, fb, (sx * 10.0, CY - 8.0, zz + 2.0), 3, BODY, extend=0.6)
            for j in range(3):
                spike(m, bd, (sx * 10.0, CY - 8.0, zz + 1.0 + j * 1.0), (sx * 0.6, -1, 0), 0.8, 2.4, solid(P, "violet"))
    tl = m.bone("tail", bd, (0, CY, 20))                                    # ragged tail fin
    m.box(tl, -0.2, CY - 8.0, 20.0, 0.2, CY + 8.0, 30.0, cutout(ragged, solid(P, "fin")))
    return m
