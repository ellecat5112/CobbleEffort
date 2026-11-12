"""Jormbuoy, the Longship Pokémon (Water), from the Zorneo x Norden region fakemon series (used with the creators'
permission), built from boxes.

A little sea serpent that bobs on the waves like a buoy: a rounded blue body with a pale stripe and a brown belly,
covered by a Viking longship's wooden hull that rises into a curled prow over its head, four round Viking shields
along each side, a big yellow-green eye, tan whiskers drooping from its snout like a beard, four small blue flippers
and a short curling tail.

Front is -z, y is up. 14 units tall; baseScale 0.6 (0.7 m long).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _jorm import P, hide, planks, shield, solid
from _route import round_eye, tone

SCALE = 0.6
HITBOX = [0.6, 0.5]
KIND = "floater"
K = 5
LOOK = ("a little blue sea serpent bobbing like a buoy under a Viking longship's wooden hull with a curled prow, round "
        "shields along its sides, a big yellow-green eye and tan whisker beard")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and ((z + 6.6) / 1.4) ** 2 + ((y - 6.6) / 1.4) ** 2 < 1:
        e = round_eye(z + 6.6 if face == "west" else -(z + 6.6), y - 6.6, 1.4, p["eye"])
        if e:
            return e
    return hide(belly_below=4.6, stripe_at=5.0)(x, y, z, face, variant)


def build() -> Model:
    m = Model("jormbuoy")
    top = m.bone("jormbuoy", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 0.5, 3.5, 6, 3, 9, hide(belly_below=4.6, stripe_at=5.0), cut=2)        # body
    m.round_box(bd, 0, 0.5, 4.2, 6.5, 7.5, 10.5, planks(), cut=2)                               # the wooden hull
    chain(m, bd, [(0, 10, -5.5), (0, 12, -7.5), (0, 13.5, -7.2), (0, 13.6, -5.8)], [2, 1.6, 1.3], planks())   # curled prow
    hd = m.bone("head", bd, (0, 6, -5))
    m.round_box(hd, 0, -7, 3, 2.5, 3.5, 8.5, headf, cut=1)
    for sx in (-0.7, 0.7):                                                                      # whisker beard
        chain(m, hd, [(sx, 4, -9.2), (sx * 1.2, 2.6, -9.6), (sx * 0.8, 1.6, -9.0)], [0.6, 0.6], solid("tan"))
    for sx, face in ((1, "west"), (-1, "east")):                                                # round shields
        for i in range(4):
            cz = -3.2 + i * 2.6
            x = sx * 3.9
            m.box(bd, min(x, x + sx * 0.6), 4.6, cz - 1.1, max(x, x + sx * 0.6), 6.8, cz + 1.1,
                  shield(x, 5.7, cz, 1.1, face))
    for nm, (lx, lz) in (("leg_front_left", (-3, -2.5)), ("leg_front_right", (3, -2.5)),
                         ("leg_back_left", (-3, 3.5)), ("leg_back_right", (3, 3.5))):
        lg = m.bone(nm, bd, (lx, 3.5, lz))
        x0, x1 = sorted((lx, lx * 1.75))
        m.box(lg, x0, 2.6, lz - 1.2, x1, 3.2, lz + 1.2, hide(), rotation=(0, 0, (1 if lx > 0 else -1) * 25),
              pivot=(lx, 3, lz))                                                                # small flat flippers
    tail = m.bone("tail", bd, (0, 6, 6))
    chain(m, tail, [(0, 6, 6), (0, 6.5, 9), (0, 8, 10.5), (0, 9.2, 9.6)], [2, 1.5, 1], hide(stripe_at=6.6))
    return m
