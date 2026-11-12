"""Sheathalis, the Knife Block Pokémon (Bug/Steel), hand-built from boxes from the user's design.

Shivnymph's cocoon is a wooden knife block: a block of grained wood with a stepped, slanted top full of slots, four
black riveted knife handles (one a chunky cleaver) sticking out of them, and the pupa's teal face with its big orange
eyes and two little fangs peeking out of a hole low in the front, feelers poking up.

Front is -z, y is up. 16 units tall to its handles; baseScale 0.62 (0.6 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _knife import P, body, handle, wood
from _route import round_eye, tone

SCALE = 0.62
HITBOX = [0.6, 0.6]
KIND = "quadruped"
K = 5
HEIGHT = 16
LOOK = ("a wooden knife block with four black riveted handles sticking out of its slanted top and a teal pupa face "
        "with big orange eyes peeking out of the front")


def block(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and any(abs(x - sx) < 0.45 for sx in (-2.4, -0.8, 0.8, 2.4)) and -1.5 < z < 3:
        return p["handle"], None                                    # the slots
    if face == "north" and (x / 2.9) ** 2 + ((y - 4.3) / 2.6) ** 2 < 1:
        return tone(p["brown_dark"], face), None                    # the hole its face peeks out of
    return wood(x, y, z, face, variant)


def facef(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(x - sx * 1.15, y - 4.8, 1.0, p["iris"])
            if e:
                return e
        if 2.6 < y < 3.3 and abs(abs(x) - 0.55) < 0.25:
            return (250, 250, 245), None                            # little fangs
    return body(x, y, z, face, variant)


def build() -> Model:
    m = Model("sheathalis")
    top = m.bone("sheathalis", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.box(bd, -4, 0, -3, 4, 8, 4, block)
    m.box(bd, -4, 8, -1, 4, 10, 4, block)                           # the stepped, slanted top
    m.box(bd, -4, 10, 1.5, 4, 11, 4, block)
    for i, (hx, hz, cleaver) in enumerate(((-2.4, 0.5, False), (-0.8, 1.5, True), (0.8, 0.0, False), (2.4, 2.0, False))):
        y0 = 10 if hz < 1.5 else 11
        t = 1.6 if cleaver else 1.0
        rod(m, bd, (hx, y0 - 0.5, hz), (hx, y0 + 4.5, hz + 1.5), t, handle)
    hd = m.bone("head", bd, (0, 4, -3))
    m.round_box(hd, 0, -3.2, 2.5, 1.2, 2.2, 6.6, facef, cut=1)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 0.9, 6.3, -4.0), (sx * 1.8, 8.6, -4.7), (sx * 2.4, 10.4, -3.9)], [0.6, 0.6],
              lambda *a, **k: (tone(P(k["variant"])["tip"], k["face"]), None))
    return m
