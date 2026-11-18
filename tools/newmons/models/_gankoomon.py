"""Shared builder for Gankoomon and Gankoomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the Royal Knight who fights as a man. Base: a lean warrior in a black bodysuit with red seams, spiky
red hair, white wristbands and a long white tattered coat, and behind him his towering golden spirit Hinukamuy, a
translucent maned beast-giant with fists wreathed in flame. X-Antibody: the warrior bare-chested in his official
design, spiky red-and-gold hair, white-and-grey hakama with silver greaves, red-clawed boots, a red cross relic at his
hip, wrapped in golden flame. Shiny: blue spirit flame, navy suit.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import cape, humanoid
from _digidetail import armour, cutout, fabric, flame_inside, local, metal, skin, solid, strands
from _route import pal, tone


def make(name, x=False):
    base = {"suit": (36, 34, 40), "suit_dark": (12, 12, 16), "seam": (200, 30, 40), "skin": (230, 180, 140),
            "skin_dark": (170, 120, 90), "tan": (180, 120, 80), "tan_dark": (120, 76, 46), "hair": (210, 40, 40),
            "hair_dark": (130, 14, 20), "hair_tip": (250, 210, 70), "white": (240, 240, 246), "white_dark": (170, 172, 190),
            "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "spirit": (250, 220, 90, 120),
            "spirit_dark": (230, 170, 40, 150), "fire": (255, 190, 40, 210), "fire_core": (255, 250, 200, 235),
            "red": (210, 30, 40), "eye": (250, 220, 60)}
    shiny = {"spirit": (110, 180, 255, 120), "spirit_dark": (60, 120, 230, 150), "fire": (90, 170, 255, 210),
             "suit": (30, 40, 90), "suit_dark": (10, 14, 40)}

    def P(v):
        return pal(base, shiny, v)

    SUIT0 = skin(P, "suit", dark="suit_dark")

    def suitf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs((xx * 0.4) % 4.0 - 2.0) < 0.12:
            return tone(p["seam"], face), None
        return SUIT0(xx, y, z, face, variant, box=box, **k)

    SKIN = skin(P, "tan" if x else "skin", dark="tan_dark" if x else "skin_dark")
    WHITE = fabric(P, "white", "white_dark", axis="y")
    SILVER = armour(P, "silver", "silver_dark", trim="red", trim_w=0.25)
    HAIR = strands(P, "hair", "hair_dark", tip="hair_tip")

    def firef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
        return c, c[:3]

    def flame(m, bone, at, w, h, seed):
        for ang in (0, 90):
            m.box(bone, at[0] - w / 2, at[1], at[2], at[0] + w / 2, at[1] + h, at[2],
                  cutout(flame_inside(4, 0.1, seed), firef), rotation=(0, ang, 0), pivot=at)

    def spiritf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        c = p["spirit_dark"] if (y * 0.6 + xx * 0.3) % 3.0 < 0.5 else p["spirit"]
        return c, c[:3]

    def build():
        m = Model(name)
        if x:
            mats = {"skin": SKIN, "pelvis": WHITE, "thigh": WHITE, "knee": SILVER, "shin": SILVER, "calf": SILVER,
                    "foot": SILVER, "talon": solid(P, "red"), "toe": SILVER, "forearm": SKIN}
        else:
            mats = {"skin": suitf, "hand": SKIN, "finger": SKIN, "foot": solid(P, "suit_dark")}
        a = humanoid(m, mats, bulk=1.0, arm_bulk=1.0, leg_bulk=1.0, talons=x, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.8, 53.6, 59.8, SKIN, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.6), 57.4, -3.1, max(sx * 0.6, sx * 1.6), 58.0, -2.9, solid(P, "eye"))
        for i in range(10):                                                          # spiky red hair
            ang = math.radians(-100 + i * 22)
            spike(m, hd, (2.2 * math.sin(ang), 59.4, 0.6 + 1.6 * math.cos(ang)), (math.sin(ang) * 0.6, 1, 0.6),
                  1.8, 6.0 + (i % 3) * 1.6, HAIR, tip=0.8)
        for nm in ("arm_left", "arm_right"):                                          # white wristbands
            w = a[nm]["wrist"]
            m.round_box(a[nm]["bone"], w[0], w[2], 1.8, 1.8, w[1], w[1] + 2.4, solid(P, "white"), cut=0)
        if x:
            m.round_box(bd, 0, 0.0, 5.2, 4.0, 33.0, 35.0, solid(P, "suit"), cut=1)       # black sash
            m.round_box(bd, 7.0, -1.0, 1.4, 1.4, 24.0, 30.0, solid(P, "red"), cut=0)     # cross relic
            m.round_box(bd, 7.0, -1.0, 3.0, 1.0, 26.4, 27.6, solid(P, "red"), cut=0)
            for j, (px, py) in enumerate(((-9.0, 30.0), (9.0, 34.0), (-7.0, 46.0), (8.0, 52.0), (0.0, 62.0))):
                flame(m, bd, (px, py, 2.0), 6.0, 10.0, j + 2)                          # golden flame aura
            return m
        cape(m, bd, 51.0, 14.0, 34.0, WHITE, z=4.0, flare=0.9)                        # long white coat
        sp = m.bone("spirit", bd, (0, 60, 10))                                          # Hinukamuy
        m.round_box(sp, 0, 12.0, 10.0, 6.0, 50.0, 78.0, spiritf, cut=3)
        m.round_box(sp, 0, 10.0, 6.0, 6.0, 78.0, 92.0, spiritf, cut=2)
        for i in range(12):
            ang = math.radians(-120 + i * 22)
            spike(m, sp, (6.0 * math.sin(ang), 88.0 + 4.0 * math.cos(ang), 12.0), (math.sin(ang), math.cos(ang), 0.2),
                  2.4, 8.0, spiritf, tip=1.0)
        for sx in (-1, 1):
            rod(m, sp, (sx * 10.0, 74.0, 12.0), (sx * 18.0, 50.0, 6.0), 6, spiritf, extend=0.6)
            m.round_box(sp, sx * 18.0, 6.0, 4.0, 4.0, 42.0, 50.0, spiritf, cut=2)
            flame(m, sp, (sx * 18.0, 48.0, 6.0), 8.0, 12.0, 5 + sx)
        return m

    return build
