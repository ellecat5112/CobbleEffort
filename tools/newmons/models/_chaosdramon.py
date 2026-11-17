"""Shared builder for Chaosdramon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the red
machine dragon. A hunched red Chrome Digizoid mecha-dragon traced with dark grid lines, a fanged dragon head with a
long nose horn, rounded red shoulder pods with grey vents and red bolts, back-mounted cannon barrels, huge grey
crab-claw arms with steel talons, thick armoured legs and a heavy segmented tail.
make(x=True): the X-Antibody form, black-and-red with two enormous grey bazooka cannons on its shoulders.
Shiny: gold for the base form, white for X.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import dome, humanoid
from _digidetail import armour, local, metal, solid
from _route import pal, tone

BASE = {"red": (200, 30, 30), "red_dark": (100, 10, 10), "red_light": (250, 110, 100), "grid": (60, 10, 10),
        "grey": (150, 152, 164), "grey_dark": (70, 72, 82), "steel": (220, 224, 234), "steel_dark": (110, 114, 126),
        "black": (34, 32, 38), "eye": (250, 230, 60), "tooth": (250, 250, 246), "mouth": (80, 10, 10),
        "orange": (250, 160, 40)}
SHINY = {"red": (236, 196, 60), "red_dark": (160, 120, 20), "red_light": (255, 240, 160), "grid": (110, 80, 10)}
SHINY_X = {"red": (230, 230, 240), "red_dark": (150, 150, 166), "red_light": (255, 255, 255), "grid": (60, 60, 80),
           "black": (180, 30, 30)}


def make(name, x=False):
    def P(v):
        return pal(BASE, SHINY_X if x else SHINY, v)

    RED = armour(P, "red", "red_dark", light="red_light")
    GREY = metal(P, "grey", dark="grey_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def gridded(xx, y, z, face, variant, box=None, **k):
        """Red plate traced with a dark grid of panel lines (black for the X form)."""
        p = P(variant)
        a, b = (xx, y) if face in ("north", "south") else (z, y) if face in ("east", "west") else (xx, z)
        if (a % 2.4) < 0.25 or (b % 2.4) < 0.25:
            return tone(p["black"] if x else p["grid"], face), None
        return RED(xx, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": gridded, "chest": gridded, "abs": gridded, "pelvis": gridded, "neck": GREY, "deltoid": RED,
                "upper_arm": GREY, "forearm": GREY, "hand": GREY, "finger": STEEL, "claw": STEEL, "thigh": gridded,
                "knee": GREY, "shin": gridded, "calf": gridded, "foot": RED, "talon": STEEL}
        a = humanoid(m, mats, bulk=1.5, arm_bulk=1.4, leg_bulk=1.6, digitigrade=True, claws=True, talons=True,
                     name=name, hand_pose="fist")
        bd = a["body"]
        hd = m.bone("head", bd, (0, 52, -4))                                      # head thrust forward
        m.round_box(hd, 0, -6.0, 3.4, 3.6, 50.0, 57.0, gridded, cut=1)
        m.box(hd, -2.8, 49.6, -16.0, 2.8, 53.6, -8.0, gridded)                      # long snout
        jw = m.bone("jaw", hd, (0, 49.6, -8))
        m.box(jw, -2.4, 47.6, -15.0, 2.4, 49.4, -8.0, RED, rotation=(16, 0, 0), pivot=(0, 49.6, -8.0))
        m.box(hd, -2.4, 49.2, -15.6, 2.4, 49.6, -8.4, solid(P, "mouth"))
        for i in range(5):
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.2, 49.6, -15.0 + i * 1.4), (0, -1, 0), 0.8, 1.4, solid(P, "tooth"))
        spike(m, hd, (0, 53.4, -15.0), (0, 0.4, -1), 2.4, 6.0, STEEL, tip=0.6)        # nose horn
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.3, sx * 3.6), 54.2, -9.0, max(sx * 3.3, sx * 3.6), 55.2, -7.0, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.6, 56.6, -4.0), (sx * 0.4, 0.4, 1), 1.6, 5.0, STEEL)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = a[nm]
            sh = ab["shoulder"]
            dome(m, ab["bone"], (sh[0] + sx * 2.4, 48.0, 0.4), 6.4, 6.0, RED, layers=4)  # shoulder pods
            for j in range(3):
                m.box(ab["bone"], sh[0] + sx * 7.6 - 0.4, 48.0 + j * 1.6, -3.0, sh[0] + sx * 7.6 + 0.4, 49.0 + j * 1.6,
                      3.0, GREY)
            h = ab["hand"]                                                          # crab-claw hands
            m.round_box(ab["bone"], h[0], h[2] - 2.0, 4.0, 4.6, h[1] - 2.0, h[1] + 5.0, GREY, cut=2)
            for d in (-1, 1):
                rod(m, ab["bone"], (h[0], h[1] - 1.0, h[2] - 2.0 + d * 2.4),
                    (h[0] + sx * 1.0, h[1] - 9.0, h[2] - 4.0 + d * 3.4), 3, STEEL, extend=0.4)
                spike(m, ab["bone"], (h[0] + sx * 1.0, h[1] - 9.0, h[2] - 4.0 + d * 3.4), (0, -1, -d * 0.5), 1.6, 4.0,
                      STEEL, tip=0.4)
        if x:                                                                       # twin bazookas
            for sx in (-1, 1):
                rod(m, bd, (sx * 6.0, 58.0, 12.0), (sx * 7.0, 66.0, -18.0), 6, GREY, extend=0)
                rod(m, bd, (sx * 7.0, 66.0, -18.0), (sx * 7.2, 66.6, -22.0), 7, solid(P, "black"), extend=0)
                m.round_box(bd, sx * 6.4, 2.0, 3.4, 3.4, 56.0, 63.0, RED, cut=1)
        else:                                                                       # back cannon barrels
            for sx in (-1, 1):
                rod(m, bd, (sx * 3.0, 54.0, 6.0), (sx * 3.4, 62.0, 2.0), 2, STEEL, extend=0)
                rod(m, bd, (sx * 3.4, 62.0, 2.0), (sx * 3.4, 64.0, 1.0), 3, GREY, extend=0)
        m.round_box(bd, 0, 1.0, 1.4, 1.4, 42.0, 45.0, solid(P, "orange", glow=True), cut=1)
        tl = m.bone("tail", bd, (0, 31, 4))
        pts = [(0, 31.0, 4.0), (0, 24.0, 12.0), (2.0, 16.0, 18.0), (4.0, 10.0, 24.0), (6.0, 6.0, 30.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, max(2, 7 - j), gridded, extend=0.6)
            spike(m, tl, p1, (0, 1, 0.3), 1.4, 2.4, STEEL)
        return m
    return build
