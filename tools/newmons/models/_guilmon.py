"""Shared builder for the Guilmon line (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
Guilmon (Child), Growmon (Adult), Megalo Growmon (Perfect), in their usual colours or as the Black versions.

A red (or dark grey) dinosaur with black (or red) markings, a white belly with the Hazard emblem, bat-wing ears,
yellow eyes; Growmon adds a white mane and elbow blades; Megalo Growmon adds cyborg armour, a cannon chest and
mechanical wings. Shiny: the other colouring (the Black version's shiny is the classic red).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import theropod
from _digidetail import armour, eye, local, metal, plane, scales, skin, solid, strands
from _route import pal, tone

RED = {"hide": (210, 40, 40), "hide_dark": (130, 14, 16), "hide_light": (250, 130, 120), "mark": (30, 26, 30)}
BLACK = {"hide": (60, 58, 66), "hide_dark": (24, 22, 28), "hide_light": (130, 128, 140), "mark": (200, 30, 40)}
COMMON = {"belly": (246, 244, 240), "belly_dark": (200, 196, 190), "hazard": (40, 36, 40), "claw": (246, 246, 246),
          "eye": (250, 200, 30), "pupil": (20, 16, 10), "white": (250, 250, 250), "mouth": (110, 20, 30),
          "tongue": (220, 80, 90), "mane": (240, 240, 246), "mane_dark": (180, 180, 196), "steel": (200, 204, 216),
          "steel_dark": (100, 104, 116), "glow": (255, 80, 60)}


def make(name, stage, black=False, colours=None, shiny_colours=None):
    base = dict(COMMON, **(BLACK if black else RED))
    shiny = dict(COMMON, **(RED if black else BLACK))
    base.update(colours or {})
    shiny.update(shiny_colours or {})

    def P(v):
        return pal(base, shiny, v)

    HIDE = scales(P, "hide", "hide_dark", size=1.8, light="hide_light", rim_mix=0.3)

    def markedf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        a, b = plane(x, y, z, face)
        if face in ("east", "west", "up", "south") and abs(((b * 0.35 + a * 0.25) % 3.0) - 1.5) < 0.35:
            return tone(p["mark"], face), None
        return HIDE(x, y, z, face, variant, box=box, **k)

    def bellyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north":
            a, b = plane(x, y, z, face)
            cy = {"child": 24.0, "adult": 30.0, "perfect": 34.0}[stage]
            r = math.hypot(a, b - cy)
            ang = math.degrees(math.atan2(b - cy, a)) % 120
            if r < 0.6 or (1.0 < r < 2.4 and abs(ang - 60) < 22):
                return p["hazard"], None
        return skin(P, "belly", dark="belly_dark")(x, y, z, face, variant, box=box, **k)

    def headf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("east", "west"):
            c = eye(p, z - ez, y - ey, 1.2, "eye", slit=True)
            if c is not None:
                return c, None
        return markedf(x, y, z, face, variant, box=box, **k)

    cfg = {"child": dict(hip_y=12.0, hip_z=2.0, chest=(0, 22.0, -1.0), body_r=5.0, chest_r=4.6, neck_top=(0, 28.0, -3.0),
                         head_len=9.0, head_w=3.8, head_h=4.0, arm_len=8.0, arm_bulk=1.1, leg_bulk=1.1, stance=3.6,
                         tail=((0, 10, 8), (2, 7, 14), (4, 5, 19)), tail_r=(3.0, 2.0, 1.2)),
           "adult": dict(hip_y=16.0, hip_z=3.0, chest=(0, 28.0, -3.0), body_r=6.0, chest_r=6.0, neck_top=(0, 35.0, -7.0),
                         head_len=11.0, head_w=4.2, head_h=4.4, arm_len=11.0, arm_bulk=1.4, leg_bulk=1.4, stance=4.8,
                         tail=((0, 14, 10), (3, 10, 18), (6, 7, 25), (8, 6, 30)), tail_r=(4.0, 3.0, 2.0, 1.2)),
           "perfect": dict(hip_y=20.0, hip_z=3.0, chest=(0, 34.0, -2.0), body_r=7.0, chest_r=7.4,
                           neck_top=(0, 42.0, -6.0), head_len=12.0, head_w=4.6, head_h=4.8, arm_len=14.0,
                           arm_bulk=1.8, leg_bulk=1.7, stance=5.6,
                           tail=((0, 18, 10), (3, 13, 18), (7, 9, 26), (10, 7, 32)), tail_r=(5.0, 3.6, 2.4, 1.4))}[stage]
    ey = cfg["neck_top"][1] + cfg["head_h"] * 0.62
    ez = cfg["neck_top"][2] - cfg["head_len"] * 0.45 + 1.6

    def build():
        m = Model(name)
        mats = {"skin": markedf, "belly": bellyf, "neck": markedf, "head": headf, "snout": HIDE, "jaw": HIDE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "white"), "tongue": solid(P, "tongue"), "arm": markedf,
                "hand": HIDE, "claw": solid(P, "claw"), "thigh": markedf, "shin": markedf, "foot": HIDE,
                "talon": solid(P, "claw"), "tail": markedf, "tail_tip": markedf}
        a = theropod(m, mats, name, mouth_open=14, teeth=5, **cfg)
        hd = a["head"]
        z0, z1 = a["skull_z"]
        top = a["skull_top"]
        for sx in (-1, 1):                                       # bat-wing ears
            x0, x1 = sorted((sx * 3.0, sx * 7.0))
            m.box(hd, x0, top - 1.0, z1 - 1.0, x1, top + 3.0, z1 - 1.0, HIDE, rotation=(0, sx * 20, -sx * 25),
                  pivot=(sx * 3.0, top, z1 - 1.0))
        if stage in ("adult", "perfect"):
            mane = m.bone("mane", hd, (0, top, z1))
            for i in range(9):                                   # white mane
                xx = -2.4 + i * 0.6
                rod(m, mane, (xx, top - 0.6, z1 - 1.0), (xx * 1.6, top - 6.0, z1 + 6.0 + (i % 2) * 2), 2,
                    strands(P, "mane", "mane_dark"), extend=0.3)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):  # elbow blades
                el = a[nm]["elbow"]
                spike(m, a[nm]["bone"], el, (sx * 0.4, 0.4, 1), 1.4, 5.0, solid(P, "claw"), tip=0.5)
        if stage == "perfect":                                   # cyborg armour, chest cannon, mechanical wings
            bd = a["body"]
            STEEL = metal(P, "steel", dark="steel_dark")
            m.box(bd, -5.0, 28.0, -12.0, 5.0, 38.0, -8.0, armour(P, "steel", "steel_dark"))
            for sx in (-1, 1):
                rod(m, bd, (sx * 2.4, 32.0, -12.0), (sx * 2.4, 32.0, -16.0), 3, STEEL, extend=0)
                m.box(bd, sx * 2.4 - 1.0, 31.0, -16.4, sx * 2.4 + 1.0, 33.0, -16.0, solid(P, "glow", glow=True))
            for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
                wb = m.bone(nm, bd, (sx * 5.0, 36.0, 4.0))
                for j in range(3):
                    rod(m, wb, (sx * 5.0, 36.0, 4.0), (sx * (14.0 + j * 2), 44.0 - j * 4, 8.0 + j), 2, STEEL,
                        extend=0.3)
            m.box(hd, -3.0, top - 1.0, z0 - 1.0, 3.0, top + 1.0, z1, armour(P, "steel", "steel_dark"))   # helm
        return m
    return build
