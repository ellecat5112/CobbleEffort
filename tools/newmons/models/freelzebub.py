"""Freelzebub, the Frost Devil Pokémon (Ice/Dark; the user's art, artist not named, name kept), Fridgimp evolved at
level 45 in the snow: a tall, lanky blue devil. Two great horns sweep up from its narrow head, a third spike rises
between them; yellow slanted eyes and a fanged grimace; spiked shoulders, a chest marked with a pale V, long thin arms
with icy claws, digitigrade legs with spiked knees and taloned feet, and a long whip tail ending in a spade.

Front is -z, y is up. 48 units tall (to the horn tips); baseScale 0.8 (2.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _route import tone
from _snowimp import P, frosty, horn, icicle, slant_eye, solid

SCALE = 0.8
HITBOX = [1.4, 2.8]
KIND = "biped"
K = 3
HEIGHT = 48
ANIM = {"leg_amp": 16}
LOOK = ("a tall lanky blue devil with two great swept horns, yellow slanted eyes and a fanged grimace, spiked shoulders, "
        "long thin clawed arms, spiked knees, taloned feet and a long spade-tipped tail")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = slant_eye(p, x - sx * 1.6, y - 34.9, 1.5, "yellow", sx, angry=1.0)
            if c is not None:
                return c, None
        if 31.4 < y < 32.8 and abs(x) < 2.0:                          # a fanged grimace
            fang = (abs(x) * 2.2) % 1 < 0.55
            return (p["white"] if fang else p["mouth"]), None
    return frosty()(x, y, z, face, variant)


def chestf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) - (y - 19.5) * 0.45) < 0.45 and y < 27:
        return tone(p["ice_mid"], face), None                          # a pale V on the chest
    return frosty()(x, y, z, face, variant)


def spadef(x, y, z, face, variant, box=None, **k):
    """The tail's spade (a cut-out plane in the yz plane)."""
    p = P(variant)
    cy, cz = box.lo[1] + box.size[1] / 2, box.lo[2] + box.size[2] / 2
    u, v = z - cz, y - cy
    if abs(u) + abs(v) * 1.2 > 2.4 or (v < -0.8 and abs(u) > 0.6):
        return (0, 0, 0, 0), None
    return tone(p["blue_dark"], face), None


def build() -> Model:
    m = Model("freelzebub")
    top = m.bone("freelzebub", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    m.round_box(bd, 0, 0.3, 2.6, 2.0, 16.0, 19.6, frosty(), cut=0.8)              # a thin waist
    m.round_box(bd, 0, 0, 4.8, 3.0, 19.4, 27.0, chestf, cut=1.1)                  # a narrow chest
    for sx in (-1, 1):
        m.round_box(bd, sx * 4.8, 0, 1.8, 2.2, 25.0, 28.0, frosty(), cut=0.8)     # shoulders
        icicle(m, bd, (sx * 5.4, 27.6, 0), (sx * 0.5, 1, 0.2), 1.6, 3.4)          # shoulder spikes
    hd = m.bone("head", bd, (0, 28, 0))
    m.round_box(hd, 0, 0, 1.4, 1.4, 27.6, 30.2, frosty(), cut=0.5)                # a thin neck
    m.round_box(hd, 0, -0.4, 3.3, 2.8, 30.0, 37.4, headf, cut=1.1)                # the narrow head
    m.box(hd, -1.6, 29.4, -2.6, 1.6, 30.6, -0.6, solid("blue_dark"))             # a pointed chin
    for sx in (-1, 1):                                                            # the great horns
        horn(m, hd, [(sx * 2.0, 36.0, 0), (sx * 5.0, 39.0, 0.6), (sx * 7.0, 43.5, 1.0), (sx * 6.6, 48.0, 0.8)],
             (3.0, 2.4, 1.6))
        spike(m, hd, (sx * 2.6, 33.6, -0.2), (sx * 1, 0.4, 0.4), 1.0, 2.6, solid("blue_dark"), tip=0.5)   # ears
    icicle(m, hd, (0, 36.6, -0.6), (0, 1, 0.2), 1.4, 4.0)                        # a spike between the horns
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                          # long thin arms
        a = m.bone(nm, bd, (sx * 5.2, 26.0, 0))
        rod(m, a, (sx * 5.4, 26.0, 0), (sx * 7.0, 19.0, -0.6), 2.4, frosty())
        rod(m, a, (sx * 7.0, 19.0, -0.6), (sx * 7.6, 12.0, -2.0), 2.2, frosty())
        icicle(m, a, (sx * 7.4, 18.8, 0.4), (sx * 0.3, 0, 1), 1.0, 2.2)          # elbow spikes
        for cz in (-0.7, 0.0, 0.7):
            spike(m, a, (sx * 7.6, 12.0, -2.0 + cz), (sx * 0.2, -1, -0.3), 0.7, 2.6, solid("ice"), tip=0.4)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                          # digitigrade legs
        lg = m.bone(nm, top, (sx * 2.2, 16.5, 0))
        rod(m, lg, (sx * 2.2, 16.5, 0), (sx * 3.4, 9.0, -2.4), 3.2, frosty())
        rod(m, lg, (sx * 3.4, 9.0, -2.4), (sx * 3.4, 3.0, 1.4), 2.6, frosty())
        icicle(m, lg, (sx * 3.4, 9.4, -3.2), (0, 0.6, -1), 1.4, 2.6)              # knee spikes
        rod(m, lg, (sx * 3.4, 3.0, 1.4), (sx * 3.4, 1.0, -0.6), 2.2, frosty())
        for cx in (-0.8, 0.8):                                                     # taloned feet
            spike(m, lg, (sx * 3.4 + cx, 0.6, -0.8), (cx * 0.3, -0.2, -1), 1.0, 3.4, solid("ice"), tip=0.5)
    tl = m.bone("tail", bd, (0, 16.5, 1.6))                                       # a long whip tail
    pts = [(0, 16.5, 1.6), (0, 13.0, 6.0), (0, 13.5, 11.0), (0, 17.0, 14.0), (0, 22.0, 14.6)]
    for a, b in zip(pts, pts[1:]):
        rod(m, tl, a, b, 1.6, frosty(), extend=0.4)
    m.box(tl, 0, 21.4, 12.2, 0, 26.6, 17.0, spadef)
    return m
