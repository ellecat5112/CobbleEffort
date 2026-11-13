"""Placofin, the Armour Fish Pokémon (Rock/Water), Minnolith evolved: a long, bullet-headed prehistoric fish in pale
blue armour plates, white underneath, with a brown stripe along each side and over its head, a small round eye in a
pale ring, a row of brown dorsal spikes (the first and the tail's tipped with white), a fan of brown lobed fins over its
tail and little pale legs underneath that it walks along riverbeds on.

Front is -z, y is up. 18 units tall to the top spike, 34 long; baseScale 0.7 (1.4 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, mix, rod, spike
from _minnow import P, fin_tipped, finf, legf, round_eye
from _route import tone

SCALE = 0.7
HITBOX = [1.0, 0.9]
KIND = "quadruped"
K = 4
HEIGHT = 18
LOOK = ("a long bullet-headed prehistoric fish in pale blue armour plates, with brown dorsal spikes, a fan of brown "
        "tail fins and little pale legs underneath")


def armourf(cz=None):
    """Blue armour, white belly, a brown side stripe; dark seams between the plates every 4.5 units."""
    def s(x, y, z, face, variant, **k):
        p = P(variant)
        if face in ("east", "west") and cz is not None:
            e = round_eye(face, z, y, -10.5, 7.2, 0.8, p, ring=True)
            if e:
                return e, None
        if face == "down" or (face in ("east", "west", "north") and y < 4.6 - 0.1 * max(0.0, -z - 6)):
            return tone(p["white"] if face != "down" else p["white_shade"], face), None
        if face in ("east", "west") and abs(y - 7.6 - 0.12 * (z + 4)) < 0.7 and -9 < z < 4:
            return tone(p["fin"], face), None                              # brown side stripe
        if face == "up" and abs(x) < 0.9 and -13 < z < -6:
            return tone(p["fin"], face), None                              # stripe over the head
        if face in ("east", "west", "up") and z > -6 and ((z + 6) % 4.5) < 0.35:
            return p["seam"], None                                         # seams between the armour plates
        c = p["blue_light"] if face == "up" else p["blue"]
        return tone(c, face), None
    return s


def build() -> Model:
    m = Model("placofin")
    top = m.bone("placofin", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    # bullet head and armoured body, tapering to the tail
    hd = m.bone("head", bd, (0, 7, -6))
    m.round_box(hd, 0, -9.5, 4.2, 4.5, 2.5, 10.5, armourf(-10.5), cut=1.8)
    m.round_box(hd, 0, -14.5, 3, 1.8, 3, 8.8, armourf(-10.5), cut=1.2)        # snout
    m.round_box(bd, 0, -1.5, 4.8, 4, 2.2, 11.5, armourf(), cut=1.8)
    m.round_box(bd, 0, 6, 4.4, 3.8, 2.6, 11, armourf(), cut=1.6)
    # dorsal spikes: a big white-tipped one up front, smaller ones down the back
    spike(m, bd, (0, 10.5, -4.5), (0, 1, 0.45), 3.4, 7, fin_tipped(15.5), tip=1.8)
    for z, hgt in ((0.5, 3.6), (4, 3.2), (7.5, 2.8)):
        spike(m, bd, (0, 10.8, z), (0, 1, 0.5), 2.6, hgt, finf, tip=1.4)
    for sx in (-1, 1):                                                         # spikes along the upper sides
        for z in (-1, 4):
            spike(m, bd, (sx * 3.8, 9.6, z), (sx * 0.7, 1, 0.4), 1.8, 2.4, finf, tip=1)
    # the tail and its fan of brown lobed fins
    tl = m.bone("tail", bd, (0, 7, 9.5))
    m.round_box(tl, 0, 11.5, 3, 2.4, 4, 9.5, armourf(), cut=1)
    spike(m, tl, (0, 9, 12), (0, 1, 0.6), 3, 6.5, fin_tipped(14.6), tip=1.6)
    for i, (ang, ln) in enumerate(((-20, 6.5), (12, 7), (42, 6))):
        a = math.radians(ang)
        for sx in (-1, 1):
            base = (sx * 2.6, 7.5, 10 + i * 1.2)
            rod(m, tl, base, (sx * (2.6 + ln * math.cos(a) * 0.8), 7.5 + ln * math.sin(a) * 0.7, 13 + i * 1.4),
                3.4, finf, extend=0.4, t2=1.2)                                  # lobed fins fanning out
    for nm, lx, lz in (("leg_front_left", -2.4, -7), ("leg_front_right", 2.4, -7),
                       ("leg_back_left", -2.4, 2), ("leg_back_right", 2.4, 2)):
        lg = m.bone(nm, top, (lx, 3, lz))
        m.box(lg, lx - 0.8, 0, lz - 1, lx + 0.8, 3.2, lz + 1, legf)          # little pale legs
    return m
