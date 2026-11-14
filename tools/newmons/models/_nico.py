"""Shared colours and parts for the Nicodex (the user's 18 nicotine- and tobacco-inspired Pokémon of the Ashtray
Wastes): cigarette paper and filters, embers, ash and tar, tobacco leaf, brass and glass, steel and menthol. Each model
keeps its own SHINY dict and calls `palette(shiny)`.
"""
from __future__ import annotations

import math

from _afake import round_eye, solid_of, ramp_of
from _route import pal

BASE = {"paper": (240, 240, 234), "paper_shade": (214, 212, 204), "filter": (214, 140, 70), "filter_dark": (176, 100, 44),
        "ember": (255, 120, 40), "ember_hot": (255, 210, 90), "ash": (132, 127, 122), "ash_dark": (90, 86, 82),
        "tar": (30, 22, 18), "tar_shine": (86, 64, 48), "amber": (240, 160, 40), "tobacco": (130, 88, 48),
        "tobacco_dark": (92, 60, 32), "tobacco_light": (176, 128, 74), "leaf": (126, 176, 70), "leaf_dark": (80, 130, 50),
        "leaf_light": (184, 214, 112), "gold": (232, 192, 82), "gold_dark": (182, 140, 52), "brass": (204, 164, 72),
        "glass": (186, 226, 236, 110), "water": (90, 150, 206, 150), "mist": (230, 226, 240, 120),
        "smoke": (180, 176, 184, 120), "steel": (182, 188, 198), "steel_dark": (110, 116, 128), "gunmetal": (70, 76, 88),
        "mint": (164, 238, 212), "mint_dark": (90, 190, 170), "ice": (206, 242, 255, 170), "navy": (40, 48, 82),
        "navy_light": (66, 78, 120), "cyan": (110, 230, 250), "white": (248, 248, 246), "pupil": (24, 22, 26),
        "red": (214, 54, 44), "pink": (240, 170, 186), "skin": (232, 198, 164), "skin_dark": (200, 160, 124),
        "purple": (150, 100, 204), "purple_light": (196, 160, 236), "teal": (60, 150, 150), "teal_dark": (36, 104, 108),
        "olive": (122, 132, 70), "olive_dark": (84, 92, 46), "tan": (214, 190, 140), "ivory": (238, 230, 210),
        "ivory_shade": (210, 198, 170), "brown": (120, 84, 56), "black": (30, 30, 34), "suit": (40, 40, 48),
        "pinstripe": (110, 110, 124), "violet": (130, 90, 220, 150), "teal_mist": (90, 210, 200, 140)}


def palette(shiny):
    """-> (P, solid, ramp) for a model with its own shiny overrides."""
    def P(v):
        return pal(BASE, shiny, v)
    return P, solid_of(P), ramp_of(P)


def translucent(P, key):
    """A shader painting a translucent palette colour (its alpha), for glass, water, smoke and mist."""
    def s(x, y, z, face, variant, **k):
        return P(variant)[key], None
    return s


def eye_on(P, iris, centres, r, face="north", ry=None, pupil_frac=0.36):
    """-> fn(x, y, z, face, variant) painting round eyes at centres [(u, v)] on a face (u = x, or z on side faces)."""
    def f(x, y, z, fc, variant):
        if fc != face:
            return None
        u = x if face in ("north", "south") else z
        for cu, cv in centres:
            e = round_eye(u - cu, y - cv, r, P(variant), iris, ry=ry, pupil_frac=pupil_frac)
            if e:
                return e
        return None
    return f


def disc_z(m, bone, cx, cy, r, z0, z1, shader):
    """A round disc facing front (-z): crossed boxes."""
    for w, h in ((1.0, 0.42), (0.93, 0.7), (0.7, 0.93), (0.42, 1.0)):
        m.box(bone, cx - r * w, cy - r * h, z0, cx + r * w, cy + r * h, z1, shader)


def tube_z(m, bone, cx, cy, r, z0, z1, shader):
    """A cylinder lying along z (cigarettes, pods): crossed boxes."""
    for w, h in ((1.0, 0.55), (0.55, 1.0), (0.85, 0.85)):
        m.box(bone, cx - r * w, cy - r * h, z0, cx + r * w, cy + r * h, z1, shader)


def puff(m, bone, c, r, shader):
    """A round puff (smoke, mist, a pearl): a rounded box."""
    m.round_box(bone, c[0], c[2], r, r, c[1] - r, c[1] + r, shader, cut=max(0.5, r * 0.45))


def ring_pts(c, r, n, plane="xz", start=0.0):
    pts = []
    for i in range(n + 1):
        a = start + 2 * math.pi * i / n
        if plane == "xz":
            pts.append((c[0] + r * math.sin(a), c[1], c[2] + r * math.cos(a)))
        else:
            pts.append((c[0] + r * math.sin(a), c[1] + r * math.cos(a), c[2]))
    return pts
