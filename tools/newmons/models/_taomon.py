"""Shared builder for Taomon and Taomon (Silver) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a tall fox onmyoji: a black-and-white fox-mask hood with tall ears and a golden fringe, a white
underrobe, a violet over-robe with huge flared sleeves trimmed white and red, a yin-yang mark on the chest, white
furred legs with black claws, a great golden fox tail, a giant calligraphy brush, and red ofuda talismans fluttering
round it. Silver: the robe turns silver-grey and the ofuda burn gold-red. Shiny: crimson robe."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, plane, solid
from _route import pal, tone

COMMON = {"white": (244, 244, 246), "white_dark": (190, 190, 200), "black": (30, 28, 34), "gold": (240, 196, 60),
          "gold_dark": (180, 120, 20), "red": (200, 30, 30), "red_dark": (120, 10, 10), "ofuda": (190, 30, 30),
          "ink": (30, 10, 10), "tail": (246, 200, 70), "tail_dark": (200, 140, 30), "eye": (60, 160, 230),
          "brush": (110, 70, 40)}
ROBES = {False: {"robe": (110, 80, 170), "robe_dark": (60, 40, 110)},
         True: {"robe": (180, 184, 196), "robe_dark": (110, 114, 126)}}


def make(name, silver=False):
    base = dict(COMMON, **ROBES[silver])
    shiny = dict(COMMON, robe=(170, 40, 50), robe_dark=(100, 16, 24))

    def P(v):
        return pal(base, shiny, v)

    ROBE = fabric(P, "robe", "robe_dark")
    WHITE = fabric(P, "white", "white_dark")

    def chestf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(x, y, z, face)
            d = math.hypot(a, b - 46.0)
            if d < 3.0:
                yy = b - 46.0
                top = yy > 0 if a * 0 == 0 else True
                inner = math.hypot(a, yy - 1.5 * (1 if a < 0 else -1)) < 1.5
                dark = (a > 0) ^ inner
                if math.hypot(a, yy - 1.5) < 0.5:
                    dark = True
                if math.hypot(a, yy + 1.5) < 0.5:
                    dark = False
                return (p["black"] if dark else p["white"]), None
        return ROBE(x, y, z, face, variant, box=box, **k)

    def maskf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(x, y, z, face)
            for sx in (-1, 1):
                if math.hypot(a - sx * 1.6, b - 58.6) < 0.8:
                    return p["eye"], None
                if math.hypot(a - sx * 1.6, b - 58.6) < 1.5:
                    return p["black"], None
            if abs(a) < 0.6 and b < 57.0:
                return p["red"], None
        return tone(p["white"], face), None

    def ofudaf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("north", "south") and box is not None:
            u = x - box.lo[0] - box.size[0] / 2
            if abs(u) < 0.35 and int(y * 2) % 3 != 0:
                return p["ink"], None
        return tone(p["ofuda"], face), (p["gold"] if silver else None)

    def build():
        m = Model(name)
        mats = {"skin": WHITE, "chest": chestf, "abs": ROBE, "pelvis": ROBE, "deltoid": ROBE, "upper_arm": ROBE,
                "forearm": ROBE, "hand": fur(P, "white", "white_dark"), "thigh": ROBE, "knee": ROBE,
                "shin": fur(P, "white", "white_dark"), "calf": fur(P, "white", "white_dark"), "foot": WHITE,
                "talon": solid(P, "black"), "neck": WHITE}
        a = humanoid(m, mats, bulk=1.05, arm_bulk=1.0, leg_bulk=1.0, talons=True, name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                              # robe skirt panels
            m.box(bd, min(sx * 0.4, sx * 6.0), 14.0, -4.6, max(sx * 0.4, sx * 6.0), 31.0, -3.8, ROBE,
                  rotation=(-8, 0, sx * 6), pivot=(sx * 3.0, 31.0, -4.2))
        m.box(bd, -6.0, 16.0, 3.6, 6.0, 31.0, 4.4, ROBE)
        m.round_box(bd, 0, -0.2, 5.2, 3.8, 30.0, 32.0, solid(P, "red"), cut=1)          # sash
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # huge flared sleeves
            arm = a[nm]
            w = arm["wrist"]
            m.box(arm["bone"], w[0] - 3.6, w[1] - 3.0, w[2] - 3.6, w[0] + 3.6, w[1] + 7.0, w[2] + 3.6, ROBE)
            m.box(arm["bone"], w[0] - 3.8, w[1] - 4.0, w[2] - 3.8, w[0] + 3.8, w[1] - 3.0, w[2] + 3.8, WHITE)
            m.box(arm["bone"], w[0] - 3.9, w[1] - 4.8, w[2] - 3.9, w[0] + 3.9, w[1] - 4.0, w[2] + 3.9, solid(P, "red"))
        hd = m.bone("head", bd, (0, 55, 0))                                             # fox-mask hood
        m.round_box(hd, 0, 0, 3.4, 3.6, 54.0, 62.0, solid(P, "black"), cut=1)
        m.round_box(hd, 0, -1.6, 2.6, 2.4, 54.6, 61.0, maskf, cut=1)
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.4, 61.6, 0.4), (sx * 0.35, 1, 0.1), 2.2, 7.0, solid(P, "black"), tip=0.8)
            spike(m, hd, (sx * 2.4, 61.6, 0.0), (sx * 0.35, 1, 0.1), 1.0, 5.0, solid(P, "white"), tip=0.8)
        for j in range(5):
            m.box(hd, -2.6 + j * 1.1, 61.0, -3.9, -1.8 + j * 1.1, 63.4, -3.4, solid(P, "gold"))
        tl = m.bone("tail", bd, (0, 30, 4))                                             # golden fox tail
        pts = [(0, 30.0, 4.6), (3.0, 24.0, 10.0), (8.0, 22.0, 14.0), (12.0, 28.0, 16.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 4 - i, fur(P, "tail", "tail_dark"), extend=1.0)
        ball(m, tl, pts[-1], 2.0, solid(P, "white"), layers=2)
        h = a["arm_right"]["hand"]                                                      # giant brush
        rbn = a["arm_right"]["bone"]
        rod(m, rbn, (h[0], h[1] + 10.0, h[2]), (h[0], h[1] - 10.0, h[2]), 1, solid(P, "brush"), extend=0.0)
        m.round_box(rbn, h[0], h[2], 1.4, 1.4, max(0.4, h[1] - 16.0), h[1] - 10.0, solid(P, "black"), cut=0)
        ob = m.bone("ofuda", bd, (0, 40, 0))                                            # floating ofuda
        for i in range(8):
            ang = i * 2 * math.pi / 8
            r = 13.0 + (i % 2) * 2.0
            cx, cz = r * math.cos(ang), r * math.sin(ang)
            cy = 24.0 + (i % 3) * 9.0
            m.box(ob, cx - 1.2, cy, cz - 0.1, cx + 1.2, cy + 6.0, cz + 0.1, ofudaf,
                  rotation=(0, -math.degrees(ang) + 90, 0), pivot=(cx, cy, cz))
        return m
    return build
