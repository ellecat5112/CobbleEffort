"""Mantasma, the Phantom Mantis Pokémon (Grass/Ghost), hand-built from boxes from the user's design.

Halfway between a gargantuan kaiju and a cute little praying mantis: a huge round head (still no eyes) that is almost
all mouth, a wide grinning maw of fangs glowing ghostly violet inside, two leafy horn-feelers and a crown of pale
spikes. A heavy thorax carries two pairs of scythe arms, each edged with a translucent, glowing ghost blade, and eight
dark legs ringed with glowing ghostly stripes. Its great striped abdomen is spiked along the top and ends in a fan of
leaves.

Front is -z, y is up. 53 units tall to its feelers; baseScale 1.06 (3.5 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, rod, spike
from _mantis import P, chitin, frond, maw, spectral, spikef, striped, tooth

SCALE = 1.06
HITBOX = [2.6, 3.4]
KIND = "quadruped"
K = 3
HEIGHT = 53
LOOK = ("a gargantuan yet cute eyeless mantis: a huge round head that is mostly a grinning maw of fangs glowing "
        "violet inside, leafy horn-feelers, four scythe arms edged with glowing ghost blades and eight dark legs ringed "
        "with ghostly stripes")


def headf(x, y, z, face, variant, **k):
    pal = P(variant)
    if face == "north" and 40.0 < y < 41.5 and abs(x) < 7:          # a brown band where eyes would be
        return pal["brown"], None
    if face == "north" and 35.0 < y < 38.5 and abs(abs(x) - 5.2) < 1.5:  # round cheeks: the cute half
        return pal["green_light"], None
    return chitin(x, y, z, face, variant)


def abdomen(x, y, z, face, variant, **k):
    pal = P(variant)
    if face != "down" and any(abs(z - c) < 0.9 for c in (7, 11, 15)):
        return pal["pale"], pal["ghost"]
    return chitin(x, y, z, face, variant)


def build() -> Model:
    m = Model("mantasma")
    top = m.bone("mantasma", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, -1, 6, 5, 17, 30, chitin, cut=2)
    tail = m.bone("tail", bd, (0, 20, 3))
    m.round_box(tail, 0, 10, 6, 8, 12, 24, abdomen, cut=3)
    for z in (6, 10.5, 15):
        spike(m, tail, (0, 23.5, z), (0, 1, 0.5), 3, 5, spikef, tip=1)
    m.box(tail, -10, 19, 17, 10, 19, 32, frond((0, 18), (-40, -14, 14, 40), 13.0, 2.6), rotation=(-30, 0, 0), pivot=(0, 19, 18))
    hd = m.bone("head", bd, (0, 30, -2))
    m.round_box(hd, 0, -4, 8.5, 6.5, 33, 45, headf, cut=3)
    m.round_box(hd, 0, -4, 7, 5, 45, 46.5, headf, cut=2)                  # rounding off the top
    m.box(hd, -7, 27, -9.6, 7, 33, 0, maw(glow=True))                     # the glowing maw
    for i in range(7):                                                     # upper fangs, the maw glowing between
        x = -6 + i * 2
        m.box(hd, x - 0.5, 30.6, -10.6, x + 0.5, 33.2, -9.6, tooth)
    for sx in (-1, 1):
        chain(m, hd, [(sx * 3, 46, -5), (sx * 5, 50, -7), (sx * 6.5, 53, -5.5)], [2, 1.5], striped("green", stripes=(), tip=0.7))
        spike(m, hd, (sx * 8, 40, -3), (sx * 1, 0.3, 0), 2, 4, spikef, tip=1)
        spike(m, hd, (sx * 6, 45, 0.5), (sx * 0.6, 0.8, 0.4), 2, 4, spikef, tip=1)
    spike(m, hd, (0, 45.5, 1), (0, 0.7, 0.7), 2, 4, spikef, tip=1)
    jaw = m.bone("jaw", hd, (0, 31, -2))
    m.round_box(jaw, 0, -4.5, 7.5, 5.5, 23, 27.5, chitin, cut=2)
    for i in range(6):                                                     # lower fangs
        x = -5 + i * 2
        m.box(jaw, x - 0.5, 27, -10.3, x + 0.5, 29.6, -9.3, tooth)
    arms = (("arm_left", 1, 28, 1.0), ("arm_right", -1, 28, 1.0), ("claw_left", 1, 23, 0.75), ("claw_right", -1, 23, 0.75))
    for nm, sx, y0, s in arms:                                             # two pairs of scythe arms
        arm = m.bone(nm, bd, (sx * 6, y0, -3))
        elbow = (sx * (6 + 6 * s), y0 - 6 * s, -3 - 6 * s)
        hand = (sx * (6 + 6.5 * s), y0 + 2 * s, -3 - 12 * s)
        rod(m, arm, (sx * 6, y0, -3), elbow, 3 * s, striped("green", stripes=(0.5,)))
        rod(m, arm, elbow, hand, 3.5 * s, striped("green", stripes=(0.3, 0.55, 0.8)))
        rod(m, arm, (elbow[0] - sx * 0.6, elbow[1] + 1, elbow[2] - 1), (hand[0] - sx * 0.6, hand[1] + 1, hand[2] - 1),
            1, spectral)                                                   # the ghost blade along its edge
        rod(m, arm, hand, (hand[0] - sx * 2 * s, hand[1] - 4 * s, hand[2] - 2 * s), 1.5, striped("claw", stripes=()))
    legs = (("leg_front", -4), ("leg_mid1", -0.5), ("leg_mid2", 3), ("leg_back", 6.5))
    for nm, hz in legs:                                                    # eight dark legs with ghostly rings
        for sx, side in ((-1, "left"), (1, "right")):
            hip = (sx * 5, 19, hz)
            leg = m.bone(f"{nm}_{side}", top, hip)
            knee = (sx * 12, 23, hz * 1.6 - 1)
            foot = (sx * 15, 0.5, hz * 2.1 - 1.5)
            rod(m, leg, hip, knee, 3, striped("leg", stripes=(0.5,), width=0.12, glow=True))
            rod(m, leg, knee, foot, 2.5, striped("leg", stripes=(0.3, 0.6), width=0.06, glow=True, tip=0.9))
    return m
