"""Fangfosh, the Gnashfish Pokémon (Water), the water starter, after the art of the A. Fakemon fanpage (the art's own
name): a little pale aqua fish sitting up on blue frog legs, with a huge grimace full of square white teeth, big round
blue eyes, a black stripe running back over its head into a black dorsal fin, a blue belly, gill slits and a blue tail
fin.

Shiny: lilac with violet legs and fins and magenta eyes.

Front is -z, y is up. 15 units tall to the top of its fin; baseScale 0.3 (0.28 m).
"""
from __future__ import annotations

import math

from _afake import round_eye
from _boxmodel import Model, mix, rod
from _fishface import P, fin, grimace, solid
from _route import tone

SCALE = 0.3
HITBOX = [0.7, 0.95]
KIND = "quadruped"
K = 6
HEIGHT = 15
LOOK = ("a little pale aqua fish on blue frog legs with a huge grimace of square white teeth, big round blue eyes, a "
        "black stripe into a black dorsal fin and a blue tail fin")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        g = grimace(p, x, y, 3.4, 4.2, 7.0, pointed=False)
        if g:
            return g, None
    if face == "down" or (face == "north" and y < 4.0) or (face in ("east", "west") and y < 3.4 and z < 1.5):
        return tone(p["blue"], face), None                                    # the blue belly
    if face == "up" and abs(x) < 1.4:
        return p["black"], None                                               # the black stripe over its head
    if face in ("east", "west") and 3.0 < y < 6.6:
        for z0 in (0.4, 1.4):
            if abs((z - z0) - (y - 4.0) * 0.3) < 0.18:
                return p["cyan_dark"], None                                   # gill slits
    return tone(p["cyan"], face), None


def eyef(sx):
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "north":
            e = round_eye(x - sx * 3.3, y - 8.8, 1.25, p, "eye", ry=1.45)
        elif face in ("east", "west") and abs(x) > 4.4:
            e = round_eye(z + 4.9, y - 8.8, 1.3, p, "eye", ry=1.45)
        else:
            e = None
        return (e, None) if e else (tone(p["cyan"], face), None)
    return s


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    return tone(p["blue"], face), None


def build() -> Model:
    m = Model("fangfosh")
    top = m.bone("fangfosh", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, -1.5, 4.2, 4.4, 2.0, 10.0, bodyf, cut=1.6)              # its big head-body
    m.round_box(bd, 0, 4.5, 3.0, 2.6, 2.5, 7.0, bodyf, cut=1.0)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.0, sx * 4.6))
        m.box(bd, x0, 7.2, -6.4, x1, 10.4, -3.4, eyef(sx))                     # big round eyes
    m.box(bd, 0, 9.6, -1.5, 0, 14.6, 6.0, fin(                                  # the black dorsal fin
        lambda a, b: b - 9.6 < 4.8 * math.sin(math.pi * max(0.0, min(1.0, (a + 1.5) / 7.5))) ** 0.7,
        lambda p, a, b: p["black"]))

    tl = m.bone("tail", bd, (0, 5, 6.8))
    m.round_box(tl, 0, 6.6, 1.6, 1.0, 3.4, 6.4, solid("blue"), cut=0.6)        # the blue tail band
    m.box(tl, 0, 0.6, 6.6, 0, 9.0, 12.4, fin(
        lambda a, b: abs(b - 4.8) < 1.0 + (a - 6.6) * 0.62 and not (a > 11.0 and abs(b - 4.8) < (a - 11.0) * 1.2),
        lambda p, a, b: p["blue_dark"] if abs(((b - 4.8) / max(0.5, a - 6.0)) * 3.0 % 1.0 - 0.5) < 0.08 else p["blue"]))

    for sx, side in ((-1, "left"), (1, "right")):
        lf = m.bone(f"leg_front_{side}", top, (sx * 3.0, 4.0, -3.2))
        rod(m, lf, (sx * 3.0, 4.0, -3.2), (sx * 4.6, 0.6, -4.6), 1.8, legf, extend=0.4)
        x0, x1 = sorted((sx * 3.4, sx * 6.0))
        m.box(lf, x0, 0.0, -7.0, x1, 1.0, -3.6, solid("blue"))                # webbed front feet
        lb = m.bone(f"leg_back_{side}", top, (sx * 2.4, 3.0, 2.6))
        rod(m, lb, (sx * 2.4, 3.0, 2.6), (sx * 3.8, 0.6, 3.6), 1.6, legf, extend=0.4)
        x0, x1 = sorted((sx * 3.0, sx * 5.2))
        m.box(lb, x0, 0.0, 3.0, x1, 1.0, 5.6, solid("blue"))
    return m
