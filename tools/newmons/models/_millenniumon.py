"""Builder for Millenniumon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the fusion of
Kimeramon and Mugendramon: a hulking black chimera dragon crouched on long clawed limbs, red-striped hide, a fanged
dragon head with red eyes, extra black claw-arms with red talons, and Mugendramon's two great steel cannons mounted on
its back, wreathed in yellow light.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, theropod
from _digidetail import armour, metal, scales, solid
from _route import pal, tone

BASE = {"hide": (40, 38, 46), "hide_dark": (14, 12, 18), "stripe": (180, 30, 40), "eye": (240, 40, 40),
        "steel": (200, 204, 216), "steel_dark": (96, 100, 114), "red": (210, 30, 40), "mouth": (130, 20, 30),
          "tooth": (250, 250, 240), "glow": (255, 240, 130, 170), "gold": (240, 200, 70)}


def make(name):
    base = dict(BASE)
    shiny = dict(base, hide=(200, 200, 210), hide_dark=(120, 120, 130))

    def P(v):
        return pal(base, shiny, v)

    HIDE0 = scales(P, "hide", "hide_dark", size=1.6)
    STEEL = metal(P, "steel", dark="steel_dark")

    def hidef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face != "down" and abs(((y * 0.5 + z * 0.4) % 4.0) - 2.0) < 0.35:
            return tone(p["stripe"], face), None
        return HIDE0(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": hidef, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "red"),
                "talon": solid(P, "red")}
        a = theropod(m, mats, name, hip_y=18.0, chest=(0, 28.0, -6.0), body_r=6.6, chest_r=6.4,
                     neck_top=(0, 34.0, -12.0), head_len=11.0, head_w=4.2, head_h=4.4, mouth_open=22, teeth=7,
                     arm_len=12.0, arm_bulk=1.4, fingers=3, leg_bulk=1.4, toes=3)
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.5, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.5,
                  ez + 0.8, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.6, ey + 2.6, ez + 3.0), (sx * 0.4, 0.6, 1), 1.6, 6.0, solid(P, "hide_dark"), tip=0.8)
        for sx in (-1, 1):                                                             # extra claw-arms
            for j in range(2):
                sh = (sx * 6.0, 24.0 - j * 3.0, -2.0 + j * 2.0)
                el = (sx * 11.0, 20.0 - j * 3.0, -6.0 + j * 2.0)
                rod(m, bd, sh, el, 2, hidef, extend=0.4)
                for f in range(3):
                    spike(m, bd, el, (sx * 0.3, -1, -0.6 + f * 0.3), 1.0, 4.0, solid(P, "red"), tip=0.8)
        s = 1.0                                                                        # back cannons
        for sx in (-1, 1):
            root = (sx * 3.6, 30.0, 2.0)
            tip = (sx * (3.6 + 4.0 * s), 30.0 + 14.0 * s, 2.0 - 12.0 * s)
            rod(m, bd, root, tip, max(2, round(6 * s)), STEEL, extend=0.6)
            ball(m, bd, root, 3.4 * s + 0.8, STEEL, layers=3)
            m.round_box(bd, tip[0], tip[2] - 0.6, 2.4 * s + 0.6, 1.2, tip[1] - 2.0 * s, tip[1] + 2.0 * s,
                        solid(P, "glow", glow=True), cut=0)
        return m

    return build
