"""Giga Waru Monzaemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the mad chef bear: a towering black stitched teddy bear with a snarling stitched muzzle
and red eyes, a tall chef's hat banded purple, a white double-breasted chef's jacket and apron over purple trousers,
a red neckerchief, a giant pizza cutter in one paw and long steel claws on the other. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage (no level on wikimon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, fur, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering black stitched teddy bear with a snarling muzzle, a tall chef's hat, a white chef's jacket and apron, "
        "a giant pizza cutter and long steel claws")
BASE = {"black": (44, 42, 48), "black_dark": (18, 16, 20), "muzzle": (220, 170, 110), "white": (246, 246, 246),
        "white_dark": (190, 190, 200), "purple": (100, 60, 140), "purple_dark": (50, 24, 80), "red": (200, 30, 40),
        "eye": (230, 40, 40), "stitch": (200, 190, 170), "steel": (220, 224, 234), "steel_dark": (110, 114, 126),
        "mouth": (110, 20, 30), "tooth": (250, 250, 240)}
SHINY = {"black": (230, 180, 120), "black_dark": (170, 120, 70)}


def P(v):
    return pal(BASE, SHINY, v)


FUR0 = fur(P, "black", "black_dark", length=0.8, density=2.0)
COAT = fabric(P, "white", "white_dark", axis="y")
PANTS = fabric(P, "purple", "purple_dark", axis="y")
STEEL = metal(P, "steel", dark="steel_dark")


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(x) < 0.3:
        return tone(p["stitch"], face), None
    return FUR0(x, y, z, face, variant, box=box, **k)


def coatf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and any(abs(x - sx * 3.0) < 0.5 and (y * 0.5) % 2.0 < 0.6 for sx in (-1, 1)):
        return tone(p["purple"], face), None
    return COAT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("gigawarumonzaemon")
    top = m.bone("gigawarumonzaemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, 0, 12.0, 9.0, 16.0, 26.0, PANTS, cut=3)                           # purple trousers
    m.round_box(bd, 0, 0, 12.6, 9.6, 24.0, 42.0, coatf, cut=3)                           # chef's jacket
    m.round_box(bd, 0, -9.0, 8.0, 1.0, 18.0, 36.0, COAT, cut=1)                          # apron
    m.round_box(bd, 0, -2.0, 6.0, 5.0, 40.0, 43.0, solid(P, "red"), cut=1)               # neckerchief
    hd = m.bone("head", bd, (0, 44, 0))
    m.round_box(hd, 0, 0, 7.0, 6.4, 42.0, 54.0, furf, cut=3)
    m.round_box(hd, 0, -6.6, 3.4, 2.0, 44.0, 49.0, solid(P, "muzzle"), cut=1)            # snarling muzzle
    m.box(hd, -2.4, 44.4, -8.8, 2.4, 46.4, -8.5, solid(P, "mouth"))
    for j in range(5):
        spike(m, hd, (-2.0 + j, 46.4, -8.7), (0, -1, 0), 0.6, 1.2, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.0, sx * 4.0), 50.0, -6.7, max(sx * 2.0, sx * 4.0), 51.2, -6.4, solid(P, "eye", glow=True))
        m.round_box(hd, sx * 6.0, 0, 2.0, 1.4, 52.0, 56.0, furf, cut=1)                  # round ears
    m.round_box(hd, 0, 0.4, 5.6, 5.0, 53.6, 56.0, solid(P, "purple"), cut=2)             # chef's hat band
    m.round_box(hd, 0, 0.4, 6.0, 5.4, 56.0, 64.0, COAT, cut=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 12.0, 38.0, 0))
        rod(m, ab, (sx * 12.0, 38.0, 0), (sx * 17.0, 26.0, -4.0), 5, COAT, extend=0.6)
        m.round_box(ab, sx * 18.0, -6.0, 3.4, 3.4, 18.0, 25.0, furf, cut=1)
    for j in range(4):                                                                      # long steel claws
        spike(m, "arm_left", (16.0 + j * 1.4, 18.0, -7.0), (0.2, -1, -0.5), 1.0, 14.0, STEEL, tip=0.8)
    ar = "arm_right"                                                                         # giant pizza cutter
    rod(m, ar, (-18.0, 22.0, -6.0), (-22.0, 32.0, -10.0), 2, STEEL, extend=0)
    m.round_box(ar, -23.0, -12.0, 6.0, 0.6, 30.0, 42.0, STEEL, cut=0)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 6.0, 18.0, 0))
        rod(m, lg, (sx * 6.0, 18.0, 0), (sx * 7.0, 4.0, 0), 6, PANTS, extend=0.6)
        m.round_box(lg, sx * 7.0, -2.0, 4.0, 5.0, 0.0, 4.0, furf, cut=1)
        for j in range(3):
            spike(m, lg, (sx * 7.0 + (j - 1) * 2.0, 0.8, -6.6), (0, -0.2, -1), 1.2, 4.0, STEEL, tip=0.8)
    return m
