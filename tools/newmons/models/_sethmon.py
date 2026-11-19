"""Shared builder for Sethmon and Sethmon Wild Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Sethmon (the Armor Digimon of knowledge): a red beast with yellow tiger flame-stripes and a pale blue
underbelly, a sweeping white skull-mask with long tusks and a black shark-fin crest, a shaggy green tail, and white
claws. Wild Mode: rearing up into a hulking red beast-man with a grizzled white-and-violet ape face under the skull
mask, a green mane, and two spiked iron maces on chains ending in black dog heads. Shiny: blue / gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digibody import humanoid
from _digidetail import armour, fur, metal, skin, solid, strands
from _route import pal, tone


def make(name, wild=False):
    base = {"red": (210, 40, 30), "red_dark": (130, 14, 10), "yellow": (250, 200, 50), "blue": (110, 170, 230),
            "white": (240, 240, 246), "white_dark": (180, 184, 196), "black": (30, 28, 32), "green": (110, 170, 60),
            "green_dark": (50, 100, 20), "violet": (90, 70, 140), "steel": (190, 194, 206), "steel_dark": (90, 94, 108),
            "eye": (250, 60, 60), "claw": (246, 246, 240)}
    shiny = {"red": (40, 80, 200), "red_dark": (14, 30, 120), "yellow": (250, 240, 160)}

    def P(v):
        return pal(base, shiny, v)

    def hidef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "down":
            return tone(p["blue"], face), None
        if abs(math.sin(z * 0.7 + abs(x) * 0.5 + y * 0.3)) > 0.9:
            return tone(p["yellow"], face), None
        return skin(P, "red", dark="red_dark", var=0.03)(x, y, z, face, variant, box=box, **k)

    MASK = armour(P, "white", "white_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        if not wild:
            mats = {"skin": hidef, "head": MASK, "snout": MASK, "jaw": hidef, "claw": solid(P, "claw")}
            a = quadruped(m, mats, name, length=28.0, body_y=14.0, body_rx=6.4, body_ry=6.0, neck=((0, 18, -14),
                          (0, 20, -18)), head_len=12.0, head_w=4.4, head_h=4.4, snout=0.7, teeth=4,
                          tail=((0, 16, 14), (0, 20, 20), (0, 22, 26)), tail_r=(2.4, 2.6, 2.0))
            hd = a["head"]
            spike(m, hd, (0, 24.0, -16.0), (0, 1, 0.5), 2.4, 12.0, solid(P, "black"), tip=0.8)      # shark-fin crest
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.0, 18.0, -28.0), (sx * 0.2, -0.3, -1), 1.2, 8.0, MASK, tip=0.8)   # tusks
                x0, x1 = sorted((sx * 4.3, sx * 4.6))
                m.box(hd, x0, 22.0, -24.0, x1, 22.8, -22.6, solid(P, "eye", glow=True))
            for j in range(5):                                                           # shaggy green tail
                spike(m, "tail", (0, 22.0, 26.0), ((j - 2) * 0.3, 0.3, 1), 1.6, 6.0, strands(P, "green", "green_dark"),
                      tip=0.8)
            return m
        mats = {"skin": hidef, "neck": fur(P, "white", "white_dark"), "claw": solid(P, "claw"),
                "talon": solid(P, "claw")}
        a = humanoid(m, mats, bulk=1.35, arm_bulk=1.4, leg_bulk=1.3, claws=True, talons=True, digitigrade=True,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 3.0, 3.2, 52.0, 59.0, fur(P, "white", "violet"), cut=1)          # ape face
        m.round_box(hd, 0, -3.6, 2.0, 1.0, 52.6, 56.0, solid(P, "violet"), cut=0)
        m.round_box(hd, 0, -1.6, 3.4, 3.8, 58.0, 62.0, MASK, cut=1)                               # skull mask
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.0), 59.6, -5.5, max(sx * 0.8, sx * 2.0), 60.6, -5.3, solid(P, "eye", glow=True))
            spike(m, hd, (sx * 2.6, 61.0, -1.0), (sx * 0.6, 1, 0.3), 1.8, 9.0, MASK, tip=0.8)
        for j in range(8):                                                               # green mane
            spike(m, bd, ((j % 4 - 1.5) * 2.0, 50.0 - (j // 4) * 4.0, 4.0), ((j % 4 - 1.5) * 0.3, 0.2, 1), 1.6, 6.0,
                  strands(P, "green", "green_dark"), tip=0.8)
        for side in ("arm_left", "arm_right"):                                           # spiked maces on chains
            h = a[side]["hand"]
            sx = 1 if side == "arm_left" else -1
            c = (h[0] + sx * 8.0, h[1] - 6.0, h[2] - 2.0)
            rod(m, a[side]["bone"], h, c, 1, STEEL, extend=0.1, t2=1)
            ball(m, a[side]["bone"], c, 3.0, STEEL, layers=3)
            for j in range(6):
                ang = 2 * math.pi * j / 6
                spike(m, a[side]["bone"], (c[0] + 2.6 * math.cos(ang), c[1] + 2.6 * math.sin(ang), c[2]),
                      (math.cos(ang), math.sin(ang), 0), 1.0, 2.6, STEEL, tip=0.8)
            m.round_box(a[side]["bone"], c[0] + sx * 4.6, c[2], 1.6, 1.8, c[1] - 1.4, c[1] + 1.4, solid(P, "black"), cut=0)
            spike(m, a[side]["bone"], (c[0] + sx * 6.2, c[1], c[2]), (sx, -0.2, 0), 1.0, 2.0, solid(P, "black"), tip=0.8)
        return m

    return build
