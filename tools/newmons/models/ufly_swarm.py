"""Ufly's Swarm Form (Bug/Psychic, battle only), after @maumesdex's art: thousands of Uflys as one great flying saucer,
about 10 blocks tall. A deep purple dome dotted with their glowing teal lights, a dark window band, a cluster of lime
backs and wings for its cockpit, a fluffy pale purple rim, and green pod lights round its underside like a UFO's, each
a great teal compound eye. From beneath it a thick stalk of Uflys curves down to an arch planted on the ground, a lime
collar at its crown, and stray Uflys drift all round it.

Front is -z, y is up. 48 units tall; baseScale 3.3 (10 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _route import tone
from _ufly import P, compound_eye, mini_bug, solid, spotted

SCALE = 3.3
HITBOX = [3.0, 2.6]
KIND = "floater"
K = 2
HEIGHT = 48
LOOK = ("a great flying saucer of thousands of Uflys: a purple dome dotted with glowing teal lights, a lime cockpit "
        "of wings, a fluffy rim with green pod lights beneath, and a stalk curving down to an arch on the ground")
CZ = -4.0                                                              # the saucer's centre (it leans forward)


def domef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and 40.2 < y < 41.8 and abs(x) < 7.5:
        return tone(p["foot"], face), None                             # the dark window band
    return spotted("purple_dark" if y > 39 else "purple", 2.6, 0.5)(x, y, z, face, variant)


def rimf(x, y, z, face, variant, **k):
    """The fluffy rim: pale purple with darker scallops round its lower edge."""
    p = P(variant)
    a = math.atan2(x, z - CZ)
    if face not in ("up", "down") and y < 33.6 + 0.9 * abs(math.sin(a * 9)):
        return tone(p["purple"], face), None
    return spotted("purple_light", 2.2, 0.45, salt=3.0)(x, y, z, face, variant)


def podf(cx, cz):
    """A green pod light: a lime cup whose outer and under faces are great teal compound eyes."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face == "down":
            c = compound_eye(p, x - cx, z - cz, 2.4)
            if c is not None:
                return c
        if face in ("north", "south"):
            c = compound_eye(p, x - cx, y - 30.4, 1.8)
            if c is not None:
                return c
        if face in ("east", "west"):
            c = compound_eye(p, z - cz, y - 30.4, 1.8)
            if c is not None:
                return c
        return tone(p["lime"], face), None
    return s


def collarf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "south") and abs((x % 2.6) - 1.3) < 0.45 and y < 16.4:
        return p["teal"], p["teal"]
    return tone(p["lime"], face), None


def build() -> Model:
    m = Model("ufly_swarm")
    top = m.bone("ufly_swarm", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 34, CZ))
    m.round_box(bd, 0, CZ, 12, 12, 30, 33, spotted("purple_dark", 2.6, 0.5), cut=4)   # the underside
    m.round_box(bd, 0, CZ, 17, 17, 32.5, 35.5, rimf, cut=6)                            # the fluffy rim
    m.round_box(bd, 0, CZ, 14, 14, 35, 39, domef, cut=5)                               # the dome
    m.round_box(bd, 0, CZ, 10.5, 10.5, 38.8, 42.5, domef, cut=4)
    m.round_box(bd, 0, CZ, 6.5, 6.5, 42.3, 44.5, domef, cut=2.5)
    for i, a in enumerate((0, 1, 2, 3, 4)):                                             # pod lights underneath
        ang = 2 * math.pi * (a + 0.5) / 5
        cx, cz = 12.5 * math.sin(ang), CZ - 12.5 * math.cos(ang)
        m.box(bd, cx - 2.6, 29, cz - 2.6, cx + 2.6, 32.5, cz + 2.6, podf(cx, cz))
    cap = m.bone("cap", bd, (0, 44, CZ))                                                 # the lime cockpit
    m.round_box(cap, 0, CZ, 4.2, 4.2, 44.2, 46.4, solid("lime"), cut=1.5)
    for (bx, bz) in ((0, CZ - 1.5), (-2.4, CZ + 1.4), (2.4, CZ + 1.4)):
        mini_bug(m, cap, (bx, 45.6, bz), 1.1)

    # the stalk of Uflys curving down from beneath it to an arch planted on the ground
    st = m.bone("stalk", bd, (0, 31, CZ + 6))
    pts = [(0, 31, CZ + 6), (-1, 26, 6), (-2, 21, 11), (-1, 17.5, 15), (0, 16, 17)]
    for a, b in zip(pts, pts[1:]):
        rod(m, st, a, b, 6, spotted("purple", 2.4, 0.45, salt=1.0), extend=1.5, t2=6)
    arch = [(-9, 0, 17), (-9.5, 6, 17), (-8, 11, 17), (-4.5, 14.5, 17), (0, 15.5, 17), (4.5, 14.5, 17), (8, 11, 17),
            (9.5, 6, 17), (9, 0, 17)]
    for a, b in zip(arch, arch[1:]):
        rod(m, st, a, b, 6.5, spotted("purple_dark", 2.4, 0.45, salt=2.0), extend=1.5, t2=6.5)
    m.box(st, -3.4, 13.5, 13.2, 3.4, 18.6, 20.8, collarf)                                # the lime collar
    # stray Uflys drifting all round it
    dr = m.bone("drift", bd, (0, 26, 0))
    for i in range(9):
        ang = 2 * math.pi * i / 9 + 0.4
        r = 21 + 3 * math.sin(i * 2.1)
        mini_bug(m, dr, (r * math.sin(ang), 8 + (i * 4.7) % 34, CZ + r * math.cos(ang)), 1.6)
    return m
