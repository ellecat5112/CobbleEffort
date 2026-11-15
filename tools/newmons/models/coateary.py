"""Coateary, the Fur Coat Pokémon (Normal/Psychic; the user's art, artist not named, name kept), Fluffear evolved at
level 20: a small pale-blue creature with big purple eyes and blue earmuffs, wrapped in an enormous snow-white fur that
rises above its head in two great loops, falls down its side, wraps round its middle and ends in a big blue pom-pom.

Front is -z, y is up. 46 units tall (the loops); baseScale 0.7 (2 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _fluff import P, boa, eye, fluff, pompom, solid
from _route import tone

SCALE = 0.7
HITBOX = [1.8, 2.6]
KIND = "biped"
K = 3
HEIGHT = 46
LOOK = ("a small pale-blue creature with big purple eyes and blue earmuffs, wrapped in an enormous white fur rising in "
        "two great loops over its head, wrapping round its middle and ending in a blue pom-pom")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.5, y - 18.6, 1.2)
            if c is not None:
                return c, None
        if abs(x) < 0.5 and 16.6 < y < 17.3:
            return p["pink"], None
    if y < 16.6 and face == "north" and abs(x) > 1.6:
        return tone(p["white"], face), None                            # fluffy white cheeks
    return tone(p["skin"] if face != "down" else p["skin_dark"], face), None


def build() -> Model:
    m = Model("coateary")
    top = m.bone("coateary", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.4, 3.6, 3.0, 2.0, 14.0, solid("skin"), cut=1.3)          # the small body inside the fur
    hd = m.bone("head", bd, (0, 14, 0))
    m.round_box(hd, 0, 0, 3.4, 3.0, 13.8, 21.4, headf, cut=1.3)
    for sx in (-1, 1):                                                            # blue earmuffs
        m.round_box(hd, sx * 3.9, 0.2, 0.9, 1.8, 16.4, 20.2, solid("blue"), cut=0.6)
        m.round_box(hd, sx * 3.6, 0.2, 0.6, 2.2, 16.0, 20.6, fluff(), cut=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                          # little arms holding the fur
        a = m.bone(nm, bd, (sx * 3.4, 11.0, 0))
        rod(m, a, (sx * 3.4, 11.0, 0), (sx * 2.6, 9.8, -4.6), 1.6, solid("skin"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.2, 3, 0))
        m.round_box(lg, sx * 2.2, -0.6, 1.4, 2.0, 0, 3.0, solid("blue"), cut=0.6)
    # the great fur: two loops above its head, down its right side, round its middle, ending in a pom-pom
    loops = m.bone("mane", bd, (0, 22, 3))
    boa(m, loops, [(0, 21.0, 3.0), (-3, 27, 3), (-7, 33, 3), (-11, 38, 2.5), (-9, 42.5, 2), (-5, 42.5, 2),
                   (-2, 38, 2.5), (0, 33, 3), (2, 38, 2.5), (5, 42.5, 2), (9, 42.5, 2), (11, 38, 2.5), (10, 32, 2),
                   (9, 26, 1)], 6)
    wrap = m.bone("skirt", bd, (0, 12, 0))
    boa(m, wrap, [(9, 26, 1), (9, 20, 0), (7.5, 14, -3), (3, 10.5, -6), (-3, 8.5, -6), (-8, 7, -3), (-10, 5, 2),
                  (-6, 3.6, 7), (0, 3.6, 9), (6, 4, 8), (11, 5, 4)], 6)
    tl = m.bone("tail", bd, (12, 5, 3))
    pompom(m, tl, (13.5, 6.0, 2.0), 3.6)
    return m
