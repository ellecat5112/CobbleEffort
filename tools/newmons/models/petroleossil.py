"""Petroleossil, the Ancient Tar Pokémon (Rock/Dragon), built from boxes after a design by @aalacer398 (used with
permission) and the user's idea.

Petroleodd grown into a MASSIVE pile of tar and sludge: a wide spreading mound with two angry red eyes glaring out of
it, and rising from it a thick column of tar carrying the huge fossil skull of an ancient tyrant dinosaur, its jaws
gaping full of teeth, two nostril holes along its snout; fossil bones and spines float in the tar all over it, a row
of fossil spikes runs down its back, and drips run off everywhere.

Front is -z, y is up. 44 units tall; baseScale 1.45 (4.0 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _fossil import TAR, TAR_SHINY, bone, fossil, tar
from _route import pal

SCALE = 1.45
HITBOX = [2.6, 3.6]
KIND = "quadruped"
K = 3
HEIGHT = 44
LOOK = ("a massive mound of tar and sludge with angry red eyes, a tar column carrying a huge gaping fossil skull of an "
        "ancient tyrant, fossil bones and spines floating all over it")


def mound(x, y, z, face, variant, **k):
    p = pal(TAR, TAR_SHINY, variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 3.6, y - 7.5
            if (dx / 1.5) ** 2 + (dy / 0.9) ** 2 < 1 and dy < 0.5 - 0.6 * (abs(x) - 3.2) * sx * sx * 0.5:
                return p["red"], p["red"]                               # angry glowing eyes
    return tar(x, y, z, face, variant)


def skullf(x, y, z, face, variant, **k):
    p = pal(TAR, TAR_SHINY, variant)
    if face in ("east", "west") and any(((z - zc) / 1.0) ** 2 + ((y - yc) / 1.0) ** 2 < 1
                                        for zc, yc in ((-11, 36.5), (-15, 35.8), (-6.5, 37.2))):
        return p["hole"], None                                          # eye socket and nostril holes
    return fossil(x, y, z, face, variant)


def toothf(x, y, z, face, variant, **k):
    return pal(TAR, TAR_SHINY, variant)["tooth"], None


def build() -> Model:
    m = Model("petroleossil")
    top = m.bone("petroleossil", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    m.round_box(bd, 0, 1, 14, 13, 0, 6, mound, cut=4)                    # the spreading mound
    m.round_box(bd, 0, 1, 11.5, 11, 5.5, 13, mound, cut=3)
    m.round_box(bd, 0, 1.5, 8, 7.5, 12.5, 17, tar, cut=2)
    for dx, dz in ((-12, -5), (11, 6), (-6, 11), (8, -10), (12, -3), (-11, 7)):
        m.box(bd, dx - 1.5, 0, dz - 1.5, dx + 1.5, 1.2, dz + 1.5, tar)   # drips
    neck = m.bone("neck", bd, (0, 11, 2))
    chain(m, neck, [(0, 10, 2), (0, 18, 0), (0, 25, -2), (0, 31, -5)], [10, 9, 7], tar)   # the tar column
    hd = m.bone("head", neck, (0, 32, -5))
    m.box(hd, -4, 33, -18, 4, 39, -3, skullf)                            # the skull's upper jaw and cranium
    m.box(hd, -3.5, 37.5, -9, 3.5, 40.5, -3, skullf)                     # its brow
    for i in range(6):                                                    # upper teeth
        zt = -16.5 + i * 2.2
        for sx in (-1, 1):
            m.box(hd, sx * 3.4 - 0.5, 31.6, zt - 0.5, sx * 3.4 + 0.5, 33.2, zt + 0.5, toothf)
    jaw = m.bone("jaw", hd, (0, 33, -4))
    m.box(jaw, -3.5, 29, -17, 3.5, 31.5, -4, skullf, rotation=(14, 0, 0), pivot=(0, 31.5, -4))   # gaping lower jaw
    for i in range(5):
        zt = -15.5 + i * 2.3
        for sx in (-1, 1):
            m.box(jaw, sx * 3 - 0.5, 31.2, zt - 0.5, sx * 3 + 0.5, 32.8, zt + 0.5, toothf,
                  rotation=(14, 0, 0), pivot=(0, 31.5, -4))
    for i, (zs, ys) in enumerate(((4, 22), (6, 17), (8, 12))):            # fossil spikes down its back
        spike(m, neck, (0, ys, zs), (0, 0.6, 1), 3, 6 - i, fossil, tip=1.5)
    floating = [((-7, 7, -6), (-11, 13, -8)), ((8, 6, -4), (12, 12, -2)), ((-9, 5, 5), (-13, 9, 9)),
                ((3, 9, 7), (6, 15, 10)), ((-2, 18, 3), (-5, 22, 6))]
    for a, b in floating:                                                 # bones floating in the tar
        rod(m, bd, a, b, 1.6, bone)
        m.box(bd, b[0] - 1.2, b[1] - 1.2, b[2] - 1.2, b[0] + 1.2, b[1] + 1.2, b[2] + 1.2, bone)
    feet = [("leg_front_left", -6, -6), ("leg_front_right", 6, -6), ("leg_back_left", -6, 7), ("leg_back_right", 6, 7)]
    for nm, fx, fz in feet:
        lg = m.bone(nm, top, (fx, 1, fz))
        m.box(lg, fx - 2.5, 0, fz - 2.5, fx + 2.5, 1.5, fz + 2.5, tar)
    return m
