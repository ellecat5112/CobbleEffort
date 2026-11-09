"""Mega Roaring Moon, hand-built from boxes in Cobblemon's style.

Roaring Moon (official art: an ancient Mega Salamence: a lean blue dragon with a white swept crest, red eyes, a yellow
chest mark, red claws, and huge crimson crescent wings edged with light-blue spikes, black at their lower tips) as a
mega: the wings sweep round into a full blood-moon crescent glowing at its edge, a bigger crest and a longer tail.
It flies.

Front is -z, y is up. ~46 units tall with the wings; baseScale 1.2 (about 3.5 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.2
HITBOX = [2.6, 3.4]
LOOK = ("a lean blue dragon with a swept white crest and yellow chest mark, its crimson wings swept round into a "
        "blood-moon crescent edged with light-blue spikes and a glowing rim, black wingtips and red claws")
KIND = "floater"
ANIM = {"wing_flap": 5}

BASE = {
    "blue": (70, 150, 210), "blue_light": (110, 186, 236), "blue_dark": (44, 104, 160), "crest": (240, 240, 246),
    "chest": (250, 210, 60), "red": (214, 30, 70), "red_dark": (160, 20, 52), "rim": (255, 110, 140), "black": (30, 26, 36),
    "spike": (130, 210, 236), "eye": (230, 40, 40), "claw": (214, 40, 60),
}
SHINY = {"blue": (90, 170, 110), "blue_light": (130, 206, 146), "blue_dark": (60, 120, 80), "red": (230, 120, 40),
         "red_dark": (180, 80, 30), "rim": (255, 200, 110), "spike": (200, 240, 140), "chest": (240, 110, 200)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def blue(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["blue_dark"] if face == "down" else (P["blue_light"] if face == "up" else P["blue"])


def torso(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and abs(x) <= 3.5 - (24 - y) * 0.4 and 17 <= y <= 24:
        return P["chest"]                               # a yellow V on the chest
    return blue(x, y, z, face, variant)


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 30.5 <= y <= 31.6 and -8.5 <= z <= -6.5:
        return P["eye"], P["eye"]
    return blue(x, y, z, face, variant)


def crest(x, y, z, face, variant, **k):
    return palette(variant)["crest"]


def spike_c(x, y, z, face, variant, **k):
    return palette(variant)["spike"]


def claw(x, y, z, face, variant, **k):
    return palette(variant)["claw"]


def wing(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, box=None, **k):
    """A crescent segment: crimson, with a glowing rim along its outer edge and black at the lowest segments."""
    P = palette(variant)
    if r <= 1:
        return P["rim"], P["rim"]
    if box.lo[1] < 18:
        return P["black"] if r > rows // 2 else P["red_dark"]
    return P["red"] if r < rows - 2 else P["red_dark"]


def build() -> Model:
    m = Model("roaringmoon_mega")
    root = m.bone("roaringmoon_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 0))
    m.box(body, -4, 14, -4, 4, 25, 4, torso)
    m.box(body, -3, 11, -3, 3, 14, 3, blue)
    # arms with red claws
    for sgn in (1, -1):
        chain(m, body, [(sgn * 4, 23, -1), (sgn * 7, 19, -3), (sgn * 8, 15, -5)], [3, 2], blue)
        for dz in (-1, 0.5):
            m.box(body, sgn * 8 - 0.5, 13, -6 + dz, sgn * 8 + 0.5, 15, -5 + dz, claw)

    hd = m.bone("head", body, (0, 25, -1))
    chain(m, hd, [(0, 24, -1), (0, 28, -3)], [4], blue)
    m.box(hd, -3, 28, -9, 3, 33, -2, head)
    m.box(hd, -2, 28, -12, 2, 31, -9, blue)
    # the swept white crest
    for sgn in (1, -1, 0):
        chain(m, hd, [(sgn * 1.5, 32.5, -6), (sgn * 3.5, 36, -2), (sgn * 4.5, 37, 3)], [2, 1.5], crest)

    # the crescent: wing segments sweeping up and round each side, nearly meeting overhead
    for sgn, side in ((1, "left"), (-1, "right")):
        wb = m.bone(f"wing_{side}", body, (sgn * 4, 23, 2))
        segs = 9
        for n in range(segs):
            a0 = math.radians(-70 + n * 18)             # from below the body round to overhead
            cxw, cyw = 20, 26
            px, py = sgn * cxw * math.cos(a0) * 0.85, cyw + 18 * math.sin(a0) * 0.95
            nx, ny = sgn * math.cos(a0), math.sin(a0)
            tilt = math.degrees(a0) * sgn
            m.box(wb, px - 3, py - 4, 3, px + 3, py + 4, 3, wing, rotation=(0, 0, tilt), pivot=(px, py, 3))
            if n % 2 == 0:                               # light-blue spikes on the outer edge
                spike(m, wb, (px + nx * 3, py + ny * 3, 3), (nx, ny, 0), 2, 4, spike_c)
        chain(m, wb, [(sgn * 4, 23, 2), (sgn * 10, 25, 3)], [3], blue)

    # tail, long and tapering
    tl = m.bone("tail", body, (0, 12, 1))
    chain(m, tl, [(0, 12, 1), (0, 8, 4), (0, 4, 6), (0, 1, 10), (0, 0, 15)], [3, 3, 2, 2], blue)
    return m
