"""Croissoar, the Paraglider Pokémon (Normal/Flying), the evolved pig in a blanket: a plump, dough-coloured pig with a
stern little frown and a flat dark-red snout, little red trotters and a curly tail, gliding along under a great
paraglider of layered, golden-baked croissant dough that arches over its back. Its two pale ears, tied at the base
with red bands, stand up like wings and steer.

Front is -z, y is up. 30 units tall to the top of the canopy; baseScale 0.65 (1.3 m).
"""
from __future__ import annotations

import math

from _blanket import P, dough_shade, hooff, layers, snoutf
from _boxmodel import Model, mix, rod
from _route import tone

SCALE = 0.65
HITBOX = [1.2, 1.4]
KIND = "floater"
K = 4
HEIGHT = 30
LOOK = ("a plump dough-coloured pig gliding under a great arched paraglider of layered golden croissant dough, its "
        "pale tied ears standing up like wings")


def bodyf(x, y, z, face, variant, **k):
    p = P(variant)
    if face in ("east", "west"):
        if math.hypot((z + 6.6) / 0.5, (y - 12.4) / 0.6) < 1:
            return p["eye"], None                                         # small dark eye
        if abs(y - 13.4 + 0.35 * (z + 6.6)) < 0.25 and -7.6 < z < -5.6:
            return p["eye"], None                                         # stern little brow
    c = mix(p["pig_tan"], p["pig_tan_dark"], 0.5) if face == "down" else p["pig_tan"]
    if face == "up":
        c = mix(c, (255, 255, 255), 0.12)
    return tone(c, face), None


def canopyf(x, y, z, face, variant, **k):
    """Croissant layers run front to back along the canopy, each a golden ridge."""
    p = P(variant)
    t = layers(x + 12, 4.0)
    return dough_shade(p, t, face), None


def earf(x, y, z, face, variant, **k):
    p = P(variant)
    if y < 15.6:
        return p["tie"], None                                             # red tie at the base
    return tone(p["ear"], face), None


def tailf(x, y, z, face, variant, **k):
    return tone(P(variant)["pig_tan_dark"], face), None


def build() -> Model:
    m = Model("croissoar")
    top = m.bone("croissoar", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    m.round_box(bd, 0, 0, 4.6, 8.5, 6.5, 14.5, bodyf, cut=2)                    # plump pig body
    m.round_box(bd, 0, -5.5, 4.2, 3, 7, 14.2, bodyf, cut=1.5)                    # head end
    m.box(bd, -2.2, 8.2, -9.6, 2.2, 11.6, -8.4, snoutf(0, 9.9, 4.4, 3.4))       # flat dark-red snout
    for lx, lz in ((-2.6, -4.5), (2.6, -4.5), (-2.6, 5), (2.6, 5)):
        m.box(bd, lx - 0.9, 5, lz - 0.9, lx + 0.9, 7, lz + 0.9, hooff)        # little red trotters
    tl = m.bone("tail", bd, (0, 11, 8.4))
    rod(m, tl, (0, 11, 8.4), (0, 12.5, 10), 1, tailf, extend=0.3)               # curly tail
    rod(m, tl, (0, 12.5, 10), (0, 11.5, 11.2), 1, tailf, extend=0.3)
    for nm, sx in (("wing_left", -1), ("wing_right", 1)):                        # pale tied ears, standing like wings
        wg = m.bone(nm, bd, (sx * 2.4, 14, -4.5))
        m.box(wg, sx * 2.4 - 0.5, 14, -5, sx * 2.4 + 0.5, 15.6, -4, earf)      # red tie
        m.box(wg, sx * 2.4, 15.4, -6.5, sx * 2.4, 21, -2.5, earf,
              rotation=(10, 0, sx * -28), pivot=(sx * 2.4, 15.4, -4.5))          # the ear itself (a plane)
    # the croissant paraglider: a continuous arch of layered slabs over the back, the sides curving down
    cp = m.bone("cap", bd, (0, 22, 2))
    R, cy, n = 11.5, 13.5, 7
    for i in range(n):
        th = math.radians(-75 + i * 150 / (n - 1))
        cx, yy = R * math.sin(th), cy + R * math.cos(th)
        w = 2 * R * math.tan(math.radians(150 / (n - 1) / 2)) + 1.2
        m.box(cp, cx - w / 2, yy - 1.6, -5.5, cx + w / 2, yy + 1.6, 8.5, canopyf,
              rotation=(0, 0, math.degrees(th)), pivot=(cx, yy, 1.5))
    m.box(cp, -2.5, cy + R + 1.4, -4.5, 2.5, cy + R + 2.8, 7.5, canopyf)          # a puffed ridge on the crown
    for sx in (-1, 1):
        th = math.radians(60)
        end = (sx * R * math.sin(th) * 0.92, cy + R * math.cos(th) * 0.92, 1)
        rod(m, cp, (sx * 2.4, 15.5, -1), end, 0.6, tailf, extend=0, t2=0.6)       # lines down to the pig
    return m
