"""Shared builder for Otamamon and its variants (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a round glossy tadpole with a big smiling mouth of little teeth, round eyes, two clawed forelimbs, a
pair of webbed hind feet and a tall finned tail. Looks: "base" (violet), "red", "x" (X-Antibody: a much fatter round
violet body with a tiny gold crown, gold armbands and a thin finned tail below).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import skin, solid
from _route import pal, tone

LOOKS = {"base": {"body": (110, 100, 200), "body_dark": (50, 40, 130)},
         "red": {"body": (200, 70, 50), "body_dark": (120, 30, 20)},
         "x": {"body": (90, 80, 190), "body_dark": (40, 30, 120)}}
COMMON = {"white": (250, 250, 250), "black": (20, 20, 26), "tooth": (250, 250, 244), "claw": (230, 230, 236),
          "fin": (230, 230, 240), "fin_dark": (150, 150, 170), "gold": (240, 200, 70)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, body=(90, 180, 110), body_dark=(30, 110, 50))
    x = look == "x"

    def P(v):
        return pal(base, shiny, v)

    BODY = skin(P, "body", dark="body_dark", var=0.02)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        r = 6.0 if not x else 8.0
        ball(m, bd, (0, 8.0 if not x else 11.0, 0), r, BODY, layers=5, ry=r * 0.9)
        cy = 8.0 if not x else 11.0
        for sx in (-1, 1):
            ball(m, bd, (sx * 2.4, cy + 1.6, -r * 0.8), 1.4, solid(P, "white"), layers=2, squash=0.5)
            m.box(bd, sx * 2.4 - 0.6, cy + 1.2, -r * 0.8 - 0.75, sx * 2.4 + 0.6, cy + 2.2, -r * 0.8 - 0.6,
                  solid(P, "black"))
        m.box(bd, -3.6, cy - 2.6, -r * 0.92, 3.6, cy - 2.0, -r * 0.85, solid(P, "black"))   # big smile
        for j in range(4):
            spike(m, bd, (-2.6 + j * 1.74, cy - 2.0, -r * 0.9), (0, -1, 0), 0.8, 1.0, solid(P, "tooth"), tip=0.8)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # clawed forelimbs
            ab = m.bone(nm, bd, (sx * r * 0.8, cy - 2.0, -1.0))
            rod(m, ab, (sx * r * 0.8, cy - 2.0, -1.0), (sx * (r + 2.6), cy - 4.0, -2.0), 1, BODY, extend=0.2, t2=2)
            for f in range(3):
                spike(m, ab, (sx * (r + 2.6), cy - 4.0, -2.0), (sx * 0.4, -0.5, -1 + f * 0.5), 0.8, 2.0,
                      solid(P, "claw"), tip=0.8)
        if x:
            m.round_box(bd, 0, 0, 1.6, 1.6, cy + r * 0.9 - 0.2, cy + r * 0.9 + 1.0, solid(P, "gold"), cut=0)
            for sx in (-1, 1):
                m.round_box(bd, sx * (r + 1.0), -2.0, 1.0, 1.0, cy - 4.6, cy - 3.4, solid(P, "gold"), cut=0)
            rod(m, bd, (0, cy - r * 0.8, 1.0), (0.6, 0.4, 2.0), 2, BODY, extend=0.3)
            m.box(bd, -0.2, 0.0, 1.0, 0.2, 3.0, 4.0, solid(P, "fin"))
        else:
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                         # webbed hind feet
                lg = m.bone(nm, top, (sx * 3.0, 4.0, 2.0))
                rod(m, lg, (sx * 3.0, 4.0, 2.0), (sx * 4.6, 1.0, 1.0), 1, BODY, extend=0.2, t2=2)
                m.round_box(lg, sx * 4.6, -0.4, 1.4, 1.8, 0.0, 0.8, BODY, cut=0)
            tb = m.bone("tail", bd, (0, 12, 4))                                         # tall finned tail
            pts = [(0, 12.0, 4.0), (0, 16.0, 7.0), (0, 20.0, 7.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, tb, p0, p1, 2, BODY, extend=0.3)
            m.box(tb, -0.3, 16.0, 5.0, 0.3, 24.0, 10.0, skin(P, "fin", dark="fin_dark"))
        return m

    return build
