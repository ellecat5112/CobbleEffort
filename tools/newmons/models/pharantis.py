"""Pharantis, the Pharaoh Pokémon (Water/Bug), hand-built from boxes from the user's design.

A cross between a nimble praying mantis and a pharaoh: a narrow face with fierce glowing orange eyes framed by a royal
headcloth striped gold and blue (lappets hanging to its shoulders) and a golden cobra rearing from its brow; a slender
segmented body of blue and pale blue with a golden medallion on the chest and a golden collar; long raised scythe arms
banded blue and white that end in golden hooks like a pharaoh's crook; a pleated golden kilt; and long thin black legs
tipped with silver claws.

Front is -z, y is up. 32.5 units tall to its cobra; baseScale 0.79 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, mix, rod
from _pharaoh import P, black, gold, ring_eye

SCALE = 0.79
HITBOX = [0.9, 1.6]
KIND = "biped"
K = 4
HEIGHT = 32.5
LOOK = ("a nimble mantis pharaoh: a gold-and-blue striped headcloth with a golden cobra, fierce orange eyes, a blue "
        "segmented body with a gold medallion, raised banded scythe arms ending in golden crook hooks, a pleated gold "
        "kilt and long black legs with silver claws")


def along(z, box):
    return (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)


def banded(x, y, z, face, variant, box=None, **k):
    """Blue / pale blue / white segments along a limb."""
    pal = P(variant)
    t = along(z, box)
    i = int(t * 5)
    c = (pal["blue"], pal["blue_pale"], pal["wrap"])[i % 3]
    if face not in ("north", "south") and abs(t * 5 - round(t * 5)) < 0.06:
        c = mix(c, pal["black"], 0.5)
    return c, None


def leg(x, y, z, face, variant, box=None, **k):
    pal = P(variant)
    if box is not None and along(z, box) > 0.86 and box.size[2] > 6:
        return pal["silver"], None
    return pal["black"], None


def body(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north" and math.hypot(x, y - 17.5) < 1.2:          # the golden medallion
        return gold(x, y, z, face, variant)
    return (pal["blue"] if (y % 2.4) < 1.4 else pal["blue_pale"]), None


def headcloth(x, y, z, face, variant, **k):
    pal = P(variant)
    v = y if face not in ("up", "down") else x
    return (pal["gold"] if (v % 1.6) < 0.8 else pal["blue"]), None


def face_f(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.2, y - 25.4
            brow = dy > 0.4 - 0.5 * (abs(x) - 1.2)      # fierce: the inner corners cut down
            e = ring_eye(dx, dy * 1.4, 0.95, variant, orange=True)
            if e and not brow:
                return e
        if abs(x) < 0.4 and 22.0 < y < 27.0:                        # a gold stripe down the nose
            return pal["gold"], None
    return mix(pal["blue"], pal["black"], 0.45), None


def kilt(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north":
        half = 2.6 * (y - 6.8) / 6.2                                # a pleated triangle pointing down
        if abs(x) > half:
            return (0, 0, 0, 0), None
        c = pal["gold"] if (x * 1.3) % 1.0 < 0.75 else pal["gold_dark"]
        return c, None
    if face == "south":
        return (0, 0, 0, 0), None
    return gold(x, y, z, face, variant)


def build() -> Model:
    m = Model("pharantis")
    top = m.bone("pharantis", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 13, 0))
    m.round_box(bd, 0, 0, 3.5, 3, 10.5, 14, gold, cut=1)                    # the kilt's band
    m.box(bd, -3, 7, -3.4, 3, 13, -2.9, kilt)                               # its pleated front
    m.round_box(bd, 0, -0.5, 3, 2.5, 14, 21, body, cut=1)                  # slender segmented thorax
    m.round_box(bd, 0, -0.5, 3.2, 2.7, 20.5, 22, gold, cut=1)               # golden collar
    tail = m.bone("tail", bd, (0, 13, 2))
    m.round_box(tail, 0, 5, 3, 3.5, 9, 15, body, cut=1)
    m.round_box(tail, 0, 8.5, 2.5, 2.5, 8, 13, body, cut=1)
    hd = m.bone("head", bd, (0, 22, -1))
    m.box(hd, -2.5, 21.5, -4, 2.5, 27.5, 0, face_f)                         # the face
    m.round_box(hd, 0, -0.5, 4.5, 2.5, 25, 30, headcloth, cut=1)            # the headcloth
    for sx in (-1, 1):                                                       # its lappets
        m.box(hd, sx * 3.8 - 1, 18.5, -3, sx * 3.8 + 1, 25.5, -0.5, headcloth)
    chain(m, hd, [(0, 28.4, -3.6), (0, 30.6, -4.4), (0, 31.8, -3.6)], [1.4, 1.1], gold)   # the cobra
    m.box(hd, -1, 31, -4.9, 1, 32.5, -3.9, gold)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, bd, (sx * 3, 20, -0.5))
        rod(m, arm, (sx * 3, 20, -0.5), (sx * 6.5, 17.5, -4), 2, banded)
        rod(m, arm, (sx * 6.5, 17.5, -4), (sx * 7.5, 26, -9), 3, banded)    # the scythe, raised in front
        chain(m, arm, [(sx * 7.5, 26, -9), (sx * 7, 28.5, -10.5), (sx * 5.3, 28.6, -11.8)], [1.5, 1.2], gold)   # crook hook
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 12, 1))
        knee = (sx * 4.5, 8.5, 2.5)
        rod(m, lg, (sx * 2.2, 12, 1), knee, 2, leg)
        rod(m, lg, knee, (sx * 3.8, 0.3, -1.5), 1.5, leg)
    return m
