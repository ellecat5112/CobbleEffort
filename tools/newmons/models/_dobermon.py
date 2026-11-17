"""Shared builder for Dobermon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a lean, long-
legged demon hound in glossy black with tan markings on its muzzle, chest and lower legs, a narrow pointed head with
red eyes and swept-back ears, a steel spiked collar, red slashes on its haunches, a ridge of short spines down its
back, steel claws and a short tail. make(x=True): Dobermon (X-Antibody), darker and heavier, with a huge ring of
steel spikes round its neck, crimson slits, steel-banded legs and a great curved silver blade sweeping up from its
back. Shiny: white coat.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import metal, skin, solid
from _route import pal, tone

BASE = {"black": (44, 44, 52), "black_dark": (12, 12, 16), "black_light": (130, 130, 150), "tan": (190, 120, 70),
        "tan_dark": (110, 60, 30), "red": (220, 40, 40), "steel": (210, 214, 226), "steel_dark": (100, 104, 116),
        "mouth": (130, 20, 30), "tooth": (250, 250, 246)}
SHINY = {"black": (230, 230, 236), "black_dark": (150, 150, 160), "black_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    COAT = skin(P, "black", dark="black_dark", light="black_light", var=0.04)
    TAN = skin(P, "tan", dark="tan_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def coatf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west") and z > 4.0 and abs((y + z * 0.6) % 4.0 - 2.0) < 0.3 and y > 14.0:
            return tone(p["red"], face), (p["red"] if x else None)              # haunch slashes
        if y < 9.0:
            return TAN(xx, y, z, face, variant, box=box, **k)                   # tan lower legs
        return COAT(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": coatf, "belly": TAN, "neck": coatf, "head": coatf, "snout": TAN, "jaw": TAN,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": coatf, "leg_lower": coatf,
                "paw": TAN, "claw": STEEL, "tail": coatf}
        a = quadruped(m, mats, name, length=30.0, body_y=20.0, body_rx=4.6, body_ry=5.0, chest_bulk=1.3 if not x else 1.5,
                      neck=((0, 24, -13), (0, 30, -17)), head_len=11.0, head_w=2.8, head_h=3.2, snout=0.9,
                      mouth_open=14 if x else 4, teeth=4 if x else 0, leg_bulk=1.1 if not x else 1.4, toes=3,
                      tail=((0, 22, 15), (0, 24, 19)), tail_r=(1.4, 1.0))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.3, ez - 0.7, max(sx * ex, sx * (ex + 0.3)), ey + 0.3,
                  ez + 0.7, solid(P, "red", glow=True))
            pts = [(sx * 1.6, ey + 1.6, ez + 2.0), (sx * 2.6, ey + 5.0, ez + 5.0), (sx * 3.0, ey + 6.0, ez + 9.0)]
            for p0, p1 in zip(pts, pts[1:]):                                    # swept-back ears
                rod(m, hd, p0, p1, 1, coatf, extend=0.4, t2=2)
        nk = a["neck"]
        n = 14 if x else 8                                                      # spiked collar
        r = 3.6 if not x else 4.2
        for i in range(n):
            ang = 2 * math.pi * i / n
            d = (math.cos(ang), math.sin(ang), -0.3)
            spike(m, nk, (r * d[0], 26.0 + r * d[1], -14.0), d, 1.0, 3.0 if not x else 6.0, STEEL, tip=0.3)
        m.round_box(nk, 0, -14.0, 3.6, 1.0, 23.4, 28.6, STEEL, cut=1)
        for i in range(8):                                                      # back spines
            spike(m, bd, (0, 25.0, -8.0 + i * 2.8), (0, 1, 0.5), 1.0, 2.0, coatf, tip=0.25)
        if x:
            pts = [(0, 25.0, 4.0), (-3.0, 32.0, 2.0), (-8.0, 38.0, -4.0), (-12.0, 38.0, -12.0), (-12.0, 34.0, -18.0)]
            for p0, p1 in zip(pts, pts[1:]):                                    # great curved silver blade
                rod(m, bd, p0, p1, 1, STEEL, extend=0.5, t2=3)
            for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
                w = a[nm]["wrist"]
                m.round_box(a[nm]["bone"], w[0], w[2], 1.8, 1.8, 6.0, 7.6, STEEL, cut=1)
        return m
    return build
