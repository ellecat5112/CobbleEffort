"""Hallowed Wings (Normal/Flying), the ancient paradox Arceus, built from boxes after the art the user shared (artist
and name not given; our name).

An Arceus that took to the air in the world's first days: a white horse-like body over grey underparts, its golden
wheel round its waist, a dark wavy mane sweeping back from its neck and a hooked, bird-like face with a red eye under a
crest of white feathers. Great wings of long white feathers, shaded grey at their roots, fan up and back from its
shoulders, and its legs end in hooves tipped with gold.

Shiny: a cream body, a white mane and a silver wheel.

Front is -z, y is up. 45 units tall (to the wing tips); about 3.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import slab_z
from _pgen1 import smooth_path
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 45
SCALE = round(3.6 * 16 / HEIGHT, 3)
HITBOX = [2.4, 38 / 16]
KIND = "quadruped"
K = 3
LOOK = ("a white feathered Arceus with its golden wheel, a dark wavy mane, a hooked bird-like face under white crest "
        "feathers, great white feathered wings and gold-tipped hooves")

BASE = {"white": (246, 246, 250), "white_dark": (204, 204, 216), "grey": (150, 150, 162), "grey_dark": (110, 110, 122),
        "mane": (70, 66, 72), "mane_light": (104, 100, 108), "gold": (232, 196, 70), "gold_dark": (184, 146, 44),
        "eye": (200, 40, 40), "beak": (236, 220, 170)}
SHINY = {"white": (250, 240, 214), "white_dark": (214, 200, 168), "mane": (230, 230, 236), "mane_light": (250, 250, 252),
         "gold": (206, 212, 226), "gold_dark": (156, 162, 180)}
BY = 22.0
WC = (0.0, BY, 4.0)       # the wheel's centre


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, **k):
    """White above, grey beneath."""
    p = P(variant)
    if face == "down" or y < BY - 3.6:
        return tone(p["grey"], face), None
    if face == "up":
        return p["white"], None
    return lit(p["white"], face, y, BY, 6), None


def legf(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 9.0 and face in ("south", "east", "west"):
        return tone(p["grey"], face), None
    return tone(p["white"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and math.hypot(z + 16.4, y - 39.0) < 0.7:
        return p["eye"], p["eye"]
    return lit(p["white"], face, y, 38, 3), None


def manef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = box.lo[2] + box.size[2] - z
    if d % 3.0 < 0.6:
        return p["mane_light"], None
    return tone(p["mane"], face), None


def featherf(x, y, z, face, variant, box=None, **k):
    """A long wing feather: white, grey at its root (rods: z runs back from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    if d < 0.25:
        return tone(p["grey"], face), None
    cy = box.lo[1] + box.size[1] / 2
    if abs(y - cy) < 0.25 and face in ("up", "down"):
        return p["white_dark"], None
    return tone(p["white"], face), None


def goldf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return mix(p["gold"], (255, 255, 255), 0.2), None
    return tone(p["gold"] if face != "down" else p["gold_dark"], face), None


def build() -> Model:
    m = Model("hallowedwings")
    top = m.bone("hallowedwings", None, (0, 0, 0))
    bd = m.bone("body", top, (0, BY, 0))
    for z0, z1, rx, ry, dy in ((-12, -7, 4.8, 5.6, 0.8), (-7, -1, 5.2, 5.8, 0.4), (-1, 5, 5.0, 5.4, 0.0),
                               (5, 10, 4.8, 5.0, 0.2), (10, 13, 4.0, 4.2, 0.8)):
        slab_z(m, bd, 0, BY + dy, z0, z1, rx, ry, bodyf)                            # the body
    for i in range(24):                                                          # the golden wheel round its waist
        a0, a1 = 2 * math.pi * i / 24, 2 * math.pi * (i + 1) / 24
        p0 = (WC[0] + math.cos(a0) * 9.4, WC[1] + math.sin(a0) * 9.4, WC[2])
        p1 = (WC[0] + math.cos(a1) * 9.4, WC[1] + math.sin(a1) * 9.4, WC[2])
        rod(m, bd, p0, p1, 1.8, goldf, extend=0.4, t2=1.8)
    for a in (0, 90, 180, 270):                                                  # its four knobs
        c = (WC[0] + math.cos(math.radians(a)) * 9.4, WC[1] + math.sin(math.radians(a)) * 9.4, WC[2])
        ellipsoid(m, bd, c[0], c[1], c[2], 1.8, 1.8, 1.8, goldf, step=1)
        rod(m, bd, (c[0] * 0.55, WC[1] + (c[1] - WC[1]) * 0.55, WC[2]), c, 1.6, goldf, extend=0.4)
    nk = m.bone("neck", bd, (0, BY + 4.0, -9.0))
    npts = smooth_path([(0, BY + 3.0, -9.0), (0, BY + 9.0, -12.0), (0, BY + 14.0, -13.0)], 6)
    for i, (a, b) in enumerate(zip(npts, npts[1:])):
        rod(m, nk, a, b, round((5.6 - 1.6 * i / (len(npts) - 2)) * 2) / 2, solid("white"), extend=0.8)
    for j in range(4):                                                           # the dark wavy mane
        root = (0, BY + 6.0 + j * 2.8, -9.4 - j * 1.0)
        pts = smooth_path([root, (0.6 * (j % 2), root[1] + 1.4, root[2] + 4.0), (0, root[1] - 0.6, root[2] + 8.0),
                           (-0.8 * (j % 2), root[1] + 0.6, root[2] + 11.0)], 6)
        for a, b in zip(pts, pts[1:]):
            rod(m, nk, a, b, 4.4 - j * 0.4, manef, extend=0.6, t2=2.0)
    hd = m.bone("head", nk, (0, BY + 15.0, -13.0))
    m.round_box(hd, 0, -14.6, 2.6, 3.0, BY + 14.4, BY + 19.4, headf, cut=1)          # head
    spike(m, hd, (0, BY + 16.0, -17.0), (0, -0.4, -1), 2.4, 4.6, solid("beak"), tip=1.0)   # hooked beak
    for i, (dx, h) in enumerate(((0.0, 7.0), (-1.4, 5.6), (1.4, 5.6), (-2.4, 4.0), (2.4, 4.0))):   # crest feathers
        spike(m, hd, (dx, BY + 19.0, -14.0), (dx * 0.2, 1, 0.55), 1.6, h, featherf, tip=0.8)
    for nm, sx in (("wing_left", 1), ("wing_right", -1)):                        # great white wings
        wg = m.bone(nm, bd, (sx * 3.6, BY + 5.0, -4.0))
        for i in range(7):
            ang = math.radians(15 + i * 13)
            d = (sx * (0.75 - 0.05 * i), math.cos(ang) * 1.1, math.sin(ang) + 0.2)
            root = (sx * (3.6 + 0.3 * i), BY + 5.0 - 0.3 * i, -4.0 + 1.2 * i)
            L = 20.0 + 6.0 * math.sin((i + 0.5) / 7 * math.pi)
            n = math.sqrt(sum(v * v for v in d))
            end = tuple(q + v / n * L for q, v in zip(root, d))
            rod(m, wg, root, end, 1.0, featherf, extend=0.4, t2=3.6)
    for nm, sx, z, front in (("leg_front_left", 1, -8.0, True), ("leg_front_right", -1, -8.0, True),
                             ("leg_back_left", 1, 8.0, False), ("leg_back_right", -1, 8.0, False)):
        hip = (sx * 4.4, BY - 2.0, z)
        lg = m.bone(nm, top, hip)
        ellipsoid(m, lg, sx * 4.6, BY - 4.0, z, 2.6, 4.4, 3.0, bodyf, step=1)
        kn = (sx * 5.0, 11.0, z + (-1.0 if front else 2.4))
        ft = (sx * 5.0, 2.0, z + (-1.6 if front else 0.6))
        rod(m, lg, (sx * 4.8, BY - 6.0, z), kn, 3.4, legf, extend=0.8)
        rod(m, lg, kn, ft, 2.8, legf, extend=0.6)
        spike(m, lg, ft, (0, -1, -0.2), 3.0, 3.6, goldf, tip=1.2)                 # gold-tipped hoof
    tl = m.bone("tail", bd, (0, BY + 1.0, 12.0))
    for i in range(3):                                                           # a few white tail feathers
        spike(m, tl, (0, BY + 1.0, 12.0), ((i - 1) * 0.5, -0.4, 1), 1.6, 8.0 - abs(i - 1) * 1.6, featherf, tip=0.6)
    return m
