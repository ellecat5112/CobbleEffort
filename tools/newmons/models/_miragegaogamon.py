"""Shared builder for Mirage Gaogamon and Mirage Gaogamon: Burst Mode (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the wolf knight: a tall warrior in deep blue armour trimmed gold with star crests, a
wolf-head helm with two swept steel horns, huge gauntlets whose knuckles are a wolf's jaws, a long red cape, a blue
tail and clawed armoured feet. Burst Mode ("burst"): silver-white armour, a mane of white blade-feathers, golden
energy blades flaring from its gauntlets and a crescent of golden light behind it.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

LOOKS = {"base": {"plate": (40, 70, 170), "plate_dark": (14, 26, 90), "plate_light": (110, 140, 230)},
         "burst": {"plate": (220, 224, 236), "plate_dark": (130, 134, 150), "plate_light": (250, 250, 255)}}
COMMON = {"gold": (230, 190, 80), "gold_dark": (150, 110, 30), "red": (190, 30, 40), "red_dark": (100, 10, 16),
          "steel": (200, 204, 216), "steel_dark": (96, 100, 114), "eye": (250, 220, 60), "light": (255, 240, 120, 200),
          "light_core": (255, 255, 230, 235), "white": (246, 246, 250)}


def make(name, burst=False):
    base = dict(COMMON, **LOOKS["burst" if burst else "base"])
    shiny = dict(base, plate=(60, 60, 70), plate_dark=(24, 24, 30), plate_light=(130, 130, 150), gold=(200, 80, 220))

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "plate", "plate_dark", light="plate_light", trim="gold", trim_w=0.3)
    STEEL = metal(P, "steel", dark="steel_dark")

    def starf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and box is not None:
            u, v, W, H = local(x, y, z, face, box)
            du, dv = u - W / 2, v - H / 2
            ang = math.atan2(dv, du)
            if math.hypot(du, dv) < min(W, H) * (0.18 + 0.12 * abs(math.cos(ang * 2.5))):
                return tone(p["gold"], face), None
        return ARM(x, y, z, face, variant, box=box, **k)

    def lightf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["light_core"] if 0.35 < u / max(W, 1e-6) < 0.65 else p["light"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": starf, "deltoid": starf, "neck": STEEL, "upper_arm": STEEL, "thigh": ARM,
                "knee": starf, "claw": STEEL, "talon": STEEL}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        if not burst:
            cape(m, bd, 52.0, 16.0, 42.0, fabric(P, "red", "red_dark"), z=4.0, flare=1.0, panels=6, seed=5)
        else:
            for i in range(9):                                                         # white blade-feather mane
                ang = math.radians(-80 + i * 20)
                spike(m, bd, (5.0 * math.sin(ang), 52.0, 3.0), (math.sin(ang) * 0.6, 0.8, 0.6), 1.6, 10.0,
                      solid(P, "white"), tip=0.8)
            for j in range(9):                                                         # crescent of golden light
                ang = math.radians(-120 + j * 30)
                m.box(bd, 18.0 * math.sin(ang) - 2.0, 40.0 + 18.0 * math.cos(ang) - 1.0, 9.0,
                      18.0 * math.sin(ang) + 2.0, 40.0 + 18.0 * math.cos(ang) + 1.0, 9.0, lightf,
                      rotation=(0, 0, -math.degrees(ang)), pivot=(18.0 * math.sin(ang), 40.0 + 18.0 * math.cos(ang), 9.0))
        for sx in (-1, 1):
            m.round_box(bd, sx * 8.0, 0.0, 3.4, 3.6, 47.0, 53.0, starf, cut=1)           # big pauldrons
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 3.0, 3.4, 54.0, 60.0, ARM, cut=1)                       # wolf-head helm
        m.round_box(hd, 0, -5.6, 1.8, 2.6, 54.4, 57.4, ARM, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.2, sx * 2.6), 58.0, -4.5, max(sx * 1.2, sx * 2.6), 58.8, -4.3,
                  solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 59.6, -1.0), (sx * 0.4, 1, 0.8), 1.6, 9.0, STEEL, tip=0.8)   # swept horns
        for nm in ("arm_left", "arm_right"):                                            # wolf-jaw gauntlets
            anc = a[nm]
            w = anc["wrist"]
            sx = 1 if w[0] > 0 else -1
            m.round_box(anc["bone"], w[0], w[2] - 1.4, 3.4, 4.0, w[1] - 4.0, w[1] + 4.0, starf, cut=1)
            for j in range(4):
                spike(m, anc["bone"], (w[0] + (j - 1.5) * 1.4, w[1] - 4.0, w[2] - 4.6), (0, -0.4, -1), 1.0, 2.4,
                      STEEL, tip=0.8)
            if burst:                                                                   # golden energy blades
                for ang in (0, 90):
                    m.box(anc["bone"], w[0] - 1.6, w[1] - 4.0, w[2] - 22.0, w[0] + 1.6, w[1] - 4.0, w[2] - 4.0, lightf,
                          rotation=(0, 0, ang), pivot=(w[0], w[1] - 4.0, w[2] - 4.0))
        tb = m.bone("tail", bd, (0, 32, 3))                                             # blue tail
        pts = [(0, 32.0, 3.0), (2.0, 26.0, 9.0), (3.0, 20.0, 13.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 2, ARM, extend=0.4)
        return m

    return build
