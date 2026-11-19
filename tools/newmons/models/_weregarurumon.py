"""Shared builder for Were Garurumon and its forms (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the wolf-man: a muscular white-furred wolf standing upright, striped with blue, a shaggy mane, blue
ripped jeans marked with a skull, a brown leather shoulder pad and belts, spiked wrist bands, gloved fists, and huge
clawed wolf feet. Looks: "base"; "black" (charcoal fur, camouflage trousers); "x" (X-Antibody: a towering wolf in
heavy blue-steel armour plates with a fan of blade-spines at its back and long claws); "sagittarius" (Sagittarius
Mode: sleek blue armour, a great crossbow-gauntlet and blades of ice-blue light fanned behind it). Shiny: gold fur."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, fabric, fur, leather, metal, plane, solid, strands
from _route import pal, tone

LOOKS = {"base": {"fur": (236, 236, 246), "fur_dark": (150, 150, 190), "stripe": (80, 90, 190), "jeans": (70, 90, 170),
                  "jeans_dark": (30, 40, 110)},
         "black": {"fur": (70, 70, 78), "fur_dark": (24, 24, 30), "stripe": (30, 30, 36), "jeans": (90, 110, 70),
                   "jeans_dark": (50, 60, 30)},
         "x": {"fur": (200, 200, 230), "fur_dark": (110, 110, 160), "stripe": (60, 70, 170), "jeans": (60, 70, 110),
               "jeans_dark": (24, 30, 60)},
         "sagittarius": {"fur": (120, 150, 230), "fur_dark": (50, 70, 160), "stripe": (30, 40, 120), "jeans": (40, 40, 50),
                         "jeans_dark": (14, 14, 18)}}
COMMON = {"leather": (130, 90, 50), "leather_dark": (70, 44, 20), "gold": (230, 186, 60), "claw": (190, 60, 110),
          "steel": (170, 180, 210), "steel_dark": (70, 80, 120), "skull": (246, 246, 240), "eye": (250, 220, 60),
          "ice": (150, 220, 255, 190), "glove": (60, 56, 60)}
SHINY = {"fur": (240, 210, 120), "fur_dark": (190, 150, 60), "stripe": (180, 110, 30)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])

    def P(v):
        return pal(base, SHINY, v)

    def furf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west", "north", "south") and (y * 0.6 + abs(x) * 0.4) % 5.0 < 0.6:
            return tone(p["stripe"], face), None
        return fur(P, "fur", "fur_dark", length=1.4)(x, y, z, face, variant, box=box, **k)

    def jeansf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if look in ("base", "black") and face == "north" and box is not None and \
                math.hypot(x - (box.lo[0] + box.size[0] / 2), y - 22.0) < 1.4:
            return tone(p["skull"], face), None
        if look == "black" and math.sin(x * 0.9 + z) * math.cos(y * 0.8) > 0.4:
            return tone(p["jeans_dark"], face), None
        return fabric(P, "jeans", "jeans_dark")(x, y, z, face, variant, box=box, **k)

    ARM = armour(P, "steel", "steel_dark", panel=(3.0, 3.0))

    def build():
        m = Model(name)
        heavy = look in ("x", "sagittarius")
        mats = {"skin": furf, "chest": ARM if heavy else furf, "abs": furf, "pelvis": jeansf, "deltoid": furf,
                "upper_arm": furf, "forearm": ARM if heavy else furf, "hand": solid(P, "glove"),
                "finger": solid(P, "glove"), "claw": solid(P, "claw"), "thigh": jeansf, "knee": jeansf,
                "shin": ARM if heavy else furf, "calf": furf, "foot": furf, "talon": solid(P, "claw"), "neck": furf}
        a = humanoid(m, mats, bulk=1.25 if look != "x" else 1.4, arm_bulk=1.3, leg_bulk=1.2, digitigrade=True,
                     claws=True, talons=True, name=name)
        bd = a["body"]
        if not heavy:
            m.round_box(bd, 7.6, 0, 3.6, 3.8, 47.0, 53.4, leather(P, "leather", "leather_dark"), cut=1)  # shoulder pad
            rod(m, bd, (-5.0, 51.0, -4.2), (5.0, 34.0, -4.4), 1, leather(P, "leather", "leather_dark"), extend=0.0)
            m.round_box(bd, 0, 0, 5.4, 4.0, 30.0, 32.0, leather(P, "leather", "leather_dark"), cut=1)
        for nm in ("arm_left", "arm_right"):                                            # spiked wrist bands
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 2.4, 2.4, w[1], w[1] + 2.0, metal(P, "gold"), cut=1)
            for j in range(4):
                ang = j * math.pi / 2
                spike(m, a[nm]["bone"], (w[0] + 2.2 * math.cos(ang), w[1] + 1.0, w[2] + 2.2 * math.sin(ang)),
                      (math.cos(ang), 0, math.sin(ang)), 0.8, 1.6, metal(P, "gold"), tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 3.2, 4.0, 54.0, 61.0, furf, cut=1)
        m.round_box(hd, 0, -5.6, 2.0, 2.0, 54.4, 57.6, furf, cut=1)                        # muzzle
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.4), 58.6, -4.4, max(sx * 0.8, sx * 2.4), 59.4, -4.0, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.4, 60.4, 0.6), (sx * 0.3, 1, 0.3), 1.6, 4.0, furf, tip=0.8)
        for j in range(9):                                                              # shaggy mane
            ang = (j - 4) * 0.4
            spike(m, hd, (math.sin(ang) * 3.0, 59.0, 2.4), (math.sin(ang) * 0.8, 0.2, 1), 1.8, 8.0,
                  strands(P, "fur", "fur_dark"), tip=0.8)
        if look == "x":                                                                 # fan of blade-spines
            for j in range(7):
                ang = (j - 3) * 0.35
                spike(m, bd, (math.sin(ang) * 4.0, 52.0, 4.0), (math.sin(ang), 0.8, 0.6), 2.0, 12.0, ARM, tip=0.8)
        if look == "sagittarius":
            h = a["arm_left"]["hand"]
            m.box(a["arm_left"]["bone"], h[0] - 8.0, h[1] - 0.8, h[2] - 2.0, h[0] + 8.0, h[1] + 0.8, h[2] - 1.0,
                  metal(P, "steel", dark="steel_dark"))                                 # crossbow limbs
            m.round_box(a["arm_left"]["bone"], h[0], h[2] - 2.0, 1.6, 4.0, h[1] - 1.6, h[1] + 1.6, ARM, cut=1)
            ib = m.bone("ice", bd, (0, 46, 4))
            for j in range(6):
                ang = (j - 2.5) * 0.4
                spike(m, ib, (0, 46.0, 4.0), (math.sin(ang), math.cos(ang), 0.4), 1.4, 22.0, solid(P, "ice", glow=True),
                      tip=0.8)
        tl = m.bone("tail", bd, (0, 30, 4))
        pts = [(0, 30.0, 4.0), (2.0, 22.0, 9.0), (4.0, 16.0, 13.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tl, p0, p1, 2, furf, extend=0.6)
        return m
    return build
