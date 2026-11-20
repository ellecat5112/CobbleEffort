"""Bristle Horn (Rock), the ancient paradox Shaymin in its Land Forme, built from boxes after sub_arashii's art
(@MadZygardeCore; the art's own name). Its Sky Forme is bristlehorn_sky.py.

A Shaymin like a little armoured hedgehog: a pale lavender-grey body under a domed back of brown bristles, every
bristle tipped red and the brown flecked with gold. A grey horn rises from its white face above its orange eyes, brown
tufts frame its head, and its fluffy pale tail curls up behind.

Shiny: a sandy back with teal tips.

Front is -z, y is up. 13 units tall (to the horn); about 0.8 blocks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _regi import _hash, ellipsoid, lit
from _route import mix, pal, tone

HEIGHT = 13
SCALE = round(0.8 * 16 / HEIGHT, 3)
HITBOX = [0.9, 11 / 16]
KIND = "quadruped"
K = 4
LOOK = ("a little armoured hedgehog Shaymin: a pale lavender body under a domed back of red-tipped brown bristles "
        "flecked with gold, a grey horn on its white face and a fluffy curled tail")

BASE = {"body": (206, 204, 226), "body_dark": (160, 158, 186), "white": (248, 246, 250), "brown": (128, 104, 86),
        "brown_dark": (92, 72, 60), "tip": (226, 70, 60), "gold": (240, 210, 110), "horn": (150, 150, 168),
        "eye": (240, 150, 50), "pupil": (40, 30, 30), "nose": (40, 34, 40)}
SHINY = {"brown": (206, 176, 120), "brown_dark": (160, 130, 84), "tip": (60, 190, 190), "gold": (255, 236, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def solid(key, glow=False):
    def s(x, y, z, face, variant, **k):
        c = P(variant)[key]
        return (c, c) if glow else (tone(c, face), None)
    return s


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    return lit(p["body"], face, y, 6, 4), None


def backf(x, y, z, face, variant, **k):
    """The domed back: brown, flecked with gold diamonds."""
    p = P(variant)
    u = (x * 0.9 + z * 0.5) % 3.4 - 1.7
    v = (z * 0.9 - x * 0.5 + y * 0.3) % 3.0 - 1.5
    if abs(u) + abs(v) < 0.45:
        return p["gold"], None
    return lit(p["brown"], face, y, 9, 4), None


def bristlef(x, y, z, face, variant, box=None, **k):
    """A bristle: brown at its root, red at its tip (rods: z runs back from the root)."""
    p = P(variant)
    d = (box.lo[2] + box.size[2] - z) / max(box.size[2], 0.01)
    return tone(p["tip"] if d > 0.72 else p["brown"], face), None


def facef(x, y, z, face, variant, **k):
    """The white face: orange eyes and a little nose on its front."""
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            r = math.hypot(x - sx * 1.3, y - 7.6)
            if r < 0.4:
                return p["pupil"], None
            if r < 0.8:
                return p["eye"], None
        if abs(x) < 0.4 and abs(y - 6.4) < 0.3:
            return p["nose"], None
    return lit(p["white"], face, y, 7, 3), None


def build() -> Model:
    m = Model("bristlehorn")
    top = m.bone("bristlehorn", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6.0, 1.0))
    ellipsoid(m, bd, 0, 5.6, 1.0, 4.4, 3.6, 5.6, bodyf, step=1)                      # the body
    ellipsoid(m, bd, 0, 8.0, 1.8, 5.0, 3.6, 6.2, backf, step=1)                      # the domed back
    for i in range(22):                                                          # red-tipped bristles
        a = _hash(i, 1) * 2 * math.pi
        e = 0.25 + 0.6 * _hash(i, 2)
        d = (math.cos(a) * math.cos(e) * 0.9, math.sin(e) + 0.25, math.sin(a) * math.cos(e) + 0.35)
        base = (math.cos(a) * 3.6 * math.cos(e), 9.0 + 2.2 * math.sin(e), 1.8 + math.sin(a) * 4.6 * math.cos(e))
        spike(m, bd, base, d, 1.4, 2.8 + 1.4 * _hash(i, 3), bristlef, tip=0.7)
    hd = m.bone("head", bd, (0, 7.0, -4.0))
    ellipsoid(m, hd, 0, 7.2, -5.4, 2.8, 2.6, 2.4, facef, step=1)                     # white face
    spike(m, hd, (0, 9.0, -6.4), (0, 1, -0.45), 1.8, 5.0, solid("horn"), tip=0.8)   # grey horn
    for sx in (-1, 1):                                                           # brown tufts round its head
        spike(m, hd, (sx * 2.4, 8.4, -4.2), (sx * 1, 0.4, 0.4), 1.6, 2.6, bristlef, tip=0.6)
    for nm, sx, z in (("leg_front_left", 1, -2.4), ("leg_front_right", -1, -2.4), ("leg_back_left", 1, 4.4),
                      ("leg_back_right", -1, 4.4)):
        lg = m.bone(nm, top, (sx * 2.6, 3.4, z))
        m.box(lg, sx * 2.6 - 1.0, 0, z - 1.2, sx * 2.6 + 1.0, 3.6, z + 1.0, bodyf)
    tl = m.bone("tail", bd, (0, 7.0, 6.6))                                          # fluffy curled tail
    for c, r in (((0, 7.4, 7.6), 1.8), ((0, 9.6, 8.8), 1.8), ((0, 11.8, 8.2), 1.5)):
        ellipsoid(m, tl, c[0], c[1], c[2], r, r, r, solid("white"), step=1)
    return m
