"""Iron Forge (Fire/Dark), the future paradox Heatran, built from boxes after the art the user shared (artist and name
not given; our name).

A robot Heatran forged of red-hot metal: its crimson body and legs are cracked with glowing yellow magma, its round
chest ribbed in bronze. Its head is an angular black helmet slit with glowing yellow-orange visor lines, its lower
legs are black armour ringed with spikes, and flames roar up from the back of its shell.

Shiny: a black-and-violet body with violet magma and violet flames.

Front is -z, y is up. 28 units tall (to the flames); about 2.6 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _heatran import BY, heatran
from _regi import ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 28
SCALE = round(2.6 * 16 / HEIGHT, 3)
HITBOX = [2.8, 24 / 16]
KIND = "quadruped"
K = 3
LOOK = ("a robot Heatran of crimson metal cracked with glowing magma, a bronze-ribbed chest, an angular black helmet "
        "with glowing visor lines, spiked black armoured legs and flames roaring from its back")

BASE = {"red": (176, 40, 40), "red_dark": (120, 24, 30), "magma": (255, 214, 110), "magma_hot": (255, 246, 190),
        "bronze": (120, 80, 50), "bronze_dark": (76, 50, 34), "black": (36, 34, 40), "black_light": (74, 72, 80),
        "visor": (255, 190, 60), "visor_red": (240, 70, 40), "spike": (110, 108, 118), "flame": (240, 60, 30),
        "flame_mid": (255, 150, 50), "flame_tip": (255, 236, 140)}
SHINY = {"red": (60, 40, 80), "red_dark": (36, 24, 56), "magma": (210, 130, 255), "magma_hot": (240, 210, 255),
         "visor": (220, 150, 255), "visor_red": (170, 80, 255), "flame": (120, 50, 220), "flame_mid": (180, 110, 255),
         "flame_tip": (236, 210, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def magmaf(x, y, z, face, variant, **k):
    """Crimson metal cracked with glowing yellow magma."""
    p = P(variant)
    n = math.sin(x * 0.55 + math.sin(y * 0.4 + z * 0.3) * 1.8) * math.sin(z * 0.5 + y * 0.35 + math.sin(x * 0.3) * 1.4)
    if n > 0.55:
        c = p["magma_hot"] if n > 0.78 else p["magma"]
        return c, c
    return lit(p["red"], face, y, BY + 2, 8), None


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if (y + 40.0) % 2.0 < 0.45:
        return p["bronze_dark"], None
    return lit(p["bronze"], face, y, BY, 7), None


def blackf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return p["black_light"], None
    return tone(p["black"], face), None


def helmetf(x, y, z, face, variant, **k):
    """The black helmet with glowing visor slits slanting up from its centre."""
    p = P(variant)
    if face in ("north", "east", "west"):
        u = abs(x) if face == "north" else -z - 8.0
        v = y - (BY + 3.6)
        if 0.6 < u < 5.0 and abs(v - 0.35 * u) < 0.36:
            c = p["visor"] if u < 3.2 else p["visor_red"]
            return c, c
    return blackf(x, y, z, face, variant)


def spikef(x, y, z, face, variant, **k):
    return tone(P(variant)["spike"], face), None


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    c = p["flame"] if d < 0.35 else (p["flame_mid"] if d < 0.7 else p["flame_tip"])
    return c, c


def build() -> Model:
    m = Model("ironforge")
    mats = {"shell": magmaf, "chest": chestf, "head": helmetf, "leg_upper": magmaf, "leg_lower": blackf,
            "foot": blackf, "toe": spikef}
    a = heatran(m, mats, "ironforge")
    bd, hd = a["body"], a["head"]
    m.round_box(hd, 0, -10.0, 5.4, 4.6, BY + 1.2, BY + 7.8, helmetf, cut=1)          # the great black helmet
    m.box(hd, -1.4, BY + 7.0, -14.6, 1.4, BY + 10.4, -7.0, helmetf)                  # its crest
    for sx in (-1, 1):                                                           # angular helmet plates
        x0, x1 = sorted((sx * 2.0, sx * 8.6))
        m.box(hd, x0, BY + 5.4, -13.0, x1, BY + 8.8, -6.0, helmetf, rotation=(0, 0, -sx * 14),
              pivot=(sx * 4.0, BY + 7.0, -9.0))
        spike(m, hd, (sx * 8.0, BY + 7.4, -8.0), (sx * 1, 0.5, 0.4), 2.6, 6.0, blackf, tip=1.0)
        for i in range(5):                                                       # jagged teeth along the jaw line
            spike(m, hd, (sx * (0.8 + i * 1.0), BY + 1.4, -14.2 + i * 0.6), (0, -1, -0.3), 1.0, 2.0, spikef)
    for nm, leg in a["legs"].items():                                               # spikes round the armoured legs
        ft, lg, sx = leg["foot"], leg["bone"], leg["side"]
        for j, (dx, dz) in enumerate(((1, 0), (0, -1), (0, 1))):
            base = (ft[0] + dx * sx * 2.4, 7.0, ft[2] + dz * 2.4)
            spike(m, lg, base, (dx * sx * 0.8, 0.9, dz * 0.8), 2.0, 3.6, spikef, tip=0.8)
    for i in range(7):                                                           # flames roaring from its back
        ang = math.radians(-60 + i * 20)
        root = (math.sin(ang) * 7.0, BY + 7.0, 6.0 + math.cos(ang) * 2.0)
        d = (math.sin(ang) * 0.5, 1, 0.5)
        h = 9.0 + 5.0 * math.cos(ang * 1.2)
        spike(m, bd, root, d, 3.2, h, flamef, tip=1.6)
    return m
