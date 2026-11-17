"""Shared builder for the soft blob babies of the C section (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a glossy rounded blob, wider at the bottom where it spreads into a soft skirt, with big shiny black eyes
and a small smile, plus optional extras: a single swept tuft (Chicomon), two little horns and floppy ears (Chocomon),
or two horns and a long tapering tail (Cocomon).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import mix, skin, solid
from _route import pal, tone


def make(name, base, shiny, tuft=False, horns=False, ears=False, tail=False, tall=1.0):
    def P(v):
        return pal(base, shiny, v)

    SKIN = skin(P, "body", dark="body_dark", light="body_light", var=0.03)

    def bodyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * 3.0, y - 7.2 * tall)
                if d < 1.4:
                    return tone(p["white"] if math.hypot(x - sx * 3.0 + 0.5, y - 7.2 * tall - 0.5) < 0.45
                                else p["eye"], face), None
            if abs(y - 5.0 * tall - 0.12 * x * x) < 0.18 and abs(x) < 1.4:
                return tone(p["eye"], face), None
            if abs(abs(x) - 4.2) < 0.7 and abs(y - 5.6 * tall) < 0.4:
                return tone(mix(p["body"], p["blush"], 0.5), face), None
        return SKIN(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 4, 0))
        for r, y0, y1 in ((8.4, 0.0, 1.6), (7.6, 1.6, 4.0), (6.8, 4.0, 8.0), (6.0, 8.0, 10.4), (4.6, 10.4, 12.0),
                          (2.6, 12.0, 13.0)):
            m.round_box(bd, 0, 0, r, r * 0.84, y0 * tall, y1 * tall, bodyf, cut=max(1, round(r * 0.35)))
        hd = m.bone("head", bd, (0, 12 * tall, 0))
        if tuft:                                                     # one swept tuft
            pts = [(0, 12.0 * tall, 0), (2.0, 16.0 * tall, 1.0), (5.0, 19.0 * tall, 2.0), (8.0, 20.0 * tall, 2.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 3 - j, SKIN, extend=0.4)
        if horns:
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.6, 11.4 * tall, 0), (sx * 0.3, 1, 0), 2.4, 3.6, SKIN, tip=0.4)
        if ears:                                                     # floppy ears
            for sx in (-1, 1):
                m.box(hd, min(sx * 5.0, sx * 11.0), 9.0 * tall, -1.6, max(sx * 5.0, sx * 11.0), 11.0 * tall, 1.6,
                      SKIN, rotation=(0, 0, -sx * 18), pivot=(sx * 5.0, 10.0 * tall, 0))
        if tail:                                                     # long tapering tail
            tl = m.bone("tail", bd, (6, 3, 2))
            pts = [(6.0, 3.0, 2.0), (11.0, 6.0, 3.0), (15.0, 3.0, 4.0), (20.0, 6.0, 4.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tl, p0, p1, 3 - j, SKIN, extend=0.4)
            spike(m, tl, pts[-1], (1, 0.4, 0), 2.0, 2.6, SKIN, tip=0.4)
        return m
    return build
