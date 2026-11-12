"""Jorminous, the World Serpent Pokémon (Water/Ghost), from the Zorneo x Norden region fakemon series (used with the
creators' permission), built from boxes: Jörmungandr crossed with a Viking raid ship.

A huge sea serpent coiled on itself: its neck rises in an S to a head carved like a longship's dragon prow (wooden
snout and plank fin, a yellow eye, jaws open on a purple tongue over a dark blue lower jaw); its body is dark blue on
top with a pale stripe and a brown banded belly; round Viking shields line its coils, oar-like fins hang down from its
sides fraying into ghostly foam, tan spikes stand along its back like masts, and its tail rises behind it trailing a
translucent, glowing sea mist.

Front is -z, y is up. 44 units tall; baseScale 1.55 (4.3 m tall, 7 m long).
"""
from __future__ import annotations

import math

from _boxmodel import Model, chain, rod, spike
from _jorm import P, mist, oar_blade, planks, segmented, shield, solid
from _route import round_eye, tone

SCALE = 1.55
HITBOX = [3.0, 4.2]
KIND = "floater"
K = 3
HEIGHT = 44
LOOK = ("a huge coiled sea serpent with a head carved like a longship's dragon prow, round Viking shields along its "
        "coils, oar fins fraying into ghostly foam, mast-like spikes and a tail trailing glowing sea mist")


def headf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west") and ((z + 14) / 1.6) ** 2 + ((y - 40) / 1.3) ** 2 < 1:
        e = round_eye(z + 14 if face == "west" else -(z + 14), y - 40, 1.5, p["eye"])
        if e:
            return e
    return planks("x")(x, y, z, face, variant)


def build() -> Model:
    m = Model("jorminous")
    top = m.bone("jorminous", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    coil = []                                                                 # the coil: a loop on the ground
    for i in range(13):
        a = i / 12 * 2 * math.pi * 0.95 + math.pi / 2
        coil.append((10 * math.cos(a), 5 + 1.2 * math.sin(i * 0.9), 4 + 9 * math.sin(a)))
    chain(m, bd, coil, [7.5] * (len(coil) - 1), segmented())
    upper = [(6.5 * math.cos(a), 11, 4 + 6 * math.sin(a)) for a in (math.pi * (0.6 + i * 0.15) for i in range(8))]
    chain(m, bd, upper, [6.5] * (len(upper) - 1), segmented())                # a second coil on top
    neck = m.bone("neck", bd, (0, 8, -5))
    chain(m, neck, [coil[0], (0, 14, -7), (0, 22, -5), (0, 29, -7), (0, 35, -9)], [7.5, 7, 6.5, 6], segmented())
    hd = m.bone("head", neck, (0, 36, -9))
    m.box(hd, -4.5, 35.5, -19, 4.5, 43, -6, headf)                            # the carved prow head
    m.box(hd, 0, 38, -7, 0, 47, 3, planks("z"), rotation=(-20, 0, 0), pivot=(0, 40, -6))   # its plank fin
    m.box(hd, -2.2, 35, -16.5, 2.2, 36.2, -9, solid("tongue"))                # purple tongue
    for i in range(5):                                                        # carved teeth
        m.box(hd, -3.2 + i * 1.6 - 0.4, 34.6, -17.2, -3.2 + i * 1.6 + 0.4, 36, -16.4, solid("tan"))
    jaw = m.bone("jaw", hd, (0, 36, -7))
    m.box(jaw, -3, 32, -16, 3, 35, -6, solid("blue_dark"), rotation=(18, 0, 0), pivot=(0, 35, -7))
    for i, j in enumerate((2, 4, 6, 8, 10)):                                  # round shields along the coil
        x, y, z = coil[j]
        a = math.atan2(z - 4, x)
        ox, oz = math.cos(a) * 3.4, math.sin(a) * 3.4
        if abs(ox) >= abs(oz):
            face = "west" if ox > 0 else "east"
            m.box(bd, x + ox - 0.3, y - 2.2, z + oz - 2.2, x + ox + 0.3, y + 2.2, z + oz + 2.2,
                  shield(x + ox, y, z + oz, 2.2, face))
        else:
            face = "south" if oz > 0 else "north"
            m.box(bd, x + ox - 2.2, y - 2.2, z + oz - 0.3, x + ox + 2.2, y + 2.2, z + oz + 0.3,
                  shield(x + ox, y, z + oz, 2.2, face))
    for i, j in enumerate((1, 3, 5, 7, 9, 11)):                               # oar fins hanging from its sides
        x, y, z = coil[j]
        a = math.atan2(z - 4, x)
        dx, dz = math.cos(a), math.sin(a)
        o = m.bone(f"oar_{i}", bd, (x + dx * 3, y, z + dz * 3))
        tip = (x + dx * 12, 2.4, z + dz * 12)
        rod(m, o, (x + dx * 3.5, y, z + dz * 3.5), tip, 1, solid("blue_dark"))
        rod(m, o, (x + dx * 9.5, 3.0, z + dz * 9.5), (x + dx * 14.5, 1.4, z + dz * 14.5), 2.6, oar_blade, t2=0.6)
    for j in (3, 5, 7, 9):                                                    # mast-like spikes on its back
        x, y, z = coil[j]
        spike(m, bd, (x, y + 2.5, z), (0, 1, 0.15), 1.6, 5, solid("tan"), tip=0.8)
    tail = m.bone("tail", bd, coil[-1])
    tail_pts = [coil[-1], (8, 9, 14), (5, 15, 18), (2, 19, 23)]
    chain(m, tail, tail_pts, [5, 4, 3], segmented())
    for (x, y, z) in tail_pts[1:]:
        spike(m, tail, (x, y + 2, z), (0, 1, 0.3), 1.4, 4, solid("tan"), tip=0.7)
    for (cx, cy, cz, r) in ((3, 20, 25, 3), (0, 22, 28, 3.6), (-2, 19, 31, 3)):   # glowing sea mist
        m.box(tail, cx - r, cy - r * 0.6, cz - r, cx + r, cy + r * 0.6, cz + r, mist)
    return m
