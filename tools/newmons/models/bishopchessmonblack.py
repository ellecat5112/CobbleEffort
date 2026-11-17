"""Bishop Chessmon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the bishop of the black chess army. A tall black armoured body shaped like a chess
bishop, a black mitre helm with a spike, a violet tabard with an orange-edged cross, wide riveted violet shoulder
plates, a long violet cape, heavy black-and-grey square feet and a tall staff topped with an arrowhead finial.
25 blocks tall.

Front is -z, y is up. 66 units tall; Perfect stage. make(white=True): Bishop Chessmon (White) (a white segmented
body with a telescoping violet-capped head, a violet cape and a white staff).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("the black chess bishop: a tall black armoured body, a black mitre helm, a violet tabard with an orange-edged "
        "cross, riveted shoulder plates, a long violet cape and a staff with an arrowhead finial")
BASE = {"black": (40, 40, 48), "black_light": (110, 110, 126), "grey": (130, 132, 144), "grey_dark": (70, 72, 82),
        "violet": (110, 60, 170), "violet_dark": (50, 24, 90), "orange": (230, 140, 50), "white": (240, 240, 244),
        "white_dark": (180, 182, 196), "eye": (255, 220, 60)}
SHINY = {"violet": (40, 140, 110), "violet_dark": (16, 80, 60), "orange": (240, 200, 60)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, white=False):
    BODY = armour(P, "white", "white_dark", seams=(1.6,)) if white else armour(P, "black", "black",
                                                                                light="black_light")
    VIOLET = riveted(P, "violet", "violet_dark")
    CAPE = fabric(P, "violet", "violet_dark", axis="y", period=3.0)

    def tabardf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        if face == "north":
            cu, cv = u - W / 2, v - H * 0.55
            if (abs(cu) < W * 0.12 and abs(cv) < H * 0.2) or (abs(cv) < H * 0.05 and abs(cu) < W * 0.32):
                return tone(p["grey"], face), None
            if min(u, W - u) < 0.5:
                return tone(p["orange"], face), None
        return fabric(P, "violet", "violet_dark", axis="y")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": BODY, "hand": BODY, "finger": BODY, "foot": metal(P, "grey", dark="grey_dark"),
                "toe": metal(P, "grey", dark="grey_dark")}
        a = humanoid(m, mats, bulk=1.15, arm_bulk=1.2, leg_bulk=1.3, name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        if white:                                                # telescoping segmented head
            for j in range(5):
                m.round_box(hd, 0, 0, 3.0 - j * 0.2, 3.0 - j * 0.2, 54.0 + j * 2.6, 56.4 + j * 2.6, BODY, cut=1)
            m.round_box(hd, 0, 0, 3.4, 3.4, 67.0, 70.0, VIOLET, cut=1)
            m.box(hd, -2.0, 56.0, -3.4, 2.0, 57.0, -3.0, solid(P, "eye", glow=True))
        else:
            m.round_box(hd, 0, 0, 3.0, 3.0, 54.0, 62.0, BODY, cut=1)
            for j in range(4):                                   # the mitre
                r = 3.0 - j * 0.7
                m.round_box(hd, 0, 0, r, r, 62.0 + j * 2.0, 64.0 + j * 2.0, BODY, cut=max(0, round(r * 0.3)))
            spike(m, hd, (0, 70.0, 0), (0, 1, 0), 1.0, 3.0, metal(P, "grey", dark="grey_dark"))
            m.box(hd, -2.0, 57.6, -3.4, 2.0, 58.4, -3.0, solid(P, "eye", glow=True))
        m.box(bd, -3.6, 18.0, -5.2, 3.6, 50.0, -4.2, tabardf)                            # tabard
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            sh = a[nm]["shoulder"]
            m.box(a[nm]["bone"], min(sh[0], sh[0] + sx * 7.0), 47.0, -4.0, max(sh[0], sh[0] + sx * 7.0), 52.0, 4.0,
                  VIOLET)
        cb = m.bone("cap", bd, (0, 51, 4))
        cape(m, cb, 52.0, 22.0, 50.0, CAPE, z=5.0, flare=0.9, panels=9, sweep=(0, 6))
        h = a["arm_right"]["hand"]                               # staff with arrowhead finial
        st = m.bone("staff", a["arm_right"]["bone"], h)
        rod(m, st, (h[0], 0.0, h[2]), (h[0], 70.0, h[2]), 1, metal(P, "white" if white else "black",
                                                                   dark="grey_dark"), extend=0)
        for sx in (-1, 1):
            m.box(st, min(h[0], h[0] + sx * 4.0), 64.0, h[2] - 0.3, max(h[0], h[0] + sx * 4.0), 70.0, h[2] + 0.3,
                  BODY, rotation=(0, 0, sx * 20), pivot=(h[0], 66.0, h[2]))
        spike(m, st, (h[0], 70.0, h[2]), (0, 1, 0), 1.6, 3.0, BODY)
        return m
    return build


build = make("bishopchessmonblack")
