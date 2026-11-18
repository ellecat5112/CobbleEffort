"""Fantomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the grim reaper. A floating spectre in a tattered pale-grey shroud stitched with dark runes, a red
hood with a radiation-like emblem over a black void of a face with two glowing eyes, a gold medallion with a red gem
at its throat, a long iron chain trailing a spiked ball, and a great curved gold scythe on a long staff. 25 blocks
tall.

Front is -z, y is up. 56 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape
from _digidetail import fabric, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 56
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a floating reaper in a tattered grey rune-stitched shroud, a red hood over a black void face with glowing eyes, "
        "a gold medallion, a chained spiked ball and a great gold scythe")
BASE = {"grey": (200, 200, 206), "grey_dark": (120, 120, 130), "red": (200, 30, 30), "red_dark": (110, 10, 14),
        "black": (14, 12, 18), "eye": (120, 220, 250), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
        "gem": (220, 30, 50), "gem_light": (255, 150, 160), "iron": (90, 90, 100), "iron_dark": (40, 40, 46),
        "rune": (60, 50, 90), "lining": (80, 60, 150)}
SHINY = {"red": (40, 60, 160), "red_dark": (14, 20, 80), "grey": (60, 60, 70), "grey_dark": (24, 24, 30)}


def P(v):
    return pal(BASE, SHINY, v)


SHROUD = fabric(P, "grey", "grey_dark", axis="y")
HOOD = fabric(P, "red", "red_dark")
GOLD = metal(P, "gold", dark="gold_dark")
IRON = metal(P, "iron", dark="iron_dark")


def shroudf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs((x * 0.6) % 4.0 - 2.0) < 0.6 and abs((y * 0.6) % 4.0 - 2.0) < 0.6:
        return tone(p["rune"], face), None
    return SHROUD(x, y, z, face, variant, box=box, **k)


def hoodf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if abs(x) < 2.6 and 38.0 < y < 43.6:
            for sx in (-1, 1):
                if abs(x - sx * 1.2) < 0.5 and abs(y - 41.4) < 0.4:
                    return p["eye"], p["eye"]
            return tone(p["black"], face), None
        if math.hypot(x, y - 46.0) < 1.4:
            return tone(p["grey"], face), None                         # hood emblem
    return HOOD(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("fantomon")
    top = m.bone("fantomon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    for i, (r, y0) in enumerate(((9.0, 6.0), (8.0, 12.0), (7.0, 18.0), (6.0, 24.0), (5.4, 30.0))):   # shroud
        m.round_box(bd, 0, 0.6, r, r * 0.8, y0, y0 + 6.2, shroudf, cut=max(1, round(r * 0.35)))
    cape(m, bd, 38.0, 18.0, 30.0, fabric(P, "red", "red_dark"), z=5.0, flare=1.0)          # red cloak behind
    for j in range(8):                                                                    # ragged hem
        ang = 2 * math.pi * j / 8
        spike(m, bd, (8.0 * math.cos(ang), 6.4, 6.4 * math.sin(ang)), (math.cos(ang) * 0.3, -1, math.sin(ang) * 0.3),
              2.6, 4.0, shroudf, tip=0.8)
    hd = m.bone("head", bd, (0, 38, 0))
    m.round_box(hd, 0, 0, 4.4, 4.0, 36.0, 48.0, hoodf, cut=2)                              # red hood
    spike(m, hd, (0, 47.0, 1.0), (0, 0.6, 1), 2.6, 4.0, HOOD, tip=0.6)
    m.round_box(bd, 0, -4.6, 2.0, 0.8, 33.0, 36.0, GOLD, cut=0)                             # gold medallion
    m.round_box(bd, 0, -5.4, 1.0, 0.4, 33.8, 35.2, gem(P, "gem", "gem_light"), cut=0)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 6.0, 32.0, 0))
        rod(m, ab, (sx * 6.0, 32.0, 0), (sx * 11.0, 26.0, -3.0), 4, shroudf, extend=0.6)       # wide sleeves
    al = "arm_left"                                                                       # iron chain + spiked ball
    for j in range(8):
        y = 24.0 - j * 1.8
        m.box(al, 11.0 + (j % 2) * 0.3 - 0.5, y - 0.8, -3.5, 11.5 + (j % 2) * 0.3, y + 0.8, -2.5, IRON)
    m.round_box(al, 11.0, -3.0, 2.4, 2.4, 6.0, 10.6, IRON, cut=1)
    for ang in range(0, 360, 60):
        r_ = math.radians(ang)
        spike(m, al, (11.0 + 2.4 * math.cos(r_), 8.3, -3.0 + 2.4 * math.sin(r_)), (math.cos(r_), 0, math.sin(r_)),
              1.0, 1.6, IRON)
    ar = "arm_right"                                                                      # the scythe
    rod(m, ar, (-11.0, 10.0, -3.0), (-11.0, 58.0, -3.0), 1, solid(P, "gold_dark"), extend=0)
    pts = [(-11.0, 58.0, -3.0), (-6.0, 60.0, -3.0), (-1.0, 58.0, -3.0), (2.0, 53.0, -3.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, ar, p0, p1, 1, GOLD, extend=0.4, t2=4 - j)
    return m
