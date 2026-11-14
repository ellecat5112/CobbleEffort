"""Mentholynx, the Menthol Lynx Pokémon (Ice/Dark), the Nicodex's Ice type (the user's design): a sleek dark navy
lynx frosted with crystalline menthol: mint-white frost along its back, mint cheek ruffs and ear tufts, icy cyan
glowing eyes, mint paws, a bobtail and clear crystal shards along its spine.

Shiny: a silver-white lynx with violet frost.

Front is -z, y is up. 22 units tall; baseScale 0.7 (0.95 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import palette, translucent
from _route import tone

SHINY = {"navy": (196, 200, 214), "navy_light": (226, 228, 238), "mint": (196, 170, 246), "mint_dark": (150, 120, 220),
         "cyan": (220, 120, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.7
HITBOX = [1.1, 1.35]
KIND = "quadruped"
K = 4
HEIGHT = 22
LOOK = ("a sleek dark navy lynx frosted with mint: frost along its back, mint cheek ruffs and ear tufts, icy glowing "
        "eyes, a bobtail and crystal shards along its spine")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" or (face in ("east", "west") and y > 13.2):
        return tone(p["mint"], face), None                                    # frost along its back
    return tone(p["navy"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.5, y - 17.0
            if (dx / 0.9) ** 2 + ((dy - dx * sx * 0.4) / 0.42) ** 2 < 1:
                return p["cyan"], p["cyan"]                                   # icy slanted eyes
        if y < 15.4 and abs(x) < 1.4:
            return p["white"], None                                           # pale muzzle
    return tone(p["navy_light"] if face == "up" else p["navy"], face), None


def build() -> Model:
    m = Model("mentholynx")
    top = m.bone("mentholynx", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 11, 0))
    m.round_box(bd, 0, 1.0, 3.6, 7.0, 8.0, 14.6, bodyf, cut=1.4)
    for z in (-2.0, 1.0, 4.0):                                                  # crystal shards on its spine
        spike(m, bd, (0, 14.4, z), (0, 1, 0.4), 1.4, 2.6, translucent(P, "ice"), tip=0.6)
    spike(m, bd, (0, 12.4, 7.8), (0, 0.6, 1), 2.0, 2.2, solid("mint"))          # bobtail
    hd = m.bone("head", bd, (0, 14, -6))
    m.round_box(hd, 0, -7.6, 3.2, 2.8, 13.6, 19.4, headf, cut=1.0)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 19.2, -7.2), (sx * 0.25, 1, 0.1), 1.6, 3.0, solid("navy"), tip=0.8)   # ears
        spike(m, hd, (sx * 2.2, 21.6, -7.0), (0, 1, 0), 0.8, 1.6, solid("mint"))          # ear tufts
        for dy in (14.6, 16.0):
            spike(m, hd, (sx * 3.0, dy, -6.6), (sx * 1, -0.3, 0.4), 1.4, 2.0, solid("mint"))   # cheek ruffs
    for sx, side in ((-1, "left"), (1, "right")):
        for role, z in (("front", -4.6), ("back", 5.4)):
            lb = m.bone(f"leg_{role}_{side}", top, (sx * 2.4, 9, z))
            m.round_box(lb, sx * 2.4, z, 1.2, 1.3, 1.2, 9.6, solid("navy"), cut=0.5)
            m.round_box(lb, sx * 2.4, z - 0.3, 1.5, 1.7, 0.0, 1.6, solid("mint"), cut=0.6)  # mint paws
    return m
