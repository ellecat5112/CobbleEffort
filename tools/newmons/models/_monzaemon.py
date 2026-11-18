"""Shared builder for Monzaemon and Monzaemon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): a giant yellow teddy bear: plush golden fur, a white belly with a crossed sticking plaster, round
ears, a cream muzzle with a black nose, stern red-lined closed eyes and stubby paws. The X-Antibody ("x"): a
patchwork bear of tan and brown felt with pink heart paw pads and ears, a red bow, stitched seams, a halo and
rainbow bubbles of hearts floating round it.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fabric, fur, solid
from _route import pal, tone

BASE = {"yellow": (250, 200, 30), "yellow_dark": (200, 150, 10), "white": (248, 248, 246), "white_dark": (200, 200, 196),
        "cream": (250, 236, 200), "black": (30, 26, 26), "red": (200, 40, 40), "plaster": (240, 230, 220),
        "tan": (220, 170, 100), "tan_dark": (160, 110, 50), "brown": (150, 90, 50), "pink": (240, 80, 160),
        "halo": (220, 200, 255, 170), "bubble": (250, 160, 230, 150)}
SHINY = {"yellow": (200, 140, 220), "yellow_dark": (140, 80, 170), "tan": (170, 200, 230), "tan_dark": (110, 140, 180)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    if x:
        F0 = fabric(P, "tan", "tan_dark", seam="brown")

        def FUR(xx, y, z, face, variant, box=None, **k):
            p = P(variant)
            if face != "down" and math.sin(xx * 0.5) * math.sin(y * 0.4 + z * 0.3) > 0.5:
                return tone(p["brown"], face), None
            return F0(xx, y, z, face, variant, box=box, **k)
    else:
        FUR = fur(P, "yellow", "yellow_dark", length=1.4, density=2.2)
    BELLY = fur(P, "white", "white_dark", length=1.0)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 20, 0))
        ball(m, bd, (0, 24.0, 0.6), 10.0, FUR, layers=6, ry=12.0, squash=0.85)            # plush body
        ball(m, bd, (0, 22.0, -5.6), 7.0, BELLY, layers=5, ry=8.0, squash=0.4)            # white belly
        for ang in (40, -40):                                                          # crossed plaster
            m.box(bd, -3.6, 20.4, -9.2, 3.6, 21.8, -9.0, solid(P, "plaster"), rotation=(0, 0, ang),
                  pivot=(0, 21.0, -9.0))
        hd = m.bone("head", bd, (0, 36, 0))
        ball(m, hd, (0, 42.0, -0.6), 7.6, FUR, layers=6, ry=6.6, squash=0.9)
        ball(m, hd, (0, 40.0, -6.0), 3.2, solid(P, "cream"), layers=3, squash=0.6)
        m.round_box(hd, 0, -8.0, 1.2, 0.6, 41.0, 42.4, solid(P, "black"), cut=0)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.8, sx * 4.4), 44.0, -6.8, max(sx * 1.8, sx * 4.4), 44.6, -6.6, solid(P, "red"))
            m.box(hd, min(sx * 1.8, sx * 4.2), 43.4, -6.85, max(sx * 1.8, sx * 4.2), 43.9, -6.75, solid(P, "black"))
            ball(m, hd, (sx * 5.6, 48.0, 0), 2.6, FUR, layers=3, squash=0.5)              # round ears
            if x:
                m.box(hd, sx * 5.6 - 1.4, 46.8, -1.4, sx * 5.6 + 1.4, 49.2, -1.2, solid(P, "pink"))
        if x:
            m.box(bd, -3.0, 33.0, -6.6, 3.0, 35.4, -6.0, solid(P, "red"))                # red bow
            for i in range(12):                                                         # halo
                ang = 2 * math.pi * i / 12
                m.box(hd, 5.0 * math.cos(ang) - 0.8, 53.0, 5.0 * math.sin(ang) - 0.8, 5.0 * math.cos(ang) + 0.8, 53.6,
                      5.0 * math.sin(ang) + 0.8, solid(P, "halo", glow=True))
            for i, (bx, by, bz) in enumerate(((-14, 40, 0), (14, 44, 2), (-12, 26, 3), (13, 28, -2), (-9, 50, 2),
                                              (10, 52, 0))):                            # heart bubbles
                ball(m, bd, (bx, by, bz), 2.4 if i % 2 else 3.0, solid(P, "bubble", glow=True), layers=3)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 8.0, 30.0, 0))
            rod(m, ab, (sx * 8.0, 30.0, 0), (sx * 12.0, 22.0, -2.0), 6, FUR, extend=0.8)
            ball(m, ab, (sx * 12.4, 20.4, -2.4), 3.4, FUR, layers=3)
            if x:
                m.box(ab, sx * 12.4 - 1.6, 18.6, -5.9, sx * 12.4 + 1.6, 21.0, -5.7, solid(P, "pink"))
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 5.0, 14.0, 0))
            rod(m, lg, (sx * 5.0, 14.0, 0), (sx * 5.4, 3.0, -0.6), 8, FUR, extend=1.0)
            m.round_box(lg, sx * 5.4, -1.4, 4.4, 5.0, 0.0, 3.0, FUR, cut=1)
            if x:
                m.box(lg, sx * 5.4 - 2.2, 0.6, -6.5, sx * 5.4 + 2.2, 2.6, -6.3, solid(P, "pink"))
        return m

    return build
