"""Shared builder for Neo Vamdemon and its Darkness Modes (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the vampire king reborn: a towering insectoid figure of glossy violet-black armour bristling with curved
blade spines, a narrow fanged mask with red eyes, clawed hands and long jointed legs. Modes: "base"; "army" (Darkness
Mode (Vampire Army): great tattered black bat wings and red-lit joints); "dragon" (Darkness Mode (Metal Greymon): its
lower body a coiled black serpent tail, vast black wings and a gaping fanged dragon maw for a chest).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, bat_wing
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, local, metal, noise2, solid
from _route import pal, tone

BASE = {"violet": (70, 60, 100), "violet_dark": (24, 20, 40), "violet_light": (150, 140, 190), "silver": (190, 190, 210),
        "silver_dark": (90, 90, 110), "red": (220, 30, 50), "eye": (250, 40, 60), "black": (24, 22, 28),
        "mouth": (90, 10, 24), "tooth": (240, 240, 244)}
SHINY = {"violet": (150, 40, 50), "violet_dark": (70, 10, 16), "violet_light": (230, 120, 120)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, mode="base"):
    ARM = armour(P, "violet", "violet_dark", light="violet_light", trim="silver_dark", trim_w=0.2)
    BLADE = metal(P, "silver", dark="silver_dark")

    def torn(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        return v / max(H, 1e-6) > 0.15 + 0.2 * noise2(u * 0.6, 3)

    WING = cutout(torn, fabric(P, "black", "violet_dark"))

    def build():
        m = Model(name)
        mats = {"skin": ARM, "claw": BLADE, "talon": BLADE}
        a = humanoid(m, mats, bulk=1.0, arm_bulk=0.95, leg_bulk=0.9, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        if mode == "dragon":                                                           # serpent lower body
            m.boxes[:] = [b for b in m.boxes if b.bone not in ("leg_left", "leg_right")]
            m.bones[:] = [b for b in m.bones if b["name"] not in ("leg_left", "leg_right")]
            tb = m.bone("tail", bd, (0, 31, 0))
            pts = [(0, 31.0, 0.4)]
            for i in range(1, 12):
                t = i / 11
                ang = t * 1.8 * math.pi
                pts.append((7.0 * math.sin(ang), 26.0 - 22.0 * t + 3.0 * math.sin(ang), 4.0 - 5.0 * math.cos(ang)))
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tb, p0, p1, max(2, 8 - j // 2), ARM, extend=0.6)
                if j % 2 == 0:
                    spike(m, tb, p0, (0, 1, 0.4), 1.4, 4.0, BLADE, tip=0.8)
            m.box(bd, -4.0, 40.0, -6.2, 4.0, 46.0, -5.8, solid(P, "mouth"))             # chest maw
            for j in range(5):
                spike(m, bd, (-3.2 + j * 1.6, 46.0, -6.2), (0, -1, -0.2), 1.0, 2.4, solid(P, "tooth"), tip=0.8)
                spike(m, bd, (-3.2 + j * 1.6, 40.0, -6.2), (0, 1, -0.2), 1.0, 2.0, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):                                                             # blade spines
            for j in range(3):
                spike(m, bd, (sx * 6.4, 51.0 - j * 2.0, 1.0 + j), (sx * 0.8, 0.9, 0.5), 1.6, 8.0 - j * 1.5, BLADE,
                      tip=0.8)
        for nm in ("arm_left", "arm_right"):
            anc = a[nm]
            el = anc["elbow"]
            sx = 1 if el[0] > 0 else -1
            spike(m, anc["bone"], el, (sx * 0.6, 0.2, 0.8), 1.2, 6.0, BLADE, tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 2.2, 3.2, 54.0, 60.0, ARM, cut=1)                      # narrow fanged mask
        m.box(hd, -1.4, 54.4, -4.3, 1.4, 55.2, -4.1, solid(P, "mouth"))
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.8), 57.6, -4.3, max(sx * 0.6, sx * 1.8), 58.4, -4.1,
                  solid(P, "eye", glow=True))
            spike(m, hd, (sx * 0.8, 54.6, -4.2), (0, -1, 0), 0.8, 1.6, solid(P, "tooth"), tip=0.8)
            spike(m, hd, (sx * 1.8, 60.0, -1.0), (sx * 0.6, 1, 0.5), 1.4, 6.0, BLADE, tip=0.8)
        if mode in ("army", "dragon"):                                                 # great tattered wings
            wb = m.bone("wings", bd, (0, 49, 3))
            for side in (1, -1):
                bat_wing(m, wb, (side * 3.0, 49.0, 3.0), 34.0 if mode == "army" else 30.0, 30.0, 5,
                         solid(P, "black"), WING, side=side, sweep=15)
            if mode == "army":
                for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):
                    anc = a.get(nm)
                    if anc:
                        j = anc.get("elbow") or anc.get("knee")
                        ball(m, anc["bone"], j, 1.0, solid(P, "red", glow=True), layers=1)
        return m

    return build
