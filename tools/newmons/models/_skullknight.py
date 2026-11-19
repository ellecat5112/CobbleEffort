"""Shared builder for Skull Knightmon and its modes (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the undead knight of the Bagra Army: a stocky knight in black armour whose chest is a big silver skull
with red eyes, a round knight helm with a barred visor and little horns, big red-and-silver drill cones on its
shoulders, and a tattered black cape. Modes: "base"; "arrow" (Arrow Mode: a golden crossbow-bow); "axe" (Big Axe
Mode: crouched in black-and-gold plate behind a huge black crescent axe-blade); "cavalier" (Cavalier Mode: a hulking
black-and-gold armoured rider with long red drill-lances and a sweeping black mane-cape); "naginata" (Naginata Mode:
two golden crescent blades on a staff); "white" (a white-cloaked wanderer with a long staff). Colours "black"
(default), "blue", "red". Shiny: white armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

COLOURS = {"black": (40, 38, 46), "blue": (50, 80, 180), "red": (190, 40, 40)}


def make(name, mode="base", colour="black"):
    body = COLOURS[colour]
    base = {"plate": body, "plate_dark": tuple(int(c * 0.35) for c in body), "silver": (210, 214, 226),
            "silver_dark": (110, 114, 130), "red": (200, 30, 40), "red_dark": (110, 10, 16), "gold": (236, 196, 70),
            "gold_dark": (150, 110, 20), "eye": (240, 40, 40), "cape": (36, 34, 40), "cloak": (240, 240, 236),
            "cloak_dark": (180, 176, 170), "wood": (170, 140, 100)}
    shiny = {"plate": (230, 230, 240), "plate_dark": (150, 150, 170)}
    if mode == "white":
        base["plate"], base["plate_dark"] = (200, 200, 210), (110, 110, 124)

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "plate", "plate_dark", trim="gold" if mode in ("axe", "cavalier") else None, trim_w=0.25)
    SILVER = metal(P, "silver", dark="silver_dark")
    GOLD = metal(P, "gold", dark="gold_dark")

    def skullf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            for sx in (-1, 1):
                d = math.hypot(x - sx * 2.0, y - 44.0)
                if d < 1.6:
                    return (p["eye"], p["eye"]) if d < 1.0 else (tone(p["plate_dark"], face), None)
            if 38.0 < y < 40.6 and abs(x) < 2.4 and (x * 2) % 1.2 < 0.6:
                return tone(p["plate_dark"], face), None
        return SILVER(x, y, z, face, variant, box=box, **k)

    def drillf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["red"] if (y + z) % 2.0 < 1.4 else p["red_dark"], face), None

    def capef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if mode == "white":
            return tone(p["cloak_dark"] if face == "north" else p["cloak"], face), None
        return tone(p["cape"], face), None

    def build():
        m = Model(name)
        bulk = 1.3 if mode in ("axe", "cavalier") else 1.15
        mats = {"skin": PLATE, "chest": skullf, "abs": skullf, "talon": SILVER, "claw": SILVER}
        a = humanoid(m, mats, bulk=bulk, arm_bulk=bulk, leg_bulk=bulk, talons=mode in ("axe", "cavalier"),
                     claws=mode in ("axe", "cavalier"), digitigrade=mode in ("axe", "cavalier"), name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 3.0, 3.0, 53.6, 60.4, SILVER, cut=1)                    # knight helm
        for j in range(4):
            m.box(hd, -2.0 + j * 1.2, 56.0, -3.5, -1.6 + j * 1.2, 58.4, -3.3, solid(P, "plate_dark"))
        m.box(hd, -2.4, 56.8, -3.6, 2.4, 57.4, -3.4, solid(P, "eye", glow=True))
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.4, 60.0, 0), (sx * 0.4, 1, 0), 1.2, 3.0, solid(P, "red"), tip=0.8)
        for sx in (-1, 1):                                                               # shoulder drill cones
            m.round_box(bd, sx * 9.0, 0, 3.0, 3.0, 47.0, 51.0, SILVER, cut=1)
            spike(m, bd, (sx * 10.0, 49.0, 0), (sx * 0.6, 0.8, 0.3) if mode != "cavalier" else (sx * 1, 0.3, -0.4),
                  3.0, 9.0 if mode != "cavalier" else 16.0, drillf, tip=0.8)
        cape(m, bd, 52.0, 16.0, 40.0 if mode != "white" else 48.0, capef, z=4.0,
             flare=2.0 if mode != "cavalier" else 3.0, panels=7, seed=3)
        w = a["arm_right"]["wrist"]
        ab = a["arm_right"]["bone"]
        wl = a["arm_left"]["wrist"]
        abl = a["arm_left"]["bone"]
        if mode == "arrow":                                                              # golden crossbow-bow
            pts = [(wl[0] + 2.0, wl[1] + 12.0, wl[2] - 4.0), (wl[0] + 4.0, wl[1], wl[2] - 6.0),
                   (wl[0] + 2.0, wl[1] - 12.0, wl[2] - 4.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, abl, p0, p1, 2, GOLD, extend=0.4)
            for p_ in (pts[0], pts[-1]):
                spike(m, abl, p_, (0, 1 if p_ is pts[0] else -1, 0), 1.0, 3.0, GOLD, tip=0.8)
            rod(m, abl, (wl[0], wl[1], wl[2]), (wl[0] + 4.0, wl[1], wl[2] - 14.0), 1, GOLD, extend=0.2)
        elif mode == "axe":                                                              # huge crescent axe-blade
            for j in range(9):
                ang = math.radians(-80 + j * 20)
                c = (w[0] - 2.0, w[1] + 12.0 + 12.0 * math.sin(ang), w[2] - 8.0 - 8.0 * math.cos(ang))
                m.box(ab, c[0] - 0.6, c[1] - 2.0, c[2] - 2.0, c[0] + 0.6, c[1] + 2.0, c[2] + 2.0,
                      metal(P, "plate", dark="plate_dark"))
            rod(m, ab, (w[0], w[1] - 6.0, w[2]), (w[0] - 2.0, w[1] + 12.0, w[2] - 2.0), 1, GOLD, extend=0.2)
        elif mode == "cavalier":                                                         # long red drill-lances
            spike(m, ab, (w[0], w[1], w[2] - 2.0), (0, 0.2, -1), 2.6, 24.0, drillf, tip=0.8)
            spike(m, abl, (wl[0], wl[1], wl[2] - 2.0), (0, 0.2, -1), 2.6, 24.0, drillf, tip=0.8)
        elif mode == "naginata":                                                         # two golden crescents
            rod(m, ab, (w[0] - 16.0, w[1] + 4.0, w[2] - 2.0), (w[0] + 16.0, w[1] + 4.0, w[2] - 2.0), 1, metal(P, "plate"),
                extend=0.2)
            for sx in (-1, 1):
                for j in range(6):
                    ang = math.radians(j * 30)
                    c = (w[0] + sx * (16.0 + 6.0 * math.sin(ang)), w[1] + 4.0 + sx * 10.0 * math.cos(ang) - sx * 5.0,
                         w[2] - 2.0)
                    m.box(ab, c[0] - 1.2, c[1] - 1.6, c[2] - 0.4, c[0] + 1.2, c[1] + 1.6, c[2] + 0.4, GOLD)
        elif mode == "white":                                                            # long staff
            rod(m, ab, (w[0], 2.0, w[2] - 2.0), (w[0], 66.0, w[2] - 2.0), 1, solid(P, "wood"), extend=0.2)
        return m

    return build
