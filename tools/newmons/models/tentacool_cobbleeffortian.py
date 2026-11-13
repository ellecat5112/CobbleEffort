"""The CobbleEffort Tentacool (Water/Dark), a little deep-sea squid after the art the user shared: a purple mantle with a
spiky tip, dotted with glowing blue ring photophores; a yellow head speckled blue with two big yellow eyes with black
slit pupils; six short yellow arms with blue tips; and two long tentacles ending in hooked ring clubs.

Front is -z, y is up: it hangs mantle-up in the water. 21 units tall; baseScale 0.68 (0.9 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _squid import P, armf, bodyf, eye, mantlef, ring_club, tentacle, tipf

SCALE = 0.68
HITBOX = [1.2, 1.3]
KIND = "floater"
K = 5
HEIGHT = 21
LOOK = ("a little deep-sea squid: a purple mantle with glowing blue ring photophores and a spiky tip, a yellow head "
        "with big slit-pupilled yellow eyes, short yellow arms and two long tentacles with hooked ring clubs")

SPOTS = [(0, 13.6, -2.8, 1.0), (-1.4, 11.4, -2.75, 0.75), (1.5, 15.6, -2.6, 0.7), (2.8, 12.6, 0.4, 0.9),
         (-2.8, 14.2, -0.6, 0.85), (2.6, 15.8, 1.6, 0.6), (-2.7, 11.6, 1.4, 0.7), (0.4, 13.0, 2.8, 0.9),
         (-1.2, 16.6, 2.4, 0.6), (0.6, 18.0, -1.9, 0.55)]


def headf(x, y, z, face, variant, **k):
    for sx in (-1, 1):
        c = eye(face, x, y, z, sx * 1.15, 8.5, -2.4, 1.05, variant)
        if c is not None:
            return c, None
    return bodyf(x, y, z, face, variant)


def build() -> Model:
    m = Model("tentacool_cobbleeffortian")
    top = m.bone("tentacool_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    mant = mantlef(SPOTS)
    m.round_box(bd, 0, 0, 2.8, 2.8, 9.6, 16.6, mant, cut=1.1)                 # the mantle
    m.round_box(bd, 0, 0.1, 2.1, 2.1, 16.2, 18.8, mant, cut=0.8)               # tapering toward its tip
    spike(m, bd, (0, 18.6, 0.1), (0, 1, 0), 1.4, 2.2, mant)                    # the spiky tip
    for sx in (-1, 1):
        spike(m, bd, (sx * 1.2, 18.2, 0.1), (sx * 0.8, 1, 0), 0.8, 1.4, mant)
    hd = m.bone("head", bd, (0, 8, 0))
    m.round_box(hd, 0, 0, 2.5, 2.4, 6.6, 10.0, headf, cut=0.9)                 # the yellow head
    sk = m.bone("skirt", bd, (0, 6.8, 0))
    for i in range(6):                                                         # six short arms
        a = i * 2 * math.pi / 6 + math.pi / 6
        x0, z0 = 1.5 * math.sin(a), 1.5 * math.cos(a)
        rod(m, sk, (x0, 7.0, z0), (x0 * 1.9, 3.8, z0 * 1.9), 1.2, armf(), extend=0.3)
        rod(m, sk, (x0 * 1.9, 4.0, z0 * 1.9), (x0 * 2.1, 2.6, z0 * 2.1), 0.9, tipf(), extend=0.1)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                        # two long tentacles with ring clubs
        tn = m.bone(nm, bd, (sx * 1.0, 7, -0.8))
        tentacle(m, tn, [(sx * 1.0, 7.0, -0.8), (sx * 3.0, 4.6, -2.0), (sx * 4.4, 2.4, -2.6)], 0.9, 0.7, armf())
        ring_club(m, tn, sx * 4.9, 1.3, -2.7, 2.4, bodyf)
    return m
