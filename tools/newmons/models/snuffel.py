"""Snuffel, the Snuff Pokémon (Normal), the Nicodex's Normal type (the user's design): a small, round, sneezy mole in a
little velvet waistcoat, with a big pink nose dusted with fine brown snuff powder, tiny squinting eyes, broad digging
paws and a snuff box tucked under its arm.

Shiny: a ginger mole with a green waistcoat.

Front is -z, y is up. 12 units tall; baseScale 0.42 (0.35 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _nico import palette
from _route import tone

SHINY = {"brown": (200, 120, 60), "purple": (60, 130, 80), "purple_light": (100, 170, 110)}
P, solid, ramp = palette(SHINY)
SCALE = 0.42
HITBOX = [0.7, 0.7]
KIND = "biped"
K = 6
HEIGHT = 12
LOOK = "a small round sneezy mole in a velvet waistcoat with a big snuff-dusted pink nose and a snuff box"


def furf(x, y, z, face, variant, **k):
    p = P(variant)
    if 2.6 < y < 6.8 and face in ("north", "east", "west") and not (face == "north" and abs(x) < 1.0):
        return tone(p["purple"], face), None                                  # the velvet waistcoat
    if face == "north" and abs(x) < 1.0 and 2.6 < y < 6.8 and int(y * 2) % 3 == 0:
        return p["gold"], None                                                # buttons
    return tone(p["brown"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.5) < 0.6 and abs(y - 9.8) < 0.2:
                return p["pupil"], None                                       # tiny squinting eyes
    return tone(p["brown"], face), None


def nosef(x, y, z, face, variant, **k):
    p = P(variant)
    if (int(x * 5) * 7 + int(y * 5) * 3) % 5 == 0:
        return p["tobacco"], None                                             # snuff dust
    return p["pink"], None


def build() -> Model:
    m = Model("snuffel")
    top = m.bone("snuffel", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    m.round_box(bd, 0, 0, 3.6, 3.2, 1.0, 7.4, furf, cut=1.2)
    hd = m.bone("head", bd, (0, 7, 0))
    m.round_box(hd, 0, -0.4, 3.0, 2.8, 7.0, 11.6, headf, cut=1.0)
    m.round_box(hd, 0, -3.6, 1.2, 1.0, 7.8, 9.8, nosef, cut=0.4)                # the big snuffy nose
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 3.4, 5, 0))
        rod(m, ar, (sx * 3.4, 5.6, 0.0), (sx * 4.4, 3.6, -1.6), 1.4, solid("brown"), extend=0.3)
        m.box(ar, sx * 4.4 - 1.2, 2.8, -2.8, sx * 4.4 + 1.2, 4.2, -1.0, solid("pink"))    # broad digging paws
        lb = m.bone(f"leg_{side}", top, (sx * 1.8, 1, 0))
        m.box(lb, sx * 1.8 - 1.0, 0.0, -1.8, sx * 1.8 + 1.0, 1.4, 0.8, solid("pink"))
    m.box("arm_right", 3.8, 3.0, 0.4, 6.0, 4.4, 2.6, solid("gold"))             # the snuff box
    return m
