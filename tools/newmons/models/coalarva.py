"""Coalarva, the Coal Grub Pokémon (Fire/Bug), the CobbleEffort starter, hand-built from boxes from the user's design.

A grub of black coal: a round coal head with two big ruby eyes, two stubby feelers and curved pincer mandibles, a coal
thorax on four little legs, and a fat segmented abdomen that burns red-hot, glowing orange with a yellow-hot ring
round every segment (an emissive layer, so it glows in the dark).

Front is -z, y is up. 10 units tall, 27 long; baseScale 0.65 (0.4 m).
"""
from __future__ import annotations

from _boxmodel import Model, chain, spike
from _coal import coal, glowing_segment, ruby

SCALE = 0.65
HITBOX = [0.6, 0.45]
KIND = "quadruped"
K = 4
LOOK = ("a grub of black coal with big ruby eyes, little feelers and curved pincers, and a fat segmented abdomen "
        "burning red-hot with a yellow-hot ring round each segment")

# abdomen segments: (cz, rx, rz, y0, y1)
SEGMENTS = [(3.5, 4.5, 2.5, 1, 9), (8, 4, 2.5, 1.5, 9.5), (12, 3.5, 2, 2.5, 9.5), (15, 2.5, 1.5, 3.5, 8.5)]


def head(x, y, z, face, variant, **k):
    if face == "north":
        for sx in (-1, 1):
            e = ruby(x - sx * 2.1, y - 6.3, 1.45, 1.3, variant)
            if e:
                return e
    return coal(x, y, z, face, variant)


def body(x, y, z, face, variant, **k):
    return coal(x, y, z, face, variant)


def make_abdomen(segments):
    def abdomen(x, y, z, face, variant, box=None, **k):
        cz_box = box.lo[2] + box.size[2] / 2
        cz, rx, rz, y0, y1 = min(segments, key=lambda s: abs(s[0] - cz_box))
        t_y = (y - y0) / (y1 - y0)
        band = max(0.0, 1 - abs(z - cz) / 1.1) if face != "north" and face != "south" else 0.5
        seam = face in ("east", "west", "up") and abs(abs(z - cz) - rz) < 0.35
        return glowing_segment(t_y, band, variant, seam)
    return abdomen


def build() -> Model:
    m = Model("coalarva")
    top = m.bone("coalarva", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    m.round_box(bd, 0, -0.5, 3.5, 2, 1.5, 7.5, body, cut=1)                     # thorax
    hd = m.bone("head", bd, (0, 5, -3))
    m.round_box(hd, 0, -5, 4, 3, 2, 9, head, cut=1)
    for sx in (-1, 1):                                                          # feelers
        spike(m, hd, (sx * 2, 8.5, -5), (sx * 0.45, 1, -0.35), 1, 3, body)
    jaw = m.bone("jaw", hd, (0, 3.5, -7.5))
    for sx in (-1, 1):                                                          # curved pincers
        chain(m, jaw, [(sx * 2.6, 3.4, -7.6), (sx * 3.1, 3.0, -9.8), (sx * 1.3, 3.0, -11.3)], [1.6, 1.2], body)
    tail = m.bone("tail", bd, (0, 5, 1.5))
    ab = make_abdomen(SEGMENTS)
    for cz, rx, rz, y0, y1 in SEGMENTS:
        m.round_box(tail, 0, cz, rx, rz, y0, y1, ab, cut=1)
    for nm, (lx, lz) in (("leg_front_left", (-2.8, -2.2)), ("leg_front_right", (2.8, -2.2)),
                         ("leg_back_left", (-2.8, 0.8)), ("leg_back_right", (2.8, 0.8))):
        leg = m.bone(nm, top, (lx, 2, lz))
        m.box(leg, lx - 0.5, 0, lz - 0.5, lx + 0.5, 2.5, lz + 0.5, body)
    return m
