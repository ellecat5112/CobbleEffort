"""Orthodread, the Braces Pokémon (Dark/Steel), hand-built from boxes from the user's design.

Eight teeth set in a horseshoe like a set of dentures (four across the front, two down each side) on a pink denture
plate, every one with its own angry face: slanted red eyes on its steel cap and a red diamond frown. A braces wire runs
round the whole arch through a bracket on every tooth (each tied with a coloured elastic), the corner caps grow into
spikes, and it scuttles on four clawed steel legs, spiked at the knee, with pink root tips for toes.

Front is -z, y is up. 29 units tall with its spikes; baseScale 1.0 (1.8 m).
"""
from __future__ import annotations

from _boxmodel import Model, mix, spike
from _teeth import P, angry_face, enamel, root, steel

SCALE = 1.0
HITBOX = [1.8, 1.9]
HEIGHT = 29
KIND = "quadruped"
K = 4
LOOK = ("eight angry teeth set in a horseshoe like dentures on a pink plate, wearing steel caps, a braces wire and "
        "brackets with coloured elastics, spiked corner caps and four clawed steel legs")

Y0, CAP, TOP = 8, 19, 24                 # tooth bottom, cap bottom, cap top
WIRE = 11.5                              # the braces wire's centre height
# (cx, cz, side the face is on)
TEETH = [(-9, -9, "north"), (-3, -9, "north"), (3, -9, "north"), (9, -9, "north"),
         (-9, -3, "east"), (-9, 3, "east"), (9, -3, "west"), (9, 3, "west")]


def _tooth(cx, cz, side):
    def h_of(x, z):
        return {"north": x - cx, "west": z - cz, "east": cz - z}[side]

    def on_face(x, z, face, depth):
        if face != side:
            return False
        return {"north": z < cz - depth, "west": x > cx + depth, "east": x < cx - depth}[side]

    def crown(x, y, z, face, variant, **k):
        pal = P(variant)
        if on_face(x, z, face, 2.9):
            f = angry_face(h_of(x, z), y, pal, ey=99, my=15.6, mw=2.2, mh=1.4)
            if f:
                return f
        col = enamel(pal, x, y, z, face)
        if CAP - 1 < y:                                   # a gum line just under the cap
            col = pal["gum"]
        elif y < Y0 + 0.6:
            col = mix(col, pal["enamel_dark"], 0.6)
        return col

    def cap(x, y, z, face, variant, **k):
        pal = P(variant)
        if on_face(x, z, face, 3.4):
            h = h_of(x, z)
            f = angry_face(h, y, pal, ey=21.5, my=-99, ex=1.65, a=1.4, b=1.45)
            if f:
                return f
            if abs(abs(h) - 3.0) < 0.3 and abs(y - 23.35) < 0.3:
                return pal["rivet"]
        return steel(pal, x, y, z, face, top_y=TOP)

    return crown, cap


def wire(x, y, z, face, variant, **k):
    pal = P(variant)
    return pal["steel_light"] if face != "down" else pal["steel"]


def bracket(x, y, z, face, variant, box=None, **k):
    pal = P(variant)
    bx, by, bz = (box.lo[i] + box.size[i] / 2 for i in range(3))
    if abs(y - by) < 0.55 and (abs(x - bx) < 0.55 if face in ("north", "south", "up", "down") else abs(z - bz) < 0.55):
        return pal["elastic"]
    if abs(y - by) < 0.25:
        return pal["steel_dark"]                          # the wire's slot
    return steel(pal, x, y, z, face)


def plate(x, y, z, face, variant, **k):
    pal = P(variant)
    col = pal["gum"]
    if face == "up" and abs(z % 2.5 - 1.25) < 0.25 and abs(x) < 4.6:
        col = mix(col, (190, 100, 110), 0.6)              # the plate's ridges
    return col if face != "down" else mix(col, (0, 0, 0), 0.2)


def legf(x, y, z, face, variant, **k):
    pal = P(variant)
    return root(pal, y, 1.0) if y < 2 else steel(pal, x, y, z, face)


def spikef(x, y, z, face, variant, **k):
    pal = P(variant)
    return pal["steel_light"] if y > 26 else steel(pal, x, y, z, face)


def build() -> Model:
    m = Model("orthodread")
    top = m.bone("orthodread", None, (0, 0, 0))
    body = m.bone("body", top, (0, 14, 0))
    for cx, cz, side in TEETH:
        crown, cap = _tooth(cx, cz, side)
        m.round_box(body, cx, cz, 3, 3, Y0, CAP + 0.5, crown, cut=1)
        m.round_box(body, cx, cz, 3.5, 3.5, CAP, TOP, cap, cut=1)
    m.box(body, -6, 14, -6, 6, 21, 6, plate)              # the denture plate inside the arch
    m.box(body, -12.5, WIRE - 0.5, -13, 12.5, WIRE + 0.5, -12, wire)
    for sx in (-1, 1):
        m.box(body, 12 if sx > 0 else -13, WIRE - 0.5, -12.5, 13 if sx > 0 else -12, WIRE + 0.5, 6, wire)
    for cx, cz, side in TEETH:
        if side == "north":
            m.box(body, cx - 1, WIRE - 1, -13.6, cx + 1, WIRE + 1, -12.6, bracket)
        else:
            sx = 1 if side == "west" else -1
            x0 = 12.6 if sx > 0 else -13.6
            m.box(body, x0, WIRE - 1, cz - 1, x0 + 1, WIRE + 1, cz + 1, bracket)
    for sx in (-1, 1):                                     # spiked corner caps
        spike(m, body, (sx * 10.5, 23.5, -10.5), (sx * 0.55, 1, -0.45), 2, 5, spikef, tip=1)
        spike(m, body, (sx * 10.5, 23.5, 4.5), (sx * 0.7, 1, 0.35), 2, 4, spikef, tip=1)
    for nm, (lx, lz) in (("leg_front_left", (-12, -7)), ("leg_front_right", (12, -7)),
                         ("leg_back_left", (-12, 4)), ("leg_back_right", (12, 4))):
        sx = 1 if lx > 0 else -1
        leg = m.bone(nm, top, (lx, 9, lz))
        m.box(leg, lx - 2, 5, lz - 2, lx + 2, 9, lz + 2, legf)
        m.box(leg, lx - 1.5, 2, lz - 1.5, lx + 1.5, 5.5, lz + 1.5, legf)
        m.box(leg, lx - 1, 0, lz - 1, lx + 1, 2, lz + 1, legf)
        spike(m, leg, (lx + sx * 2, 7, lz), (sx, 0.25, 0), 2, 4, spikef, tip=1)
    return m
