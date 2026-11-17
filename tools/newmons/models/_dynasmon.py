"""Shared builder for Dynasmon, the wyvern Royal Knight (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a broad knight in pale lavender-white armour trimmed with gold spikes and studded with gold bosses, a
wyvern-skull helm, huge clawed gauntlets with a red gem in the palm, great tattered violet wings and legs ending in
huge golden cone-spikes. make(x=True): Dynasmon (X-Antibody), dark navy armour edged with teal light and copper,
spikier gauntlets with pink gems and jagged dark wings. Shiny: gold armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import dome, humanoid
from _digidetail import armour, cutout, gem, local, metal, noise2, solid
from _route import pal, tone

BASE = {"plate": (226, 226, 244), "plate_dark": (140, 140, 180), "plate_light": (255, 255, 255), "lav": (160, 160, 220),
        "lav_dark": (80, 80, 140), "gold": (240, 196, 60), "gold_dark": (160, 110, 20), "wing": (90, 70, 170),
        "wing_dark": (40, 26, 90), "red": (220, 40, 40), "red_light": (255, 160, 150), "navy": (40, 50, 80),
        "navy_dark": (12, 16, 30), "navy_light": (110, 130, 170), "teal": (80, 240, 220), "copper": (200, 120, 70),
        "pink": (240, 80, 140), "pink_light": (255, 190, 220), "eye": (250, 220, 60)}
SHINY = {"plate": (250, 220, 130), "plate_dark": (180, 140, 50), "lav": (240, 190, 90), "navy": (90, 30, 40),
         "navy_dark": (40, 10, 14)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = metal(P, "gold", dark="gold_dark")


def make(name, x=False):
    PLATE = armour(P, "navy", "navy_dark", light="navy_light", trim="teal", trim_w=0.25) if x else \
        armour(P, "plate", "plate_dark", light="plate_light", trim="gold", trim_w=0.25)
    LAV = armour(P, "navy", "navy_dark", trim="copper") if x else armour(P, "lav", "lav_dark")
    GEM = gem(P, "pink", "pink_light") if x else gem(P, "red", "red_light")

    def wingf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        key = ("navy" if x else "wing") if v / max(H, 1e-6) > 0.3 else ("navy_dark" if x else "wing_dark")
        return tone(p[key], face), None

    def tatter(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        return noise2(u * 0.5, v * 0.4, 41) < 0.82

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "chest": PLATE, "abs": LAV, "pelvis": PLATE, "neck": LAV, "deltoid": PLATE,
                "upper_arm": LAV, "forearm": PLATE, "hand": PLATE, "finger": PLATE, "claw": GOLD, "thigh": PLATE,
                "knee": GOLD, "shin": PLATE, "calf": PLATE, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.3, arm_bulk=1.4, leg_bulk=1.3, claws=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.6, 3.0, 4.2, 54.0, 60.0, PLATE, cut=1)                      # wyvern-skull helm
        spike(m, hd, (0, 57.0, -5.6), (0, -0.3, -1), 2.4, 3.0, PLATE, tip=0.6)
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.2, sx * 2.6), 57.0, -5.9, max(sx * 1.2, sx * 2.6), 57.8, -5.7, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.6, 59.4, 0.0), (sx * 0.5, 0.8, 1), 1.6, 6.0, GOLD, tip=0.3)
            dome(m, bd, (sx * 8.6, 49.0, 0), 4.6, 3.8, PLATE)
            for j in range(4):                                                         # gold spikes and bosses
                spike(m, bd, (sx * 10.0, 50.0, -3.0 + j * 2.0), (sx, 0.6, 0), 1.0, 3.6, GOLD, tip=0.25)
            m.round_box(bd, sx * 3.0, -4.6, 1.0, 0.6, 44.0, 46.0, GOLD, cut=0)
        for nm in ("arm_left", "arm_right"):                                           # huge clawed gauntlets
            ar = a[nm]
            hx, hy, hz = ar["hand"]
            m.round_box(ar["bone"], hx, hz, 3.4, 3.0, hy - 2.0, hy + 4.0, PLATE, cut=1)
            m.box(ar["bone"], hx - 1.2, hy, hz - 3.4, hx + 1.2, hy + 2.4, hz - 2.8, GEM)
            for j in range(4):
                spike(m, ar["bone"], (hx + (j - 1.5) * 1.6, hy - 2.0, hz - 1.0), (0, -1, -0.5), 1.0, 6.0 if x else 4.6,
                      GOLD, tip=0.25)
        for nm in ("leg_left", "leg_right"):                                           # golden cone-spike feet
            ak = a[nm]["ankle"]
            spike(m, a[nm]["bone"], (ak[0], 3.0, ak[2] - 2.0), (0, -0.3, -1), 5.0, 9.0, GOLD, tip=2.0)
        for side in (1, -1):                                                           # great wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 4.0))
            bat_wing(m, wb, (side * 3.0, 50.0, 4.0), 30.0 if not x else 36.0, 34.0, 4, PLATE, cutout(tatter, wingf),
                     side=side, sweep=15)
        return m
    return build
