"""Shared builder for Leomon and Leomon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail standard after the
official art on wikimon.net): the lion warrior: a muscular golden lion-man with a shaggy blond mane, a fanged scowl, a
bead necklace, black trousers with a belt, studded leather wrist and knee straps, a short sword at the hip and a lion's
tail with a tuft. X-Antibody: dark plate armour over the legs and arms with white fur cuffs, a long tattered red cape
and a huge two-handed greatsword. Shiny: silver lion.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, fabric, fur, leather, metal, riveted, skin, solid, strands
from _route import pal, tone

BASE = {"tan": (220, 160, 90), "tan_dark": (150, 96, 40), "tan_light": (250, 210, 150), "mane": (240, 200, 70),
        "mane_dark": (180, 120, 20), "black": (36, 34, 38), "black_dark": (12, 12, 14), "leather": (110, 80, 50),
        "leather_dark": (60, 40, 20), "red": (200, 40, 40), "red_dark": (120, 14, 18), "steel": (190, 190, 210),
        "steel_dark": (90, 90, 110), "white": (246, 246, 246), "white_dark": (180, 180, 186), "eye": (60, 50, 40),
        "bead": (220, 80, 60), "mouth": (140, 40, 40), "tooth": (250, 250, 240), "plate": (110, 104, 130),
        "plate_dark": (50, 46, 66)}
SHINY = {"tan": (200, 200, 210), "tan_dark": (120, 120, 136), "tan_light": (240, 240, 250), "mane": (230, 230, 240),
         "mane_dark": (150, 150, 170)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    SKIN = fur(P, "tan", "tan_dark", tip="tan_light", length=0.7)
    PANTS = fabric(P, "black", "black_dark")
    STRAP = riveted(P, "leather", "leather_dark")
    PLATE = armour(P, "plate", "plate_dark", trim="steel", trim_w=0.25)

    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": PANTS, "neck": SKIN, "deltoid": SKIN if not x else PLATE,
                "upper_arm": SKIN, "forearm": STRAP if not x else PLATE, "hand": SKIN, "finger": SKIN,
                "claw": solid(P, "black"), "thigh": PANTS if not x else PLATE, "knee": STRAP if not x else PLATE,
                "shin": PANTS if not x else PLATE, "calf": PANTS if not x else PLATE, "foot": SKIN,
                "talon": solid(P, "black")}
        a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.1, claws=True, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        m.round_box(bd, 0, 0.0, 5.2, 4.0, 33.0, 34.6, leather(P, "leather", "leather_dark"), cut=1)   # belt
        for i in range(9):                                                         # bead necklace
            ang = math.radians(-80 + i * 20)
            m.round_box(bd, 3.2 * math.sin(ang), -2.6 * math.cos(ang) - 0.6, 0.5, 0.5, 49.4 - 1.4 * math.cos(ang),
                        50.4 - 1.4 * math.cos(ang), solid(P, "bead"), cut=0)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 3.0, 3.2, 54.0, 61.0, SKIN, cut=1)
        m.round_box(hd, 0, -3.6, 2.0, 1.2, 54.4, 57.4, SKIN, cut=1)
        m.box(hd, -1.4, 54.6, -4.9, 1.4, 55.4, -4.7, solid(P, "mouth"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.9, sx * 2.2), 58.0, -3.5, max(sx * 0.9, sx * 2.2), 58.8, -3.3, solid(P, "eye"))
            spike(m, hd, (sx * 1.0, 55.4, -4.8), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
        MANE = strands(P, "mane", "mane_dark")
        for ring, (r, n, ln) in enumerate(((3.6, 14, 6.0), (4.6, 16, 8.0))):         # shaggy mane
            for i in range(n):
                ang = 2 * math.pi * (i + ring * 0.5) / n
                if math.sin(ang) < -0.6:
                    continue
                spike(m, hd, (r * math.cos(ang) * 0.9, 58.0 + r * math.sin(ang), 1.0 + ring),
                      (math.cos(ang), math.sin(ang) * 0.8 - 0.4, 0.6), 2.0, ln, MANE, tip=0.8)
        tb = m.bone("tail", bd, (0, 32, 3))
        pts = [(0, 32.0, 3.4), (2.0, 24.0, 9.0), (3.0, 16.0, 11.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 1, SKIN, extend=0.3, t2=1)
        spike(m, tb, pts[-1], (0.2, -1, 0.2), 1.6, 3.0, MANE, tip=0.8)
        if not x:
            rod(m, bd, (-4.6, 32.0, -1.0), (-6.0, 18.0, 1.0), 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=2)   # sword
            m.round_box(bd, -4.4, -1.0, 1.4, 1.4, 32.0, 34.0, solid(P, "black"), cut=0)
        else:
            for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):           # white fur cuffs
                anc = a[nm]
                j = anc.get("wrist") or anc.get("ankle")
                m.round_box(anc["bone"], j[0], j[2], 2.4, 2.4, j[1] - 0.6, j[1] + 1.6, fur(P, "white", "white_dark"), cut=1)
            cape(m, bd, 53.0, 16.0, 44.0, fabric(P, "red", "red_dark"), z=4.0, flare=0.9, panels=8, sweep=(6.0, 6.0))
            hr = a["arm_right"]                                                    # huge greatsword
            hx, hy, hz = hr["hand"]
            m.round_box(hr["bone"], hx, hz, 1.0, 1.0, hy - 2.0, hy + 3.0, solid(P, "black"), cut=0)
            m.round_box(hr["bone"], hx, hz, 4.0, 1.4, hy - 3.4, hy - 2.0, metal(P, "steel", dark="steel_dark"), cut=0)
            m.round_box(hr["bone"], hx, hz - 0.4, 2.6, 0.8, hy - 40.0, hy - 3.4, metal(P, "steel", dark="steel_dark"), cut=0)
        return m

    return build
