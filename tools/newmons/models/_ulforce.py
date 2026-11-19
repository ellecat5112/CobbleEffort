"""Shared builder for Ulforce V-dramon, its X-Antibody and Future Mode (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the Royal Knight of speed: a slim blue armoured dragon-man with a gold V on its chest
and brow, a horned dragon helm, silver-white plating on its chest and legs, pink-lined wings, and V-bracelet shields
on its forearms, a glowing cyan blade jutting from one. X-Antibody: darker navy and gold armour edged in spikes, huge
violet-and-crimson wings and a long crystal sword. Future Mode: sleeker violet armour, vast purple wings and a green
energy crescent. Shiny: crimson."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

LOOKS = {
    "base": {"blue": (60, 110, 210), "blue_dark": (24, 50, 120), "wing": (230, 140, 180), "wing_dark": (150, 70, 120)},
    "x": {"blue": (40, 50, 120), "blue_dark": (14, 18, 60), "wing": (150, 60, 140), "wing_dark": (90, 20, 60)},
    "future": {"blue": (80, 80, 190), "blue_dark": (34, 30, 110), "wing": (140, 70, 180), "wing_dark": (70, 30, 110)},
}
COMMON = {"silver": (226, 230, 240), "silver_dark": (130, 134, 150), "gold": (240, 196, 60), "gold_dark": (170, 120, 20),
          "cyan": (120, 250, 240, 210), "green": (130, 250, 140, 190), "eye": (255, 230, 90), "bar": (60, 60, 80)}
SHINY = {"blue": (190, 50, 60), "blue_dark": (110, 16, 24)}


def make(name, look="base"):
    base = dict(COMMON, **LOOKS[look])

    def P(v):
        return pal(base, SHINY, v)

    BLUE = armour(P, "blue", "blue_dark", trim="gold" if look == "x" else "silver", panel=(3.0, 3.0))
    SILVER = armour(P, "silver", "silver_dark", trim="gold", panel=(3.0, 3.0))
    GOLD = metal(P, "gold", dark="gold_dark")

    def chestf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and 42.0 < y < 50.0 and abs(abs(x) - (y - 42.0) * 0.5) < 0.6:
            return tone(p["gold"], face), None
        return SILVER(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": BLUE, "chest": chestf, "abs": BLUE, "pelvis": BLUE, "deltoid": BLUE, "upper_arm": BLUE,
                "forearm": BLUE, "hand": BLUE, "thigh": BLUE, "knee": SILVER, "shin": SILVER, "calf": SILVER,
                "foot": BLUE, "talon": metal(P, "silver"), "neck": BLUE}
        a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, digitigrade=True, talons=True, name=name)
        bd = a["body"]
        for sx in (-1, 1):
            m.round_box(bd, sx * 7.0, 0, 3.0, 3.4, 48.0, 53.4, BLUE, cut=1)
            spike(m, bd, (sx * 8.4, 53.0, 0), (sx * 0.6, 1, 0), 1.6, 5.0 if look != "x" else 8.0, GOLD, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 3.0, 3.8, 54.0, 61.0, BLUE, cut=1)
        m.round_box(hd, 0, -4.4, 1.8, 1.4, 55.0, 58.0, BLUE, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.4), 58.4, -4.1, max(sx * 0.8, sx * 2.4), 59.2, -3.8, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.0, 60.0, 1.0), (sx * 0.4, 0.8, 1), 1.4, 7.0, BLUE, tip=0.8)
            m.box(hd, min(0.0, sx * 2.6), 60.6, -3.9, max(0.0, sx * 2.6), 61.4, -3.5, GOLD,
                  rotation=(0, 0, -sx * 30), pivot=(0, 60.6, -3.7))                   # V crest
        spike(m, hd, (0, 58.0, -5.6), (0, 0.4, -1), 1.2, 3.0, BLUE, tip=0.8)
        for sx in (-1, 1):                                                              # wings
            wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
            span = 22.0 if look == "base" else 30.0
            bat_wing(m, wb, (sx * 3.0, 48.0, 4.0), span, 20.0 if look == "base" else 26.0, 4, metal(P, "blue_dark"),
                     solid(P, "wing"), side=sx, sweep=20)
        for nm in ("arm_left", "arm_right"):                                            # V-bracelet shields
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 2.0, 2.0, w[1] + 1.0, w[1] + 6.0, SILVER, cut=1)
            spike(m, a[nm]["bone"], (w[0], w[1] + 6.0, w[2]), (0, 1, 0.2), 1.6, 3.0, SILVER, tip=0.8)
        w = a["arm_right"]["wrist"]
        rb = a["arm_right"]["bone"]
        if look == "x":                                                                 # crystal sword
            h = a["arm_right"]["hand"]
            m.box(rb, h[0] - 2.0, h[1] - 0.4, h[2] - 0.8, h[0] + 2.0, h[1] + 0.8, h[2] + 0.8, GOLD)
            m.box(rb, h[0] - 1.2, max(0.4, h[1] - 26.0), h[2] - 0.5, h[0] + 1.2, h[1] - 0.4, h[2] + 0.5,
                  solid(P, "cyan", glow=True))
        elif look == "future":                                                          # green energy crescent
            cb = m.bone("crescent", bd, (0, 36, 0))
            for i in range(12):
                ang = -0.4 + i * 0.26
                cx, cy = -6.0 - 16.0 * math.cos(ang), 30.0 + 16.0 * math.sin(ang)
                m.box(cb, cx - 1.6, cy - 1.6, -3.0, cx + 1.6, cy + 1.6, -1.8, solid(P, "green", glow=True))
        else:                                                                           # cyan blade from the bracelet
            spike(m, rb, (w[0], w[1] + 1.0, w[2] - 1.0), (0, -1, -0.1), 1.6, 16.0, solid(P, "cyan", glow=True), tip=0.8)
        return m
    return build
