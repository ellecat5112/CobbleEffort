"""Shared builder for Ogudomon and Ogudomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the avatar of the Seven Great Demon Lords' sins: a towering black body hunched on four enormous long
legs striped violet and ending in red hooked claws, a ring of red eyes and a fanged maw on its chest, a small
crowned green-and-violet head on top, red spikes on its shoulders and the Demon Lords' emblems floating round it.
The X-Antibody ("x"): a crystalline horror of crimson-black thorns, its legs splitting into fractal barbs, wreathed in
pink light.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import armour, metal, skin, solid
from _route import pal, tone

BASE = {"black": (34, 32, 40), "black_dark": (10, 10, 14), "violet": (120, 70, 160), "red": (210, 40, 40),
        "red_dark": (120, 14, 14), "green": (90, 170, 60), "eye": (240, 40, 60), "mouth": (100, 10, 30),
        "tooth": (250, 250, 240), "pink": (250, 120, 200, 170), "crimson": (190, 30, 70), "emblem": (240, 220, 160)}
SHINY = {"black": (210, 210, 220), "black_dark": (140, 140, 150), "violet": (60, 140, 200), "crimson": (60, 90, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    BODY = armour(P, "black", "black_dark", trim="crimson" if x else "violet", trim_w=0.3)

    def legf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and face != "down" and (y * 0.6) % 3.0 < 1.0:
            return tone(p["violet"], face), None
        return BODY(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 40, 0))
        m.round_box(bd, 0, 0, 9.0, 7.0, 36.0, 56.0, BODY, cut=2)                        # towering body
        for i in range(6):                                                             # ring of red eyes
            ang = math.radians(-75 + i * 30)
            m.box(bd, 5.0 * math.sin(ang) - 0.6, 49.0 + 2.0 * math.cos(ang) - 0.6, -7.3, 5.0 * math.sin(ang) + 0.6,
                  49.0 + 2.0 * math.cos(ang) + 0.6, -7.1, solid(P, "eye", glow=True))
        m.box(bd, -4.0, 40.0, -7.2, 4.0, 44.0, -7.0, solid(P, "mouth"))                 # chest maw
        for j in range(6):
            spike(m, bd, (-3.4 + j * 1.36, 44.0, -7.2), (0, -1, -0.2), 0.9, 2.0, solid(P, "tooth"), tip=0.8)
        hd = m.bone("head", bd, (0, 56, 0))
        m.round_box(hd, 0, -1.0, 2.6, 2.6, 56.0, 61.0, skin(P, "green", dark="black"), cut=1)
        for i in range(5):                                                             # violet crown
            spike(m, hd, ((i - 2) * 1.0, 61.0, -1.0), ((i - 2) * 0.3, 1, 0), 1.0, 3.0, solid(P, "violet"), tip=0.8)
        for sx in (-1, 1):                                                             # red shoulder spikes
            spike(m, bd, (sx * 8.0, 55.0, 0), (sx * 0.8, 0.8, 0), 2.0, 7.0, solid(P, "crimson" if x else "red"), tip=0.8)
        for i, (sx, sz) in enumerate(((1, -1), (-1, -1), (1, 1), (-1, 1))):            # four enormous legs
            lb = m.bone("leg_%d" % i, bd, (sx * 7.0, 44.0, sz * 4.0))
            knee = (sx * 18.0, 50.0, sz * 10.0)
            foot = (sx * 22.0, 4.0, sz * 14.0)
            rod(m, lb, (sx * 7.0, 44.0, sz * 4.0), knee, 4, legf, extend=0.6)
            rod(m, lb, knee, foot, 3, legf, extend=0.6)
            for f in range(3):
                spike(m, lb, foot, (sx * 0.5 + (f - 1) * 0.4, -0.6, sz * 0.5), 1.4, 6.0,
                      solid(P, "crimson" if x else "red"), tip=0.8)
            if x:                                                                       # fractal barbs
                for j in range(3):
                    q = tuple(knee[t] + (foot[t] - knee[t]) * (0.25 + j * 0.25) for t in range(3))
                    spike(m, lb, q, (sx * 1, 0.3, sz * 0.3), 1.0, 5.0, solid(P, "crimson"), tip=0.8)
        for i in range(7):                                                             # floating emblems / light
            ang = 2 * math.pi * i / 7
            c = (16.0 * math.cos(ang), 64.0 + 3.0 * math.sin(ang * 2), 6.0 * math.sin(ang))
            if x:
                ball(m, bd, c, 2.2, solid(P, "pink", glow=True), layers=2)
            else:
                m.round_box(bd, c[0], c[2], 1.6, 1.6, c[1] - 1.6, c[1] + 1.6, solid(P, "emblem", glow=True), cut=1)
        return m

    return build
