"""Mega Iron Thorns, hand-built from boxes in Cobblemon's style.

Iron Thorns (official art: a future Tyranitar robot: lime-green armour with teal glass windows, a black belly, a
spiked head crest, spikes on the back and a thick tail, clawed hands and feet) as a mega: a fortress of extra spikes
humming with electricity, glowing teal windows and a taller crest.

Front is -z, y is up. ~40 units tall; baseScale 1.2 (about 3 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, spike

SCALE = 1.2
HITBOX = [2.6, 3.0]
LOOK = ("a lime-green robot Tyranitar with glowing teal windows, a black belly, a tall spiked crest and a fortress "
        "of spikes down its back and tail")
KIND = "biped"

BASE = {"green": (130, 196, 70), "green_light": (164, 222, 100), "green_dark": (90, 150, 50), "teal": (80, 220, 200),
        "black": (40, 44, 48), "claw": (40, 40, 44), "eye": (250, 220, 60)}
SHINY = {"green": (200, 180, 70), "green_light": (230, 210, 110), "green_dark": (160, 140, 50), "teal": (255, 120, 120)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def armour(x, y, z, face, variant, r=0, c=0, rows=1, cols=1, **k):
    """Green armour with glowing teal window panels on the sides."""
    P = palette(variant)
    if face in ("east", "west") and rows >= 7 and cols >= 7 and 2 <= r < rows - 3 and 2 <= c < cols - 2:
        return P["teal"], P["teal"]
    return P["green_dark"] if face == "down" else (P["green_light"] if face == "up" else P["green"])


def torso(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and abs(x) < 5:
        return P["black"]                              # the black belly
    return armour(x, y, z, face, variant, **k)


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("east", "west") and 34 <= y <= 35.5 and -9 <= z <= -7:
        return P["eye"], P["eye"]
    return armour(x, y, z, face, variant, **k)


def green(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["green_dark"] if face == "down" else P["green"]


def claw(x, y, z, face, variant, **k):
    return palette(variant)["claw"]


def build() -> Model:
    m = Model("ironthorns_mega")
    root = m.bone("ironthorns_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 16, 0))
    m.box(body, -8, 9, -6, 8, 28, 7, torso)
    for z, y in ((-2, 28), (3, 27), (7, 24)):            # back spikes
        for sgn in (1, -1, 0):
            spike(m, body, (sgn * 4, y - 0.5, z), (sgn * 0.5, 1, 0.7), 3, 7 if sgn == 0 else 5, green, tip=1)
    hd = m.bone("head", body, (0, 28, -2))
    m.box(hd, -4, 28, -11, 4, 37, -2, headf)
    m.box(hd, -3, 27, -14, 3, 32, -11, green)
    for ang, h in ((0, 9), (-35, 6), (35, 6)):
        a = math.radians(ang)
        spike(m, hd, (3 * math.sin(a), 36.5, -6), (math.sin(a) * 0.5, 1, 0.5), 3, h, green, tip=1)

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 8, 24, -2))
        chain(m, arm, [(sgn * 8, 24, -2), (sgn * 11, 19, -4), (sgn * 11, 14, -7)], [4, 4], armour)
        spike(m, arm, (sgn * 11, 22, -3), (sgn, 0.5, 0.2), 2, 4, green)
        for dx in (-1.5, 0.5):
            m.box(arm, sgn * 11 + dx, 11, -9, sgn * 11 + dx + 1, 13, -7, claw)

    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 5, 10, 0))
        m.box(leg, sgn * 5 - 3.5, 2, -3.5, sgn * 5 + 3.5, 10, 3.5, armour)
        m.box(leg, sgn * 5 - 4, 0, -6, sgn * 5 + 4, 2, 4, green)
        for dx in (-2.5, -0.5, 1.5):
            m.box(leg, sgn * 5 + dx, 0, -8, sgn * 5 + dx + 1, 1.5, -6, claw)

    tl = m.bone("tail", body, (0, 12, 6))
    chain(m, tl, [(0, 12, 6), (0, 9, 13), (0, 6, 20), (0, 4, 26)], [7, 5, 3], armour)
    for z, y in ((11, 13.5), (17, 10), (23, 7)):
        spike(m, tl, (0, y, z), (0, 1, 0.6), 3, 5, green, tip=1)
    return m
