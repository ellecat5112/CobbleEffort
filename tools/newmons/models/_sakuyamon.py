"""Shared builder for Sakuyamon and its forms (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the shrine maiden of the Kyubimon line. Base: a tall warrior priestess in violet-and-gold armour with a
gold fox mask-helm, a long silver mane, yin-yang marks on the breastplate, a long golden shakujo staff with rings,
violet sleeve-plates and four little fox spirits (Kuda-gitsune) circling her. X-Antibody: white-and-gold radiant
armour, a great gold halo-ring on her staff and a swirling aura of blue fox-fire. Miko Mode: a plain shrine maiden in
a white haori and long red hakama with a gold fox mask, long silver hair and a purification wand (haraegushi).
Shiny: rose / green.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid, strands
from _route import pal, tone


def make(name, look="base"):
    base = {"violet": (90, 60, 160), "violet_dark": (40, 24, 90), "gold": (240, 200, 70), "gold_dark": (160, 120, 20),
            "silver": (230, 230, 240), "silver_dark": (170, 170, 190), "white": (248, 248, 252),
            "white_dark": (200, 200, 214), "red": (190, 30, 40), "red_dark": (110, 10, 16), "black": (30, 26, 34),
            "fox": (250, 220, 120, 200), "fire": (120, 170, 255, 170), "eye": (90, 200, 250), "paper": (252, 252, 246)}
    shiny = {"violet": (200, 80, 140), "violet_dark": (120, 30, 80), "red": (40, 140, 90), "red_dark": (14, 80, 40)}

    def P(v):
        return pal(base, shiny, v)

    GOLD = metal(P, "gold", dark="gold_dark")
    ARM = armour(P, "white" if look == "x" else "violet", "white_dark" if look == "x" else "violet_dark", trim="gold",
                 trim_w=0.25)

    def plate(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and 42.0 < y < 50.0:
            d = math.hypot(x, y - 46.0)
            if d < 2.6:
                if d > 2.2:
                    return tone(p["black"], face), None
                return tone(p["white"] if (x > 0) ^ (math.hypot(x, y - 47.2 if x > 0 else y - 44.8) < 1.2) else p["black"],
                            face), None
        return ARM(x, y, z, face, variant, box=box, **k)

    HAORI = fabric(P, "white", "white_dark", axis="y", period=3.0)
    HAKAMA = fabric(P, "red", "red_dark", axis="y", period=2.0)

    def build():
        m = Model(name)
        if look == "miko":
            mats = {"skin": HAORI, "pelvis": HAKAMA, "thigh": HAKAMA, "knee": HAKAMA, "shin": HAKAMA, "calf": HAKAMA,
                    "foot": solid(P, "white"), "hand": solid(P, "white"), "finger": solid(P, "white")}
        else:
            mats = {"skin": plate, "neck": metal(P, "black"), "hand": GOLD, "finger": GOLD, "knee": GOLD, "foot": ARM}
        a = humanoid(m, mats, bulk=0.75, arm_bulk=0.75, leg_bulk=0.8, name=name)
        bd = a["body"]
        if look == "miko":
            for i in range(6):                                                           # long flared hakama
                r = 4.6 + i * 0.9
                m.round_box(bd, 0, 0.4, r, r * 0.85, 30.0 - (i + 1) * 5.0, 30.0 - i * 5.0 + 0.2, HAKAMA,
                            cut=max(1, round(r * 0.3)))
            for side in ("arm_left", "arm_right"):                                       # wide haori sleeves
                e = a[side]["elbow"]
                sx = 1 if side == "arm_left" else -1
                m.box(a[side]["bone"], e[0] + sx * 0.4 - 2.4, e[1] - 12.0, e[2] - 2.4, e[0] + sx * 0.4 + 2.4, e[1] + 2.0,
                      e[2] + 2.4, HAORI)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, solid(P, "silver"), cut=1)
        m.round_box(hd, 0, -2.4, 2.4, 0.8, 54.6, 59.4, GOLD, cut=0)                          # gold fox mask
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 57.4, -3.3, max(sx * 0.6, sx * 1.8), 58.0, -3.1, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 1.6, 60.0, -1.0), (sx * 0.3, 1, 0), 1.4, 4.0, GOLD, tip=0.8)  # fox ears
        m.box(hd, -2.6, 30.0 if look != "x" else 34.0, 0.4, 2.6, 58.0, 3.2, strands(P, "silver", "silver_dark"))   # mane
        w = a["arm_right"]["wrist"]
        ab = a["arm_right"]["bone"]
        if look == "miko":                                                               # purification wand
            rod(m, ab, (w[0], w[1] - 2.0, w[2] - 1.0), (w[0] + 4.0, w[1] + 20.0, w[2] - 2.0), 1, solid(P, "gold_dark"),
                extend=0.2)
            for j in range(5):
                m.box(ab, w[0] + 2.6 + j * 0.6, w[1] + 12.0, w[2] - 3.0, w[0] + 3.4 + j * 0.6, w[1] + 18.0, w[2] - 1.0,
                      solid(P, "paper"))
            return m
        rod(m, ab, (w[0], w[1] - 26.0, w[2] - 1.0), (w[0], w[1] + 28.0, w[2] - 1.0), 1, GOLD, extend=0.2)   # shakujo
        top = (w[0], w[1] + 30.0, w[2] - 1.0)
        rr = 5.0 if look == "x" else 3.0
        for i in range(12):
            ang = 2 * math.pi * i / 12
            m.box(ab, top[0] - 0.4, top[1] + rr * math.sin(ang) - 0.6, top[2] + rr * math.cos(ang) - 0.6,
                  top[0] + 0.4, top[1] + rr * math.sin(ang) + 0.6, top[2] + rr * math.cos(ang) + 0.6, GOLD)
        for sx in (-1, 1):
            m.round_box(bd, sx * 7.6, 0, 3.0, 3.2, 46.0, 51.0, ARM, cut=1)
        fb = m.bone("ring_spirits", bd, (0, 40, 0))                                      # fox spirits / fox-fire
        for j in range(4 if look != "x" else 8):
            ang = 2 * math.pi * j / (4 if look != "x" else 8)
            c = (14.0 * math.cos(ang), 40.0 + 6.0 * math.sin(ang * 2), 14.0 * math.sin(ang))
            ball(m, fb, c, 1.6, solid(P, "fox" if look != "x" else "fire", glow=True), layers=2)
            spike(m, fb, c, (math.cos(ang + 1.6), 0.2, math.sin(ang + 1.6)), 1.0, 3.0,
                  solid(P, "fox" if look != "x" else "fire", glow=True), tip=0.8)
        return m

    return build
