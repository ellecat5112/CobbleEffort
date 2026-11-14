"""Spiritskull, the Haunted Bottle Pokémon (Ghost/Poison), a Liquor Meadows Pokémon (the user's design): a floating,
translucent crystal skull filled with glowing haunted liquor, violet above and amber below, dark eye sockets leaking
wisps of vapour, a cracked crystal brow and a loose jaw that rattles when it laughs.

Shiny: a smoky-black crystal with green liquor.

Front is -z, y is up. 14 units tall; baseScale 0.5 (0.45 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model
from _liquor import palette, puff, translucent

SHINY = {"crystal": (90, 90, 100, 150), "violet_glass": (80, 220, 120, 170), "amber_glass": (170, 240, 90, 170),
         "violet": (100, 255, 140)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [0.8, 0.85]
KIND = "floater"
K = 5
HEIGHT = 14
LOOK = "a floating translucent crystal skull full of glowing violet-and-amber liquor with vapour leaking from its eyes"


def shellf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.7) < 1.0 and abs(y - 8.6) < 0.9:
                return (20, 14, 30), None                                     # dark eye sockets
        if abs(x) < 0.5 and 6.4 < y < 7.4:
            return (20, 14, 30), None                                         # nasal cavity
    return p["crystal"], None


def liquorf(key, glow):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return c, (P(variant)[glow] if face == "up" else None)
    return s


def teethf(x, y, z, face, variant, **k):
    if face == "north" and abs((x % 0.8) - 0.4) < 0.08:
        return (60, 60, 70, 200), None
    return P(variant)["crystal"][:3] + (200,), None


def build() -> Model:
    m = Model("spiritskull")
    top = m.bone("spiritskull", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    hd = m.bone("head", bd, (0, 5, 0))
    m.round_box(hd, 0, 0, 4.0, 3.6, 5.0, 12.0, shellf, cut=1.4)                 # the crystal skull
    m.round_box(hd, 0, 0.4, 3.2, 2.8, 5.6, 8.0, liquorf("amber_glass", "amber_light"), cut=1.0)   # amber below
    m.round_box(hd, 0, 0.4, 3.2, 2.8, 8.0, 11.2, liquorf("violet_glass", "violet"), cut=1.0)      # violet above
    jw = m.bone("jaw", hd, (0, 5, 0))
    m.round_box(jw, 0, -0.6, 2.6, 2.4, 2.8, 5.0, teethf, cut=0.8)              # the rattling jaw
    for sx in (-1, 1):
        for i, (dy, r) in enumerate(((9.6, 0.8), (11.4, 0.7), (13.0, 0.6))):
            puff(m, hd, (sx * (1.7 + i * 0.4), dy, -3.8 - i * 0.6), r, translucent(P, "violet_glass"))   # leaking vapour
    return m
