"""Mega Iron Bundle, hand-built from boxes in Cobblemon's style.

Iron Bundle (official art: a future Delibird robot: a white head with a spiky crest and big blue goggle eyes, a yellow
beak, a red round body with a white zigzag collar, red flipper-wings, a glowing blue ring "sack" at its back used as a
jet, yellow feet) as a mega: the ring grows into a great ice cannon glowing blue, the crest grows taller and the
goggles glow.

Front is -z, y is up. ~30 units tall; baseScale 0.9 (about 1.7 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 0.9
HITBOX = [1.4, 1.7]
LOOK = ("a robot Delibird with a tall spiky white crest, glowing blue goggle eyes, a red body with a white zigzag "
        "collar, red flippers and a great glowing blue ice-cannon ring on its back")
KIND = "floater"

BASE = {"white": (246, 246, 250), "white_dark": (210, 214, 224), "red": (220, 50, 46), "red_dark": (170, 34, 34),
        "blue": (80, 190, 240), "blue_dark": (40, 110, 180), "yellow": (250, 210, 60), "black": (40, 40, 50)}
SHINY = {"red": (60, 120, 220), "red_dark": (40, 80, 170), "blue": (255, 150, 200), "blue_dark": (200, 90, 150)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def white(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["white_dark"] if face == "down" else P["white"]


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north":
        for sgn in (1, -1):
            dx, dy = x - sgn * 2.6, y - 21.5
            if dx * dx + dy * dy <= 4.5:
                if dx * dx + dy * dy <= 1.0:
                    return P["black"]
                return P["blue"], P["blue"]
    return white(x, y, z, face, variant)


def bodyf(x, y, z, face, variant, **k):
    """Red body; a white zigzag collar round the top; a glowing blue gem on the front."""
    P = palette(variant)
    zig = 14.5 - abs(((x + z) % 3) - 1.5)
    if face != "down" and y > zig:
        return P["white"]
    if face == "north" and abs(x) <= 1 and 8 <= y <= 10:
        return P["blue"], P["blue"]
    return P["red_dark"] if face == "down" else P["red"]


def red(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["red_dark"] if face == "down" else P["red"]


def ring(x, y, z, face, variant, **k):
    P = palette(variant)
    return (P["blue"] if face in ("north", "south") else P["blue_dark"]), P["blue"]


def yellow(x, y, z, face, variant, **k):
    return palette(variant)["yellow"]


def build() -> Model:
    m = Model("ironbundle_mega")
    root = m.bone("ironbundle_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 10, 0))
    m.round_box(body, 0, 0, 6, 5, 4, 16, bodyf, cut=2)
    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 6, 13, 0))
        m.box(arm, sgn * 6 - (0 if sgn > 0 else 7), 9, -2, sgn * 6 + (7 if sgn > 0 else 0), 14, 2, red,
              rotation=(0, 0, sgn * -25), pivot=(sgn * 6, 13, 0))
    # the ice cannon: a ring of glowing blue segments on its back
    for n in range(10):
        a = 2 * math.pi * n / 10
        py, px = 11 + 6 * math.sin(a), 6 * math.cos(a)
        m.box(body, px - 1.5, py - 1.5, 5, px + 1.5, py + 1.5, 9, ring, rotation=(0, 0, math.degrees(a)), pivot=(px, py, 7))

    hd = m.bone("head", body, (0, 16, 0))
    m.round_box(hd, 0, 0, 5, 4, 16, 26, headf, cut=2)
    m.box(hd, -1.5, 18, -6, 1.5, 20, -4, yellow)             # beak
    for ang, h in ((-50, 6), (-25, 8), (0, 9), (25, 8), (50, 6)):
        a = math.radians(ang)
        spike(m, hd, (4 * math.sin(a), 25.5, 0), (math.sin(a), 1, 0.2), 3, h, white, tip=1)

    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 3, 4, 0))
        m.box(leg, sgn * 3 - 1.5, 0, -4, sgn * 3 + 1.5, 4, 1, yellow)
    return m
