"""Shared builder for Wizarmon and Wizarmon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the wandering wizard: a broad blue wizard's hat with a skull and a buckle, a high collar hiding all but
its green eyes, yellow-and-red striped clothes held with buckled straps, a ragged purple cape lined with stars, brown
boots, and a staff topped with a golden sun-wheel, a glowing orange spell orb in its raised hand. X-Antibody: the
cape blooms into a huge tattered spiked mantle of navy and crimson, a gold mask, armoured red-and-gold gauntlets and
a crackle of blue sparks. Shiny: green hat and cape."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import fabric, leather, metal, solid
from _route import pal, tone

BASE = {"hat": (60, 60, 160), "hat_dark": (24, 24, 90), "cape": (90, 60, 150), "cape_dark": (40, 24, 80),
        "yellow": (240, 210, 70), "yellow_dark": (180, 140, 30), "red": (200, 40, 40), "skull": (240, 236, 220),
        "boot": (150, 100, 50), "boot_dark": (90, 56, 24), "gold": (240, 196, 60), "eye": (90, 230, 90),
        "orb": (255, 160, 50, 200), "black": (24, 22, 30), "star": (250, 240, 160), "crimson": (150, 20, 40),
        "spark": (120, 200, 255)}
SHINY = {"hat": (50, 130, 80), "hat_dark": (20, 70, 40), "cape": (60, 140, 90), "cape_dark": (24, 80, 40)}


def make(name, x=False):
    def P(v):
        return pal(BASE, SHINY, v)

    def stripef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if (y % 3.0) < 1.0:
            return tone(p["red"], face), None
        return fabric(P, "yellow", "yellow_dark")(xx, y, z, face, variant, box=box, **k)

    def capef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and (int(xx * 1.3 + 40) * 7 + int(y * 1.3) * 3) % 19 == 0:
            return p["star"], p["star"]
        if x and face != "north" and y < 30.0:
            return tone(p["crimson"], face), None
        return fabric(P, "cape", "cape_dark")(xx, y, z, face, variant, box=box, **k)

    BOOT = leather(P, "boot", "boot_dark")

    def build():
        m = Model(name)
        mats = {"skin": stripef, "chest": stripef, "abs": stripef, "pelvis": stripef, "deltoid": stripef,
                "upper_arm": stripef, "forearm": metal(P, "gold") if x else stripef,
                "hand": leather(P, "red" if x else "black", "black"), "thigh": stripef, "knee": stripef, "shin": BOOT,
                "calf": BOOT, "foot": BOOT, "neck": fabric(P, "hat", "hat_dark")}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.8, leg_bulk=0.85, name=name)
        bd = a["body"]
        for j in range(3):                                                             # buckled straps
            m.box(bd, -4.0, 36.0 + j * 5.0, -4.0, 4.0, 37.0 + j * 5.0, -3.4, leather(P, "black", "black"))
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 3.4, 3.4, 52.0, 59.0, fabric(P, "hat", "hat_dark"), cut=1)      # high collar
        m.box(hd, -2.0, 56.6, -3.6, 2.0, 58.0, -3.2, solid(P, "black"))
        for sx in (-1, 1):
            m.box(hd, sx * 1.0 - 0.4, 57.0, -3.7, sx * 1.0 + 0.4, 57.6, -3.5, solid(P, "eye", glow=True))
        if x:
            m.box(hd, -2.4, 55.0, -3.8, 2.4, 58.6, -3.6, metal(P, "gold"))
        m.round_box(hd, 0, 0, 7.0, 7.0, 59.0, 60.0, fabric(P, "hat", "hat_dark"), cut=3)      # broad hat
        for j in range(4):
            r = 3.4 - j * 0.7
            m.round_box(hd, j * 0.3, j * 0.6, max(r, 0.8), max(r, 0.8), 60.0 + j * 2.0, 62.0 + j * 2.0,
                        fabric(P, "hat", "hat_dark"), cut=1 if r > 1.2 else 0)
        ball(m, hd, (0, 61.6, -3.4), 1.2, solid(P, "skull"), layers=1)
        cb = m.bone("cape", bd, (0, 52, 4))
        cape(m, cb, 52.0, 16.0 if x else 12.0, 46.0 if x else 40.0, capef, z=4.4, flare=1.0 if x else 0.7,
             panels=8 if x else 6, seed=11)
        if x:                                                                          # spiked mantle
            for j in range(7):
                ang = (j - 3) * 0.4
                spike(m, cb, (math.sin(ang) * 6.0, 52.0, 5.0), (math.sin(ang), 1, 0.4), 2.0, 14.0, capef, tip=0.8)
            for j in range(5):
                ball(m, bd, (-9.0 + j * 0.8, 40.0 + j * 2.0, -4.0), 0.6, solid(P, "spark", glow=True), layers=1)
        h = a["arm_left"]["hand"]                                                      # spell orb
        ball(m, a["arm_left"]["bone"], (h[0], h[1] + 3.0, h[2] - 1.0), 2.2, solid(P, "orb", glow=True), layers=2)
        h = a["arm_right"]["hand"]                                                     # sun-wheel staff
        rb = a["arm_right"]["bone"]
        rod(m, rb, (h[0], 1.0, h[2]), (h[0], h[1] + 10.0, h[2]), 1, leather(P, "boot", "boot_dark"), extend=0.0)
        ball(m, rb, (h[0], h[1] + 11.0, h[2]), 1.2, metal(P, "gold"), layers=1)
        for j in range(8):
            ang = j * math.pi / 4
            spike(m, rb, (h[0] + 1.0 * math.cos(ang), h[1] + 11.0 + 1.0 * math.sin(ang), h[2]),
                  (math.cos(ang), math.sin(ang), 0), 0.8, 2.0, metal(P, "gold"), tip=0.8)
        return m
    return build
