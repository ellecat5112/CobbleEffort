"""Shared builder for Rasenmon and Rasenmon: Fury Mode (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Rasenmon: a lion-beast knight in dark gunmetal armour with a white fur mane and a spiky golden crest,
red-veined black blade-quills fanning from its back like a wheel of spears, red claws, a golden belt, and a blazing
sun-orb in one hand. Fury Mode: a nine-tailed violet beast of rage: a hunched striped violet-and-black body with long
golden claws, nine great coiling blue tails webbed with glowing lines, and a snarling fur-maned head. Shiny: silver /
crimson.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digibody import humanoid
from _digidetail import armour, fur, metal, solid
from _route import pal, tone


def make(name, fury=False):
    base = {"gun": (60, 58, 70), "gun_dark": (20, 20, 26), "white": (240, 236, 230), "white_dark": (180, 176, 170),
            "gold": (240, 200, 60), "gold_dark": (160, 110, 20), "red": (200, 30, 40), "red_dark": (110, 10, 16),
            "black": (24, 22, 28), "sun": (255, 210, 80), "violet": (120, 70, 190), "violet_dark": (50, 24, 100),
            "blue": (40, 60, 170), "blue_dark": (14, 20, 80), "line": (170, 170, 255), "eye": (240, 50, 50)}
    shiny = ({"gun": (200, 204, 216), "gun_dark": (110, 114, 130)} if not fury else
             {"violet": (190, 40, 50), "violet_dark": (100, 14, 20), "blue": (150, 20, 40), "blue_dark": (70, 8, 16),
              "line": (255, 170, 120)})

    def P(v):
        return pal(base, shiny, v)

    GUN = armour(P, "gun", "gun_dark", trim="gold", trim_w=0.2)
    MANE = fur(P, "white", "white_dark", length=1.6)
    GOLD = metal(P, "gold", dark="gold_dark")

    def quillf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["red"] if (x + y + z) % 3.0 < 0.8 else p["black"], face), None

    def stripef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if (y + abs(x) * 0.5) % 3.0 < 1.0:
            return tone(p["black"], face), None
        return armour(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)

    def tailf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if abs(((x + z) * 0.6 + y * 0.6) % 3.0 - 1.5) < 0.12 or abs(((x - z) * 0.6 - y * 0.6) % 3.0 - 1.5) < 0.12:
            return p["line"], p["line"]
        return armour(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        if not fury:
            mats = {"skin": GUN, "neck": MANE, "hand": GUN, "finger": GUN, "claw": solid(P, "red"),
                    "talon": solid(P, "red")}
            a = humanoid(m, mats, bulk=1.1, arm_bulk=1.1, leg_bulk=1.1, claws=True, talons=True, digitigrade=True,
                         name=name)
            bd = a["body"]
            m.round_box(bd, 0, 0, 6.6, 5.0, 46.0, 53.0, MANE, cut=2)                     # white mane
            m.round_box(bd, 0, 0, 5.0, 3.8, 32.0, 34.0, GOLD, cut=1)                      # golden belt
            hd = m.bone("head", bd, (0, 55, 0))
            m.round_box(hd, 0, -0.8, 2.8, 3.2, 54.0, 60.0, MANE, cut=1)
            m.round_box(hd, 0, -3.8, 1.8, 1.4, 54.0, 57.0, GUN, cut=0)
            for sx in (-1, 1):
                m.box(hd, min(sx * 1.0, sx * 2.0), 57.4, -4.1, max(sx * 1.0, sx * 2.0), 58.2, -3.9,
                      solid(P, "eye", glow=True))
            for j in range(9):                                                           # golden crest
                ang = math.radians(-60 + j * 15)
                spike(m, hd, (2.4 * math.sin(ang), 60.0, -0.4), (math.sin(ang) * 0.6, 1, 0.3), 1.0, 4.0 + (j % 2) * 2.0,
                      GOLD, tip=0.8)
            wb = m.bone("quills", bd, (0, 46, 4))                                        # wheel of blade-quills
            for j in range(10):
                ang = math.radians(-30 + j * 24)
                spike(m, wb, (0, 44.0, 4.0), (math.cos(ang), math.sin(ang), 0.6), 2.2, 26.0, quillf, tip=0.8)
            h = a["arm_right"]["hand"]
            ball(m, a["arm_right"]["bone"], (h[0] - 2.0, h[1], h[2] - 2.0), 4.0, solid(P, "sun", glow=True), layers=3)
            return m
        mats = {"skin": stripef, "head": stripef, "neck": MANE, "claw": GOLD, "paw": stripef}
        a = quadruped(m, mats, name, length=30.0, body_y=22.0, body_rx=8.0, body_ry=8.0, neck=((0, 28, -16),
                      (0, 32, -20)), head_len=10.0, head_w=4.6, head_h=5.0, teeth=4, tail=((0, 24, 15), (0, 24, 18),
                      (0, 24, 20)), tail_r=(3.0, 2.6, 2.0))
        bd = a["body"]
        m.round_box(bd, 0, -14.0, 7.0, 5.0, 24.0, 34.0, MANE, cut=2)
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 4.4, sx * 4.8))
            m.box(a["head"], x0, 33.0, -25.0, x1, 34.0, -23.6, solid(P, "eye", glow=True))
            for zz in (-11.0, 11.0):                                                     # long golden claws
                for f in range(3):
                    spike(m, bd, (sx * 6.0 + (f - 1) * 1.4, 1.0, zz - 3.0), (0, -0.2, -1), 1.0, 6.0, GOLD, tip=0.8)
        for j in range(9):                                                               # nine coiling tails
            ang = math.radians(-80 + j * 20)
            tb = m.bone(f"tail_{j}", "tail", (0, 24, 20))
            pts = [(0, 24.0, 20.0)]
            for i in range(1, 6):
                r = i * 6.0
                pts.append((r * math.sin(ang) * 0.9, 24.0 + r * math.cos(ang) * 0.9 + 4.0 * math.sin(i),
                            20.0 + r * 0.5 + 4.0 * math.cos(i * 1.3)))
            for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tb, p0, p1, max(2, 5 - i), tailf, extend=0.6)
        return m

    return build
