"""Agumon (Fire; a Digimon of the CobbleEffort: Digital crossover, built after the official art): a little yellow-orange
dinosaur standing upright, a big head with a rounded snout full of small teeth, bright green eyes, stubby arms and
feet with big white claws, and a thick tail.

Front is -z, y is up. 22 units tall; baseScale 0.75 (1 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import P, claw_fan, eye, solid, teeth_row
from _route import tone

SCALE = 0.75
HITBOX = [1.3, 1.4]
KIND = "biped"
K = 5
HEIGHT = 22
LOOK = ("a little yellow-orange dinosaur standing upright: a big head with a rounded snout full of small teeth, bright "
        "green eyes, stubby arms and feet with big white claws, and a thick tail")


def hide(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "down":
        return tone(p["orange_dark"], face), None
    if face == "north" and abs(x) < 2.0 and 8 < y < 15:
        return tone(p["belly"], face), None
    return tone(p["orange"], face), None


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 2.6, y - 20.4, 1.25)
        if c is not None:
            return c, None
    if face == "north" and 19.0 < y < 19.6 and abs(abs(x) - 1.0) < 0.35:
        return p["pupil"], None                                        # nostrils
    return hide(x, y, z, face, variant)


def build() -> Model:
    m = Model("agumon")
    top = m.bone("agumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 1))
    m.round_box(bd, 0, 1.0, 3.4, 3.2, 7.0, 13.0, hide, cut=1.2)
    m.round_box(bd, 0, 0.0, 3.0, 2.8, 12.8, 16.6, hide, cut=1.0)
    hd = m.bone("head", bd, (0, 16.5, -0.5))
    m.round_box(hd, 0, -1.8, 3.4, 3.6, 16.2, 22.2, headf, cut=1.4)
    m.box(hd, -2.6, 17.4, -9.2, 2.6, 20.4, -4.6, headf)                     # the rounded snout
    m.box(hd, -2.1, 20.2, -8.6, 2.1, 20.8, -4.6, headf)
    teeth_row(m, hd, [(sx * 2.3, 17.5, z) for sx in (-1, 1) for z in (-8.4, -6.9, -5.4)], (0, -1, 0), 0.7, 0.8)
    jw = m.bone("jaw", hd, (0, 17.2, -2.5))
    m.box(jw, -2.3, 15.6, -8.4, 2.3, 17.3, -3.0, hide)
    teeth_row(m, jw, [(sx * 2.0, 17.2, z) for sx in (-1, 1) for z in (-7.6, -6.0)], (0, 1, 0), 0.6, 0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 3.0, 14.2, -0.6))
        rod(m, a, (sx * 3.0, 14.2, -0.6), (sx * 4.0, 11.6, -3.6), 2.4, hide, extend=0.5)
        claw_fan(m, a, (sx * 4.0, 11.2, -4.4), (0, -0.35, -1), 3, 0.8, 1.8, 0.75)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 8.0, 1.0))
        m.round_box(lg, sx * 2.6, 1.4, 2.1, 2.5, 2.4, 8.6, hide, cut=0.8)
        m.box(lg, sx * 2.6 - 2.0, 0, -2.6, sx * 2.6 + 2.0, 2.6, 3.0, hide)
        claw_fan(m, lg, (sx * 2.6, 0.8, -2.6), (0, -0.1, -1), 3, 0.9, 1.8, 1.2)
    tl = m.bone("tail", bd, (0, 9.5, 4))
    rod(m, tl, (0, 9.5, 3.6), (0, 6.5, 9.0), 3.6, hide, extend=0.6)
    rod(m, tl, (0, 6.5, 9.0), (0, 4.0, 13.0), 2.4, hide, extend=0.5)
    return m
