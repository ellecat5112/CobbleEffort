"""Shared builder for Siesamon and Siesamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the shisa guardian lion-dog. Siesamon: a white-and-gold shisa with a spiral golden mane, a single horn,
violet face markings, golden cloud-swirl fur on its legs and body, violet claws, and a huge curling golden tail; little
cloud puffs drift round it. X-Antibody: a gleaming golden armoured shisa with spiked silver horns, a red tasselled
collar, cyan cloud swirls and a long flaming orange-red tail. Shiny: black / silver.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digidetail import armour, fur, metal, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"white": (246, 244, 236), "white_dark": (190, 186, 170), "gold": (240, 200, 80), "gold_dark": (170, 120, 30),
            "violet": (130, 90, 200), "red": (210, 40, 40), "cyan": (90, 200, 220), "cloud": (246, 240, 220),
            "steel": (210, 214, 226), "flame": (250, 120, 40), "eye": (200, 40, 40)}
    shiny = {"white": (60, 56, 66), "white_dark": (24, 22, 28)} if not x else {"gold": (210, 214, 226),
                                                                            "gold_dark": (120, 124, 140)}

    def P(v):
        return pal(base, shiny, v)

    def swirlf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        r = math.hypot(((xx + z) % 5.0) - 2.5, (y % 5.0) - 2.5)
        if abs(r - 1.4) < 0.3:
            return tone(p["cyan" if x else "gold_dark"], face), None
        if x:
            return armour(P, "gold", "gold_dark")(xx, y, z, face, variant, box=box, **k)
        if y < 12.0:
            return fur(P, "gold", "gold_dark", length=1.2)(xx, y, z, face, variant, box=box, **k)
        return fur(P, "white", "white_dark", length=1.2)(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": swirlf, "head": swirlf, "snout": swirlf, "jaw": swirlf, "claw": solid(P, "violet")}
        a = quadruped(m, mats, name, length=24.0, body_y=14.0, body_rx=6.0, body_ry=6.0, chest_bulk=1.2,
                      neck=((0, 20, -12), (0, 23, -15)), head_len=9.0, head_w=4.6, head_h=4.6, teeth=4, mouth_open=12,
                      tail=((0, 18, 12), (0, 26, 16), (0, 30, 12)), tail_r=(3.0, 3.6, 3.0))
        hd = a["head"]
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 4.5, sx * 4.8))
            m.box(hd, x0, 25.0, -20.0, x1, 26.0, -18.6, solid(P, "eye"))
        if not x:
            spike(m, hd, (0, 28.0, -16.0), (0, 1, -0.3), 1.4, 5.0, solid(P, "white"), tip=0.8)
            for j in range(12):                                                          # spiral golden mane
                ang = 2 * math.pi * j / 12
                c = (5.4 * math.cos(ang), 24.0 + 5.4 * math.sin(ang), -12.0)
                spike(m, hd, c, (math.cos(ang), math.sin(ang), 0.5), 2.2, 4.0, strands(P, "gold", "gold_dark"), tip=0.8)
            for j in range(5):                                                           # huge curling tail
                spike(m, "tail", (0, 30.0, 12.0), ((j - 2) * 0.3, 0.6, -0.4 + j * 0.2), 2.6, 8.0,
                      strands(P, "gold", "gold_dark"), tip=0.8)
            for c in ((-12.0, 26.0, -6.0), (12.0, 30.0, 0.0), (-10.0, 8.0, 6.0)):       # cloud puffs
                ball(m, a["body"], c, 2.0, solid(P, "cloud"), layers=2)
        else:
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.4, 28.0, -14.0), (sx * 0.4, 1, 0.2), 1.4, 6.0, metal(P, "steel"), tip=0.8)
            spike(m, hd, (0, 28.0, -16.0), (0, 1, -0.3), 1.4, 7.0, metal(P, "steel"), tip=0.8)
            m.round_box(a["neck"], 0, -12.0, 5.0, 4.0, 18.0, 20.0, solid(P, "red"), cut=1)  # red tasselled collar
            for sx in (-1, 1):
                rod(m, a["neck"], (sx * 4.0, 19.0, -14.0), (sx * 5.0, 10.0, -16.0), 1, solid(P, "red"), extend=0.2, t2=2)
            tl = m.bone("tail_flame", "tail", (0, 30, 12))
            pts = [(0, 30.0, 12.0), (0, 34.0, 20.0), (0, 30.0, 28.0), (0, 24.0, 32.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, tl, p0, p1, 3, solid(P, "flame", glow=True), extend=0.4)
        return m

    return build
