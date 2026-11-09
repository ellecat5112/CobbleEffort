"""Mega Iron Hands, hand-built from boxes in Cobblemon's style.

Iron Hands (official art: a future Hariyama robot: a big round grey body with a dark navy belly and legs, a small
helmeted head with a visor, and huge hands, grey with glowing yellow fingers) as a mega: its hands become colossal
pistons with glowing yellow knuckles and shoulder pylons, and its body heavier.

Front is -z, y is up. ~34 units tall; baseScale 1.3 (about 2.8 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain

SCALE = 1.3
HITBOX = [2.8, 2.8]
LOOK = ("a round grey robot with a navy belly and legs, a small helmeted head with a glowing visor, shoulder pylons "
        "and colossal piston hands with glowing yellow fingers")
KIND = "biped"

BASE = {"grey": (176, 182, 190), "grey_light": (206, 212, 220), "grey_dark": (130, 136, 148), "navy": (46, 56, 96),
        "yellow": (252, 214, 50), "visor": (120, 220, 255), "black": (40, 40, 50)}
SHINY = {"grey": (190, 170, 150), "grey_light": (220, 200, 180), "grey_dark": (150, 130, 110), "navy": (110, 50, 70),
         "yellow": (120, 240, 160), "visor": (255, 160, 90)}


def palette(variant):
    return BASE if variant != "shiny" else {**BASE, **SHINY}


def grey(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["grey_dark"] if face == "down" else (P["grey_light"] if face == "up" else P["grey"])


def bodyf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face in ("north", "down") and y < 14:
        return P["navy"]
    if face == "north" and abs(x) < 0.6 and y > 14:
        return P["yellow"], P["yellow"]                 # a glowing seam down the chest
    return grey(x, y, z, face, variant)


def headf(x, y, z, face, variant, **k):
    P = palette(variant)
    if face == "north" and 28.5 <= y <= 29.6 and abs(x) <= 2.5:
        return P["visor"], P["visor"]
    return P["navy"] if y > 30.5 else grey(x, y, z, face, variant)


def navy(x, y, z, face, variant, **k):
    return palette(variant)["navy"]


def finger(x, y, z, face, variant, **k):
    P = palette(variant)
    return P["yellow"], P["yellow"]


def build() -> Model:
    m = Model("ironhands_mega")
    root = m.bone("ironhands_mega", None, (0, 0, 0))
    body = m.bone("body", root, (0, 15, 0))
    m.round_box(body, 0, 0, 11, 9, 7, 26, bodyf, cut=4)
    hd = m.bone("head", body, (0, 26, 0))
    m.round_box(hd, 0, -1, 4, 4, 26, 32, headf, cut=1)

    for sgn, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, body, (sgn * 11, 22, 0))
        m.box(arm, sgn * 11 - 3, 22, -3, sgn * 11 + 3, 28, 3, grey)          # shoulder pylon
        chain(m, arm, [(sgn * 12, 22, 0), (sgn * 16, 17, -2), (sgn * 18, 12, -5)], [4, 4], grey)
        # the colossal hand: a block palm and glowing fingers
        m.box(arm, sgn * 18 - 5, 4, -12, sgn * 18 + 5, 13, -2, grey)
        for n, fx in enumerate((-3.5, -1, 1.5, 4)):
            m.box(arm, sgn * 18 + fx - 1, 1, -13, sgn * 18 + fx + 1, 6, -10, finger)

    for sgn, nm in ((1, "leg_front_left"), (-1, "leg_front_right")):
        leg = m.bone(nm, root, (sgn * 5, 8, 0))
        m.box(leg, sgn * 5 - 3, 2, -3, sgn * 5 + 3, 8, 3, navy)
        m.box(leg, sgn * 5 - 3.5, 0, -5, sgn * 5 + 3.5, 2, 3, navy)
    return m
