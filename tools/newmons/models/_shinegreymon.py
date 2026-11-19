"""Shared builder for Shine Greymon and its modes (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the light dragon of the Savers line: a tall dragon-man in white armour banded red with gold trim and a
horned golden dragon helm over an orange hide, a long tail, golden clawed gauntlets and talons, and eight great red
blade-wings fanned behind it tipped with glowing blue lights, a golden sun-wheel at its feet. Looks: "base"; "burst"
(Burst Mode: radiant red-and-white armour, wings of roaring orange-gold flame, a blazing flame sword in one hand and a
flame shield in the other); "ruin" (Ruin Mode: black armour streaked red, glowing red eyes, huge feathered wings of
smoky silver light and a dark vortex in its claw). Shiny: blue / violet / white.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, cutout, feathers, flame_inside, metal, skin, solid
from _route import pal, tone


def make(name, look="base"):
    ruin = look == "ruin"
    base = {"plate": (36, 34, 40) if ruin else (240, 240, 246), "plate_dark": (10, 10, 12) if ruin else (170, 172, 190),
            "red": (200, 30, 40), "red_dark": (110, 10, 16), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
            "hide": (240, 140, 40), "hide_dark": (170, 80, 20), "blue": (90, 200, 255), "eye": (250, 50, 50) if ruin
            else (60, 160, 250), "fire": (255, 160, 40, 220), "smoke": (210, 214, 236, 170), "vortex": (110, 120, 220)}
    shiny = {"red": (40, 70, 200), "red_dark": (14, 30, 120)} if look == "base" else (
        {"red": (130, 40, 200), "red_dark": (70, 14, 120), "fire": (200, 120, 255, 220)} if look == "burst" else
        {"plate": (230, 230, 240), "plate_dark": (150, 150, 170)})

    def P(v):
        return pal(base, shiny, v)

    def platef(x, y, z, face, variant, box=None, **k):
        if (y % 7.0) < 1.6:
            return armour(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)
        return armour(P, "plate", "plate_dark", trim="gold", trim_w=0.2)(x, y, z, face, variant, box=box, **k)

    GOLD = metal(P, "gold", dark="gold_dark")
    FIRE = cutout(flame_inside(tongues=4), solid(P, "fire", glow=True))

    def bladef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["red"] if face != "down" else p["red_dark"], face), None

    def build():
        m = Model(name)
        mats = {"skin": platef, "neck": skin(P, "hide", dark="hide_dark"), "upper_arm": skin(P, "hide", dark="hide_dark"),
                "thigh": skin(P, "hide", dark="hide_dark"), "hand": GOLD, "finger": GOLD, "claw": GOLD, "talon": GOLD}
        a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.6, 2.8, 4.0, 54.0, 60.0, GOLD, cut=1)                    # golden dragon helm
        m.round_box(hd, 0, -5.4, 1.6, 1.6, 54.0, 57.0, GOLD, cut=0)
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.7, sx * 2.9), 57.4, -4.0, max(sx * 2.7, sx * 2.9), 58.4, -2.6, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 60.0, -1.0), (sx * 0.4, 1, 0.5), 1.4, 7.0, GOLD, tip=0.8)
        wb = m.bone("wings", bd, (0, 50, 4))
        for sx in (-1, 1):
            for j in range(4):
                ang = math.radians(10 + j * 22)
                d = (sx * math.cos(ang), math.sin(ang), 0.4)
                if look == "base":                                                       # red blade-wings
                    spike(m, wb, (sx * 3.0, 50.0, 4.0 + j * 0.3), d, 2.0, 24.0 - j * 2.0, bladef, tip=0.8)
                    tip_ = (sx * 3.0 + d[0] * (24.0 - j * 2.0), 50.0 + d[1] * (24.0 - j * 2.0), 4.0 + j * 0.3 + 0.4 * 20)
                    m.box(wb, tip_[0] - 0.8, tip_[1] - 0.8, tip_[2] - 0.8, tip_[0] + 0.8, tip_[1] + 0.8, tip_[2] + 0.8,
                          solid(P, "blue", glow=True))
                elif look == "burst":                                                    # wings of flame
                    x0, x1 = sorted((sx * 3.0, sx * (30.0 - j * 3.0)))
                    m.box(wb, x0, 44.0, 4.0 + j * 0.4, x1, 58.0, 4.0 + j * 0.4, FIRE,
                          rotation=(0, -sx * 10, sx * (math.degrees(ang) - 30)), pivot=(sx * 3.0, 50.0, 4.0))
                else:                                                                    # smoky feathered wings
                    spike(m, wb, (sx * 3.0, 50.0, 4.0 + j * 0.3), d, 3.4, 26.0 - j * 2.0,
                          feathers(P, "smoke", "plate_dark"), tip=0.8)
        tl = m.bone("tail", bd, (0, 32, 3))
        pts = [(0, 32.0, 3.0), (2.0, 22.0, 12.0), (2.0, 12.0, 20.0), (0, 6.0, 26.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 4 - i, platef, extend=0.6)
        if look == "base":                                                               # golden sun-wheel
            for i in range(10):
                ang = 2 * math.pi * i / 10
                spike(m, tl, (0, 6.0, 26.0), (math.cos(ang), math.sin(ang), 0), 0.9, 4.0, GOLD, tip=0.8)
        if look == "burst":                                                              # flame sword + shield
            w = a["arm_right"]["wrist"]
            m.box(a["arm_right"]["bone"], w[0] - 0.8, w[1] - 30.0, w[2] - 2.0, w[0] + 0.8, w[1] - 2.0, w[2] - 0.4, FIRE,
                  rotation=(-15, 0, 0), pivot=(w[0], w[1], w[2]))
            w = a["arm_left"]["wrist"]
            m.box(a["arm_left"]["bone"], w[0] + 1.0, w[1] - 8.0, w[2] - 6.0, w[0] + 1.0, w[1] + 6.0, w[2] + 4.0, FIRE)
        if ruin:                                                                         # dark vortex
            h = a["arm_left"]["hand"]
            for i in range(10):
                ang = 2 * math.pi * i / 10
                r = 2.0 + i * 0.4
                m.box(a["arm_left"]["bone"], h[0] + 3.0, h[1] + r * math.sin(ang) - 0.6, h[2] + r * math.cos(ang) - 0.6,
                      h[0] + 3.6, h[1] + r * math.sin(ang) + 0.6, h[2] + r * math.cos(ang) + 0.6,
                      solid(P, "vortex", glow=True))
        return m

    return build
