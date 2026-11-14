"""CobbleEffortian Gastly (Ghost/Fire), after @tomats_art's art: a red ball with a single horn on top and yellow
spots, one big white cyclops eye, a dark purple mouth with two fangs, wrapped in a cloud of glowing yellow-orange
flame gas that trails off in a curling wisp.

Shiny: a blue ball in pale cyan flame.

Front is -z, y is up. 16 units tall; baseScale 0.6 (0.7 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, spike
from _hellfire import P, flame_shader, gas, red_spotted, solid

SCALE = 0.6
HITBOX = [1.0, 1.0]
KIND = "floater"
K = 5
HEIGHT = 16
LOOK = ("a red ball with one horn and yellow spots, a big white cyclops eye and a fanged purple mouth, in a cloud of "
        "glowing yellow-orange flame gas")


def face(x, y, z, f, variant):
    if f != "north":
        return None
    p = P(variant)
    dx, dy = x, y - 8.6
    if (dx / 2.6) ** 2 + (dy / 1.3) ** 2 < 1 and dy > -0.9 + 0.12 * dx * dx:
        return p["pupil"] if dx * dx + (dy - 0.1) ** 2 < 0.28 else p["white"]        # the cyclops eye
    if abs(y - 6.4) < 0.6 and abs(x) < 2.0 - 0.6 * abs(y - 6.4):
        if abs(abs(x) - 1.2) < 0.3 and y < 6.4:
            return p["fang"]                                                       # fangs
        return p["mouth"]
    return None


def build() -> Model:
    m = Model("gastly_cobbleeffortian")
    top = m.bone("gastly_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    hd = m.bone("head", bd, (0, 8, 0))
    m.round_box(hd, 0, 0, 3.6, 3.4, 4.6, 11.8, red_spotted([(-2.6, 10.4, 0.7), (2.6, 10.4, 0.7), (3.0, 8.0, 0.5)], face),
                cut=1.3)
    spike(m, hd, (0, 11.6, 0), (0, 1, 0.1), 1.6, 2.8, solid("red"), tip=0.7)        # the horn
    for c, r, hot in (((-4.4, 9.0, 1.8), 2.2, False), ((4.2, 7.6, 2.0), 2.0, False), ((0.0, 3.6, 2.2), 2.0, True),
                      ((2.2, 12.8, 2.8), 1.8, False), ((-2.8, 13.0, 2.6), 1.6, True), ((-4.8, 5.2, 1.6), 1.6, False)):
        gas(m, bd, c, r, hot)                                                      # the cloud of flame gas
    tl = m.bone("tail", bd, (3, 12, 3))
    for c, r in (((4.2, 13.4, 3.6), 1.8), ((6.0, 14.6, 4.4), 1.4), ((7.6, 15.0, 5.0), 1.0)):
        gas(m, tl, c, r)                                                           # its curling wisp
    return m
