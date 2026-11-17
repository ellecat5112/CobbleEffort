"""Shared builder for Deckerdramon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a long,
low, crocodile-like war machine. A brown armoured hull riding on two steel caterpillar tracks, a long armoured
crocodile snout with a red eye, a slate-blue gun deck with twin turrets and a missile pod, short grey clawed arms and
a segmented tail ending in a missile launcher. make(float_mode=True): Float Mode, the same hull turned hovercraft:
two big black pontoons with hex panels at its sides, the deck flattened into a raft and the snout tucked down at the
front. Shiny: olive green and sand.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

BASE = {"brown": (120, 96, 70), "brown_dark": (60, 44, 30), "brown_light": (190, 160, 120), "slate": (80, 96, 120),
        "slate_dark": (34, 40, 56), "slate_light": (150, 170, 200), "grey": (150, 150, 166), "grey_dark": (70, 70, 84),
        "black": (40, 40, 46), "black_dark": (12, 12, 16), "steel": (200, 204, 214), "steel_dark": (100, 104, 114),
        "red": (230, 40, 40), "green": (80, 230, 120)}
SHINY = {"brown": (110, 120, 60), "brown_dark": (50, 60, 20), "brown_light": (180, 190, 120), "slate": (200, 180, 130),
         "slate_dark": (120, 100, 60)}


def P(v):
    return pal(BASE, SHINY, v)


HULL = armour(P, "brown", "brown_dark", light="brown_light", rivets=True)
DECK = armour(P, "slate", "slate_dark", light="slate_light", trim="black", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")
TRACK = riveted(P, "black", "black_dark", spacing=1.6)
GREY = metal(P, "grey", dark="grey_dark")


def podf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north"):
        a, b = (z, y) if face != "north" else (x, y)
        if abs((a * 0.5) % 3.0 - 1.5) + abs((b * 0.5) % 3.0 - 1.5) * 0.6 < 0.3:
            return tone(p["slate_light"], face), None              # hex panel seams
    return armour(P, "black", "black_dark")(x, y, z, face, variant, box=box, **k)


def make(name, float_mode=False):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 8, 0))
        m.round_box(bd, 0, 0, 7.0, 14.0, 5.0, 13.0, HULL, cut=2)                       # the hull
        m.box(bd, -6.0, 13.0, -10.0, 6.0, 16.0 if not float_mode else 14.0, 10.0, DECK)  # gun deck
        hd = m.bone("head", bd, (0, 10, -14))
        snout_y = 9.0 if not float_mode else 6.0
        m.round_box(hd, 0, -20.0, 3.6, 7.0, snout_y - 3.0, snout_y + 3.0, HULL, cut=1)  # long croc snout
        for j in range(5):
            m.box(hd, -3.4, snout_y - 3.6, -26.0 + j * 2.6, 3.4, snout_y - 3.0, -25.0 + j * 2.6, STEEL)  # tooth plates
        for sx in (-1, 1):
            m.box(hd, min(sx * 3.4, sx * 3.8), snout_y + 1.0, -16.0, max(sx * 3.4, sx * 3.8), snout_y + 2.0, -14.6,
                  solid(P, "red", glow=True))
        if not float_mode:
            for sx in (-1, 1):                                                        # caterpillar tracks
                x0, x1 = sorted((sx * 6.0, sx * 9.0))
                m.round_box(top, (x0 + x1) / 2, 0, 1.5, 13.0, 0.0, 6.0, TRACK, cut=1)
            for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                       # short clawed arms
                ab = m.bone(nm, bd, (sx * 7.0, 10.0, -8.0))
                rod(m, ab, (sx * 7.0, 10.0, -8.0), (sx * 9.0, 4.0, -11.0), 3, GREY, extend=0.4)
                for j in range(3):
                    spike(m, ab, (sx * 9.0 + (j - 1) * 1.0, 3.0, -11.6), (0, -0.4, -1), 1.0, 2.6, GREY, tip=0.2)
            tb = m.bone("turret", bd, (0, 16, 0))                                     # twin turrets
            m.round_box(tb, 0, 2.0, 4.0, 4.0, 16.0, 19.0, DECK, cut=1)
            for sx in (-1, 1):
                rod(m, tb, (sx * 1.6, 17.6, 0.0), (sx * 1.6, 18.6, -12.0), 1, STEEL, extend=0, t2=1)
            m.box(bd, -5.0, 16.0, 5.0, -1.0, 19.0, 9.0, DECK)                         # missile pod
            for j in range(4):
                m.box(bd, -4.6 + (j % 2) * 2.0, 16.6 + (j // 2) * 1.2, 4.6, -3.4 + (j % 2) * 2.0, 17.6 + (j // 2) * 1.2,
                      5.0, solid(P, "black"))
            tl = m.bone("tail", bd, (0, 10, 14))
            pts = [(0, 10.0, 14.0), (0, 13.0, 20.0), (0, 18.0, 24.0), (0, 22.0, 24.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tl, p0, p1, 3 - j // 2, HULL, extend=0.5)
            m.round_box(tl, 0, 22.0, 2.0, 4.0, 22.0, 25.0, DECK, cut=1)               # tail launcher
            spike(m, tl, (0, 23.6, 18.0), (0, 0, -1), 1.4, 3.0, STEEL, tip=0.4)
        else:
            for sx in (-1, 1):                                                        # pontoons
                m.round_box(top, sx * 11.0, 0, 4.0, 15.0, 0.0, 12.0, podf, cut=2)
                m.box(top, min(sx * 7.0, sx * 8.0), 4.0, -8.0, max(sx * 7.0, sx * 8.0), 8.0, 8.0, GREY)
                m.round_box(top, sx * 11.0, 0, 1.0, 1.0, 12.0, 15.0, STEEL, cut=0)       # antennae masts
            for j in range(5):                                                        # raft planks
                m.box(bd, -6.0, 14.0, -9.0 + j * 4.0, 6.0, 14.6, -6.6 + j * 4.0, HULL)
        return m
    return build
