"""Petroleodd, the Tar Pokémon (Rock), a fossil Pokémon, built from boxes after a design by @aalacer398 (used with
permission) and the user's idea.

A pile of ancient tar brought back to life with the bones of old Pokémon inside it: a lumpy, glossy black blob with
drips round its base, a cream skull worn over the top of its head (a dark eye socket on the side), a long bone stuck
in it at an angle and a smaller one poking out the back, and two sleepy white eyes peeking out of the tar near the
bottom.

Front is -z, y is up. 20 units tall to its bone; baseScale 0.5 (0.6 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod
from _fossil import TAR, TAR_SHINY, bone, tar
from _route import pal

SCALE = 0.5
HITBOX = [1.2, 1.2]
KIND = "quadruped"
K = 5
HEIGHT = 20
LOOK = ("a lumpy pile of glossy black tar with a cream skull over the top of its head, bones stuck in it and two "
        "sleepy white eyes peeking out near the bottom")


def body(x, y, z, face, variant, **k):
    p = pal(TAR, TAR_SHINY, variant)
    if face == "north":
        for sx in (-1, 1):
            dx, dy = x - sx * 1.6, y - 4.3
            if (dx / 1.25) ** 2 + (dy / 0.8) ** 2 < 1:
                if dy > 0.2:                                          # half-closed: a sleepy lid
                    return p["tar_light"], None
                return (p["eye"] if abs(dx + sx * 0.3) > 0.25 else (40, 40, 50)), None
    return tar(x, y, z, face, variant)


def skull(x, y, z, face, variant, **k):
    p = pal(TAR, TAR_SHINY, variant)
    if face == "east" and ((z + 1.8) / 1.1) ** 2 + ((y - 11.4) / 1.2) ** 2 < 1:
        return p["hole"], None                                         # the eye socket
    if face in ("north", "up") and abs(x) < 0.2 and y > 11:
        return p["bone_dark"], None                                    # the skull's seam
    return bone(x, y, z, face, variant)


def build() -> Model:
    m = Model("petroleodd")
    top = m.bone("petroleodd", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, 0, 5.5, 5, 0, 3, body, cut=2)                     # spreading base with drips
    m.round_box(bd, 0, 0, 4.5, 4, 2.5, 7, body, cut=2)
    for dx, dz in ((-5.2, -2.5), (4.8, 1.5), (-1.5, 4.8), (3, -4.6)):
        m.box(bd, dx - 1, 0, dz - 1, dx + 1, 1, dz + 1, tar)
    hd = m.bone("head", bd, (0, 7, 0))
    m.round_box(hd, 0, 0.3, 3.5, 3.2, 6.5, 11, body, cut=1)              # the head lump
    m.round_box(hd, -0.3, -0.2, 3.3, 3.2, 10, 13.5, skull, cut=1)         # the skull over it
    m.box(hd, -2.8, 9, -3.6, 0.4, 10.5, -2.4, skull)                      # its brow, overhanging one side
    chain(m, hd, [(0.8, 12.5, 0.5), (2.6, 16.5, 0.2), (3.8, 19, 0)], [1.2, 1.2], bone)   # the long bone
    for dx, dy in ((-0.7, 0.4), (0.7, -0.4)):                             # its knobbly end
        m.box(hd, 3.8 + dx - 0.8, 19 + dy - 0.8, -0.8, 3.8 + dx + 0.8, 19 + dy + 0.8, 0.8, bone)
    rod(m, hd, (2.5, 9.5, 2), (5.5, 10.5, 3.5), 1, bone)                  # a small bone out the back
    m.box(hd, 5, 9.6, 2.8, 6.4, 11.2, 4.2, bone)
    feet = [("leg_front_left", -3, -3), ("leg_front_right", 3, -3), ("leg_back_left", -3, 3), ("leg_back_right", 3, 3)]
    for nm, fx, fz in feet:
        lg = m.bone(nm, top, (fx, 1, fz))
        m.box(lg, fx - 1.2, 0, fz - 1.2, fx + 1.2, 1.2, fz + 1.2, tar)
    return m
