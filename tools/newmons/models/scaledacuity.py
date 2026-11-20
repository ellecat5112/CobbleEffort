"""Scaled Acuity (Dragon/Psychic), the ancient paradox Uxie, built from boxes after @Alex_LR04's art (the art's own
name).

An Uxie whose golden helmet has grown into a great coiled shell of scales, ridged like a ram's horn round its sides,
with a crest of red, orange and gold scales flaring from its crown. Its eyes are shut, a red gem horn juts from its
brow, teal spotted fins spread from its shoulders, and its two pale tails curl round below it, each ending in three
lobes set with red gems.

Shiny: a rose-gold shell and violet fins.

Front is -z, y is up. 28 units tall (to the crest); about 0.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _boxmodel import spike
from _lake import body, brow_gem, fins, scallop, skin, solid, tail
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 28
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.7, HEIGHT / 16]
KIND = "floater"
K = 4
LOOK = ("an Uxie whose golden helmet is a great coiled shell of scales with a crest of red and gold scales, closed "
        "eyes, a red gem horn, teal spotted shoulder fins and two tails ending in red-gemmed lobes")

BASE = {"skin": (228, 238, 255), "skin_dark": (190, 204, 236), "gold": (246, 204, 88), "gold_dark": (206, 158, 52),
        "gold_line": (168, 116, 36), "red": (220, 40, 52), "red_light": (255, 128, 116), "orange": (250, 140, 50),
        "yellow": (255, 222, 96), "teal": (100, 184, 206), "teal_dark": (44, 116, 150), "teal_light": (160, 220, 236),
        "line": (130, 140, 176), "lid": (70, 56, 80)}
SHINY = {"gold": (238, 172, 160), "gold_dark": (200, 124, 120), "gold_line": (150, 80, 90), "teal": (150, 110, 200),
         "teal_dark": (90, 60, 140), "teal_light": (200, 170, 240)}
CY = 12.0
HC = (0, 22.0, 1.0)     # the shell cap's centre
COIL = (19.4, 1.2)      # the side coils' centre (y, z)


def P(v):
    return pal(BASE, SHINY, v)


def capf(x, y, z, face, variant, **k):
    """The cap of the shell: rows of round gold scales."""
    p = P(variant)
    u, v = (x, z) if face in ("up", "down") else ((z, y) if face in ("east", "west") else (x, y))
    if scallop(u, v):
        return p["gold_line"], None
    return lit(p["gold"], face, y, HC[1], 3.4), None


def coilf(x, y, z, face, variant, **k):
    """A side coil curled like a ram's horn: a spiral groove on its outer face, ridges round its rim."""
    p = P(variant)
    if face in ("east", "west"):
        r = math.hypot(y - COIL[0], z - COIL[1])
        a = math.atan2(y - COIL[0], z - COIL[1])
        if (r - a / (2 * math.pi) * 1.4) % 1.4 < 0.3:
            return p["gold_line"], None
        return mix(p["gold"], p["gold_dark"], min(1.0, r / 5.0) * 0.5), None
    if (y * 1.2 + z * 0.4) % 1.3 < 0.25:
        return p["gold_line"], None
    return lit(p["gold_dark"], face, y, COIL[0], 3.6), None


def facef(x, y, z, face, variant, **k):
    """The pale face with its eyes shut: two dark arcs."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.25, y - 18.4
            if abs(dx) < 0.85 and abs(dy - 0.35 * (dx * dx) + 0.1) < 0.2:
                return p["lid"], None
        if abs(x) < 0.4 and abs(y - 16.9) < 0.15:
            return p["lid"], None
    return lit(p["skin"], face, y, 18.2, 3), None


def flamef(x, y, z, face, variant, box=None, **k):
    """A crest scale: red at its root, orange, then gold at its tip (rods: z runs back from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    c = p["red"] if d < 0.4 else (p["orange"] if d < 0.75 else p["yellow"])
    return tone(c, face), None


def build() -> Model:
    m = Model("scaledacuity")
    top = m.bone("scaledacuity", None, (0, 0, 0))
    bd = m.bone("body", top, (0, CY, 0))
    body(m, bd, CY, P)
    fins(m, bd, [(2.0, 16.2), (5.0, 17.2), (8.6, 16.0), (7.4, 15.0), (8.0, 13.8), (6.2, 13.6), (6.4, 12.4),
                 (4.4, 12.8), (2.0, 14.0)], 0.8, P)
    hd = m.bone("head", bd, (0, 16.4, 0))
    ellipsoid(m, hd, 0, 18.2, -1.6, 3.2, 2.9, 3.0, facef, step=1)                  # the pale face
    ellipsoid(m, hd, HC[0], HC[1], HC[2], 4.0, 3.4, 4.2, capf, step=1)            # the scaled cap
    for sx in (-1, 1):                                                           # the coils, curled like ram's horns
        ellipsoid(m, hd, sx * 4.4, COIL[0], COIL[1], 2.2, 3.8, 3.8, coilf, step=1)
    brow_gem(m, hd, (-0.4, 20.6, -3.6), (-0.25, 1, -0.5), P, w=1.8, h=4.0)
    crest = m.bone("cap", hd, (-1.0, 25.0, 0.6))                                   # crest of flaring scales
    for i in range(5):
        a = math.radians(95 + i * 20)
        d = (math.cos(a), math.sin(a) + 0.1, 0.15)
        L = 5.0 + 2.6 * math.sin((i + 0.5) / 5 * math.pi)
        root = (-0.6 - 0.7 * i, 24.6 - 0.5 * i, 0.6 + 0.4 * (i % 2))
        spike(m, crest, root, d, 2.4, L, flamef, tip=1.2)
    tail(m, m.bone("tail_left", bd, (0.8, 9.6, 1.6)),
         [(0.8, 9.6, 1.6), (3.8, 7.6, 3.0), (6.4, 4.2, 2.2), (5.6, 4.4, 0.8), (2.6, 5.2, -0.4)], 1.8, 1.0, P, lobe=5.0)
    tail(m, m.bone("tail_right", bd, (-0.8, 9.6, 1.6)),
         [(-0.8, 9.6, 1.6), (-3.2, 6.8, 2.6), (-5.6, 5.6, 1.6), (-8.6, 5.4, 0.4)], 1.8, 1.0, P, lobe=5.0)
    return m
