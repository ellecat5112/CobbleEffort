"""Awkwaddle, the Clumsy Pokémon (Ice/Water; the user's art, artist not named, name kept): a chubby penguin chick, navy
with a white belly, its swim goggles too big for its head, a blue swim ring round its middle it never takes off, flapping
little flippers, yellow feet and beads of nervous sweat.

Front is -z, y is up. 17 units tall; baseScale 0.5 (0.5 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod
from _penguin import P, lens, penguin, solid
from _route import tone

SCALE = 0.5
HITBOX = [0.9, 1.05]
KIND = "biped"
K = 6
HEIGHT = 17
LOOK = ("a chubby navy penguin chick with a white belly, oversized swim goggles, a blue swim ring round its middle, "
        "little flippers, yellow feet and nervous sweat drops")


def head_extra(x, y, z, face, p):
    if face == "north":
        for sx in (-1, 1):
            c = lens(p, x - sx * 1.6, y - 12.4, 1.5)
            if c is not None:
                return c, None
        if abs(y - 12.4) < 0.3 and abs(x) < 0.4:
            return p["rim"], None                                      # the goggles' bridge
    if face in ("east", "west", "south") and abs(y - 12.4) < 0.5:
        return tone(p["rim"], face), None                              # the strap round its head
    return None


def ringf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "up" and int((math.atan2(x, z) + math.pi) / (math.pi / 4)) % 2 == 0:
        return tone(p["ring_light"], face), None                       # pale panels on the ring
    return tone(p["ring"], face), None


def build() -> Model:
    m = Model("awkwaddle")
    top = m.bone("awkwaddle", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 2, 0))
    body = penguin((2, 11.5), 3.2, 6.5, 5.5, head_extra)
    for y0, y1, rx, rz, cut in ((1.2, 3.6, 3.8, 3.4, 1.4), (3.4, 10.2, 4.8, 4.2, 1.8), (10.0, 13.8, 4.4, 3.9, 1.6),
                                (13.6, 15.6, 3.4, 3.0, 1.2)):
        m.round_box(bd, 0, 0, rx, rz, y0, y1, body, cut=cut)
    m.box(bd, -0.7, 9.8, -5.6, 0.7, 10.8, -4.0, solid("beak"))                    # a little beak
    for i in range(16):                                                           # the swim ring
        a = 2 * math.pi * i / 16
        cx, cz = 6.0 * math.sin(a), 6.0 * math.cos(a)
        m.box(bd, cx - 1.3, 4.6, cz - 1.25, cx + 1.3, 7.2, cz + 1.25, ringf, rotation=(0, math.degrees(a) + 90, 0),
              pivot=(cx, 5.9, cz))
    for (dx, dy) in ((5.0, 15.0), (4.4, 16.6)):                                   # nervous sweat
        m.box(bd, dx - 0.4, dy - 0.6, -1.4, dx + 0.4, dy + 0.6, -0.8, solid("drop"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                           # flapping little flippers
        a = m.bone(nm, bd, (sx * 4.4, 10.0, 0))
        rod(m, a, (sx * 4.4, 10.0, 0), (sx * 7.4, 12.6, -0.6), 2.6, solid("navy"), extend=0.4, t2=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 1.8, 1.5, 0))
        m.box(lg, sx * 1.8 - 1.4, 0, -3.0, sx * 1.8 + 1.4, 1.2, 0.8, solid("feet"))
    return m
