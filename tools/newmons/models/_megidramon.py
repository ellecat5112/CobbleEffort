"""Shared builder for Megidramon and Megidramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the evil dragon of the apocalypse: a crimson armoured dragon standing on a coiled serpent tail banded
red and white, a white ribcage over its chest, long gold-clawed arms, a horned fanged dragon head with a gold crest,
and great crimson bat wings whose membranes burn yellow and orange. The X-Antibody ("x"): darker crimson armour
bristling with black spikes, wings of pure translucent fire, a molten honeycomb-scaled tail and fire in its claws.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, jaws
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, scales, solid
from _route import pal, tone

LOOKS = {"base": {"red": (190, 30, 30), "red_dark": (100, 10, 14), "tail_band": (240, 236, 226)},
         "x": {"red": (150, 20, 24), "red_dark": (60, 6, 8), "tail_band": (250, 140, 30)}}
COMMON = {"gold": (240, 190, 60), "gold_dark": (160, 110, 20), "bone": (240, 236, 226), "bone_dark": (170, 164, 150),
          "black": (34, 30, 34), "eye": (250, 230, 60), "mouth": (110, 10, 20), "tooth": (250, 250, 240),
          "fire": (255, 150, 40, 215), "fire_core": (255, 236, 120, 235), "membrane": (240, 170, 40)}


def make(name, look="base"):
    x = look == "x"
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, red=(40, 40, 60), red_dark=(14, 14, 26), membrane=(120, 200, 255), fire=(90, 170, 255, 215),
                 fire_core=(220, 240, 255, 235))

    def P(v):
        return pal(base, shiny, v)

    ARM = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark")
    BONE = armour(P, "bone", "bone_dark")

    def tailf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x:
            if face != "down" and (abs((x_ * 0.8 + y * 0.5) % 2.2 - 1.1) < 0.2 or abs((x_ * 0.8 - y * 0.5) % 2.2 - 1.1)
                                   < 0.2):
                return p["tail_band"], p["tail_band"]
            return ARM(x_, y, z, face, variant, box=box, **k)
        if face == "down" or (face == "north" and abs(x_) < 3) or abs((y * 0.8 + z * 0.2) % 3.0 - 1.5) < 0.45:
            return tone(p["tail_band"], face), None
        return ARM(x_, y, z, face, variant, box=box, **k)

    def chestf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x_) < 4.6 and (abs(x_) < 0.6 or abs((y % 2.4) - 1.2) < 0.45):
            return tone(p["bone"], face), None
        return ARM(x_, y, z, face, variant, box=box, **k)

    def firef(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x_, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.35 else p["fire"]
        return c, c[:3]

    def memf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x_, y, z, face, box)
        t = v / max(H, 1e-6)
        c = p["membrane"] if t < 0.5 else p["fire"][:3] if t < 0.8 else p["red"]
        return tone(c, face), (c if t < 0.5 else None)

    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": chestf, "abs": chestf, "pelvis": ARM, "neck": ARM, "deltoid": GOLD,
                "upper_arm": ARM, "forearm": ARM, "hand": ARM, "finger": ARM, "claw": GOLD, "thigh": ARM, "knee": ARM,
                "shin": ARM, "calf": ARM, "foot": ARM, "talon": GOLD}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.0, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]     # a serpent below the waist
        m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 3.4, 3.6, 54.0, 61.0, ARM, cut=1)
        m.round_box(hd, 0, -6.0, 2.4, 3.0, 56.4, 59.4, ARM, cut=1)                    # snout
        jb = m.bone("jaw", hd, (0, 56, -2))
        m.round_box(jb, 0, -5.6, 2.0, 2.8, 54.4, 56.2, ARM, cut=0)
        m.box(jb, -1.6, 56.2, -8.2, 1.6, 56.4, -3.6, solid(P, "mouth"))
        for j in range(5):
            for sx in (-1, 1):
                spike(m, hd, (sx * 1.8, 56.4, -8.0 + j * 1.0), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.4, sx * 3.0), 59.0, -4.3, max(sx * 1.4, sx * 3.0), 60.0, -4.1,
                  solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.4, 60.4, -1.0), (sx * 0.6, 0.8, 0.8), 1.8, 9.0, GOLD, tip=0.8)   # gold horns
            spike(m, hd, (sx * 3.2, 58.0, 0.0), (sx * 1.0, 0.2, 0.6), 1.4, 6.0, GOLD, tip=0.8)
        spike(m, hd, (0, 61.0, -3.0), (0, 1, 0.6), 1.6, 5.0, GOLD, tip=0.8)                    # crest
        for sx in (-1, 1):                                                                       # shoulder spikes
            for j in range(3 if not x else 5):
                spike(m, bd, (sx * 7.4, 51.0, -1.0 + j * 1.2), (sx * 0.8, 1, 0.3 + j * 0.2), 1.4, 5.0 + j,
                      solid(P, "black") if x else GOLD, tip=0.8)
        if x:
            for nm in ("arm_left", "arm_right"):                                                 # fire in its claws
                hnd = a[nm]["hand"]
                for ang in (0, 90):
                    m.box(a[nm]["bone"], hnd[0] - 3.0, hnd[1] - 6.0, hnd[2] - 2.0, hnd[0] + 3.0, hnd[1] + 2.0,
                          hnd[2] - 2.0, cutout(flame_inside(4, 0.1, 3), firef), rotation=(0, ang, 0),
                          pivot=(hnd[0], hnd[1], hnd[2] - 2.0))
        wb = m.bone("wings", bd, (0, 48, 3))
        for side in (1, -1):                                                                     # great wings
            if not x:
                bat_wing(m, wb, (side * 4.0, 48.0, 3.0), 34.0, 26.0, 4, ARM, memf, side=side, sweep=20)
            else:
                for j in range(5):
                    ang = math.radians(10 + j * 18)
                    x0, x1 = sorted((side * 4.0, side * (34.0 - j * 3.0)))
                    m.box(wb, x0, 46.0, 4.0 + j * 0.5, x1, 54.0, 4.0 + j * 0.5,
                          cutout(flame_inside(5, side * 0.2, j + 1), firef),
                          rotation=(0, side * 15, side * (30 - j * 18)), pivot=(side * 4.0, 48.0, 4.0))
                    rod(m, wb, (side * 4.0, 48.0, 3.0), (side * 4.0 + side * 18.0 * math.cos(ang),
                                                          48.0 + 18.0 * math.sin(ang) - 6.0, 5.0 + j), 1,
                        solid(P, "black"), extend=0.2)
        tb = m.bone("tail", bd, (0, 30, 2))                                                      # coiled serpent tail
        pts = [(0, 33.0, 0.5)]
        for i in range(1, 16):
            t = i / 15
            ang = t * 2.0 * math.pi
            pts.append((8.0 * math.sin(ang), 28.0 - 24.0 * t + 4.0 * math.sin(ang * 0.5), 2.0 + 7.0 * (1 - math.cos(ang))))
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tb, p0, p1, max(2, 8 - j // 2), tailf, extend=0.6)
        spike(m, tb, pts[-1], (0, -0.2, -1), 1.6, 5.0, GOLD if not x else solid(P, "black"), tip=0.8)
        return m

    return build
