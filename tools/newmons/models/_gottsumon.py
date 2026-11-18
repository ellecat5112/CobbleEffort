"""Shared builder for Gottsumon and Gottsumon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net). Gottsumon: a little pile of grey faceted rocks with two yellow eyes in a dark face hollow, rock-chunk
ears, a body and limbs built of stacked stones. X-Antibody: a squat hunched rock golem of smooth grey slabs with a
small helmeted head, one yellow eye, a stone horn and a huge spread stone hand. Shiny: sandstone.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import fbm, skin, solid
from _route import pal, tone


def make(name, x=False):
    base = {"rock": (150, 152, 160), "rock_dark": (80, 82, 90), "rock_light": (200, 202, 210), "hollow": (20, 18, 22),
            "eye": (250, 200, 40)}
    shiny = {"rock": (210, 170, 120), "rock_dark": (150, 110, 60), "rock_light": (240, 210, 170)}

    def P(v):
        return pal(base, shiny, v)

    ROCK0 = skin(P, "rock", dark="rock_dark", light="rock_light")

    def rockf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if fbm(xx * 0.6, y * 0.6, z * 0.6, seed=8) > 0.66:
            return tone(p["rock_dark"], face), None
        return ROCK0(xx, y, z, face, variant, box=box, **k)

    def facef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in ((-1, 1) if not x else (0,)):
                d = math.hypot(xx - sx * 1.6, y - ey)
                if d < 0.5:
                    return tone(p["hollow"], face), None
                if d < 1.1:
                    return tone(p["eye"], face), None
            if abs(xx) < 3.0 and abs(y - ey + 1.6) < 1.0 and not x:
                return tone(p["hollow"], face), None
        return rockf(xx, y, z, face, variant, box=box, **k)

    ey = 17.0 if not x else 21.0

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        if not x:
            for c, r in (((0, 10.0, 0), 3.4), ((1.0, 6.0, 0.4), 3.0), ((-1.0, 13.0, 0.4), 2.6)):
                m.round_box(bd, c[0], c[2], r, r * 0.9, c[1] - r, c[1] + r, rockf, cut=1)
            hd = m.bone("head", bd, (0, 16, 0))
            m.round_box(hd, 0, -0.4, 4.0, 3.4, 14.0, 21.0, facef, cut=2)
            for sx in (-1, 1):
                m.round_box(hd, sx * 3.6, 0, 1.6, 1.6, 20.0, 23.0, rockf, cut=1)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
                ab = m.bone(nm, bd, (sx * 3.4, 12.0, 0))
                for j in range(3):
                    m.round_box(ab, sx * (4.4 + j * 1.6), -j * 0.6, 1.4, 1.4, 11.0 - j * 2.4, 13.4 - j * 2.4, rockf, cut=0)
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 2.0, 8.0, 0))
                for j in range(3):
                    m.round_box(lg, sx * 2.0, 0, 1.6, 1.6, j * 2.6, j * 2.6 + 2.4, rockf, cut=0)
            return m
        m.round_box(bd, 0, 1.0, 6.0, 5.0, 6.0, 20.0, rockf, cut=2)                          # squat golem
        hd = m.bone("head", bd, (0, 20, -1))
        m.round_box(hd, 0, -1.0, 3.0, 2.8, 18.0, 24.0, facef, cut=1)
        spike(m, hd, (0, 23.6, -1.0), (0.4, 1, 0.2), 1.8, 5.0, rockf, tip=0.9)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 6.0, 17.0, 0))
            rod(m, ab, (sx * 6.0, 17.0, 0), (sx * 11.0, 20.0, -2.0), 3, rockf, extend=0.6)
            m.round_box(ab, sx * 13.0, -3.0, 2.6, 1.6, 18.0, 24.0, rockf, cut=1)               # spread stone hand
            for j in range(4):
                spike(m, ab, (sx * (11.4 + j * 1.1), 24.0, -3.0), (sx * 0.2 * (j - 1.5), 1, 0), 1.0, 3.0, rockf,
                      tip=0.8)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 3.0, 8.0, 0))
            m.round_box(lg, sx * 3.6, -0.6, 2.6, 3.0, 0.0, 8.0, rockf, cut=1)
        return m

    return build
