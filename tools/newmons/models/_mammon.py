"""Shared builder for Mammon and Mammon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail standard after the
official art on wikimon.net): the armoured mammoth: a huge shaggy brown mammoth with a steel-plated head and trunk
engraved with gold, a single glaring eye on its helm, long curved ivory tusks, a black spiked crest, pale translucent
wing-fins and cream hooves. X-Antibody: a heavier, dark-armoured beast with a dark blue eye-mask, a red saddle cloth,
great bronze wing-fins and stubby pale tusks. Shiny: white woolly.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, cutout, fabric, fur, gem, local, metal, solid
from _route import pal, tone


def make(name, x=False):
    base = {"fur": (140, 90, 50), "fur_dark": (80, 46, 20), "fur_light": (200, 150, 100), "steel": (170, 176, 190) if not x else (60, 70, 100),
            "steel_dark": (80, 86, 100) if not x else (20, 24, 40), "gold": (230, 190, 70), "ivory": (246, 236, 210),
            "black": (30, 28, 34), "eye": (240, 220, 60), "wing": (220, 190, 200, 170) if not x else (160, 110, 90, 200),
            "red": (170, 30, 40), "hoof": (230, 220, 200), "mouth": (160, 40, 50)}
    shiny = {"fur": (240, 236, 226), "fur_dark": (180, 170, 160), "fur_light": (255, 255, 250)}

    def P(v):
        return pal(base, shiny, v)

    FUR = fur(P, "fur", "fur_dark", tip="fur_light", length=2.0)
    HELM = metal(P, "steel", dark="steel_dark")

    def wing_in(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        a, b = u / max(W, 1e-6), v / max(H, 1e-6)
        return b > 0.15 * a and b < 1.0 - 0.3 * a

    def build():
        m = Model(name)
        mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": HELM, "snout": HELM, "jaw": FUR, "mouth": solid(P, "mouth"),
                "tooth": solid(P, "ivory"), "leg_upper": FUR, "leg_lower": FUR, "paw": solid(P, "hoof"),
                "claw": solid(P, "hoof"), "tail": FUR}
        a = quadruped(m, mats, name, length=30.0, body_y=16.0, body_rx=8.0, body_ry=8.0, chest_bulk=1.2,
                      neck=((0, 22, -14), (0, 22, -18)), head_len=9.0, head_w=4.4, head_h=5.0, snout=0.3, mouth_open=6,
                      teeth=0, leg_bulk=1.8, toes=3, tail=((0, 18, 16), (0, 14, 20)), tail_r=(1.0, 0.8))
        bd, hd = a["body"], a["head"]
        hc = a["head_c"]
        m.box(hd, -1.0, hc[1] + 1.4, hc[2] - 5.4, 1.0, hc[1] + 2.6, hc[2] - 5.2, solid(P, "eye", glow=True))   # single eye
        pts = [(0, hc[1] - 1.0, hc[2] - 4.0), (0, hc[1] - 8.0, hc[2] - 6.0), (0, hc[1] - 14.0, hc[2] - 4.0),
               (0, hc[1] - 16.0, hc[2] - 7.0)]                                     # trunk
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 - j // 2, HELM, extend=0.4)
        for sx in (-1, 1):                                                         # curved ivory tusks
            tp = [(sx * 2.4, hc[1] - 2.0, hc[2] - 3.0), (sx * 4.0, hc[1] - 7.0, hc[2] - 8.0), (sx * 3.0, hc[1] - 6.0, hc[2] - 14.0)]
            if x:
                tp = tp[:2]
            for p0, p1 in zip(tp, tp[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "ivory"), extend=0.3, t2=2)
        for j in range(5):                                                         # black spiked crest
            spike(m, hd, ((j - 2) * 0.8, hc[1] + 4.6, hc[2] + 1.0), ((j - 2) * 0.2, 1, 0.4), 1.2, 5.0 - abs(j - 2), solid(P, "black"),
                  tip=0.8)
        for side in (1, -1):                                                       # wing-fins
            x0, x1 = sorted((side * 6.0, side * (16.0 if not x else 18.0)))
            m.box(bd, x0, 22.0, -6.0, x1, 34.0, -6.0, cutout(wing_in, solid(P, "wing")), rotation=(0, side * -30, side * -20),
                  pivot=(side * 6.0, 22.0, -6.0))
        if x:
            m.round_box(bd, 0, 0, 8.8, 6.0, 22.0, 25.0, fabric(P, "red", "black"), cut=2)
        return m

    return build
