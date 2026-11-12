"""Cutlassfly, the Blade Wing Pokémon (Bug/Steel), hand-built from boxes from the user's design.

A huge dragonfly whose four wings are long steel knife blades: a straight spine, a bright bevelled cutting edge that
sweeps up to the point and a darker fuller line, each fixed to its body with a steel bolster. Its body is teal on top
and brown underneath, with huge orange compound eyes, six brown legs dangling as it hovers, and a long segmented
abdomen ending in a small blade.

Front is -z, y is up. Hovers; 20 units tall, a 48-unit wingspan; baseScale 1.0 (1.6 m long).
"""
from __future__ import annotations

from _boxmodel import Model, chain, mix, rod
from _knife import P, blade_plane, body, steel
from _route import round_eye, tone, along

SCALE = 1.0
HITBOX = [1.6, 1.2]
KIND = "floater"
K = 3
HEIGHT = 20
LOOK = ("a huge teal-and-brown dragonfly with huge orange eyes and four long steel knife blades for wings, hovering "
        "with six legs dangling and a blade at the tip of its long tail")


def eye(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("north", "east", "west", "up"):
        h = (x * 1.3 + y * 0.7 + z * 1.1) % 1.0
        c = p["iris"] if h > 0.12 else mix(p["iris"], (120, 40, 10), 0.4)      # compound facets
        if face == "north" and abs(abs(x) - 2.0) < 0.5 and abs(y - 16.6) < 0.5:
            return (255, 255, 255), None
        return c, None
    return tone(mix(p["iris"], (0, 0, 0), 0.3), face), None


def abdomen(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if box is not None and int(along(z, box) * 4) % 2 and face != "down":
        return tone(p["teal_light"], face), None
    return body(x, y, z, face, variant)


def legf(x, y, z, face, variant, **k):
    return tone(P(variant)["brown"], face), None


def build() -> Model:
    m = Model("cutlassfly")
    top = m.bone("cutlassfly", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 15, 0))
    m.round_box(bd, 0, 0.5, 3, 3.5, 12, 18, lambda *a, **k: body(*a, belly=13.5, **k), cut=1)   # thorax
    tail = m.bone("tail", bd, (0, 14.5, 3.5))
    chain(m, tail, [(0, 14.5, 3.5), (0, 14.2, 9), (0, 13.6, 15), (0, 12.8, 21)], [2.5, 2, 1.5], abdomen)
    m.box(tail, 0, 10.5, 20.5, 0, 14.5, 26, blade_plane(13.6, 11.2, 25.8, 20.5, axes="zy"))     # the tail blade
    hd = m.bone("head", bd, (0, 15.5, -3))
    m.round_box(hd, 0, -4, 2.5, 2, 13, 17.5, lambda *a, **k: body(*a, belly=14, **k), cut=1)
    for sx in (-1, 1):                                                        # huge compound eyes
        m.round_box(hd, sx * 2.6, -4.6, 2.2, 2.2, 13.5, 18, eye, cut=1)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        w = m.bone(nm, bd, (sx * 3, 18, 0.5))
        xa, xb = sorted((sx * 3, sx * 25))
        tilt = (0, 0, sx * 16)                                                # wings angled up, blades showing
        m.box(w, xa, 18.6, -2, xb, 18.6, 3, blade_plane(-1.4, 2.6, 25, 3.5, axes="xz", sign=sx),
              rotation=tilt, pivot=(sx * 3, 18.6, 0))                          # fore blade
        xa, xb = sorted((sx * 3, sx * 22))
        m.box(w, xa, 18.4, 3, xb, 18.4, 8, blade_plane(3.4, 7.2, 22, 3.5, axes="xz", sign=sx),
              rotation=tilt, pivot=(sx * 3, 18.4, 5))                          # hind blade
        xa, xb = sorted((sx * 2.5, sx * 4.5))
        m.box(w, xa, 17.8, -1.5, xb, 19.2, 7.5, steel)                        # the bolster holding them
    legs = [("foot_front_left", -1.8, -1), ("foot_front_right", 1.8, -1), ("foot_mid_left", -2, 1),
            ("foot_mid_right", 2, 1), ("foot_back_left", -2, 3), ("foot_back_right", 2, 3)]
    for nm, lx, lz in legs:
        sx = 1 if lx > 0 else -1
        lg = m.bone(nm, bd, (lx, 12.5, lz))
        knee = (lx + sx * 2.5, 10.5, lz - 1.5)
        rod(m, lg, (lx, 12.5, lz), knee, 1, legf)
        rod(m, lg, knee, (lx + sx * 2, 6.5, lz - 2.5), 1, legf)
    return m
