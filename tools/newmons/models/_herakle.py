"""Shared builder for Herakle Kabuterimon and Herakle Kabuterimon (X-Antibody) (CobbleEffort: Digital; hand-built after
the official art on wikimon.net): the great Hercules beetle: a towering olive-gold armoured insect standing upright,
a great curved horn sweeping up from its head with a second over its back, four clear wings, four arms with heavy
clawed hands, red joints and spiked legs. X-Antibody: bright gold with red-orange wings, holding a radiant golden orb.
Shiny: blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, gem, local, metal, solid
from _route import pal, tone


def make(name, x=False):
    base = {"shell": (190, 180, 110) if not x else (240, 200, 50), "shell_dark": (120, 110, 50) if not x else (170, 120, 10),
            "shell_light": (230, 220, 160) if not x else (255, 240, 150), "red": (200, 50, 40),
            "wing": (200, 230, 250, 110) if not x else (250, 120, 40, 150), "vein": (120, 140, 160, 200),
            "eye": (230, 40, 40), "orb": (255, 220, 80), "orb_light": (255, 255, 220)}
    shiny = {"shell": (70, 110, 200), "shell_dark": (24, 50, 130), "shell_light": (150, 180, 250)}

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "shell", "shell_dark", light="shell_light", trim="red", trim_w=0.25)

    def wingf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        if (u % 3.0) < 0.3 or abs(v - H * 0.5) < 0.25:
            return p["vein"], None
        return p["wing"], None

    def build():
        m = Model(name)
        mats = {"skin": ARM, "claw": metal(P, "shell_dark"), "talon": metal(P, "shell_dark")}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.1, claws=True, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, -1))
        m.round_box(hd, 0, -1.4, 3.0, 3.6, 53.0, 59.6, ARM, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.0, sx * 2.6), 56.6, -5.1, max(sx * 1.0, sx * 2.6), 57.6, -4.9, solid(P, "eye", glow=True))
        pts = [(0, 58.0, -3.0), (0, 66.0, -8.0), (0, 74.0, -6.0), (0, 78.0, -1.0)]               # great curved horn
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 3 - j // 2, metal(P, "shell", dark="shell_dark"), extend=0.4)
        pts = [(0, 52.0, 4.0), (0, 62.0, 10.0), (0, 66.0, 6.0)]                                 # back horn
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 2, metal(P, "shell", dark="shell_dark"), extend=0.4)
        for side in (1, -1):
            for j in range(2):
                x0, x1 = sorted((side * 4.0, side * (24.0 - j * 4.0)))
                m.box(bd, x0, 46.0 - j * 4.0, 5.0 + j, x1, 50.0 - j * 4.0, 5.0 + j, wingf,
                      rotation=(0, side * 20, side * (20 - j * 30)), pivot=(side * 4.0, 48.0 - j * 4.0, 5.0))
        for sx in (-1, 1):                                                                       # second pair of arms
            ab = m.bone("arm2_" + ("left" if sx > 0 else "right"), bd, (sx * 6.0, 40.0, -1.0))
            rod(m, ab, (sx * 6.0, 40.0, -1.0), (sx * 12.0, 34.0, -5.0), 3, ARM, extend=0.4)
            for j in range(3):
                spike(m, ab, (sx * 12.0 + (j - 1) * 1.2, 33.0, -6.0), (sx * 0.3, -0.5, -1), 1.0, 4.0, ARM, tip=0.8)
        if x:
            h = a["arm_right"]["hand"]
            m.round_box(a["arm_right"]["bone"], h[0], h[2] - 2.0, 3.0, 3.0, h[1] + 8.0, h[1] + 14.0, gem(P, "orb", "orb_light"),
                        cut=1)
        return m

    return build
