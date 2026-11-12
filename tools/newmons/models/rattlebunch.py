"""Rattlebunch, the Rat King Pokémon (Grass/Normal), hand-built from boxes from the user's design.

A rat king of radishes: four Raddent bundled together like a bunch of radishes, their leafy tops tied in a knot of
twine at the top so they can never come apart. One faces each way (front, left, right and back, a little higher), each
with its own face, snout, buck tooth and whiskers, and the knotted leaves burst up from the twine like a leafy crown.
They scurry about on the front rats' feet.

Front is -z, y is up. 26 units tall to its leaves; baseScale 0.48 (0.8 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod
from _radish import dark, foot, light, nose, radish, snout, stem, tooth, twine, whisker
from _route import leaf_plane

SCALE = 0.48
HITBOX = [0.8, 0.8]
KIND = "quadruped"
K = 4
HEIGHT = 26
LOOK = ("four radish rats bundled together like a bunch of radishes, their leafy tops knotted in twine into a leafy "
        "crown, a face looking each way")

# (facing, centre x, centre z, bottom y, outward direction (dx, dz))
RATS = [("north", 0, -5, 1, (0, -1)), ("east", -5.5, 0, 1.5, (-1, 0)), ("west", 5.5, 0, 1.5, (1, 0)),
        ("south", 0, 5, 3, (0, 1))]


def face_parts(m, bone, cx, cy, cz, dx, dz):
    """Snout, nose, buck tooth and whiskers on a rat whose face is at (cx, cy, cz) looking along (dx, dz)."""
    px, pz = -dz, dx                                                     # sideways
    tip = (cx + dx * 4.2, cy - 0.8, cz + dz * 4.2)
    rod(m, bone, (cx, cy, cz), tip, 2, snout)
    m.box(bone, tip[0] - 0.6 + dx * 0.4, tip[1] - 0.6, tip[2] - 0.6 + dz * 0.4,
          tip[0] + 0.6 + dx * 0.4, tip[1] + 0.6, tip[2] + 0.6 + dz * 0.4, nose)
    tx, tz = cx + dx * 3.2, cz + dz * 3.2
    m.box(bone, tx - 0.5, cy - 2.2, tz - 0.5, tx + 0.5, cy - 1.2, tz + 0.5, tooth)
    for s in (-1, 1):
        a = (cx + dx * 3.0 + px * s * 0.9, cy - 0.5, cz + dz * 3.0 + pz * s * 0.9)
        b = (a[0] + px * s * 3.2 + dx * 0.3, cy - 0.2, a[2] + pz * s * 3.2 + dz * 0.3)
        rod(m, bone, a, b, 0.3, whisker)


def build() -> Model:
    m = Model("rattlebunch")
    top = m.bone("rattlebunch", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    for facing, cx, cz, y0, (dx, dz) in RATS:
        cy = y0 + 4.5
        shader = radish(facing, cx + dx * 4, cy, cz + dz * 4)
        m.round_box(bd, cx, cz, 4.5, 4.5, y0, y0 + 9, shader, cut=2)
        face_parts(m, bd, cx + dx * 4.3, cy, cz + dz * 4.3, dx, dz)
        for s in (-1, 1):                                                 # little round ears
            ex, ez = cx + (-dz) * s * 2.4 + dx * 2.6, cz + dx * s * 2.4 + dz * 2.6
            m.box(bd, ex - 0.6, y0 + 8.2, ez - 0.6, ex + 0.6, y0 + 10, ez + 0.6, shader)
        rod(m, bd, (cx * 0.8, y0 + 8.5, cz * 0.8), (0, 17, 0), 1.5, stem)   # its stem, up to the knot
    m.round_box(bd, 0, 0, 2, 2, 15.5, 18.5, twine, cut=1)               # the knot of twine
    crown = m.bone("crown", bd, (0, 18, 0))
    m.box(crown, -6, 18, 0, 6, 26, 0, leaf_plane((0, 18), (-40, -14, 14, 40), 8, 1.8, light, dark, axes="xy"))
    m.box(crown, 0, 18, -6, 0, 26, 6, leaf_plane((0, 18), (-40, -14, 14, 40), 8, 1.8, light, dark, axes="zy"))
    for nm, (lx, lz) in (("leg_front_left", (-2.5, -6.5)), ("leg_front_right", (2.5, -6.5)),
                         ("leg_back_left", (-6, 2)), ("leg_back_right", (6, 2))):
        leg = m.bone(nm, top, (lx, 2, lz))
        m.box(leg, lx - 1, 0, lz - 1.5, lx + 1, 2, lz + 1, foot)
    return m
