"""Shared builder for Mantaraymon and Mantaraymon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the Armor Digimon manta: a broad violet manta ray with pointed wing-fins, a row of tall dorsal spikes,
pale stripe markings, a golden diamond crest between red eyes and a long whip tail with a crested tip. X-Antibody:
dark navy armour plates with silver edges, gold chevrons, a glowing electric orb under its snout and a cyan tail
blade. Shiny: teal.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, gem, skin, solid
from _route import pal, tone


def make(name, x=False):
    base = {"violet": (100, 80, 180) if not x else (40, 60, 140), "violet_dark": (50, 30, 110) if not x else (14, 20, 70),
            "violet_light": (170, 160, 230) if not x else (120, 150, 220), "white": (240, 240, 250), "gold": (240, 200, 70),
            "eye": (230, 40, 40), "silver": (210, 214, 226), "cyan": (100, 230, 250), "orb": (250, 230, 80),
            "orb_light": (255, 255, 220)}
    shiny = {"violet": (40, 150, 150), "violet_dark": (10, 80, 80), "violet_light": (130, 220, 220)}

    def P(v):
        return pal(base, shiny, v)

    BODY = armour(P, "violet", "violet_dark", light="violet_light", trim="silver", trim_w=0.25) if x else \
        skin(P, "violet", dark="violet_dark", light="violet_light")

    def bodyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "up" and abs(math.sin(xx * 0.5 + z * 0.3)) > 0.95:
            return tone(p["white"], face), None
        return BODY(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        m.round_box(bd, 0, 0, 5.0, 10.0, 8.0, 13.0, bodyf, cut=2)                      # central body
        for side in (1, -1):                                                         # pointed wing-fins
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 10.0, 0))
            for j in range(4):
                x0, x1 = sorted((side * 4.0, side * (24.0 - j * 4.6)))
                m.box(wb, x0, 9.6 + j * 0.2, -8.0 + j * 4.0, x1, 11.0 + j * 0.2, -4.0 + j * 4.0, bodyf,
                      rotation=(0, side * -20, 0), pivot=(side * 4.0, 10.0, 0))
        hd = m.bone("head", bd, (0, 11, -10))
        m.round_box(hd, 0, -11.0, 3.6, 2.0, 8.6, 12.4, bodyf, cut=1)
        m.round_box(hd, 0, -12.9, 1.0, 0.3, 11.0, 12.6, solid(P, "gold"), cut=0)
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.5, sx * 3.8), 10.6, -12.0, max(sx * 3.5, sx * 3.8), 11.4, -10.8, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 3.0, 9.0, -12.0), (sx * 0.3, -0.4, -1), 0.9, 2.6, bodyf, tip=0.8)   # cephalic fins
        for j in range(4):                                                           # dorsal spikes
            spike(m, bd, (0, 13.0, -6.0 + j * 4.0), (0, 1, 0.6), 1.6, 6.0 - j, bodyf, tip=0.8)
        tb = m.bone("tail", bd, (0, 10, 10))
        pts = [(0, 10.0, 10.0), (2.0, 11.0, 18.0), (5.0, 13.0, 26.0), (9.0, 16.0, 30.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 1, bodyf, extend=0.3, t2=1)
        spike(m, tb, pts[-1], (0.6, 0.6, 0.6), 1.4, 3.0, solid(P, "cyan" if x else "gold"), tip=0.8)
        if x:
            m.round_box(hd, 0, -12.6, 1.6, 1.6, 5.0, 8.4, gem(P, "orb", "orb_light"), cut=1)       # electric orb
            for sx in (-1, 1):
                rod(m, bd, (sx * 2.0, 13.4, -2.0), (sx * 6.0, 13.4, 2.0), 1, solid(P, "gold"), extend=0, t2=1)
        return m

    return build
