"""Shared builder for Ofanimon and its forms (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
the Ophan angel: a slender woman in sleek teal-green armour from helm to greaves, a visored helm with a gold crest,
a long white robe-skirt, a golden spear-staff with a ring head, and four pairs of golden blade-feather wings fanned
behind her. Looks: "base"; "x" (X-Antibody: brighter armour, a red plume, translucent crystal wings, a wheel at her
feet); "falldown" (Falldown Mode: dark teal-black armour with a star crest, golden bat wings, red fire swirling round
her); "falldownx" (Falldown Mode X-Antibody: black-teal armour, red tendrils, three spiked golden rings orbiting);
"core" (Ofanimon Core: blue armour and wings of golden flame, after its pixel sprite). Built covered (full armour).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, solid
from _route import pal, tone

LOOKS = {"base": {"plate": (50, 150, 140), "plate_dark": (14, 80, 76)},
         "x": {"plate": (70, 190, 160), "plate_dark": (20, 110, 90)},
         "falldown": {"plate": (40, 70, 76), "plate_dark": (12, 24, 28)},
         "falldownx": {"plate": (30, 50, 60), "plate_dark": (8, 14, 20)},
         "core": {"plate": (60, 90, 200), "plate_dark": (20, 34, 120)}}
COMMON = {"gold": (236, 196, 80), "gold_dark": (160, 120, 30), "white": (244, 244, 250), "white_dark": (190, 192, 210),
          "red": (210, 40, 50), "red_dark": (120, 14, 20), "visor": (30, 40, 50), "eye": (90, 230, 250),
          "crystal": (250, 230, 150, 150), "fire": (255, 150, 40, 210), "fire_core": (255, 240, 150, 235),
          "redfire": (230, 40, 60, 200)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])
    shiny = dict(base, plate=(200, 200, 214), plate_dark=(120, 120, 136), gold=(200, 120, 220), gold_dark=(120, 60, 150))
    fall = look in ("falldown", "falldownx")

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "plate", "plate_dark", trim="gold", trim_w=0.25)
    GOLD = metal(P, "gold", dark="gold_dark")
    ROBE = fabric(P, "white", "white_dark", seam="gold")

    def firef(key):
        def f(x, y, z, face, variant, box=None, **k):
            p = P(variant)
            u, v, W, H = local(x, y, z, face, box)
            c = p["fire_core"] if (key == "fire" and u / max(W, 1e-6) < 0.3) else p[key]
            return c, c[:3]
        return f

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "neck": PLATE, "hand": PLATE, "finger": PLATE, "knee": GOLD}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name=name)
        bd = a["body"]
        if not fall:                                                                    # long white robe-skirt
            for j in range(5):
                r = 4.2 + j * 1.0
                m.round_box(bd, 0, 0.4, r, r * 0.8, 31.0 - (j + 1) * 5.0, 31.4 - j * 5.0, ROBE, cut=max(1, int(r * 0.3)))
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.6, 2.8, 54.0, 60.0, PLATE, cut=1)                    # visored helm
        m.box(hd, -2.0, 56.6, -3.1, 2.0, 58.0, -2.9, solid(P, "visor"))
        m.box(hd, -1.4, 57.0, -3.15, 1.4, 57.6, -3.1, solid(P, "eye", glow=True))
        if look == "x":
            for i in range(4):
                spike(m, hd, (0, 60.0, -1.0 + i), (0, 1, 0.4 + i * 0.2), 1.2, 6.0, solid(P, "red"), tip=0.8)
        elif fall:
            for i in range(5):                                                         # star crest
                ang = math.radians(90 + i * 72)
                spike(m, hd, (0, 61.0, -2.0), (math.cos(ang), math.sin(ang), 0), 0.9, 2.4, GOLD, tip=0.8)
        else:
            spike(m, hd, (0, 60.0, -1.0), (0, 1, 0.3), 1.4, 5.0, GOLD, tip=0.8)
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 58.0, 0), (sx * 0.6, 0.8, 0.5), 1.0, 4.0, GOLD, tip=0.8)
        wb = m.bone("wings", bd, (0, 48, 3))                                            # wings
        for side in (1, -1):
            if look == "falldown":
                bat_wing(m, wb, (side * 3.0, 48.0, 3.0), 26.0, 18.0, 4, GOLD, fabric(P, "gold", "gold_dark"),
                         side=side, sweep=15)
                continue
            for j in range(4):
                ang = 40 - j * 22
                x0, x1 = sorted((side * 3.0, side * (26.0 - j * 3.0)))
                if look == "core":
                    sh = cutout(flame_inside(4, side * 0.2, j), firef("fire"))
                elif look == "x":
                    sh = solid(P, "crystal", glow=True)
                else:
                    sh = GOLD
                m.box(wb, x0, 47.0, 4.0 + j * 0.5, x1, 49.4, 4.6 + j * 0.5, sh, rotation=(0, side * 10, side * ang),
                      pivot=(side * 3.0, 48.0, 4.0))
        ar = a["arm_right"]                                                             # golden spear-staff
        h = ar["hand"]
        rod(m, ar["bone"], (h[0], h[1] - 24.0, h[2]), (h[0], h[1] + 22.0, h[2]), 1, GOLD, extend=0.2)
        for i in range(10):
            ang = 2 * math.pi * i / 10
            m.box(ar["bone"], h[0] - 0.5, h[1] + 22.0 + 2.4 * math.sin(ang) - 0.5, h[2] + 2.4 * math.cos(ang) - 0.5,
                  h[0] + 0.5, h[1] + 22.0 + 2.4 * math.sin(ang) + 0.5, h[2] + 2.4 * math.cos(ang) + 0.5, GOLD)
        spike(m, ar["bone"], (h[0], h[1] + 24.4, h[2]), (0, 1, 0), 1.4, 6.0, GOLD, tip=0.8)
        if look == "x":                                                                 # wheel at her feet
            for i in range(12):
                ang = 2 * math.pi * i / 12
                m.box(a["top"], -0.6, 4.0 + 3.6 * math.sin(ang) - 0.8, -4.0 + 3.6 * math.cos(ang) - 0.8, 0.6,
                      4.0 + 3.6 * math.sin(ang) + 0.8, -4.0 + 3.6 * math.cos(ang) + 0.8, GOLD)
        if look == "falldown":                                                          # red fire swirl
            for i in range(6):
                ang = 2 * math.pi * i / 6
                c = (12.0 * math.cos(ang), 46.0 + 6.0 * math.sin(ang), 4.0 * math.sin(ang))
                for rot in (0, 90):
                    m.box(bd, c[0] - 2.0, c[1], c[2], c[0] + 2.0, c[1] + 6.0, c[2],
                          cutout(flame_inside(3, 0.2, i), firef("redfire")), rotation=(0, rot, 0), pivot=c)
        if look == "falldownx":                                                         # orbiting spiked rings
            for i in range(3):
                ang = 2 * math.pi * i / 3
                c = (14.0 * math.cos(ang), 46.0 + 8.0 * math.sin(ang), 4.0)
                ball(m, bd, c, 2.6, GOLD, layers=3)
                for j in range(6):
                    a2 = j * math.pi / 3
                    spike(m, bd, c, (math.cos(a2), math.sin(a2), 0), 1.0, 4.0, GOLD, tip=0.8)
            for i in range(5):                                                          # red tendrils
                ang = math.radians(-60 + i * 30)
                rod(m, bd, (0, 46.0, 3.0), (16.0 * math.sin(ang), 46.0 + 12.0 * math.cos(ang), 8.0), 1,
                    solid(P, "red"), extend=0.2, t2=2)
        return m

    return build
