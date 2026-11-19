"""Shared builder for Takutoumon and its Wrath Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): an armoured guardian god: gold-and-teal plate over blue scale mail, a red tabard to the shins, white
trousers patterned with blue flames, a black cape, a gold-crested blue helm, a glowing cyan pagoda raised in the left
hand and a cyan crystal sword in the right, golden ribbons trailing round it. Wrath Mode: red armoured claw-feet and
gauntlets, flaming horns on the helm and flame braziers on the shoulders, and the sword becomes a long golden
trident-spear with a crystal blade. Shiny: violet plate, crimson tabard."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, scales, solid
from _route import pal, tone

BASE = {"gold": (230, 186, 70), "gold_dark": (150, 100, 30), "teal": (70, 130, 150), "teal_dark": (30, 70, 90),
        "blue": (80, 130, 190), "blue_dark": (40, 70, 120), "red": (180, 34, 40), "red_dark": (100, 14, 20),
        "white": (236, 236, 240), "white_dark": (180, 184, 196), "black": (34, 32, 40), "black_dark": (12, 12, 16),
        "crystal": (120, 240, 230), "crystal_dark": (60, 170, 180), "flame": (255, 140, 40), "flame_hot": (255, 230, 120),
        "eye": (255, 230, 120), "ribbon": (250, 220, 110)}
SHINY = {"teal": (120, 80, 160), "teal_dark": (70, 40, 110), "red": (140, 20, 60), "red_dark": (80, 8, 30)}


def make(name, wrath=False):
    def P(v):
        return pal(BASE, SHINY, v)

    GOLD = metal(P, "gold", dark="gold_dark")
    TEAL = armour(P, "teal", "teal_dark", trim="gold", panel=(3.0, 3.0))
    MAIL = scales(P, "blue", "blue_dark", size=1.2)
    REDA = armour(P, "red", "red_dark", trim="gold", panel=(2.6, 2.6))
    CRYS = solid(P, "crystal", glow=True)

    def trousers(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        t = (y * 0.8 + math.sin(x * 1.3 + z) * 1.4) % 4.0
        if t < 0.7 and y < 26:
            return tone(p["blue"], face), None
        return fabric(P, "white", "white_dark")(x, y, z, face, variant, box=box, **k)

    def tabard(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if box is not None and (x < box.lo[0] + 0.6 or x > box.lo[0] + box.size[0] - 0.6):
            return tone(p["gold"], face), None
        return fabric(P, "red", "red_dark")(x, y, z, face, variant, box=box, **k)

    def flamef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        c = p["flame_hot"] if box is not None and y < box.lo[1] + box.size[1] * 0.35 else p["flame"]
        return c, c

    def build():
        m = Model(name)
        mats = {"skin": MAIL, "chest": TEAL, "abs": MAIL, "pelvis": GOLD, "deltoid": GOLD, "upper_arm": MAIL,
                "forearm": REDA if wrath else TEAL, "hand": REDA if wrath else solid(P, "black"),
                "thigh": trousers, "knee": trousers, "shin": trousers, "calf": trousers,
                "foot": REDA if wrath else GOLD, "talon": GOLD, "neck": MAIL}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.1, leg_bulk=1.15, talons=wrath, name=name)
        bd = a["body"]
        m.box(bd, -2.8, 6.0, -4.8, 2.8, 31.0, -3.8, tabard)                                 # red tabard
        m.round_box(bd, 0, 0, 5.8, 4.2, 29.6, 32.0, GOLD, cut=1)
        ball(m, bd, (0, 46.0, -5.0), 1.6, solid(P, "eye", glow=True), layers=1)          # chest jewel
        for sx in (-1, 1):
            m.round_box(bd, sx * 7.0, 0, 3.2, 3.4, 48.6, 53.6, GOLD, cut=1)               # pauldrons
            if wrath:                                                                  # shoulder braziers
                for j in range(3):
                    spike(m, bd, (sx * 7.0 + (j - 1) * 1.2, 53.6, 0), ((j - 1) * 0.2 + sx * 0.3, 1, 0), 1.6,
                          7.0 - abs(j - 1) * 2.0, flamef, tip=0.8)
            if wrath:                                                                  # leg claws
                lg = a["leg_left" if sx > 0 else "leg_right"]
                ank = lg["ankle"]
                m.round_box(lg["bone"], ank[0], ank[2] - 0.6, 3.0, 3.6, 2.0, 9.0, REDA, cut=1)
                for t in range(3):
                    spike(m, lg["bone"], (ank[0] + (t - 1) * 1.6, 1.2, ank[2] - 3.6), (0, -0.2, -1), 1.2, 4.0, GOLD,
                          tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, 0, 3.2, 3.4, 54.0, 61.0, armour(P, "blue", "blue_dark", trim="gold"), cut=1)
        m.box(hd, -2.4, 55.4, -3.9, 2.4, 58.6, -3.3, solid(P, "black"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 57.2, -4.1, max(sx * 0.6, sx * 1.8), 57.9, -3.8, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 3.0, 59.0, 0), (sx * 0.6, 1, 0), 1.2, 4.0, GOLD, tip=0.8)
            if wrath:
                for j in range(3):
                    spike(m, hd, (sx * (3.6 + j), 60.0, 0), (sx * 0.5, 1, 0.1), 1.4, 6.0 + j * 1.5, flamef, tip=0.8)
        spike(m, hd, (0, 60.6, -1.0), (0, 1, 0), 1.4, 7.0, GOLD, tip=0.8)
        cb = m.bone("cape", bd, (0, 52, 4))
        cape(m, cb, 52.0, 13.0, 40.0, fabric(P, "black", "black_dark"), z=4.4, flare=0.6, panels=6, seed=5)
        rb = m.bone("ring", bd, (0, 40, 6))                                              # golden ribbons
        for i in range(16):
            ang = i * 2 * math.pi / 16
            cx, cy = 15.0 * math.cos(ang), 40.0 + 15.0 * math.sin(ang)
            m.box(rb, cx - 1.0, cy - 1.0, 6.0, cx + 1.0, cy + 1.0, 6.8, solid(P, "ribbon", glow=True))
        h = a["arm_left"]["hand"]                                                       # the pagoda
        lb = a["arm_left"]["bone"]
        for j in range(6):
            r = 2.2 - j * 0.25
            m.round_box(lb, h[0], h[2], r, r, h[1] + 2.0 + j * 2.4, h[1] + 3.6 + j * 2.4, CRYS, cut=0)
            m.round_box(lb, h[0], h[2], r + 0.8, r + 0.8, h[1] + 3.6 + j * 2.4, h[1] + 4.4 + j * 2.4,
                        solid(P, "crystal_dark", glow=True), cut=0)
        spike(m, lb, (h[0], h[1] + 16.4, h[2]), (0, 1, 0), 1.0, 3.0, GOLD, tip=0.8)
        h = a["arm_right"]["hand"]
        rbn = a["arm_right"]["bone"]
        if wrath:                                                                      # trident-spear, held across
            rod(m, rbn, (h[0] + 16.0, h[1] + 6.0, h[2]), (h[0] - 16.0, h[1] - 6.0, h[2]), 1, GOLD, extend=0.0)
            spike(m, rbn, (h[0] - 16.0, h[1] - 6.0, h[2]), (-1, -0.37, 0), 2.4, 12.0, CRYS, tip=0.8)
            for sy in (-1, 1):
                spike(m, rbn, (h[0] - 15.0, h[1] - 5.6 + sy * 1.6, h[2]), (-1, -0.37 + sy * 0.6, 0), 1.0, 5.0, GOLD,
                      tip=0.8)
        else:                                                                          # crystal sword, point down
            m.box(rbn, h[0] - 2.0, h[1] - 0.4, h[2] - 0.8, h[0] + 2.0, h[1] + 0.6, h[2] + 0.8, GOLD)
            m.box(rbn, h[0] - 0.6, h[1] + 0.6, h[2] - 0.6, h[0] + 0.6, h[1] + 3.6, h[2] + 0.6, solid(P, "red"))
            m.box(rbn, h[0] - 1.1, max(0.4, h[1] - 22.0), h[2] - 0.5, h[0] + 1.1, h[1] - 0.4, h[2] + 0.5, CRYS)
        return m
    return build
