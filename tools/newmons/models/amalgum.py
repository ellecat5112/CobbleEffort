"""Amalgum, the Filling Pokémon (Dark/Steel), hand-built from boxes from the user's design.

Three molars fused together: two side by side in front and a taller one behind peeking over them, each with its own
sad face. Their cavities have been filled: each crown wears a rounded steel cap whose edge drips down the enamel, and
grey amalgam fillings patch their sides. Pink roots tipped with metal points carry it.

Front is -z, y is up. 28.5 units tall; baseScale 0.62 (1.09 m).
"""
from __future__ import annotations

from _boxmodel import Model, mix
from _teeth import P, amalgam, blush, enamel, root, sad_face, steel, tri

SCALE = 0.62
HITBOX = [1.1, 1.1]
KIND = "quadruped"
K = 4
LOOK = ("three fused molars with sad faces, the two in front and a taller one behind, capped in dripping steel with "
        "grey amalgam fillings, on pink roots tipped with metal points")

# (cx, cz, crown bottom, cap bottom): front left, front right, back
TEETH = [(-6, -2, 6, 16), (6, -2, 6, 16), (0, 5, 8, 25)]


def tooth_of(box):
    """The tooth a box belongs to (the nearest centre to the box's own)."""
    bx, bz = box.lo[0] + box.size[0] / 2, box.lo[2] + box.size[2] / 2
    return min(range(3), key=lambda i: (bx - TEETH[i][0]) ** 2 + (bz - TEETH[i][1]) ** 2)


def crown(x, y, z, face, variant, box=None, **k):
    pal = P(variant)
    i = tooth_of(box)
    cx, cz, y0, cap = TEETH[i]
    front = face == "north" and z < cz - 4.9
    ey, my = (cap - 3.7, cap - 7.0) if i < 2 else (cap - 1.8, cap - 3.9)
    if front:
        f = sad_face(x - cx, y, pal, ey, my, ex=1.95, a=1.15, b=1.5, mw=1.7, mh=0.9) if i < 2 else \
            sad_face(x - cx, y, pal, ey, my, ex=1.9, a=1.0, b=1.2, mw=1.4, mh=0.75)
        if f:
            return f
    if y > cap - 0.9 - 0.9 * tri((x + z) * 0.45):          # the cap's edge drips down the enamel
        return steel(pal, x, y, z, face)
    col = enamel(pal, x, y, z, face, groove=cz)
    if front:
        col = mix(col, pal["blush"], 0.8 * blush(x - cx, y, ey, ex=1.95))
    if face in ("east", "west") and i < 2 and abs(x) > 11.5 and amalgam(pal, x, y, z, x, cap - 5, cz + 1, 1.7, i):
        return pal["steel"] if amalgam(pal, x, y, z, x, cap - 5, cz + 1, 1.3, i) else pal["steel_dark"]
    if i == 2 and face in ("east", "west") and amalgam(pal, x, y, z, x, cap - 6, cz + 1, 1.8, 2.0):
        return pal["steel"]
    if y < y0 + 0.8:
        col = mix(col, pal["gum"], (y0 + 0.8 - y) / 0.8 * 0.6)
    return col


def cap(x, y, z, face, variant, box=None, **k):
    pal = P(variant)
    i = tooth_of(box)
    top = TEETH[i][3] + 3
    if face == "up" and (x - TEETH[i][0] + 2) ** 2 + (z - TEETH[i][1] + 1.5) ** 2 < 2.2:
        return (250, 252, 255) if variant != "shiny" else (255, 244, 200)   # a shine
    return steel(pal, x, y, z, face, top_y=top)


def roots(x, y, z, face, variant, **k):
    pal = P(variant)
    return root(pal, y, 1.0) if y >= 2.6 else steel(pal, x, y, z, face)


def build() -> Model:
    m = Model("amalgum")
    top = m.bone("amalgum", None, (0, 0, 0))
    body = m.bone("body", top, (0, 8, 0))
    for cx, cz, y0, cy in TEETH:
        m.round_box(body, cx, cz, 6, 5, y0, cy + 0.5, crown, cut=2)
        m.round_box(body, cx, cz, 6.5, 5.5, cy, cy + 3, cap, cut=2)
        for sx in (-1, 1):                                   # a cusp on each side of the cap
            m.box(body, cx + sx * 3 - 1.5, cy + 2.5, cz - 1.5, cx + sx * 3 + 1.5, cy + 3.5, cz + 1.5, cap)
    for nm, (lx, lz, y_top) in (("leg_front_left", (-7, -2, 6.5)), ("leg_front_right", (7, -2, 6.5)),
                                ("leg_back_left", (-3, 5, 8.5)), ("leg_back_right", (3, 5, 8.5))):
        leg = m.bone(nm, top, (lx, y_top, lz))
        m.box(leg, lx - 1.5, 2.5, lz - 1.5, lx + 1.5, y_top, lz + 1.5, roots)
        m.box(leg, lx - 1, 0, lz - 1, lx + 1, 3, lz + 1, roots)
    return m
