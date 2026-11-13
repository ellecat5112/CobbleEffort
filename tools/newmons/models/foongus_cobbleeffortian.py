"""The CobbleEffort Foongus (Grass/Steel), a little screw mushroom after the art the user shared: a steel dome cap like a
Phillips head screw (a cross slot on top, notched sides, a ring of rivets), a tuft of steely hair under it, a round
white body with swirly eyes and a cheery open mouth, two threaded screw shafts for arms, and little copper feet.

Front is -z, y is up. 12 units tall; baseScale 0.55 (0.45 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _screw import P, capf, copperf, facef, hairf, screw, steelf

SCALE = 0.55
HITBOX = [1.3, 0.9]
KIND = "biped"
K = 6
HEIGHT = 12
LOOK = ("a little screw mushroom: a steel Phillips-head dome cap with rivets, a round white body with swirly eyes and "
        "a cheery mouth, two threaded screw arms and little copper feet")


def build() -> Model:
    m = Model("foongus_cobbleeffortian")
    top = m.bone("foongus_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 2.7, 2.5, 1.0, 7.4, facef(1.05, 5.3, 0.85, 3.8, 0.85, -2.5), cut=1.5)   # round white body
    hd = m.bone("head", bd, (0, 8, 0))
    cap = capf(0, 0, 8.6, 11.6, 0.42)
    m.round_box(hd, 0, 0, 5.0, 5.0, 7.6, 9.6, cap, cut=1.5)                    # the screw head: rim
    m.round_box(hd, 0, 0, 4.0, 4.0, 9.4, 11.6, cap, cut=1.2)                   # a smooth dome
    for i, (x, z) in enumerate(((0.6, 1.8), (-0.8, 1.6), (1.6, 0.9), (-1.7, 0.6), (0, 2.1))):   # steely hair tuft
        spike(m, hd, (x, 7.7, z), (x * 0.3, -0.6, 1), 0.8, 1.6 + (i % 2) * 0.5, hairf)
    for nm, sx in (("arm_left", 1), ("arm_right", -1)):                        # threaded screw arms
        ar = m.bone(nm, bd, (sx * 2.4, 4.6, 0))
        screw(m, ar, (sx * 2.2, 4.6, 0), (sx, 0.12, 0), 5.2, 2.0, pitch=0.9)
    for nm, sx in (("leg_left", 1), ("leg_right", -1)):
        lg = m.bone(nm, top, (sx * 1.0, 1.2, 0))
        rod(m, lg, (sx * 1.0, 1.4, -0.2), (sx * 1.2, 0, -0.9), 0.9, copperf, extend=0.1)   # little copper feet
    return m
