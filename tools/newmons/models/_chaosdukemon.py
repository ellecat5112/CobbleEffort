"""Shared builder for Chaos Dukemon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the
fallen knight. Blackened Holy Knight armour with violet-grey edges, a tall helm trailing long black plume cords, a
great round black shield with a grey rim and engraved ring on its left arm, a long tapering black lance on its right,
and a tattered violet-black cape. make(core=True): Chaos Dukemon Core, the same knight rendered as a pale blue spectre
(its data core). Shiny: crimson armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, dome, humanoid
from _digidetail import armour, fabric, local, metal, solid
from _route import pal, tone

DARK = {"armour": (46, 44, 56), "armour_dark": (14, 14, 20), "armour_light": (120, 116, 140), "edge": (130, 120, 160),
        "cape": (50, 40, 90), "cape_dark": (16, 10, 36), "lance": (60, 60, 70), "lance_light": (150, 150, 170),
        "eye": (250, 60, 60), "under": (24, 24, 30)}
CORE = {"armour": (150, 170, 240), "armour_dark": (80, 100, 190), "armour_light": (220, 230, 255), "edge": (240, 244, 255),
        "cape": (120, 140, 230), "cape_dark": (70, 80, 180), "lance": (160, 180, 240), "lance_light": (240, 244, 255),
        "eye": (255, 255, 255), "under": (90, 110, 200)}
SHINY_DARK = {"armour": (140, 20, 30), "armour_dark": (60, 6, 10), "armour_light": (220, 90, 100)}
SHINY_CORE = {"armour": (240, 160, 200), "armour_dark": (190, 90, 140), "cape": (230, 120, 180)}


def make(name, core=False):
    base = CORE if core else DARK
    shiny = dict(base, **(SHINY_CORE if core else SHINY_DARK))

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "armour", "armour_dark", light="armour_light", trim="edge", trim_w=0.35,
                 glow_key="edge" if core else None)
    LANCE = metal(P, "lance", dark="armour_dark", light="lance_light")
    CAPE = fabric(P, "cape", "cape_dark", axis="y", period=3.0)

    def shieldf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        d = math.hypot(u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5) * 2
        if face in ("north", "south"):
            if d > 0.88 or 0.5 < d < 0.58:
                return tone(p["edge"], face), None
            if d < 0.16:
                return tone(p["armour_light"], face), None
        return ARM(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": solid(P, "under"), "chest": ARM, "abs": ARM, "pelvis": ARM, "deltoid": ARM, "upper_arm": ARM,
                "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": ARM, "knee": ARM, "shin": ARM, "calf": ARM,
                "foot": ARM, "toe": ARM}
        a = humanoid(m, mats, bulk=1.1, arm_bulk=1.05, leg_bulk=1.05, name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.8, 3.0, 54.0, 61.4, ARM, cut=1)
        m.box(hd, -2.0, 57.2, -3.3, 2.0, 57.8, -3.1, solid(P, "eye", glow=True))
        spike(m, hd, (0, 61.0, -1.0), (0, 1, 0.3), 1.6, 3.4, ARM)
        for sx in (-1, 1):                                             # long plume cords
            pts = [(sx * 1.2, 61.0, 1.0), (sx * 3.0, 66.0, 6.0), (sx * 6.0, 64.0, 14.0), (sx * 9.0, 56.0, 20.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, solid(P, "armour_dark"), extend=0.3)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            dome(m, a[nm]["bone"], (a[nm]["shoulder"][0] + sx * 1.6, 49.4, 0.3), 4.2, 4.0, ARM, layers=4)
        al = a["arm_left"]                                             # the great round shield
        h = al["hand"]
        sb = m.bone("shield", al["bone"], h)
        cx, cy, cz = h[0] + 2.0, h[1] + 6.0, h[2] - 3.0          # facing front, held before the left arm
        for fy, fx in ((1.0, 0.42), (0.92, 0.72), (0.72, 0.92), (0.42, 1.0)):
            m.box(sb, cx - 10.0 * fx, cy - 11.0 * fy, cz - 1.4, cx + 10.0 * fx, cy + 11.0 * fy, cz, shieldf)
        ar = a["arm_right"]                                            # the long lance
        h = ar["hand"]
        lb = m.bone("lance", ar["bone"], h)
        m.round_box(lb, h[0], h[2], 2.8, 2.8, h[1] - 1.0, h[1] + 1.4, ARM, cut=1)
        steps = 6
        tip = (h[0] - 4.0, h[1] - 34.0, h[2] - 14.0)
        for i in range(steps):
            p0 = tuple(a0 + (b0 - a0) * i / steps for a0, b0 in zip(h, tip))
            p1 = tuple(a0 + (b0 - a0) * (i + 1) / steps for a0, b0 in zip(h, tip))
            rod(m, lb, p0, p1, max(1, round(5 * (1 - i / steps))), LANCE, extend=0.3)
        cb = m.bone("cap", bd, (0, 52, 3))
        cape(m, cb, 52.0, 22.0, 50.0, CAPE, z=4.4, flare=1.2, panels=9, sweep=(0, 10), seed=8)
        return m
    return build
