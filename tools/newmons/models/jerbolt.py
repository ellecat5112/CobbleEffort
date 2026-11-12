"""Jerbolt, the Hop Mouse Pokémon (Electric/Psychic), built from boxes after a design by NyonTox (used with
permission) and the user's idea: a Pikachu-like mouse inspired by desert hopping mice (jerboas).

A tiny yellow jerboa floating along: a round head with big hypnotic spiral eyes, a pointed snout with a little blue
nose, long ears rimmed in red, a round body with tiny front paws, long hind legs with big red-brown feet, and an
excessively long tail curled into a full hypnotic circle round it, banded yellow and violet and tipped with a
lightning bolt, always turning.

Front is -z, y is up. Floats; 21 units tall with its ring; baseScale 0.24 (0.3 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _jerboa import P, bolt_points, bolt_shader, fur, red, ring
from _route import tone

SCALE = 0.24
HITBOX = [0.4, 0.4]
KIND = "floater"
K = 6
HEIGHT = 21
LOOK = ("a tiny floating yellow jerboa with hypnotic spiral eyes, long red-rimmed ears, big red-brown feet and an "
        "excessively long tail curled into a turning yellow-and-violet ring round it, tipped with a lightning bolt")

CY = 11                                                   # the ring's centre height (the body's middle)


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.3, y - 13.2
            r = math.hypot(dx, dy)
            if r < 1.05:                                  # a hypnotic spiral eye
                ang = math.atan2(dy, dx)
                spiral = (r * 3.2 - ang / math.pi * sx) % 1.0 < 0.5
                return (p["eye"] if spiral else p["white"]), None
    return fur()(x, y, z, face, variant)


def nose(x, y, z, face, variant, **k):
    return P(variant)["nose"], None


def ear(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and box is not None:
        u = (x - box.lo[0]) / max(box.size[0], 1e-6)
        if 0.22 < u < 0.78 and y < box.lo[1] + box.size[1] - 0.6:
            return p["pink"], None
    return tone(p["red"], face), None


def build() -> Model:
    m = Model("jerbolt")
    top = m.bone("jerbolt", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    m.round_box(bd, 0, 0.5, 2.5, 3, 8.5, 12.5, fur(belly_y=10.5), cut=1)
    hd = m.bone("head", bd, (0, 12, -1.5))
    m.round_box(hd, 0, -2, 2.5, 2.2, 11.5, 15, headf, cut=1)
    rod(m, hd, (0, 12.6, -3.8), (0, 12.2, -6.2), 1.4, fur())            # pointed snout
    m.box(hd, -0.5, 11.7, -6.8, 0.5, 12.7, -6.0, nose)
    for sx in (-1, 1):                                                    # long ears
        x0, x1 = sorted((sx * 0.6, sx * 2.0))
        m.box(hd, x0, 14.5, -1.4, x1, 19, -1.4, ear, rotation=(-12, 0, sx * 16), pivot=(sx * 1.3, 14.5, -1.4))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                  # tiny front paws
        a = m.bone(nm, bd, (sx * 1.6, 10, -2))
        m.box(a, sx * 1.6 - 0.5, 8.6, -3.2, sx * 1.6 + 0.5, 10, -2.2, red)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                  # long hind legs, big feet
        lg = m.bone(nm, bd, (sx * 1.8, 9.5, 1.5))
        rod(m, lg, (sx * 1.8, 9.5, 1.5), (sx * 2.0, 7.0, 0.5), 1.4, fur())
        m.box(lg, sx * 2.0 - 0.8, 6.0, -2.6, sx * 2.0 + 0.8, 7.0, 1.2, red)
    rod(m, bd, (0, 9.5, 3.4), (0, 7.5, 5), 0.8, fur())                    # the tail leaving its rump
    rg = m.bone("ring", bd, (0, CY, 5))
    ring(m, rg, 0, CY, 5, 9, 1.4, 0.8)
    pts = bolt_points(5.6, CY + 6.4, 1.2)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    m.box(rg, min(xs), min(ys), 5, max(xs), max(ys), 5, bolt_shader(pts))   # the lightning-bolt tip
    return m
