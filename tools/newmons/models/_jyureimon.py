"""Shared builder for Jyureimon and Jyureimon (Christmas Tree) (CobbleEffort: Digital; hand-built after the official
art on wikimon.net): the haunted forest tree: a gnarled grey-brown trunk with a scowling face of hollow knots and
glowing yellow eyes, green vine garlands, a great round crown of dark green leaves dotted with red berries and a
spreading tangle of roots. Christmas Tree: a tiered festive fir crowned with a golden star and a red bow, hung with
coloured baubles, glowing lights and a golden bell, with wrapped presents round its roots.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digidetail import fur, gem, solid, twisted
from _route import pal, tone

BASE = {"bark": (130, 110, 90), "bark_dark": (70, 56, 44), "bark_light": (190, 170, 150), "leaf": (40, 100, 50),
        "leaf_dark": (14, 50, 20), "leaf_light": (90, 160, 90), "berry": (210, 30, 40), "eye": (250, 230, 60),
        "mouth": (30, 24, 20), "vine": (110, 190, 60), "gold": (250, 210, 60), "gold_light": (255, 245, 190),
        "red": (220, 40, 50), "blue": (60, 120, 230), "pink": (240, 140, 190), "white": (250, 250, 250),
        "green": (40, 150, 70)}
SHINY = {"leaf": (150, 90, 40), "leaf_dark": (90, 40, 14), "leaf_light": (220, 160, 90)}


def P(v):
    return pal(BASE, SHINY, v)


BARK = twisted(P, "bark", "bark_dark", light="bark_light", period=1.8)
LEAVES = fur(P, "leaf", "leaf_dark", tip="leaf_light", length=1.4)


def make(name, xmas=False):
    def trunkf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and not xmas:
            for sx in (-1, 1):
                if math.hypot(x - sx * 2.4, y - 16.0) < 0.9:
                    return tone(p["eye"], face), p["eye"]
            if abs(y - 12.0) < 1.0 and abs(x) < 2.6:
                return tone(p["mouth"], face), None
        return BARK(x, y, z, face, variant, box=box, **k)

    def leaff(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not xmas and (int(x * 1.3) * 7 + int(y * 1.7) * 3 + int(z * 1.1) * 5) % 23 == 0:
            return tone(p["berry"], face), None
        return LEAVES(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        for i in range(10):                                                       # spreading roots
            ang = 2 * math.pi * i / 10 + 0.3
            pts = [(2.4 * math.cos(ang), 6.0, 2.4 * math.sin(ang)), (7.0 * math.cos(ang), 2.0, 7.0 * math.sin(ang)),
                   (11.0 * math.cos(ang + 0.2), 0.4, 11.0 * math.sin(ang + 0.2))]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, top, p0, p1, 1, BARK, extend=0.4, t2=2)
        bd = m.bone("body", top, (0, 6, 0))
        m.round_box(bd, 0, 0, 4.4, 4.0, 2.0, 24.0, trunkf, cut=2)                     # trunk
        for sx in (-1, 1):                                                         # branch arms
            ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 4.0, 18.0, 0))
            rod(m, ab, (sx * 4.0, 18.0, 0), (sx * 9.0, 22.0, -2.0), 2, BARK, extend=0.4)
            for j in range(3):
                spike(m, ab, (sx * 9.0, 22.0, -2.0), (sx * 0.6, -0.4 + j * 0.4, -0.6), 1.0, 3.0, BARK, tip=0.8)
        hd = m.bone("head", bd, (0, 24, 0))
        if not xmas:
            ball(m, hd, (0, 33.0, 0), 11.0, leaff, layers=6, squash=0.8)               # round leafy crown
            for j in range(2):                                                     # vine garlands
                for i in range(8):
                    a0, a1 = math.pi * i / 8 - math.pi / 2, math.pi * (i + 1) / 8 - math.pi / 2
                    rod(m, bd, (4.6 * math.sin(a0), 20.0 - j * 4.0 - 1.6 * math.cos(a0), -4.4 * math.cos(a0)),
                        (4.6 * math.sin(a1), 20.0 - j * 4.0 - 1.6 * math.cos(a1), -4.4 * math.cos(a1)), 1,
                        solid(P, "vine"), extend=0.2, t2=1)
        else:
            for t, (r, y0, y1) in enumerate(((14.0, 14.0, 22.0), (11.0, 21.0, 29.0), (8.0, 28.0, 35.0), (5.0, 34.0, 40.0))):
                m.round_box(hd, 0, 0, r, r, y0, y1, LEAVES, cut=max(1, int(r * 0.4)))  # tiered fir
                for i in range(8):                                                   # baubles and lights
                    ang = 2 * math.pi * (i + t * 0.5) / 8
                    key = ("red", "gold", "blue", "pink")[(i + t) % 4]
                    m.round_box(hd, (r - 0.6) * math.cos(ang), (r - 0.6) * math.sin(ang), 0.9, 0.9, y0 + 0.4, y0 + 2.2,
                                gem(P, key, "gold_light"), cut=0)
            for j in range(5):                                                     # golden star
                ang = 2 * math.pi * j / 5
                spike(m, hd, (0, 43.0, 0), (math.sin(ang), math.cos(ang), 0), 1.6, 3.4, solid(P, "gold", glow=True), tip=0.8)
            for sx in (-1, 1):                                                      # red bow
                m.round_box(hd, sx * 2.0, -5.4, 1.8, 0.6, 37.0, 39.0, solid(P, "red"), cut=0)
            m.round_box(hd, 0, -8.6, 1.2, 1.2, 30.0, 32.4, solid(P, "gold"), cut=0)   # bell
            for i, (px, pz, s, key) in enumerate(((-9.0, -9.0, 2.0, "red"), (8.0, -10.0, 2.4, "green"), (11.0, 2.0, 1.8,
                                                   "blue"), (-11.0, 3.0, 2.2, "pink"), (0, -12.0, 1.6, "gold"))):
                m.box(top, px - s, 0.0, pz - s, px + s, 2 * s, pz + s, solid(P, key))     # presents
                m.box(top, px - 0.3, 0.0, pz - s - 0.05, px + 0.3, 2 * s + 0.05, pz + s + 0.05, solid(P, "white"))
        return m

    return build
