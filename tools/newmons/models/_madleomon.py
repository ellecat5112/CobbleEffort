"""Shared builder for the Mad Leomon forms (CobbleEffort: Digital; hand-built at the detail standard after the official
art on wikimon.net): Leomon turned undead: a hunched violet-grey lion-man with stitched patchy skin, a wild black mane,
bone horns, white-fanged snarl, a black tail tuft. Base: banded black armour on both forearms and shins. Armed Mode:
one arm a huge spiked chainsaw. Final Mode: a towering red-maned violet beast on all fours with bone spikes and red
claws, a loincloth. Orochi Mode: a grey-armoured lion beast entwined with silver serpents with yellow and white heads.
Shiny: green undead.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, fabric, fur, metal, riveted, scales, skin, solid, strands
from _route import pal, tone

BASE = {"violet": (120, 100, 150), "violet_dark": (60, 46, 80), "violet_light": (180, 160, 210), "black": (34, 32, 38),
        "black_dark": (10, 10, 12), "bone": (230, 224, 206), "red": (200, 40, 50), "red_dark": (120, 14, 20),
        "steel": (150, 152, 164), "steel_dark": (70, 72, 84), "eye": (240, 40, 60), "tan": (200, 170, 110),
        "silver": (220, 224, 232), "yellow": (240, 210, 60), "mane_gold": (210, 170, 80), "mane_gold_dark": (140, 100, 40)}
SHINY = {"violet": (100, 150, 100), "violet_dark": (40, 80, 40), "violet_light": (170, 220, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, mode="base"):
    SKIN = skin(P, "violet", dark="violet_dark", light="violet_light")
    BAND = riveted(P, "black", "black_dark")
    ARMG = armour(P, "steel", "steel_dark", trim="black", trim_w=0.2)
    final = mode == "final"
    orochi = mode == "orochi"

    def build():
        m = Model(name)
        body = SKIN if not orochi else ARMG
        mats = {"skin": body, "chest": body, "abs": body, "pelvis": fabric(P, "tan", "black") if final else BAND,
                "neck": body, "deltoid": body, "upper_arm": body, "forearm": BAND if mode in ("base", "armed") else body,
                "hand": body, "finger": body, "claw": solid(P, "red" if final else "bone"), "thigh": body,
                "knee": body, "shin": BAND if mode in ("base", "armed") else body, "calf": body, "foot": body,
                "talon": solid(P, "red" if final else "bone")}
        a = humanoid(m, mats, bulk=1.35 if final else 1.2, arm_bulk=1.4 if final else 1.25, leg_bulk=1.2, claws=True,
                     talons=True, digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 54, -2))
        m.round_box(hd, 0, -2.0, 3.0, 3.4, 52.6, 59.6, body, cut=1)
        m.round_box(hd, 0, -5.4, 2.0, 1.6, 52.8, 56.0, body, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.9, sx * 2.2), 57.0, -5.5, max(sx * 0.9, sx * 2.2), 57.8, -5.3, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 1.0, 53.6, -7.0), (0, -1, 0), 0.8, 1.6, solid(P, "bone"), tip=0.8)
            spike(m, hd, (sx * 2.6, 59.0, -1.0), (sx * 0.6, 0.6, 0.4), 1.2, 4.0, solid(P, "bone"), tip=0.8)   # bone horns
        mane_key = "red" if final else ("mane_gold" if orochi else "black")
        MANE = strands(P, mane_key, "red_dark" if final else ("mane_gold_dark" if orochi else "black_dark"))
        for ring, (r, n, ln) in enumerate(((3.8, 14, 7.0), (5.0, 16, 10.0))):         # wild mane
            for i in range(n):
                ang = 2 * math.pi * (i + ring * 0.5) / n
                spike(m, hd, (r * math.cos(ang) * 0.9, 56.0 + r * math.sin(ang), ring * 1.2 - 1.0),
                      (math.cos(ang), math.sin(ang), 0.6), 2.2, ln, MANE, tip=0.8)
        tb = m.bone("tail", bd, (0, 32, 3))
        pts = [(0, 32.0, 3.4), (3.0, 26.0, 10.0), (6.0, 32.0, 14.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, tb, p0, p1, 1, body, extend=0.3, t2=1)
        spike(m, tb, pts[-1], (0.3, 1, 0.3), 1.6, 3.6, MANE, tip=0.8)
        if final:                                                                  # bone spikes
            for j, (px, py) in enumerate(((7.0, 52.0), (-7.0, 52.0), (9.0, 44.0), (-9.0, 44.0), (6.0, 30.0), (-6.0, 30.0))):
                spike(m, bd, (px, py, 1.0), (math.copysign(1, px), 0.4, 0.3), 1.6, 6.0, solid(P, "bone"), tip=0.8)
        if mode == "armed":                                                        # chainsaw arm
            hr = a["arm_right"]
            hx, hy, hz = hr["hand"]
            m.round_box(hr["bone"], hx, hz, 3.0, 3.0, hy - 4.0, hy + 4.0, BAND, cut=1)
            m.round_box(hr["bone"], hx - 1.0, hz - 1.0, 1.0, 3.0, hy - 34.0, hy - 4.0, metal(P, "steel", dark="steel_dark"), cut=0)
            for j in range(12):
                spike(m, hr["bone"], (hx - 1.0, hy - 6.0 - j * 2.4, hz - 4.0), (0, 0, -1), 0.8, 1.6, solid(P, "black"), tip=0.8)
                spike(m, hr["bone"], (hx - 1.0, hy - 6.0 - j * 2.4, hz + 2.0), (0, 0, 1), 0.8, 1.6, solid(P, "black"), tip=0.8)
        if orochi:                                                                 # silver serpents
            SN = scales(P, "silver", "steel_dark", size=1.0)
            for k_, (sx, key) in enumerate(((1, "yellow"), (-1, "bone"), (1, "silver"))):
                sb = m.bone("serpent_%d" % k_, bd, (sx * 4.0, 44.0 - k_ * 10.0, 2.0))
                pts = [(sx * 4.0, 44.0 - k_ * 10.0, 2.0), (sx * 12.0, 48.0 - k_ * 14.0, -2.0), (sx * 16.0, 56.0 - k_ * 22.0, -6.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    rod(m, sb, p0, p1, 2, SN, extend=0.6)
                e = pts[-1]
                m.round_box(sb, e[0], e[2] - 2.0, 1.6, 3.0, e[1] - 1.2, e[1] + 1.4, solid(P, key), cut=1)
        return m

    return build
