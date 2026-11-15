"""Fluffear, the Earmuff Pokémon (Normal; the user's art, artist not named, name kept): a snow-white bunny in a fluffy
ruff, its tall ears ending in big fluffy puffs like earmuffs, big purple eyes, a pink nose, pale-blue paws and a blue
pom-pom tail.

Front is -z, y is up. 23 units tall (to the ear puffs); baseScale 0.45 (0.65 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _fluff import P, eye, fluff, pompom, solid
from _route import tone

SCALE = 0.45
HITBOX = [0.8, 1.4]
KIND = "biped"
K = 6
HEIGHT = 23
LOOK = ("a snow-white bunny in a fluffy ruff, tall ears ending in fluffy earmuff puffs, big purple eyes, a pink nose, "
        "pale-blue paws and a blue pom-pom tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.5, y - 12.4, 1.15)
            if c is not None:
                return c, None
        if abs(x) < 0.5 and 10.6 < y < 11.3:
            return p["pink"], None                                     # a pink nose
        if abs(y - (10.1 + 0.3 * abs(x))) < 0.22 and abs(x) < 0.9:
            return p["pupil"], None                                    # a little mouth
    return fluff()(x, y, z, face, variant)


def earf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up":
        return tone(p["inner"], face), None                            # the inside, facing forward
    return fluff()(x, y, z, face, variant)


def build() -> Model:
    m = Model("fluffear")
    top = m.bone("fluffear", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0.4, 2.8, 2.6, 2.4, 7.6, fluff(), cut=1.0)                  # a small body
    m.round_box(bd, 0, -0.2, 3.8, 3.4, 6.4, 9.2, fluff(), cut=1.4)                 # the fluffy ruff
    hd = m.bone("head", bd, (0, 9, 0))
    m.round_box(hd, 0, -0.2, 3.4, 3.0, 8.8, 14.8, headf, cut=1.3)
    for sx in (-1, 1):
        m.round_box(hd, sx * 3.0, -0.6, 1.2, 1.4, 9.4, 11.6, fluff(), cut=0.5)     # fluffy cheeks
    for sx, nm in ((1, "ear_left"), (-1, "ear_right")):                          # tall ears with earmuff puffs
        e = m.bone(nm, hd, (sx * 1.4, 14.6, 0.2))
        rod(m, e, (sx * 1.4, 14.4, 0.2), (sx * 2.2, 19.4, 0.4), 1.6, earf, extend=0.3, t2=1.0)
        m.round_box(e, sx * 2.3, 0.4, 1.9, 1.7, 18.8, 22.6, fluff(), cut=0.8)
        pompom(m, e, (sx * 2.3, 20.6, -1.6), 0.9)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        a = m.bone(nm, bd, (sx * 2.4, 6.6, -0.6))
        rod(m, a, (sx * 2.4, 6.6, -0.6), (sx * 3.0, 4.4, -1.8), 1.3, solid("skin"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.6, 2.6, 0))
        m.round_box(lg, sx * 1.6, -0.6, 1.2, 1.8, 0, 2.6, solid("skin"), cut=0.5)
    tl = m.bone("tail", bd, (0, 4, 2.6))
    pompom(m, tl, (0, 4.6, 3.6), 1.6)
    return m
