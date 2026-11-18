"""Shared builder for Gesomon and Gesomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Gesomon: a white squid-beast with a pointed mantle painted with grey tribal marks, a wide fanged maw
with a red tongue, two long muscular arms ending in black hooked claws and a mass of white tentacles beneath, one
clutching a coiled shell. X-Antibody: a squat pale-blue squid with tiger-striped mantle, gold rings in its fin, a
grinning toothy maw and two thick tentacle arms ending in their own snapping mouths. Shiny: pink.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import metal, skin, solid
from _route import pal, tone


def make(name, x=False):
    base = {"white": (240, 242, 250) if not x else (170, 200, 240), "white_dark": (170, 176, 196) if not x else
            (100, 130, 190), "mark": (120, 120, 130) if not x else (30, 40, 80), "black": (30, 28, 34),
            "mouth": (150, 20, 40), "tongue": (220, 60, 70), "tooth": (250, 250, 240), "gold": (240, 200, 60),
            "gold_dark": (160, 120, 20), "shell": (200, 150, 140), "eye": (230, 40, 40)}
    shiny = {"white": (250, 190, 210), "white_dark": (200, 120, 150)}

    def P(v):
        return pal(base, shiny, v)

    SKIN0 = skin(P, "white", dark="white_dark")

    def mantlef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(abs(xx) - (y - box.lo[1]) * 0.25) < 0.3:
            return tone(p["mark"], face), None
        if x and abs(((y + abs(xx) * 0.6) % 2.6) - 1.3) < 0.25 and face == "north":
            return tone(p["mark"], face), None
        return SKIN0(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 14, 0))
        s = 0.8 if x else 1.0
        m.round_box(bd, 0, 0, 6.0 * s, 5.0 * s, 10.0, 22.0, mantlef, cut=2)              # head-body
        for j, r in enumerate((5.4, 4.4, 3.2, 1.8)):                                    # pointed mantle
            m.round_box(bd, 0, 1.0, r * s, r * 0.7 * s, 22.0 + j * 3.4, 25.6 + j * 3.4, mantlef, cut=1)
        for sx in (-1, 1):                                                              # mantle fins
            spike(m, bd, (sx * 3.0 * s, 30.0, 1.0), (sx, 0.3, 0.2), 1.6, 5.0, mantlef, tip=0.9)
            if x:
                for j in range(3):
                    m.round_box(bd, sx * (4.0 + j * 1.2), 1.0, 0.4, 0.4, 30.0, 31.0, metal(P, "gold", dark="gold_dark"),
                                cut=0)
        m.box(bd, -4.0 * s, 10.6, -5.2 * s - 0.4, 4.0 * s, 15.0, -5.0 * s, solid(P, "mouth"))     # fanged maw
        for j in range(7):
            spike(m, bd, (-3.6 * s + j * 1.2 * s, 15.0, -5.2 * s - 0.4), (0, -1, 0), 0.7, 1.6, solid(P, "tooth"))
            spike(m, bd, (-3.6 * s + j * 1.2 * s, 10.6, -5.2 * s - 0.4), (0, 1, 0), 0.7, 1.2, solid(P, "tooth"))
        m.box(bd, -1.0, 10.8, -5.6 * s, 1.0, 12.0, -5.2 * s, solid(P, "tongue"))
        for sx in (-1, 1):
            m.box(bd, min(sx * 2.0, sx * 3.4), 17.0, -5.3 * s, max(sx * 2.0, sx * 3.4), 17.8, -5.0 * s,
                  solid(P, "eye" if x else "black"))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # two long arms
            ab = m.bone(nm, bd, (sx * 5.0, 14.0, -1.0))
            pts = [(sx * 5.0, 14.0, -1.0), (sx * 11.0, 18.0, -3.0), (sx * 15.0, 12.0, -5.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 3 if not x else 4, SKIN0, extend=0.6)
            if x:                                                                          # snapping tentacle mouths
                m.round_box(ab, sx * 16.0, -6.0, 2.6, 2.6, 9.6, 14.4, SKIN0, cut=1)
                m.box(ab, sx * 16.0 - 2.0, 11.4, -8.8, sx * 16.0 + 2.0, 12.6, -8.5, solid(P, "mouth"))
            else:
                for j in range(3):
                    spike(m, ab, (sx * 15.0 + (j - 1) * 0.9, 11.0, -5.0), (sx * 0.4, -1, -0.5), 0.8, 5.0,
                          solid(P, "black"), tip=0.8)
        for i in range(8):                                                                 # tentacles beneath
            ang = 2 * math.pi * i / 8
            p0 = (3.6 * s * math.cos(ang), 10.0, 3.0 * s * math.sin(ang))
            p1 = (6.0 * s * math.cos(ang), 4.0, 5.0 * s * math.sin(ang))
            p2 = (7.0 * s * math.cos(ang + 0.5), 0.6, 6.0 * s * math.sin(ang + 0.5))
            rod(m, bd, p0, p1, 2, SKIN0, extend=0.3)
            rod(m, bd, p1, p2, 1, SKIN0, extend=0.3, t2=2)
        if not x:
            m.round_box(bd, -6.0, -4.0, 1.6, 1.6, 2.0, 5.0, solid(P, "shell"), cut=1)
        return m

    return build
