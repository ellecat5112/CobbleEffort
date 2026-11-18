"""Shared builder for Prince Mamemon and Prince Mamemon (X-Antibody) (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the little prince of the Mamemon: a round yellow ball of a face with a smug grin and
spiral pink cheeks, a jewelled golden crown on a cushion of ermine, a royal-blue suit with gold epaulettes, white
gloves, red-topped boots, and a great red cape lined grey and trimmed in ermine. X-Antibody: big round blue eyes and a
cheeky grin, a tall red crown, a vast red-and-white ermine robe, a long green sceptre topped by a golden orb, black
boots and a gold tassel. Shiny: silver face.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape
from _digidetail import fabric, fur, gem, leather, metal, solid
from _route import pal, tone

BASE = {"yellow": (250, 220, 50), "yellow_dark": (210, 160, 20), "black": (24, 20, 20), "white": (252, 252, 252),
        "spiral": (240, 120, 150), "mouth": (200, 60, 80), "gold": (236, 196, 70), "gold_dark": (150, 110, 20),
        "blue": (40, 60, 160), "blue_dark": (16, 24, 90), "red": (200, 30, 40), "red_dark": (110, 10, 16),
        "grey": (190, 190, 200), "ermine": (250, 250, 255), "ermine_dark": (200, 200, 214), "gem": (40, 180, 90),
        "gem_red": (220, 40, 60), "eye": (70, 120, 220), "green": (40, 140, 90), "boot": (30, 28, 34)}
SHINY = {"yellow": (220, 224, 236), "yellow_dark": (150, 154, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ERMINE = fur(P, "ermine", "ermine_dark", length=0.8, density=1.2)
GOLD = metal(P, "gold", dark="gold_dark")


def make(name, x=False):
    def facef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                if x:
                    d = math.hypot(xx - sx * 2.0, (y - 23.0) * 0.8)
                    if d < 0.6:
                        return tone(p["black"], face), None
                    if d < 1.6:
                        return tone(p["eye"] if d < 1.1 else p["white"], face), None
                else:
                    if abs(xx - sx * 2.0) < 1.0 and abs(y - 23.0 + (xx * sx - 2.0) * 0.3) < 0.35:
                        return tone(p["black"], face), None
                    d = math.hypot(xx - sx * 4.2, y - 20.6)
                    if d < 1.2 and int(d * 3) % 2 == 0:
                        return tone(p["spiral"], face), None
            if 18.0 < y < 19.6 and abs(xx) < 2.0 - (19.6 - y) * 0.6 and (xx > -0.6 or not x):
                return tone(p["mouth"], face), None
        return tone(p["yellow"] if face != "down" else p["yellow_dark"], face), None

    def capef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x:
            return tone(p["ermine"] if (math.sin(xx * 1.3) * math.sin(y * 1.1) > 0.85) else p["red"], face), None
        return tone(p["grey"] if face == "north" else p["red"], face), None

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0, 3.6, 3.0, 8.0, 14.0, fabric(P, "blue", "blue_dark", axis="y"), cut=1)
        hd = m.bone("head", bd, (0, 14, 0))
        ball(m, hd, (0, 21.0, -0.6), 6.4, facef, layers=5)                              # round yellow face
        m.round_box(hd, 0, 0, 3.6, 3.6, 26.4, 28.0, ERMINE, cut=1)                       # ermine band
        if x:
            m.round_box(hd, 0.6, 0, 3.8, 3.8, 28.0, 32.0, fabric(P, "red", "red_dark", axis="y"), cut=1)
        for i in range(5):                                                               # crown points
            ang = 2 * math.pi * i / 5
            spike(m, hd, (2.8 * math.cos(ang), 28.0 if not x else 31.6, 2.8 * math.sin(ang)), (0, 1, 0), 1.2, 3.0,
                  GOLD, tip=0.8)
            ball(m, hd, (2.8 * math.cos(ang), (31.0 if not x else 34.6), 2.8 * math.sin(ang)), 0.6,
                 gem(P, "gem_red", "white"), layers=1)
        m.round_box(hd, 0, 0, 3.0, 3.0, 28.0, 29.4, GOLD, cut=1)
        m.box(hd, -0.8, 27.4, -3.6, 0.8, 28.6, -3.2, gem(P, "gem", "white"))
        for sx in (-1, 1):                                                               # gold epaulettes
            m.round_box(bd, sx * 3.8, 0, 1.6, 2.0, 12.6, 14.0, GOLD, cut=0)
            for j in range(3):
                m.box(bd, sx * 3.8 + (j - 1) * 0.8 - 0.2, 11.0, -1.4, sx * 3.8 + (j - 1) * 0.8 + 0.2, 12.6, -1.0, GOLD)
        cape(m, bd, 14.6, 12.0, 14.0 if not x else 16.0, capef, z=3.0, flare=1.6 if not x else 2.2, panels=6, seed=5)
        m.round_box(bd, 0, 0.6, 5.4, 3.8, 13.4, 15.2, ERMINE, cut=1)                      # ermine collar
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 3.6, 13.0, 0))
            rod(m, ab, (sx * 3.6, 13.0, 0), (sx * 6.6, 10.0, -2.0), 1, fabric(P, "blue", "blue_dark", axis="x"),
                extend=0.2, t2=2)
            ball(m, ab, (sx * 7.4, 9.6, -2.4), 1.8, solid(P, "white"), layers=2)
            m.round_box(ab, sx * 6.6, -2.0, 1.4, 1.4, 9.4, 10.6, ERMINE, cut=0)
        if x:                                                                            # sceptre
            rod(m, "arm_right", (-7.4, 9.6, -2.4), (-9.0, -1.0, -4.0), 1, solid(P, "green"), extend=0.4)
            rod(m, "arm_right", (-7.4, 9.6, -2.4), (-6.0, 18.0, -1.0), 1, solid(P, "green"), extend=0.4)
            ball(m, "arm_right", (-6.0, 19.6, -1.0), 1.8, GOLD, layers=2)
            rod(m, "arm_right", (-6.6, 12.0, -1.6), (-5.0, 6.0, -3.0), 1, GOLD, extend=0.2)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 1.8, 8.0, 0))
            m.round_box(lg, sx * 1.8, 0, 1.2, 1.2, 3.0, 8.4, fabric(P, "blue", "blue_dark", axis="y"), cut=0)
            m.round_box(lg, sx * 1.8, -0.6, 1.6, 2.2, 0.0, 4.0, leather(P, "boot", "black"), cut=0)
            if not x:
                m.round_box(lg, sx * 1.8, 0, 1.8, 1.8, 3.6, 4.6, solid(P, "red"), cut=0)
        return m

    return build
