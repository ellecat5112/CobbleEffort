"""Shared builder for the Sistermon sisters (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
nuns of the Digital World in long modest habits. Blanc: a white habit with gold crosses and a pink rabbit-eared hood,
long silver hair, pink feathered wings, white boots and a golden trident (Awakened: the trident blazing with light and
the pink wings spread wide). Ciel: a grey-white habit with clover marks and a pale-blue mouse-eared hood, long teal hair,
a black-lined cloak, grey boots and a long katana (Awakened: a golden lightning blade and torn cloak-wings). Noir: a
black habit with a white collar and cat-eared hood, long black hair, black boots and two silver pistols (Awakened:
cloak-wings flaring and a glowing card gun). Built covered: full-length habits. Shiny: inverted colours.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, feather_wing
from _digibody import cape, humanoid
from _digidetail import fabric, feathers, leather, metal, skin, solid, strands
from _route import pal, tone

SISTERS = {"blanc": {"habit": (248, 248, 252), "habit_dark": (200, 200, 214), "hood": (246, 190, 210),
                     "hair": (220, 220, 232), "hair_dark": (160, 160, 180), "mark": (230, 190, 70), "boot": (246, 246, 250)},
           "ciel": {"habit": (220, 222, 230), "habit_dark": (150, 152, 166), "hood": (150, 210, 230),
                    "hair": (80, 190, 190), "hair_dark": (30, 120, 120), "mark": (60, 60, 70), "boot": (170, 172, 186)},
           "noir": {"habit": (40, 38, 46), "habit_dark": (14, 12, 18), "hood": (40, 38, 46), "hair": (36, 34, 40),
                    "hair_dark": (12, 12, 16), "mark": (240, 240, 246), "boot": (30, 28, 34)}}
COMMON = {"skin": (250, 230, 220), "eye": (90, 110, 160), "white": (250, 250, 250), "gold": (236, 196, 70),
          "gold_dark": (150, 110, 20), "pink": (246, 180, 200), "pink_dark": (210, 120, 160), "steel": (210, 214, 226),
          "steel_dark": (110, 114, 130), "black": (24, 22, 28), "bolt": (255, 240, 120), "glow": (255, 250, 200)}


def make(name, who="blanc", awake=False):
    base = dict(COMMON, **SISTERS[who])
    inv = {"habit": base["habit_dark"], "habit_dark": base["habit"]} if who != "noir" else \
        {"habit": (230, 230, 240), "habit_dark": (170, 170, 186), "hood": (230, 230, 240)}
    shiny = dict(base, **inv)

    def P(v):
        return pal(base, shiny, v)

    HABIT = fabric(P, "habit", "habit_dark", axis="y", period=3.0)

    def blackf(x, y, z, face, variant, box=None, **k):
        return tone(P(variant)["black"], face), None

    def habitf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and y < 30.0 and abs((x % 4.0) - 2.0) < 0.5 and abs((y % 6.0) - 3.0) < 1.2 and \
                (abs((x % 4.0) - 2.0) < 0.2 or abs((y % 6.0) - 3.0) < 0.3):
            return tone(p["mark"], face), None
        return HABIT(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": habitf, "neck": skin(P, "skin"), "hand": skin(P, "skin"), "finger": skin(P, "skin"),
                "shin": leather(P, "boot", "habit_dark"), "calf": leather(P, "boot", "habit_dark"),
                "foot": leather(P, "boot", "habit_dark"), "knee": leather(P, "boot", "habit_dark")}
        a = humanoid(m, mats, bulk=0.72, arm_bulk=0.7, leg_bulk=0.75, name=name)
        bd = a["body"]
        for i in range(5):                                                               # long habit skirt
            r = 4.4 + i * 1.1
            m.round_box(bd, 0, 0.4, r, r * 0.85, 32.0 - (i + 1) * 3.6, 32.0 - i * 3.6 + 0.2, habitf,
                        cut=max(1, round(r * 0.3)))
        m.round_box(bd, 0, -0.2, 4.2, 3.4, 47.0, 51.0, solid(P, "white"), cut=1)          # collar
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.2, 2.4, 54.0, 59.6, skin(P, "skin"), cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.6), 57.0, -2.9, max(sx * 0.6, sx * 1.6), 57.8, -2.7, solid(P, "eye"))
        m.round_box(hd, 0, 0.6, 2.8, 2.8, 56.6, 61.0, solid(P, "hood"), cut=1)             # hood
        m.box(hd, -2.8, 46.0, 0.6, 2.8, 61.0, 3.2, solid(P, "hood"))
        m.box(hd, -2.4, 30.0 if who != "noir" else 36.0, 1.4, 2.4, 56.0, 3.6, strands(P, "hair", "hair_dark"))
        for sx in (-1, 1):                                                               # hood ears
            if who == "blanc":
                m.box(hd, sx * 2.6 - 0.8, 40.0, -0.6, sx * 2.6 + 0.8, 60.0, 1.6, solid(P, "hood"),
                      rotation=(0, 0, sx * 6), pivot=(sx * 2.6, 60.0, 0))
            elif who == "ciel":
                ball(m, hd, (sx * 2.4, 61.6, 0.6), 1.4, solid(P, "hood"), layers=2, squash=0.5)
            else:
                spike(m, hd, (sx * 1.8, 61.0, 0.6), (sx * 0.3, 1, 0), 1.4, 3.0, solid(P, "hood"), tip=0.8)
        w = a["arm_right"]["wrist"]
        ab = a["arm_right"]["bone"]
        if who == "blanc":                                                               # golden trident + wings
            rod(m, ab, (w[0], 2.0, w[2] - 2.0), (w[0], 68.0, w[2] - 2.0), 1, metal(P, "gold", dark="gold_dark"), extend=0.2)
            for f in (-1, 0, 1):
                spike(m, ab, (w[0] + f * 2.0, 66.0, w[2] - 2.0), (f * 0.2, 1, 0), 0.9, 4.0,
                      solid(P, "glow" if awake else "gold", glow=awake), tip=0.8)
            m.box(ab, w[0] - 2.4, 65.0, w[2] - 2.6, w[0] + 2.4, 66.0, w[2] - 1.4, metal(P, "gold", dark="gold_dark"))
            for sx in (-1, 1):
                feather_wing(m, bd, (sx * 3.0, 48.0, 3.0), 18.0 if not awake else 28.0, 12.0, 5,
                             feathers(P, "pink", "pink_dark"), side=sx, sweep=20, droop=6.0 if not awake else -10.0)
        elif who == "ciel":                                                              # katana / lightning blade
            m.box(ab, w[0] - 0.4, w[1] - 30.0 if not awake else w[1] - 2.0, w[2] - 1.4, w[0] + 0.4,
                  w[1] - 2.0 if not awake else w[1] + 28.0, w[2] - 0.4,
                  solid(P, "bolt", glow=True) if awake else metal(P, "steel", dark="steel_dark"),
                  rotation=(-10, 0, 0), pivot=(w[0], w[1], w[2]))
            cape(m, bd, 52.0, 14.0, 44.0, blackf,
                 z=4.0, flare=1.6 if not awake else 3.0, panels=6, seed=4)
        else:                                                                            # silver pistols
            for side in ("arm_left", "arm_right"):
                ww = a[side]["wrist"]
                m.box(a[side]["bone"], ww[0] - 0.5, ww[1] - 4.0, ww[2] - 6.0, ww[0] + 0.5, ww[1] - 1.6, ww[2] - 0.4,
                      metal(P, "steel", dark="steel_dark"))
            if awake:
                cape(m, bd, 52.0, 16.0, 40.0, blackf,
                     z=4.0, flare=3.0, panels=7, seed=6)
                m.box(ab, w[0] - 1.6, w[1] - 6.0, w[2] - 8.0, w[0] + 1.6, w[1] - 1.0, w[2] - 1.0, solid(P, "glow", glow=True))
        return m

    return build
