"""Mawntis, the Maw Mantis Pokémon (Grass/Bug), hand-built from boxes from the user's design.

Prayling grown monstrous: still eyeless, but its head has split into a large toothy maw (an upper jaw with a row of
fangs over a hinged lower jaw), long whip feelers and a spiky crest. Its forelegs are big scythe claws striped pale
yellow with spines along the inside and brown hooks at the tips, and it now scuttles on a second set of legs (six in
all). Spikes run down its back to a striped abdomen that ends in a fan of leaves.

Front is -z, y is up. 25.5 units tall to its feelers; baseScale 0.69 (1.1 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _mantis import P, chitin, frond, maw, spikef, striped, tooth

SCALE = 0.69
HITBOX = [1.0, 1.1]
KIND = "quadruped"
K = 4
LOOK = ("a monstrous eyeless mantis with a large toothy maw, whip feelers, a spiky crest, big striped scythe claws "
        "with spines, six legs and a striped abdomen ending in leaves")


def headf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north" and 19.0 < y < 20.0:                           # a brown band where eyes would be
        return pal["brown"], None
    return chitin(x, y, z, face, variant)


def abdomen(x, y, z, face, variant, **k):
    pal = P(variant)
    if face != "down" and any(abs(z - c) < 0.6 for c in (4.5, 7.5, 10.0)):
        return pal["pale"], None
    if 2.5 < z < 3.5:
        return pal["brown"], None
    return chitin(x, y, z, face, variant)


def build() -> Model:
    m = Model("mawntis")
    top = m.bone("mawntis", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, -0.5, 2.5, 2.5, 9, 16, chitin, cut=1)
    spike(m, bd, (0, 15.5, 1), (0, 1, 0.6), 2, 3, spikef, tip=1)
    tail = m.bone("tail", bd, (0, 10, 2))
    m.round_box(tail, 0, 6.5, 3.5, 5, 7, 13, abdomen, cut=2)
    for z in (5, 9):
        spike(m, tail, (0, 12.5, z), (0, 1, 0.5), 2, 3, spikef, tip=1)
    m.box(tail, -6, 10, 10.5, 6, 10, 21, frond((0, 11), (-38, -12, 12, 38), 9.0, 1.8), rotation=(-30, 0, 0), pivot=(0, 10, 11))
    hd = m.bone("head", bd, (0, 16, -1.5))
    m.round_box(hd, 0, -3.5, 4, 3, 17, 21, headf, cut=1)
    m.box(hd, -3.5, 14, -5.9, 3.5, 17, -1.5, maw())                        # inside the mouth
    for x in (-3, -1.5, 0, 1.5, 3):                                        # upper fangs
        m.box(hd, x - 0.5, 15.1, -6.6, x + 0.5, 17.1, -5.6, tooth)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 1.5, 20.8, -3), (sx * 3.5, 23.5, -4.5), (sx * 6, 25, -3), (sx * 8, 24.5, -0.5)], [1, 1, 1],
              striped("green", stripes=()))
        spike(m, hd, (sx * 2.2, 20.6, -1.5), (sx * 0.4, 1, 0.5), 1, 3, spikef)
    jaw = m.bone("jaw", hd, (0, 16.5, -1.5))
    m.box(jaw, -3.5, 11.5, -6.5, 3.5, 13.5, -1.5, chitin)
    for x in (-2.25, -0.75, 0.75, 2.25):                                   # lower fangs
        m.box(jaw, x - 0.5, 13.2, -6.4, x + 0.5, 15.2, -5.4, tooth)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        arm = m.bone(nm, bd, (sx * 3, 15, -2))
        rod(m, arm, (sx * 3, 15, -2), (sx * 6, 11, -5), 2, striped("green", stripes=(0.5,)))
        rod(m, arm, (sx * 6, 11, -5), (sx * 6.5, 17, -9), 3, striped("green", stripes=(0.3, 0.55, 0.8)))
        for f in (0.3, 0.55, 0.8):                                         # spines along the inside of the scythe
            p = (sx * (6 + 0.5 * f - 1.2), 11 + 6 * f, -5 - 4 * f)
            spike(m, arm, p, (-sx * 1, -0.2, -0.3), 1, 2, spikef)
        rod(m, arm, (sx * 6.5, 17, -9), (sx * 5.2, 13.8, -10.5), 1, striped("claw", stripes=()))
    for nm, (hx, hz), (fx, fz) in (("leg_front_left", (-2.3, -1.5), (-8, -4.5)), ("leg_front_right", (2.3, -1.5), (8, -4.5)),
                                   ("leg_mid_left", (-2.5, 1.0), (-9, 2)), ("leg_mid_right", (2.5, 1.0), (9, 2)),
                                   ("leg_back_left", (-2.8, 3.5), (-8, 8)), ("leg_back_right", (2.8, 3.5), (8, 8))):
        leg = m.bone(nm, top, (hx, 10, hz))
        knee = (hx + (fx - hx) * 0.6, 13.5, hz + (fz - hz) * 0.5)
        rod(m, leg, (hx, 10, hz), knee, 1.5, striped("green_dark", stripes=()))
        rod(m, leg, knee, (fx, 0.5, fz), 1.5, striped("green_dark", stripes=(0.5,), tip=0.88))
    return m
