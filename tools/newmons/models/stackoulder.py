"""Stackoulder, the Balance Pokémon (Rock; the user's art, artist not named, name kept), Stackid evolved: one round
grey boulder with big stern eyes, stubby feet and a pebble fist, balancing a tower of flat stones on its head and an
olive pebble on the long flat stone it holds out like a tray.

Front is -z, y is up. 26 units tall; baseScale 0.7 (1.1 m).
"""
from __future__ import annotations

from _boxmodel import Model
from _cairn import P, pebble, stern, stone

SCALE = 0.7
HITBOX = [1.2, 1.6]
KIND = "biped"
K = 4
HEIGHT = 26
LOOK = ("a round grey boulder with big stern eyes and stubby feet, balancing a tower of flat stones on its head and an "
        "olive pebble on the flat stone it holds out like a tray")


def face(x, y, z, f, p):
    if f == "north":
        for sx in (-1, 1):
            c = stern(p, x - sx * 2.5, y - 11.4, 1.5, 1.6, sx)
            if c is not None:
                return c
        if abs(y - (8.6 - 0.08 * x * x)) < 0.28 and abs(x) < 1.4:       # a small frown
            return p["eye"]
    return None


def build() -> Model:
    m = Model("stackoulder")
    top = m.bone("stackoulder", None, (0, 0, 0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.4, 2.5, 0))
        pebble(m, lg, (sx * 3.4, 0, -0.8), 2.2, 2.8, 3.0, stone("grey_dark", seed=sx))
    bd = m.bone("body", top, (0, 2.5, 0))
    for y0, y1, rx, rz, cut in ((2.2, 4.2, 4.8, 4.2, 2.0), (4.0, 6.6, 6.6, 5.8, 2.6), (6.4, 13.6, 7.4, 6.4, 3.0),
                                (13.4, 16.0, 6.6, 5.8, 2.6), (15.8, 17.8, 5.0, 4.4, 2.0)):    # the round boulder
        m.round_box(bd, 0, 0, rx, rz, y0, y1, stone("grey", extra=face), cut=cut)
    a = m.bone("arm_right", bd, (-7, 9, 0))                                              # a pebble fist
    pebble(m, a, (-8.6, 7.4, -0.5), 1.8, 1.7, 3.2, stone("grey", seed=3))
    a = m.bone("arm_left", bd, (7, 10, 0))                                               # the flat tray stone
    m.round_box(a, 11.4, -0.4, 4.6, 3.0, 9.0, 10.8, stone("brown", seed=4), cut=1.2)
    pebble(m, a, (12.6, 10.6, -0.2), 1.6, 1.3, 2.2, stone("olive", seed=5))
    hd = m.bone("head", bd, (0, 17.6, 0))                                                # the tower on its head
    m.round_box(hd, 0.4, 0.2, 6.2, 4.4, 17.4, 19.6, stone("brown", seed=6), cut=1.6)
    pebble(m, hd, (-0.3, 19.5, 0), 4.0, 3.2, 3.4, stone("brown_dark", seed=7))
    pebble(m, hd, (0.3, 22.8, 0.1), 2.6, 2.2, 3.0, stone("grey", seed=8))
    return m
