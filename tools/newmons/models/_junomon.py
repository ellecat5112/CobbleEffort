"""Shared builder for Junomon and Junomon: Hysteric Mode (CobbleEffort: Digital; hand-built at the detail standard
after the official art on wikimon.net): the queen of the Olympos Twelve. Junomon: a goddess in golden armour with a
tall crown of golden spikes over a masked face, a red double halo, a white bodysuit with a gold belt, a vast violet
cape lined with blue scales like peacock feathers, golden chains and two golden staffs, one crowned with a blue orb.
Hysteric Mode: the cape spreads into a huge tattered violet mantle with two great golden peacock-feather blades
tipped with spikes, its crown a burst of needles and chains swinging round it. Shiny: emerald cape, silver gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, gem, local, metal, noise2, scales, solid
from _route import pal, tone

BASE = {"gold": (240, 200, 80), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 180), "white": (246, 246, 250),
        "white_dark": (180, 184, 204), "violet": (80, 60, 170), "violet_dark": (30, 20, 80), "scale": (70, 120, 210),
        "scale_dark": (30, 60, 140), "red": (220, 40, 50), "orb": (80, 140, 240), "orb_light": (220, 240, 255),
        "mask": (230, 230, 236), "eye": (240, 60, 80)}
SHINY = {"violet": (40, 140, 90), "violet_dark": (10, 70, 40), "scale": (80, 200, 160), "scale_dark": (20, 120, 90),
         "gold": (220, 224, 236), "gold_dark": (130, 136, 156)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light")
METAL = metal(P, "gold", dark="gold_dark", light="gold_light")
SUIT = fabric(P, "white", "white_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face == "north" and v / max(H, 1e-6) < 0.45:                            # blue scale lining toward the hem
        su, sv = u % 1.6, v % 1.4
        return tone(p["scale_dark"] if math.hypot(su - 0.8, sv - 1.4) < 0.8 and sv < 0.5 else p["scale"], face), None
    return fabric(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.18 * abs(math.sin(u * 0.7)) + 0.08 * noise2(u, 0.0, 5)


def make(name, hysteric=False):
    def build():
        m = Model(name)
        mats = {"skin": SUIT, "chest": GOLD, "abs": SUIT, "pelvis": GOLD, "neck": SUIT, "deltoid": GOLD,
                "upper_arm": SUIT, "forearm": GOLD, "hand": SUIT, "finger": SUIT, "thigh": SUIT, "knee": GOLD,
                "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=0.78, arm_bulk=0.8, leg_bulk=0.82, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, solid(P, "mask"), cut=1)
        m.round_box(hd, 0, -2.8, 2.0, 0.3, 56.8, 57.6, solid(P, "eye", glow=True), cut=0)
        n = 9 if not hysteric else 15                                              # crown of spikes
        for i in range(n):
            ang = math.radians(-70 + 140 * i / (n - 1))
            spike(m, hd, (2.4 * math.sin(ang), 59.6, 0.4 + 0.6 * math.cos(ang)), (math.sin(ang) * 0.5, 1, 0.1), 1.2,
                  (8.0 if not hysteric else 11.0) - abs(i - n // 2) * 0.5, METAL, tip=0.8)
        hb = m.bone("ring_halo", hd, (0, 68, 1))                                    # red double halo
        for r in (3.0, 4.2):
            for i in range(12):
                a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
                rod(m, hb, (r * math.cos(a0), 68.0, 1.0 + r * math.sin(a0)), (r * math.cos(a1), 68.0, 1.0 + r * math.sin(a1)),
                    1, solid(P, "red", glow=True), extend=0.2, t2=1)
        if not hysteric:
            cape(m, bd, 53.0, 22.0, 48.0, capef, z=4.0, flare=1.0, panels=10, sweep=(0.0, 6.0))
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                   # two golden staffs
                hx, hy, hz = a[nm]["hand"]
                rod(m, a[nm]["bone"], (hx, hy - 24.0, hz), (hx + sx * 3.0, hy + 22.0, hz), 1, METAL, extend=0, t2=1)
                if sx < 0:
                    m.round_box(a[nm]["bone"], hx + sx * 3.0, hz, 1.8, 1.8, hy + 22.0, hy + 25.6, gem(P, "orb", "orb_light"),
                                cut=1)
                    for j in range(5):
                        ang = math.radians(-60 + j * 30)
                        spike(m, a[nm]["bone"], (hx + sx * 3.0, hy + 23.8, hz), (math.sin(ang), math.cos(ang), 0), 0.9,
                              3.0, METAL, tip=0.8)
                else:
                    spike(m, a[nm]["bone"], (hx + sx * 3.0, hy + 22.0, hz), (0, 1, 0), 1.4, 6.0, METAL, tip=0.8)
        else:
            for side in (1, -1):                                                    # spread tattered mantle
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 52.0, 4.0))
                for j in range(4):
                    x0, x1 = sorted((side * 3.0, side * (30.0 - j * 3.0)))
                    m.box(wb, x0, 6.0 + j * 6.0, 4.4 + j * 0.2, x1, 52.0, 4.4 + j * 0.2, cutout(tatter, capef),
                          rotation=(0, side * -12, side * (6 - j * 4)), pivot=(side * 3.0, 52.0, 4.4))
                fb = m.bone("feather_left" if side > 0 else "feather_right", bd, (side * 4.0, 46.0, -2.0))
                c = (side * 16.0, 50.0, -4.0)                                        # golden peacock-feather blade
                for j in range(6):
                    r = 6.0 - j * 0.6
                    m.round_box(fb, c[0] + side * j * 0.6, c[2], r, 1.2, c[1] + 6.0 - j * 1.6 - r * 0.7,
                                c[1] + 6.0 - j * 1.6 + r * 0.7, GOLD, cut=max(1, int(r * 0.3)))
                m.round_box(fb, c[0], c[2] - 1.4, 1.6, 0.4, c[1] + 3.0, c[1] + 6.0, gem(P, "red", "red"), cut=0)
                spike(m, fb, (c[0], c[1] - 4.0, c[2]), (-side * 0.6, -1, -0.2), 2.6, 22.0, METAL, tip=0.8)
                for j in range(3):                                                  # swinging chains
                    pts = [(side * 6.0, 50.0 - j * 4.0, 2.0), (side * (20.0 + j * 4.0), 30.0 - j * 6.0, 6.0),
                           (side * (34.0 + j * 2.0), 8.0, 4.0)]
                    for p0, p1 in zip(pts, pts[1:]):
                        rod(m, wb, p0, p1, 1, METAL, extend=0.2, t2=1)
        return m

    return build
