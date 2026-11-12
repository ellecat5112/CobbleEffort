"""Blanketula, the Leaf Blanket Pokémon (Bug/Grass), hand-built from boxes from the user's design.

Pipider grown into a fuzzy little spider that has traded its seed for a big green leaf it wears like a safety blanket:
draped over its back and tucked over its head like a hood, with its two front legs clutching the edge. Underneath:
a tan-and-brown fuzzy body, two big orange eyes with four little ones above them, and eight legs.

Front is -z, y is up. 15 units tall; baseScale 0.55 (0.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, mix, rod
from _route import leaf_plane, pal, round_eye, tone

SCALE = 0.55
HITBOX = [0.6, 0.5]
KIND = "quadruped"
K = 5
LOOK = ("a fuzzy little spider with big orange eyes that wears a big green leaf over its back and head like a "
        "safety blanket, clutching its edge with its front legs")

BASE = {"fur": (196, 160, 116), "fur_dark": (132, 100, 70), "leaf": (110, 196, 80), "leaf_dark": (60, 130, 50),
        "iris": (255, 120, 20), "leg": (110, 84, 60)}
SHINY = {"leaf": (240, 150, 50), "leaf_dark": (180, 90, 24), "iris": (90, 210, 255), "fur": (220, 200, 170)}


def fur(x, y, z, face, variant, **k):
    P = pal(BASE, SHINY, variant)
    c = P["fur"] if int((x * 2.3 + y * 1.7 + z * 2.9) * 1.3) % 5 else P["fur_dark"]   # fuzzy flecks
    return tone(c, face), None


def headf(x, y, z, face, variant, **k):
    P = pal(BASE, SHINY, variant)
    if face == "north":
        for sx in (-1, 1):
            e = round_eye(x - sx * 1.35, y - 6.0, 1.2, P["iris"])
            if e:
                return e
            e = round_eye(x - sx * 0.7, y - 8.0, 0.45, P["iris"])
            if e:
                return e
        if abs(x) < 0.8 and abs(y - 4.4) < 0.25:
            return P["fur_dark"], None
    return fur(x, y, z, face, variant)


def legf(x, y, z, face, variant, **k):
    return tone(pal(BASE, SHINY, variant)["leg"], face), None


LEAF = leaf_plane((0, 10), (180,), 21, 8.5, lambda v: pal(BASE, SHINY, v)["leaf"], lambda v: pal(BASE, SHINY, v)["leaf_dark"],
                  axes="xz", serrate=0.08)


def build() -> Model:
    m = Model("blanketula")
    top = m.bone("blanketula", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    m.round_box(bd, 0, 3.5, 4, 4.5, 3, 10, fur, cut=2)                     # abdomen
    m.round_box(bd, 0, -1.5, 3, 2.5, 3, 8, fur, cut=1)                     # body
    hd = m.bone("head", bd, (0, 6, -3))
    m.round_box(hd, 0, -4, 3, 2, 3, 9.5, headf, cut=1)
    # the leaf blanket: hood over the head, falling back over the abdomen
    cape = m.bone("cape", bd, (0, 11, 0))
    m.box(cape, -9, 11.5, -11, 9, 11.5, 0, LEAF, rotation=(28, 0, 0), pivot=(0, 11.5, 0))     # hood over its head
    m.box(cape, -9, 11.5, 0, 9, 11.5, 10, LEAF, rotation=(-32, 0, 0), pivot=(0, 11.5, 0))     # falling down its back
    legs = [("leg_front_left", -2.5, -3), ("leg_front_right", 2.5, -3), ("leg_mid1_left", -2.8, -1),
            ("leg_mid1_right", 2.8, -1), ("leg_mid2_left", -3, 1), ("leg_mid2_right", 3, 1),
            ("leg_back_left", -3, 3), ("leg_back_right", 3, 3)]
    for i, (nm, lx, lz) in enumerate(legs):
        sx = 1 if lx > 0 else -1
        leg = m.bone(nm, top, (lx, 6, lz))
        if i < 2:                                                            # front legs clutch the leaf's edge
            rod(m, leg, (lx, 6, lz), (sx * 4.5, 9, -6), 1, legf)
            rod(m, leg, (sx * 4.5, 9, -6), (sx * 3.5, 11.2, -8.5), 1, legf)
            continue
        knee = (lx + sx * 3.5, 9, lz * 1.6)
        rod(m, leg, (lx, 6, lz), knee, 1, legf)
        rod(m, leg, knee, (lx + sx * 6, 0.2, lz * 2.2), 1, legf)
    return m
