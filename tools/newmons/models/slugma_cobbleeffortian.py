"""CobbleEffortian Slugma (Poison/Fire; after @Kai_FakemonsR's art): a slug of oily sludge rising from a lime puddle
on a long neck to a wavy, drippy mushroom cap, its edges burning with a glowing oil-slick rainbow, big glinting eyes
under the cap and coloured spots down its neck.

Shiny: violet sludge on a gold puddle.

Front is -z, y is up. 17 units tall; baseScale 0.65 (0.7 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _petro import P, angle_t, sheen, solid
from _route import tone

SCALE = 0.65
HITBOX = [0.9, 1.05]
KIND = "quadruped"
K = 5
HEIGHT = 17
LOOK = ("a slug of oily sludge rising from a lime puddle to a wavy drippy cap, its edges burning with a glowing "
        "oil-slick rainbow")
CAP_Y = 12.0


def body(x, y, z, face, variant, **k):
    p = P(variant)
    if face not in ("up", "down") and abs(y - 2.6) < 0.5:
        return sheen(p, angle_t(x, z))                                 # a burning rainbow seam along its sides
    for sx, sy, sz in ((0.0, 7.0, -3.4), (-1.0, 5.0, -3.0), (1.2, 9.0, -3.2), (2.6, 3.4, 1.0)):
        if face in ("north", "east", "west") and math.hypot(x - sx, y - sy) < 0.55:
            return sheen(p, (sx + sy) * 0.13)                          # coloured spots
    return tone(p["teal"] if y > 2.0 else p["teal_dark"], face), None


def cap(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            d = math.hypot((x - sx * 1.9) / 1.05, (y - CAP_Y - 0.9) / 0.75)
            if d < 1:
                if math.hypot(x - sx * 1.9 + 0.3, y - CAP_Y - 1.2) < 0.35:
                    return p["eye_white"], None
                return (sheen(p, 0.85 + 0.1 * sx)[0], None) if d > 0.55 else (p["eye_white"], None)
    if y < CAP_Y + 0.8 and face != "up":
        return sheen(p, angle_t(x, z, 0, -1.5))                        # the cap's burning rim
    return tone(p["teal"], face), None


def build() -> Model:
    m = Model("slugma_cobbleeffortian")
    top = m.bone("slugma_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.6, 6.0, 7.0, 0.0, 1.0, solid("lime"), cut=2.4)          # the puddle
    for dx, dz in ((5.6, -4.0), (-6.0, 2.6), (2.0, 7.0)):
        m.round_box(bd, dx, dz, 1.6, 1.4, 0.0, 0.8, solid("lime_dark"), cut=0.6)  # its lobes
    m.round_box(bd, 0, 1.6, 3.0, 4.6, 0.8, 3.6, body, cut=1.2)                  # the slug's foot
    for i, (y0, y1, r) in enumerate(((3.4, 6.0, 2.4), (6.0, 8.6, 2.1), (8.6, 11.2, 2.0))):
        m.round_box(bd, 0, -1.2 - 0.3 * i, r, r, y0, y1, body, cut=0.8)         # the neck
    hd = m.bone("head", bd, (0, 11, -1.5))
    for y0, y1, rx, rz in ((CAP_Y - 1.0, CAP_Y + 1.0, 5.2, 4.6), (CAP_Y + 1.0, CAP_Y + 2.8, 4.6, 4.2),
                           (CAP_Y + 2.8, CAP_Y + 3.8, 3.4, 3.2)):
        m.round_box(hd, 0, -1.5, rx, rz, y0, y1, cap, cut=1.4)                  # the wavy cap
    for a in range(0, 360, 60):                                                 # waves round its rim
        r = math.radians(a)
        m.round_box(hd, 4.8 * math.sin(r), -1.5 - 4.2 * math.cos(r), 1.3, 1.3, CAP_Y + 0.6, CAP_Y + 2.6, cap, cut=0.5)
    for dx, dz, ln in ((-3.6, -4.4, 2.6), (2.8, -4.8, 1.8), (4.6, 0.6, 2.2)):   # drips hanging from the cap
        rod(m, hd, (dx, CAP_Y - 0.8, dz), (dx, CAP_Y - 0.8 - ln, dz), 0.9, solid("teal"), extend=0.2)
    return m
