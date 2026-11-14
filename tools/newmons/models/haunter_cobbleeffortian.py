"""CobbleEffortian Haunter (Ghost/Fire), after @tomats_art's art: a round red head with two curved horns and yellow
spots, one glaring white eye under a scowling brow, a jagged mouth from which a long blue ghost tongue trails like a
tail, red-and-yellow flames flaring from its sides like wings, and two floating red hands with orange claws and
flame cuffs.

Shiny: blue with pale cyan flames and a pink tongue.

Front is -z, y is up. 24 units tall; baseScale 0.75 (1.6 m). A floater.
"""
from __future__ import annotations

from _boxmodel import Model, chain, spike
from _hellfire import P, flame_shader, flames, red_spotted, solid

SCALE = 0.75
HITBOX = [1.4, 1.5]
KIND = "floater"
K = 4
HEIGHT = 24
LOOK = ("a round red head with two curved horns, one glaring eye and a jagged mouth trailing a long blue ghost tongue, "
        "flame wings and two floating clawed hands")


def face(x, y, z, f, variant):
    if f != "north":
        return None
    p = P(variant)
    dx, dy = x, y - 15.4
    if abs(dy - 1.3 - 0.35 * abs(dx)) < 0.35 and abs(dx) < 1.8:
        return p["red_dark"]                                                       # the scowling brow
    if dx * dx / 2.2 + dy * dy / 1.0 < 1:
        return p["pupil"] if dx * dx + dy * dy < 0.3 else p["white"]
    if 12.0 < y < 13.6 and abs(x) < 2.6:
        if y > 12.8 and int((x + 3) * 1.6) % 2 == 0:
            return p["white"]                                                      # jagged teeth
        return p["mouth"]
    return None


def tongue(x, y, z, face, variant, **k):
    c = P(variant)["blue" if y > 6 else "blue_light"]
    return c, None


def build() -> Model:
    m = Model("haunter_cobbleeffortian")
    top = m.bone("haunter_cobbleeffortian", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 14, 0))
    hd = m.bone("head", bd, (0, 15, 0))
    m.round_box(hd, 0, 0, 4.4, 3.8, 11.4, 19.6, red_spotted([(-3.4, 17.4, 0.8), (3.4, 17.4, 0.8), (-2.4, 18.8, 0.5)], face),
                cut=1.5)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 19.0, 0.4), (sx * 0.45, 1, 0.15), 1.8, 5.4, solid("red"), tip=0.9)   # curved horns
    tg = m.bone("tail", bd, (0, 12, -1))
    chain(m, tg, [(0, 12.2, -2.0), (0.6, 9.0, -1.4), (-0.4, 6.0, -0.6), (0.8, 3.0, 0.4), (0.0, 1.0, 1.0)],
          [2.6, 2.2, 1.6, 1.0], tongue)                                           # the long blue ghost tongue
    for sx, side in ((-1, "left"), (1, "right")):
        w = m.bone(f"wing_{side}", bd, (sx * 4, 16, 1))
        flames(m, w, (sx * 4.0, 16.0, 1.0), 3, 8.0, 2.8, spread=0.6, up=(sx * 1.4, 0.7, 0.2))   # flame wings
        ar = m.bone(f"arm_{side}", bd, (sx * 8, 11, -1))
        m.round_box(ar, sx * 8.4, -1.4, 1.8, 1.8, 8.0, 11.8, solid("red"), cut=0.6)  # floating hands
        flames(m, ar, (sx * 8.4, 11.6, -0.6), 2, 2.6, 1.2, spread=0.6, up=(sx * 0.4, 1, 0.4))     # flame cuffs
        for i in range(3):
            spike(m, ar, (sx * (7.4 + i * 1.0), 8.2, -2.8), (0, -0.6, -1), 0.8, 1.8, solid("claw"), tip=0.4)   # claws
    return m
