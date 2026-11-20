"""Burning Verdure (Fire/Grass), the ancient paradox Heatran, built from boxes after sub_arashii's art (@MadZygardeCore;
the art's own name).

A Heatran overgrown like an old forest floor: its rust-brown shell is splashed with glowing orange lava and its round
chest is ribbed in dark grey. Its four legs are charred tree stumps carved with glowing red runes, set with orange
claws and crowned with clumps of tan and olive moss nesting white eggs. Bare dark branches like antlers grow from its
back, one burning at its tip, and its hooded face has glowing orange eyes ringed with white studs.

Shiny: an ashen shell, blue lava and a blue flame.

Front is -z, y is up. 38 units tall (to the branches); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _heatran import BY, heatran
from _pgen1 import CLEAR
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 38
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [2.8, 24 / 16]
KIND = "quadruped"
K = 3
LOOK = ("a Heatran overgrown like a forest floor: lava-splashed rust shell, charred tree-stump legs carved with glowing "
        "runes and crowned with moss and white eggs, and bare branches growing from its back, one aflame")

BASE = {"rust": (150, 76, 46), "rust_dark": (106, 52, 34), "lava": (250, 140, 50), "lava_light": (255, 200, 90),
        "chest": (78, 76, 82), "chest_dark": (50, 48, 54), "hood": (70, 68, 74), "eye": (255, 130, 40),
        "stud": (232, 230, 226), "bark": (60, 44, 40), "bark_dark": (40, 30, 28), "rune": (230, 50, 40),
        "claw": (246, 140, 60), "moss": (196, 180, 120), "moss_dark": (150, 150, 80), "moss_green": (130, 150, 70),
        "egg": (240, 240, 236), "branch": (70, 60, 56), "branch_light": (110, 100, 92), "flame": (255, 120, 40),
        "flame_tip": (255, 220, 110)}
SHINY = {"rust": (110, 106, 104), "rust_dark": (76, 72, 72), "lava": (80, 170, 255), "lava_light": (180, 230, 255),
         "eye": (110, 200, 255), "rune": (80, 170, 255), "claw": (110, 190, 255), "flame": (70, 140, 255),
         "flame_tip": (200, 240, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def shellf(x, y, z, face, variant, **k):
    """Rust-brown shell splashed with glowing lava."""
    p = P(variant)
    n = math.sin(x * 0.45 + math.sin(z * 0.3) * 2.0) * math.sin(z * 0.4 + math.sin(x * 0.35) * 1.6)
    if n > 0.62:
        c = p["lava_light"] if n > 0.8 else p["lava"]
        return c, c
    if face == "up":
        return mix(p["rust"], (255, 255, 255), 0.08), None
    return lit(p["rust"], face, y, BY + 3, 7), None


def chestf(x, y, z, face, variant, **k):
    """The round chest, ribbed in dark grey bands."""
    p = P(variant)
    if (y + 40.0) % 2.4 < 0.5:
        return p["chest_dark"], None
    return lit(p["chest"], face, y, BY, 7), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 1.7, y - (BY + 4.0)) < 0.9:
                return p["eye"], p["eye"]
    return lit(p["hood"], face, y, BY + 3.6, 4), None


def barkf(x, y, z, face, variant, **k):
    """A charred stump: dark bark in vertical grain, carved with glowing red runes."""
    p = P(variant)
    if face in ("north", "south", "east", "west") and 2.4 < y < 7.6:
        u = (x if face in ("north", "south") else z) * 1.0
        cell = math.floor(u / 2.2)
        uu = u - cell * 2.2
        vv = y - 2.4
        g = int(_hash(cell, 5) * 3)
        if (g == 0 and (abs(uu - 1.1) < 0.25 or abs(vv - 2.6) < 0.25 and 0.4 < uu < 1.8)) or \
           (g == 1 and abs(uu - 0.4 - vv * 0.3) < 0.25) or (g == 2 and abs(vv - 1.6 - uu * 0.8) < 0.25 and uu < 1.6):
            return p["rune"], p["rune"]
    if (x * 1.7 + z * 1.3) % 1.4 < 0.3:
        return p["bark_dark"], None
    return tone(p["bark"], face), None


def mossf(x, y, z, face, variant, **k):
    p = P(variant)
    n = math.sin(x * 1.3 + z * 0.7) + math.sin(z * 1.1 - y * 0.9)
    c = p["moss_green"] if n > 1.1 else (p["moss_dark"] if n < -0.9 else p["moss"])
    return tone(c, face), None


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    c = mix(p["flame"], p["flame_tip"], d)
    return c, c


def branch(m, bone, a, b, t, depth, seed):
    """A bare branch from a to b that forks twice more toward its tip."""
    rod(m, bone, a, b, t, solid("branch"), extend=0.4)
    if depth == 0:
        return b
    d = tuple(q - p for p, q in zip(a, b))
    L = math.sqrt(sum(v * v for v in d))
    for j, s in enumerate((-1, 1)):
        ang = 0.6 * s + 0.2 * (_hash(seed, j) - 0.5)
        c, sn = math.cos(ang), math.sin(ang)
        nd = (d[0] * c - d[1] * sn * 0.5, d[1] * 0.9 + abs(d[0]) * 0.2, d[2] * c + d[0] * sn * 0.4)
        n = math.sqrt(sum(v * v for v in nd))
        end = tuple(p + v / n * L * 0.6 for p, v in zip(b, nd))
        branch(m, bone, b, end, max(0.8, t - 0.6), depth - 1, seed * 3 + j)
    return b


def build() -> Model:
    m = Model("burningverdure")
    mats = {"shell": shellf, "chest": chestf, "head": headf, "leg_upper": shellf}
    a = heatran(m, mats, "burningverdure", lower=False)
    bd, hd = a["body"], a["head"]
    for i in range(7):                                                           # white studs round its face
        ang = math.radians(200 + i * 23)
        c = (math.cos(ang) * 5.2, BY + 3.6 - math.sin(ang) * 4.6 * -1, -9.2)
        ellipsoid(m, hd, c[0], c[1], c[2], 1.2, 1.4, 1.1, solid("stud"), step=1)
    for nm, leg in a["legs"].items():                                               # charred tree-stump legs
        ft, lg, sx = leg["foot"], leg["bone"], leg["side"]
        m.round_box(lg, ft[0], ft[2], 3.8, 3.8, 0, 9.0, barkf, cut=1)
        for c in (-1.6, 0.0, 1.6):                                               # orange claws
            ellipsoid(m, lg, ft[0] + c, 1.2, ft[2] - 3.8, 0.8, 1.2, 0.7, solid("claw", True), step=1)
        for j in range(3):                                                       # moss with white eggs on top
            ox, oz = (j - 1) * 2.2, (_hash(j, 3) - 0.5) * 3.0
            ellipsoid(m, lg, ft[0] + ox, 10.0 + j % 2, ft[2] + oz, 2.6, 2.2, 2.6, mossf, step=1)
        ellipsoid(m, lg, ft[0] + sx * 1.6, 11.6, ft[2] - 1.6, 0.9, 1.2, 0.9, solid("egg"), step=1)
    for j, (cx, cz) in enumerate(((-6.0, 6.0), (6.0, 8.0), (-3.0, -2.0))):          # moss on its shell
        ellipsoid(m, bd, cx, BY + 8.0, cz, 3.2, 2.2, 3.2, mossf, step=1)
        ellipsoid(m, bd, cx + 1.4, BY + 9.6, cz - 1.0, 0.9, 1.2, 0.9, solid("egg"), step=1)
    tips = []
    for j, (root, end) in enumerate((((-5.0, BY + 7.0, 8.0), (-10.0, BY + 16.0, 12.0)),
                                     ((-2.0, BY + 8.0, 4.0), (-3.0, BY + 18.0, 6.0)),
                                     ((4.0, BY + 8.0, 5.0), (7.0, BY + 17.0, 7.0)),
                                     ((7.0, BY + 6.0, 9.0), (13.0, BY + 13.0, 13.0)))):
        tips.append(branch(m, bd, root, end, 2.0, 2, j + 1))                     # bare branches like antlers
    spike(m, bd, (12.6, BY + 13.0, 12.6), (0.2, 1, 0), 2.6, 6.4, flamef, tip=1.2)   # one branch aflame
    return m
