"""Mega Koraidon, hand-built from boxes in Cobblemon's style.

Koraidon (official art: a red bipedal dragon with a black armoured chest ringed by spikes, white "tyre" feathers at its
sides, a red tail with white feather spikes, and a head with a big feather crest (blue, purple and white) and two
long white braided antennae) as a mega: its crest flares into a blazing crown of feathers with glowing orange tips,
the chest armour glows like molten orichalcum, and the white side-feathers spread into wheel-like fans.

Front is -z, y is up. ~46 units tall; baseScale 1.3 (about 3.7 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.3
HITBOX = [2.6, 3.7]
LOOK = ("a red bipedal dragon whose feather crest flares into a blazing crown with glowing orange tips, a black chest "
        "plate glowing like molten orichalcum, white feather fans at its sides, long white antennae and a feathered tail")
KIND = "biped"

BASE = {
    "red": (220, 52, 40), "red_light": (240, 90, 70), "red_dark": (170, 36, 30), "black": (34, 32, 40),
    "glow": (255, 160, 50), "white": (244, 244, 246), "white_dark": (210, 210, 220), "blue": (40, 80, 180),
    "purple": (150, 60, 160), "flame": (255, 196, 70), "eye": (250, 210, 60), "pupil": (40, 20, 10), "claw": (250, 250, 250),
}
SHINY = {"red": (240, 170, 50), "red_light": (255, 200, 90), "red_dark": (200, 130, 30), "glow": (120, 230, 255),
         "blue": (40, 160, 160), "purple": (60, 120, 200), "flame": (160, 240, 255)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def red(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["red_dark"] if face == "down" else (P["red_light"] if face == "up" else P["red"])


def chest(x, y, z, face, variant, r=0, c=0, **k):
    """Black armour with glowing orange seams."""
    P = palette(variant)
    if face == "north" and (int(math.floor(y)) in (21, 25) and abs(x) < 5 or abs(x) < 0.6 and y > 19):
        return P["glow"], P["glow"]
    return P["black"]


def head(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 37 <= y <= 38.6 and -10.5 <= z <= -8:
        return (P["pupil"] if z < -9.6 else P["eye"]), P["eye"]
    if face == "north" and 33.6 <= y <= 34.4:
        return P["black"]                               # the mouth line
    return red(x, y, z, face, variant)


def white(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["white_dark"] if face == "down" else P["white"]


def feather(colour):
    def s(x, y, z, face, variant, r=0, rows=1, **k):
        P = palette(variant)
        if r <= 1:
            return P["flame"], P["flame"]                # glowing tips
        return P[colour]
    return s


def claw(x, y, z, face, variant, **k):
    return palette(variant)["claw"]


def build() -> Model:
    m = Model("koraidon_mega")
    root = m.bone("koraidon_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 20, 0))
    m.box(body, -6, 14, -5, 6, 28, 5, red)
    m.box(body, -6.5, 18, -6, 6.5, 28, -2, chest)            # the chest plate
    for ang in (-60, -30, 0, 30, 60):                     # spikes round the chest
        a = math.radians(ang)
        spike(m, body, (6 * math.sin(a), 27.5, -4 * math.cos(a)), (math.sin(a), 0.5, -math.cos(a) * 0.6), 2, 4, white)
    # white feather fans at its sides, like wheels
    for sgn in (1, -1):
        for n in range(6):
            a = math.radians(n * 60)
            m.box(body, sgn * 7, 20 + 5 * math.sin(a) - 1, 1 + 5 * math.cos(a) - 3, sgn * 7, 20 + 5 * math.sin(a) + 1,
                  1 + 5 * math.cos(a) + 3, white, rotation=(math.degrees(a), 0, 0), pivot=(sgn * 7, 20, 1))
        m.box(body, sgn * 6.5 - (1 if sgn > 0 else 0), 18, -1, sgn * 6.5 + (0 if sgn > 0 else 1), 22, 3, white)

    hd = m.bone("head", body, (0, 28, -2))
    chain(m, hd, [(0, 27, -1), (0, 32, -4)], [5], red)
    m.box(hd, -3.5, 32, -11, 3.5, 40, -4, head)
    m.box(hd, -2.5, 32, -14, 2.5, 36, -11, red)
    # the crown of feathers: blue, purple and white, glowing at the tips
    for n, (ang, col, h) in enumerate(((-50, "blue", 9), (-25, "purple", 12), (0, "white", 14), (25, "purple", 12), (50, "blue", 9))):
        a = math.radians(ang)
        base = (2.5 * math.sin(a), 39.5, -6)
        d = (math.sin(a) * 0.8, 1, 0.35)
        spike(m, hd, base, d, 3, h, feather(col), tip=2)
    for sgn in (1, -1):                                   # long white antennae
        chain(m, hd, [(sgn * 2, 40, -8), (sgn * 6, 46, -4), (sgn * 11, 48, 2), (sgn * 14, 45, 8)], [1, 1, 1], white)

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 6, 26, -1))
        chain(m, arm, [(sgn * 6, 26, -1), (sgn * 9, 21, -3), (sgn * 9, 16, -6)], [3, 3], red)
        for dx in (-1, 0.5):
            m.box(arm, sgn * 9 + dx, 14, -8, sgn * 9 + dx + 1, 16, -6, claw)

    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 5, 15, 0))
        chain(m, leg, [(sgn * 5, 15, 0), (sgn * 6, 8, -2), (sgn * 5, 2, 0)], [5, 4], red)
        m.box(leg, sgn * 5 - 3, 0, -4, sgn * 5 + 3, 2, 2, red)
        for dx in (-2, 0, 2):
            m.box(leg, sgn * 5 + dx - 0.5, 0, -6, sgn * 5 + dx + 0.5, 1, -4, claw)

    tl = m.bone("tail", body, (0, 16, 4))
    chain(m, tl, [(0, 16, 4), (0, 12, 11), (0, 8, 18), (0, 6, 26)], [5, 4, 3], red)
    for z, y in ((9, 15), (15, 11), (21, 8.5)):
        spike(m, tl, (0, y, z), (0, 1, 0.8), 2, 4, white)
    return m
