"""Shared builder for Magnamon and Magnamon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail standard after
the official art on wikimon.net): the Royal Knight of miracles: a sturdy blue dragon-man in gleaming golden armour with
angular spiked plates, a horned golden helm with a V crest, huge golden boot-greaves and gauntlets over blue claws,
and a blue tail. X-Antibody: sharper faceted gold-orange armour with cyan crystal edges and more spikes. Shiny:
silver armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, gem, scales, solid
from _route import pal, tone


def make(name, x=False):
    base = {"gold": (250, 210, 60) if not x else (250, 170, 60), "gold_dark": (170, 120, 10) if not x else (170, 90, 20),
            "gold_light": (255, 245, 170) if not x else (255, 220, 160), "blue": (60, 110, 220), "blue_dark": (20, 50, 140),
            "cyan": (120, 230, 250), "cyan_light": (230, 255, 255), "eye": (60, 220, 120), "claw": (220, 224, 234)}
    shiny = {"gold": (220, 224, 236), "gold_dark": (130, 136, 156), "gold_light": (255, 255, 255)}

    def P(v):
        return pal(base, shiny, v)

    GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="cyan" if x else "gold_dark", trim_w=0.25)
    BLUE = scales(P, "blue", "blue_dark", size=1.0)

    def build():
        m = Model(name)
        mats = {"skin": BLUE, "chest": GOLD, "abs": BLUE, "pelvis": GOLD, "neck": BLUE, "deltoid": GOLD, "upper_arm": BLUE,
                "forearm": GOLD, "hand": BLUE, "finger": BLUE, "claw": solid(P, "claw"), "thigh": BLUE, "knee": GOLD,
                "shin": GOLD, "calf": GOLD, "foot": GOLD, "talon": solid(P, "claw")}
        a = humanoid(m, mats, bulk=1.1, arm_bulk=1.15, leg_bulk=1.2, claws=True, talons=True, name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                         # angular spiked plates
            m.round_box(bd, sx * 8.4, 0, 3.6, 4.0, 46.0, 53.0, GOLD, cut=1)
            for j in range(2 if not x else 4):
                spike(m, bd, (sx * 9.6, 52.0 - j * 1.6, -1.0 + j), (sx * 0.6, 1, 0.2), 1.6, 7.0 - j, GOLD, tip=0.8)
            spike(m, bd, (sx * 4.0, 50.0, 3.6), (sx * 0.4, 0.8, 1), 1.6, 8.0, GOLD, tip=0.8)
        for nm in ("leg_left", "leg_right"):                                       # huge boot greaves
            kn = a[nm]["knee"]
            sx = 1 if kn[0] > 0 else -1
            m.round_box(a[nm]["bone"], kn[0], kn[2] - 0.6, 3.4, 3.6, 0.0, kn[1] - 2.0, GOLD, cut=1)
            spike(m, a[nm]["bone"], kn, (sx * 0.2, 0.6, -1), 1.6, 4.0, GOLD, tip=0.8)
        for nm in ("arm_left", "arm_right"):                                       # gauntlets
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 3.0, 3.0, w[1] - 1.0, w[1] + 6.0, GOLD, cut=1)
        hd = m.bone("head", bd, (0, 55, -1))
        m.round_box(hd, 0, -1.0, 2.8, 3.4, 53.6, 60.4, GOLD, cut=1)
        m.round_box(hd, 0, -4.4, 1.8, 1.4, 54.0, 56.6, BLUE, cut=1)
        m.box(hd, -1.6, 57.4, -4.5, 1.6, 58.2, -4.4, solid(P, "eye", glow=True))
        for sx in (-1, 1):                                                         # V crest
            rod(m, hd, (0, 60.0, -3.0), (sx * 5.0, 66.0, -2.0), 1, GOLD, extend=0.2, t2=2)
            spike(m, hd, (sx * 2.6, 59.6, 0.6), (sx * 0.6, 0.8, 0.6), 1.2, 4.0, GOLD, tip=0.8)
        tb = m.bone("tail", bd, (0, 32, 3))
        pts = [(0, 32.0, 3.4), (0, 24.0, 10.0), (3.0, 18.0, 16.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 2, BLUE, extend=0.4, t2=1)
        if x:                                                                      # cyan crystal edges
            for j, (px, py) in enumerate(((6.0, 44.0), (-6.0, 44.0), (8.0, 36.0), (-8.0, 36.0))):
                spike(m, bd, (px, py, -3.0), (math.copysign(1, px), 0.4, -0.4), 1.2, 4.0, gem(P, "cyan", "cyan_light"), tip=0.8)
        return m

    return build
