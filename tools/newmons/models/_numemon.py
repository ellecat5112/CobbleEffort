"""Shared builder for the Numemon-type slugs (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
a glossy blob of slime that pools out at its base into stubby lobes, two bloodshot eyes on long stalks, a huge gaping
mouth with a row of big square teeth and a long lolling pink tongue. Looks set the colours: Geremon (yellow with
brown spots), Gigantic Numemon (lime green with blue patches), Gold Numemon (molten gold), plus extras: golden
wings and a pearl necklace for the Gold Numemon.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digidetail import fbm, feathers, metal, skin, solid
from _route import pal, tone

LOOKS = {"geremon": {"slime": (250, 214, 50), "slime_dark": (200, 150, 20), "slime_light": (255, 245, 160),
                     "spot": (130, 80, 40)},
         "gigantic": {"slime": (150, 220, 60), "slime_dark": (90, 160, 20), "slime_light": (220, 255, 150),
                      "spot": (60, 80, 200)},
         "gold": {"slime": (240, 190, 50), "slime_dark": (170, 120, 20), "slime_light": (255, 240, 160),
                  "spot": (200, 140, 30)}}
COMMON = {"white": (250, 250, 246), "iris": (200, 30, 40), "pupil": (20, 16, 16), "mouth": (60, 14, 24),
          "tooth": (250, 250, 240), "tongue": (240, 90, 130), "tongue_dark": (170, 40, 90), "gold": (250, 210, 60),
          "gold_dark": (170, 120, 20), "gem": (220, 30, 60)}


def make(name, look, crown=False, shiny_look=None, wings=False):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(COMMON, **(shiny_look or {"slime": (120, 120, 140), "slime_dark": (60, 60, 76),
                                           "slime_light": (200, 200, 220), "spot": (40, 40, 50)}))

    def P(v):
        return pal(base, shiny, v)

    SLIME0 = metal(P, "slime", dark="slime_dark", light="slime_light") if look == "gold" else \
        skin(P, "slime", dark="slime_dark", light="slime_light")

    def slimef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if look != "gold" and fbm(x * 0.35, y * 0.35, z * 0.35, seed=5) > 0.68:
            return tone(p["spot"], face), None
        return SLIME0(x, y, z, face, variant, box=box, **k)

    def eyef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            cx = box.lo[0] + box.size[0] / 2
            cy = box.lo[1] + box.size[1] / 2
            d = math.hypot(x - cx, y - cy)
            if d < 0.5:
                return tone(p["pupil"], face), None
            if d < 1.1:
                return tone(p["iris"], face), None
        return tone(p["white"], face), None

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 6, 0))
        for i, (r, y0, y1) in enumerate(((11.0, 0.0, 3.0), (9.6, 2.6, 8.0), (8.4, 7.6, 14.0), (7.0, 13.6, 19.0),
                                         (5.0, 18.6, 22.0))):
            m.round_box(bd, 0, 0.4, r, r * 0.85, y0, y1, slimef, cut=max(1, int(r * 0.35)))
        for j in range(6):                                                         # pooling lobes
            ang = 2 * math.pi * j / 6 + 0.3
            m.round_box(bd, 10.0 * math.cos(ang), 10.0 * math.sin(ang) * 0.8, 2.6, 2.6, 0.0, 2.4, slimef, cut=1)
        m.box(bd, -6.0, 6.0, -8.4, 6.0, 15.0, -7.6, solid(P, "mouth"))              # huge gaping mouth
        for j in range(5):                                                         # big square teeth
            m.box(bd, -5.6 + j * 2.3, 12.6, -8.6, -4.0 + j * 2.3, 15.0, -8.0, solid(P, "tooth"))
        m.box(bd, -4.0, 6.2, -8.6, -2.0, 8.2, -8.0, solid(P, "tooth"))
        rod(m, bd, (1.0, 8.0, -8.4), (5.0, 2.0, -12.0), 3, skin(P, "tongue", dark="tongue_dark"), extend=0.4, t2=2)
        hd = m.bone("head", bd, (0, 21, -2))
        for sx in (-1, 1):                                                         # eyes on stalks
            rod(m, hd, (sx * 1.6, 20.0, -2.0), (sx * 3.4, 27.0, -3.0), 1, slimef, extend=0.2, t2=1)
            m.round_box(hd, sx * 3.4, -3.0, 2.0, 2.0, 26.6, 30.6, eyef, cut=1)
        if wings:                                                                  # golden wings + pearls
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 16.0, 4.0))
                feather_wing(m, wb, (side * 6.0, 16.0, 4.0), 22.0, 9.0, 3,
                             feathers(P, "gold", "gold_dark", size=(1.6, 2.8)), side=side, sweep=10, droop=-14.0)
            for j in range(9):
                ang = math.pi * (0.15 + 0.7 * j / 8)
                m.round_box(bd, 8.0 * math.cos(ang), -6.6 + 2.0 * math.sin(ang) - 2.0, 0.6, 0.6, 15.0, 16.2,
                            solid(P, "white"), cut=0)
        if crown:
            m.round_box(hd, 0, 0.4, 3.2, 3.0, 21.4, 23.6, metal(P, "gold", dark="gold_dark"), cut=1)
            for j in range(5):
                spike(m, hd, ((j - 2) * 1.4, 23.4, -2.4), (0, 1, 0), 1.0, 2.0, metal(P, "gold", dark="gold_dark"))
            m.round_box(hd, 0, -2.8, 0.7, 0.3, 22.0, 23.0, solid(P, "gem"), cut=0)
        return m

    return build
