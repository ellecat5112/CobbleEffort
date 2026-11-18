"""Shared builder for Mephismon and Mephismon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the fallen angel with a goat's skull for a head: a white skull with ram horns curling down, black bat
wings, a dark muscular torso, violet puffed shoulders and red-banded arms ending in huge white gloves, enormous puffy
violet fur trousers, black goat legs and grey hooves. The X-Antibody ("x"): a dandy: a small brown top hat between its
horns, long lilac hair, a blue tailcoat over a laced corset, grey puffed trousers, lilac goat legs and a cane.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, fabric, fur, metal, skin, solid, strands
from _route import pal, tone

BASE = {"bone": (236, 232, 230), "bone_dark": (160, 150, 160), "horn": (150, 150, 160), "horn_dark": (70, 70, 80),
        "black": (40, 36, 46), "black_dark": (14, 12, 18), "violet": (110, 70, 120), "violet_dark": (54, 30, 64),
        "red": (210, 60, 40), "glove": (240, 240, 248), "glove_dark": (170, 176, 200), "hoof": (140, 144, 150),
        "eye": (240, 40, 60), "wing": (50, 40, 60), "lilac": (200, 170, 230), "lilac_dark": (130, 100, 170),
        "coat": (60, 70, 150), "coat_dark": (24, 30, 80), "grey": (170, 170, 180), "grey_dark": (100, 100, 110),
        "brown": (150, 80, 40), "brown_dark": (80, 40, 16), "gold": (240, 200, 70)}
SHINY = {"violet": (60, 120, 90), "violet_dark": (24, 60, 40), "black": (90, 30, 30), "black_dark": (40, 10, 10),
         "coat": (150, 40, 60), "coat_dark": (80, 14, 24), "lilac": (240, 220, 140), "lilac_dark": (180, 150, 70)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    BODY = skin(P, "black", dark="black_dark")
    PUFF = fur(P, "violet", "violet_dark", length=1.6, density=2.0) if not x else fabric(P, "grey", "grey_dark")
    GLOVE = skin(P, "glove", dark="glove_dark")
    COAT = fabric(P, "coat", "coat_dark", seam="gold")
    LEG = skin(P, "lilac", dark="lilac_dark") if x else BODY

    def armf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        if not x and abs((y % 2.4) - 1.2) < 0.5:
            return tone(p["red"], face), None
        return (COAT if x else BODY)(x_, y, z, face, variant, box=box, **k)

    def corsetf(x_, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x_) < 2.0 and abs(((y + abs(x_)) % 1.6) - 0.8) < 0.2:
            return tone(p["red"], face), None
        return fabric(P, "lilac", "lilac_dark")(x_, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": BODY, "chest": corsetf if x else BODY, "abs": corsetf if x else BODY,
                "pelvis": PUFF, "neck": BODY, "deltoid": COAT if x else PUFF, "upper_arm": armf, "forearm": armf,
                "hand": GLOVE, "finger": GLOVE, "thigh": PUFF, "knee": PUFF, "shin": LEG, "calf": LEG,
                "foot": solid(P, "hoof"), "toe": solid(P, "hoof")}
        a = humanoid(m, mats, bulk=1.05 if not x else 0.85, arm_bulk=1.0, leg_bulk=1.0, digitigrade=True, toes=2,
                     fingers=4, name=name)
        bd = a["body"]
        for sx in (-1, 1):                                                                # puffy trousers
            lg = a["leg_left" if sx > 0 else "leg_right"]["bone"]
            r = 5.6 if not x else 4.2
            ball(m, lg, (sx * 3.6, 23.0, 0.0), r, PUFF, layers=5, ry=r * 1.4, squash=0.9)
        for nm in ("arm_left", "arm_right"):                                          # huge white gloves
            hnd = a[nm]["hand"]
            if not x:
                ball(m, a[nm]["bone"], (hnd[0], hnd[1] - 1.0, hnd[2]), 3.0, GLOVE, layers=3, squash=0.7)
            else:
                m.round_box(a[nm]["bone"], hnd[0], hnd[2], 2.0, 2.0, 33.0, 35.0, fabric(P, "glove", "glove_dark"), cut=0)
        if x:                                                                             # tailcoat + cane
            for sx in (-1, 1):
                x0, x1 = sorted((sx * 1.0, sx * 6.0))
                m.box(bd, x0, 22.0, 3.6, x1, 46.0, 4.4, COAT, rotation=(10, 0, sx * 6), pivot=(sx * 3.0, 46.0, 4.0))
            ar = a["arm_right"]
            h = ar["hand"]
            rod(m, ar["bone"], (h[0], h[1], h[2] - 1.0), (h[0] - 1.0, 2.0, h[2] - 4.0), 1, metal(P, "black"),
                extend=0.4)
            ball(m, ar["bone"], (h[0], h[1] + 0.6, h[2] - 1.0), 1.0, metal(P, "gold"), layers=2)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 2.6, 3.0, 55.0, 61.0, armour(P, "bone", "bone_dark"), cut=1)   # goat skull
        m.round_box(hd, 0, -4.6, 1.6, 2.0, 54.0, 57.6, armour(P, "bone", "bone_dark"), cut=1)  # long muzzle
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.0), 58.0, -4.1, max(sx * 0.8, sx * 2.0), 59.4, -3.9, solid(P, "black"))
            m.box(hd, min(sx * 1.1, sx * 1.7), 58.4, -4.2, max(sx * 1.1, sx * 1.7), 59.0, -4.1,
                  solid(P, "eye", glow=True))
            pts = [(sx * 2.0, 60.4, 0.0), (sx * 5.0, 63.0, 2.0), (sx * 8.0, 61.0, 2.0), (sx * 8.0, 57.0, 0.0),
                   (sx * 6.0, 55.6, -1.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                              # curled ram horns
                rod(m, hd, p0, p1, max(1, 3 - j // 2), metal(P, "horn", dark="horn_dark"), extend=0.4)
        if x:
            m.round_box(hd, 0, -0.6, 1.6, 1.6, 61.0, 61.6, solid(P, "brown"), cut=0)      # top hat brim + crown
            m.round_box(hd, 0, -0.6, 1.1, 1.1, 61.6, 64.4, solid(P, "brown"), cut=0)
            m.box(hd, -1.15, 61.8, -1.75, 1.15, 62.4, 0.55, solid(P, "red"))
            for i in range(7):                                                            # long lilac hair
                ang = math.radians(-70 + i * 23)
                rod(m, hd, (2.4 * math.sin(ang), 60.0, 1.0 + math.cos(ang)), (4.0 * math.sin(ang), 48.0, 4.0), 1,
                    strands(P, "lilac", "lilac_dark"), extend=0.2, t2=2)
        wb = m.bone("wings", bd, (0, 48, 3))
        for side in (1, -1):
            bat_wing(m, wb, (side * 3.0, 48.0, 3.0), 26.0 if not x else 20.0, 18.0, 4, BODY,
                     skin(P, "wing", dark="black_dark"), side=side, sweep=18)
        return m

    return build
