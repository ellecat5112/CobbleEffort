"""Shared builder for Metal Garurumon and its colour variants (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): Garurumon rebuilt as a war machine: a powerful wolf of blue-grey steel plates with ball joints, a
gold-trimmed armoured muzzle with red eyes, a yellow armoured back with missile hatches, two swept wing-blades on its
back trailing yellow light, a long blade on its tail, red missile pods on its haunches, and huge pink-red claws.
Looks: "base"; "black" (gunmetal black plates, white claws); "red" (crimson plates, the old pixel-sprite colours).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digidetail import armour, local, metal, solid
from _route import pal, tone

LOOKS = {"base": {"plate": (130, 140, 200), "plate_dark": (60, 66, 120), "claw": (230, 60, 110)},
         "black": {"plate": (70, 70, 78), "plate_dark": (26, 26, 30), "claw": (236, 236, 240)},
         "red": {"plate": (210, 50, 40), "plate_dark": (120, 16, 14), "claw": (250, 220, 90)}}
COMMON = {"gold": (240, 200, 70), "gold_dark": (160, 120, 20), "joint": (90, 94, 110), "steel": (220, 224, 236),
          "steel_dark": (110, 114, 126), "eye": (250, 50, 50), "mouth": (130, 20, 40), "tooth": (250, 250, 246),
          "pod": (230, 70, 40), "light": (255, 250, 120, 190), "light_core": (255, 255, 220, 230)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, **({"plate": (230, 230, 240), "plate_dark": (150, 150, 170)} if look != "red"
                          else {"plate": (60, 160, 90), "plate_dark": (20, 80, 40)}), gold=(90, 200, 250))

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "plate", "plate_dark", trim="joint", trim_w=0.25, rivets=True)
    GOLD = armour(P, "gold", "gold_dark", trim="plate_dark", trim_w=0.25)
    STEEL = metal(P, "steel", dark="steel_dark")

    def lightf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p["light_core"] if u / max(W, 1e-6) < 0.3 else p["light"]
        return c, c[:3]

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "claw")}
        a = quadruped(m, mats, name, length=30.0, body_y=17.0, body_rx=6.2, body_ry=5.8, chest_bulk=1.35,
                      neck=((0, 21, -13), (0, 24, -17)), head_len=11.0, head_w=3.6, head_h=4.0, snout=0.9,
                      mouth_open=14, teeth=6, leg_bulk=1.5, toes=4,
                      tail=((0, 20, 15), (0, 21, 20), (0, 22, 25)), tail_r=(1.8, 1.4, 1.2))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.6, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, ey + 3.0, ez + 2.0), (sx * 0.4, 1, 0.6), 1.8, 4.6, GOLD, tip=0.8)   # ear fins
        hc = a["head_c"]
        m.round_box(hd, 0, hc[2] - 2.0, 2.6, 4.0, ey + 0.6, ey + 2.4, GOLD, cut=1)                  # gold muzzle plate
        m.round_box(bd, 0, -4.0, 4.6, 7.0, 21.0, 24.0, GOLD, cut=1)                               # yellow back armour
        for sx in (-1, 1):
            for j in range(3):                                                                 # missile hatches
                m.box(bd, min(sx * 4.7, sx * 4.9), 21.6, -8.0 + j * 2.6, max(sx * 4.7, sx * 4.9), 23.0,
                      -6.6 + j * 2.6, solid(P, "plate_dark"))
            ball(m, bd, (sx * 6.4, 18.0, 9.0), 3.0, solid(P, "pod"), layers=3, squash=1.3)        # haunch pods
            wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 2.0, 23.0, -2.0))
            root = (sx * 2.0, 23.5, -2.0)
            tip = (sx * 9.0, 33.0, 4.0)
            rod(m, wb, root, tip, 2, STEEL, extend=0.4, t2=3)                                  # swept wing-blade
            spike(m, wb, tip, (sx * 0.6, 0.8, 0.5), 1.6, 3.0, GOLD, tip=0.8)
            for ang in (0, 90):                                                                # trailing light
                x0, x1 = sorted((tip[0], tip[0] + sx * 12.0))
                m.box(wb, x0, tip[1] - 1.4, tip[2], x1, tip[1] + 1.4, tip[2], lightf,
                      rotation=(ang, 0, sx * 35), pivot=tip)
        tp = a["tail_pts"][-1]
        rod(m, a["tail"], tp, (tp[0], tp[1] + 1.0, tp[2] + 10.0), 1, STEEL, extend=0.2, t2=3)   # tail blade
        spike(m, a["tail"], (tp[0], tp[1] + 1.0, tp[2] + 10.0), (0, 0, 1), 1.6, 3.0, STEEL, tip=0.8)
        for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):    # ball joints
            anc = a[nm]
            j = anc.get("elbow") or anc.get("knee")
            if j:
                ball(m, anc["bone"], j, 1.8, solid(P, "joint"), layers=2)
        return m

    return build
