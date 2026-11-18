"""Shared builder for Knight Chessmon (Black) and (White) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the chess knight: a horse-headed puppet with a flowing orange-red mane, a lacquered body (black or white)
jointed with gold rings, a gold collar and saddle, coiled spring hocks, gold-ringed wheel hooves, and a huge striped
drill-lance mounted on its back pointing forward. Shiny: the other colour swapped with blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, metal, solid, strands
from _route import pal, tone


def make(name, white=False):
    body = (240, 236, 224) if white else (40, 40, 46)
    body_dark = (170, 164, 150) if white else (12, 12, 16)
    body_light = (255, 255, 250) if white else (110, 110, 124)
    base = {"body": body, "body_dark": body_dark, "body_light": body_light, "gold": (240, 190, 50),
            "gold_dark": (160, 110, 14), "mane": (240, 110, 40), "mane_dark": (170, 50, 14), "steel": (200, 204, 216),
            "steel_dark": (90, 94, 106), "eye": (240, 60, 40), "black": (24, 24, 30)}
    shiny = {"body": (60, 90, 200), "body_dark": (20, 34, 120), "body_light": (140, 170, 250)}

    def P(v):
        return pal(base, shiny, v)

    BODY = armour(P, "body", "body_dark", light="body_light", trim="gold", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark")

    def lancef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if (z * 0.9 + y * 0.4) % 3.0 < 0.8:
            return tone(p["gold"], face), None
        return BODY(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 16, 0))
        m.round_box(bd, 0, 2.0, 4.0, 7.0, 15.0, 23.0, BODY, cut=2)                      # barrel
        m.round_box(bd, 0, 1.0, 4.4, 3.6, 22.6, 24.0, GOLD, cut=1)                      # saddle
        hd = m.bone("head", bd, (0, 24, -6))
        rod(m, hd, (0, 22.0, -4.0), (0, 30.0, -7.0), 3, BODY, extend=0.6)                # neck
        m.round_box(hd, 0, -9.0, 2.4, 4.4, 28.0, 33.0, BODY, cut=1)                      # horse head
        m.round_box(hd, 0, -6.0, 3.0, 3.0, 27.0, 28.4, GOLD, cut=1)                      # gold collar
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.3, sx * 2.6), 31.0, -11.0, max(sx * 2.3, sx * 2.6), 31.8, -9.6, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 1.4, 33.0, -7.6), (sx * 0.2, 1, 0.3), 1.0, 2.6, BODY, tip=0.8)       # ears
        for i in range(7):                                                            # flowing mane
            rod(m, hd, (0, 33.0 - i * 1.2, -6.0 + i * 1.0), (0.4 * (i % 2), 28.0 - i * 1.6, 1.0 + i * 1.6), 1,
                strands(P, "mane", "mane_dark"), extend=0.3, t2=2)
        lb = m.bone("lance", bd, (0, 26, 4))                                            # drill-lance on the back
        for j in range(6):
            r = 3.4 - j * 0.3
            rod(m, lb, (0, 26.0 + j * 2.0, 10.0 - j * 3.0), (0, 28.0 + j * 2.0, 7.0 - j * 3.0), max(1, round(r)), lancef,
                extend=0.3)
        spike(m, lb, (0, 38.0, -8.0), (0, 0.55, -1), 2.4, 8.0, metal(P, "steel", dark="steel_dark"), tip=0.8)
        for sx, sz, nm in ((1, -1, "leg_front_left"), (-1, -1, "leg_front_right"), (1, 1, "leg_back_left"),
                           (-1, 1, "leg_back_right")):
            lg = m.bone(nm, top, (sx * 2.6, 15.0, sz * 4.0 + 2.0))
            hip = (sx * 2.6, 15.0, sz * 4.0 + 2.0)
            kn = (sx * 3.0, 8.0, sz * 4.0 + (1.0 if sz > 0 else 0.0))
            rod(m, lg, hip, kn, 2, BODY, extend=0.4)
            m.round_box(lg, kn[0], kn[2], 1.4, 1.4, kn[1] - 0.8, kn[1] + 0.8, GOLD, cut=0)
            for t in range(3):                                                        # coiled spring
                m.round_box(lg, kn[0], kn[2], 1.2, 1.2, kn[1] - 2.0 - t * 1.4, kn[1] - 1.4 - t * 1.4,
                            metal(P, "steel", dark="steel_dark"), cut=0)
            m.round_box(lg, kn[0], kn[2], 1.8, 1.8, 0.0, 2.6, GOLD, cut=1)              # wheel hoof
        return m

    return build
