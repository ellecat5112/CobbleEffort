"""Shared builder for Elecmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a little red
four-legged electric beast striped with blue, big blue-ringed eyes, long pointed ears with pink insides, a black nose,
white claws, and a huge fan of nine tail feathers in red tipped with blue streaks that crackle with electricity.
make(violet=True): Elecmon (Violet), purple striped with yellow, red eyes and a violet fan streaked with yellow.
Shiny: green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import fur, local, solid
from _route import pal, tone

LOOKS = {
    False: ({"coat": (230, 50, 40), "coat_dark": (150, 20, 20), "stripe": (70, 110, 220), "eye": (60, 130, 220),
             "tail": (230, 40, 40), "tail_tip": (90, 140, 230)},
            {"coat": (90, 180, 80), "coat_dark": (40, 110, 30), "tail": (90, 180, 80)}),
    True: ({"coat": (110, 90, 200), "coat_dark": (60, 40, 130), "stripe": (250, 220, 50), "eye": (220, 40, 40),
            "tail": (120, 100, 210), "tail_tip": (250, 220, 50)},
           {"coat": (230, 140, 60), "coat_dark": (150, 80, 20), "tail": (230, 140, 60)}),
}
COMMON = {"pink": (250, 170, 190), "white": (250, 250, 250), "black": (24, 24, 28), "pupil": (16, 16, 20),
          "mouth": (120, 20, 30), "tooth": (250, 250, 246)}


def make(name, violet=False):
    base, shiny = LOOKS[violet]
    base = {**COMMON, **base}

    def P(v):
        return pal(base, shiny, v)

    COAT = fur(P, "coat", "coat_dark", length=1.0, density=2.6)

    def coatf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "up") and abs((z * 0.5 + y * 0.3) % 3.0 - 1.5) < 0.3:
            return tone(p["stripe"], face), None
        return COAT(x, y, z, face, variant, box=box, **k)

    def featherf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6)
        if t < 0.3 or abs((u * 0.9 + v * 0.4) % 4.0 - 2.0) < 0.35:
            return tone(p["tail_tip"], face), None
        return tone(p["tail"], face), None

    def build():
        m = Model(name)
        mats = {"skin": coatf, "belly": coatf, "neck": coatf, "head": coatf, "snout": coatf, "jaw": coatf,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": coatf, "leg_lower": coatf,
                "paw": coatf, "claw": solid(P, "white"), "tail": coatf}
        a = quadruped(m, mats, name, length=16.0, body_y=6.0, body_rx=4.0, body_ry=3.6, chest_bulk=1.1,
                      neck=((0, 7, -6), (0, 8, -8)), head_len=7.0, head_w=3.6, head_h=3.6, snout=0.4, mouth_open=4,
                      teeth=0, leg_bulk=1.0, toes=3, tail=((0, 8, 7), (0, 10, 9)), tail_r=(1.4, 1.2))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.8, ez - 1.0, max(sx * ex, sx * (ex + 0.3)), ey + 0.8,
                  ez + 1.0, solid(P, "eye"))
            m.box(hd, min(sx * (ex + 0.1), sx * (ex + 0.35)), ey - 0.4, ez - 0.5, max(sx * (ex + 0.1),
                  sx * (ex + 0.35)), ey + 0.4, ez + 0.5, solid(P, "pupil"))
            pts = [(sx * 2.0, ey + 1.6, ez + 1.0), (sx * 4.0, ey + 4.0, ez + 2.0), (sx * 6.0, ey + 6.4, ez + 3.0)]
            for p0, p1 in zip(pts, pts[1:]):                                         # long pointed ears
                rod(m, hd, p0, p1, 1, coatf, extend=0.4, t2=3)
        m.round_box(hd, 0, a["snout_front"] - 0.4, 1.0, 0.6, ey - 2.0, ey - 0.8, solid(P, "black"), cut=0)
        tb = m.bone("tail_fan", bd, (0, 10, 9))                                     # fan of nine tail feathers
        for i in range(9):
            ang = math.radians(-70 + i * 17.5)
            m.box(tb, -1.4, 10.0, 9.0, 1.4, 22.0 - abs(i - 4) * 0.8, 9.0, featherf,
                  rotation=(-20, 0, math.degrees(ang) * -1), pivot=(0, 10.0, 9.0))
        return m
    return build
