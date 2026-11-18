"""Shared builder for Lord Knightmon and Lord Knightmon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail
standard after the official art on wikimon.net): the rose Royal Knight: a slender knight in rose-pink armour with gold
trim, a sharp-crested helm, long golden ribbons streaming from its shoulders, a large golden oval shield with a blue
gem on its left arm, and long pointed greaves. X-Antibody: a crimson rose-shaped shield, a long rapier, and great
fanned wings of golden blade-feathers with cyan crystal tips. Shiny: ice blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, gem, local, metal, solid
from _route import pal, tone

BASE = {"pink": (230, 110, 160), "pink_dark": (140, 40, 90), "pink_light": (255, 190, 220), "gold": (240, 200, 90),
        "gold_dark": (160, 120, 30), "gold_light": (255, 240, 180), "blue": (80, 160, 240), "blue_light": (210, 240, 255),
        "rose": (210, 40, 80), "rose_dark": (120, 10, 40), "eye": (90, 220, 250), "blade": (230, 236, 246),
        "blade_dark": (120, 130, 150), "cyan": (120, 230, 250, 220)}
SHINY = {"pink": (120, 170, 230), "pink_dark": (40, 80, 160), "pink_light": (200, 230, 255)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "pink", "pink_dark", light="pink_light", trim="gold", trim_w=0.3)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def make(name, x=False):
    def build():
        m = Model(name)
        mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": GOLD, "deltoid": ARM, "upper_arm": ARM,
                "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": ARM, "knee": GOLD, "shin": ARM, "calf": ARM,
                "foot": ARM, "toe": ARM}
        a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, name=name)
        bd = a["body"]
        for nm in ("leg_left", "leg_right"):                                       # long pointed greaves
            anc = a[nm]
            ank = anc["ankle"]
            spike(m, anc["bone"], (ank[0], 1.0, ank[2] - 2.0), (0, -0.1, -1), 1.6, 5.0, ARM, tip=0.8)
            kn = anc["knee"]
            spike(m, anc["bone"], kn, (0, 0.6, -1), 1.2, 3.0, GOLD, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.8, 54.0, 60.4, ARM, cut=1)
        m.box(hd, -1.6, 57.0, -3.3, 1.6, 57.6, -3.2, solid(P, "eye", glow=True))
        spike(m, hd, (0, 60.0, -1.6), (0, 1, 0.6), 1.6, 6.0, GOLD, tip=0.8)              # crest
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.2, 59.4, 0), (sx * 0.6, 1, 0.6), 1.0, 4.0, ARM, tip=0.8)
            m.round_box(bd, sx * 7.4, 0, 3.0, 3.4, 47.0, 53.0, ARM, cut=2)                # pauldrons
            for j in range(2):                                                     # golden ribbons
                pts = [(sx * 8.0, 50.0, 2.0), (sx * (12.0 + j * 3.0), 44.0, 6.0 + j * 2.0), (sx * (14.0 + j * 4.0), 34.0, 4.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, bd, p0, p1, 1, fabric(P, "gold", "gold_dark"), extend=0.3, t2=3)
        hl = a["arm_left"]
        lx, ly, lz = hl["hand"]
        if not x:                                                                  # golden oval shield
            m.round_box(hl["bone"], lx + 1.0, lz - 2.0, 5.0, 0.8, ly - 8.0, ly + 8.0, GOLD, cut=0)
            m.round_box(hl["bone"], lx + 1.0, lz - 2.9, 1.2, 0.3, ly - 1.2, ly + 1.2, gem(P, "blue", "blue_light"), cut=0)
        else:                                                                      # rose shield, rapier, blade wings
            for i in range(8):
                ang = 360.0 * i / 8
                m.box(hl["bone"], lx - 1.0, ly, lz - 2.4, lx + 3.0, ly + 6.0, lz - 2.4, ARM if i % 2 else solid(P, "rose"),
                      rotation=(0, 0, ang), pivot=(lx + 1.0, ly, lz - 2.4))
            m.round_box(hl["bone"], lx + 1.0, lz - 2.8, 1.4, 0.4, ly - 1.4, ly + 1.4, gem(P, "rose", "pink_light"), cut=0)
            hr = a["arm_right"]
            hx, hy, hz = hr["hand"]
            m.round_box(hr["bone"], hx, hz, 2.0, 1.0, hy - 0.4, hy + 0.6, GOLD, cut=0)
            rod(m, hr["bone"], (hx, hy, hz), (hx, hy - 30.0, hz - 2.0), 1, metal(P, "blade", dark="blade_dark"), extend=0, t2=1)
            for side in (1, -1):
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 4.0))
                for j in range(7):
                    ang = math.radians(-20 + j * 20)
                    ln = 18.0 - abs(j - 3) * 2.0
                    end = (side * (3.0 + ln * math.cos(ang)), 50.0 + ln * math.sin(ang), 6.0)
                    rod(m, wb, (side * 3.0, 50.0, 4.0), end, 1, GOLD, extend=0, t2=3)
                    spike(m, wb, end, (side * math.cos(ang), math.sin(ang), 0), 1.2, 3.0, solid(P, "cyan", glow=True), tip=0.8)
        return m

    return build
