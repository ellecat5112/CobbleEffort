"""Shared builder for Deadly Tuwarmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a
towering gold-armoured war machine with a white breastplate bearing a star, a tall pointed gold cone head with a red
crest and a little gold figure perched on its shoulder, two great white rolled-scroll wings on its back, a long gold
pickaxe staff, a gold lance-blade on its right arm, black legs bound with steel rings and huge curved gold axe blades
for feet. make(hell=True): Hell Mode, studded all over with black spikes, a heavier cannon arm with a green gem and a
spiked tail. Shiny: silver armour.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import dome, humanoid
from _digidetail import armour, gem, local, metal, solid
from _route import pal, tone

BASE = {"gold": (236, 196, 60), "gold_dark": (150, 110, 20), "gold_light": (255, 240, 160), "white": (236, 236, 240),
        "white_dark": (160, 160, 170), "black": (40, 40, 46), "black_dark": (14, 14, 18), "red": (210, 30, 30),
        "steel": (200, 204, 214), "steel_dark": (100, 104, 114), "green": (60, 220, 100), "green_light": (200, 255, 210),
        "eye": (20, 20, 24)}
SHINY = {"gold": (200, 206, 220), "gold_dark": (110, 116, 130), "gold_light": (255, 255, 255), "red": (60, 120, 230)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.25)
WHITE = armour(P, "white", "white_dark")
BLACK = metal(P, "black", dark="black_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        r = math.hypot(x, y - 46.0)
        a = math.atan2(y - 46.0, x)
        if r < 2.6 * (0.55 + 0.45 * abs(math.cos(2.5 * a))):
            return tone(p["white_dark"], face), None                    # the star
    return WHITE(x, y, z, face, variant, box=box, **k)


def scrollf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        u, v, W, H = local(x, y, z, face, box)
        r = math.hypot(u - W / 2, v - H / 2)
        if abs(r % 1.6 - 0.8) < 0.18:
            return tone(p["white_dark"], face), None                    # the rolled spiral
    return WHITE(x, y, z, face, variant, box=box, **k)


def make(name, hell=False):
    def build():
        m = Model(name)
        mats = {"skin": GOLD, "chest": chestf, "abs": BLACK, "pelvis": GOLD, "neck": BLACK, "deltoid": GOLD,
                "upper_arm": BLACK, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": GOLD, "knee": GOLD,
                "shin": BLACK, "calf": BLACK, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.25, arm_bulk=1.2, leg_bulk=1.3, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        for j, r in enumerate((3.6, 3.0, 2.4, 1.8, 1.2)):                     # tall cone head
            m.round_box(hd, 0, -0.4, r, r, 54.0 + j * 2.0, 56.0 + j * 2.0, GOLD, cut=1)
        m.box(hd, -0.6, 58.0, -2.6, 0.6, 66.0, -1.0, solid(P, "red"))         # red crest
        m.box(hd, -2.4, 55.0, -4.0, 2.4, 56.4, -3.4, solid(P, "eye"))         # visor slit
        rb = m.bone("rider", bd, (6, 53, 0))                                  # little gold rider
        m.round_box(rb, 7.0, 1.0, 1.4, 1.4, 53.0, 56.0, GOLD, cut=1)
        dome(m, rb, (7.0, 56.0, 1.0), 1.4, 1.6, GOLD)
        for sx in (-1, 1):                                                    # rolled scroll wings
            for j in range(2):
                x0, x1 = sorted((sx * 3.0, sx * (16.0 - j * 3.0)))
                m.round_box(bd, (x0 + x1) / 2, 5.0 + j * 1.0, (x1 - x0) / 2, 2.6, 50.0 - j * 7.0, 56.0 - j * 7.0,
                            WHITE, cut=1)
                xe = sx * (16.0 - j * 3.0)
                m.round_box(bd, xe, 5.0 + j, 1.6, 3.2, 49.0 - j * 7.0, 57.0 - j * 7.0, scrollf, cut=1)
            dome(m, bd, (sx * 8.0, 50.0, 0), 4.2, 3.4, GOLD)                  # big pauldrons
        ar = a["arm_left"]                                                    # pickaxe staff
        hx, hy, hz = ar["hand"]
        rod(m, ar["bone"], (hx, hy - 16.0, hz), (hx, hy + 22.0, hz), 1, GOLD, extend=0)
        for sgn in (-1, 1):
            rod(m, ar["bone"], (hx, hy + 22.0, hz), (hx + sgn * 6.0, hy + 18.0, hz - 1.0), 1, GOLD, extend=0.4)
        ar = a["arm_right"]                                                   # lance-blade / cannon arm
        hx, hy, hz = ar["hand"]
        if hell:
            m.round_box(ar["bone"], hx, hz - 2.0, 3.6, 4.0, hy - 6.0, hy + 4.0, GOLD, cut=1)
            m.box(ar["bone"], hx - 1.6, hy - 2.6, hz - 6.8, hx + 1.6, hy + 0.6, hz - 5.6, gem(P, "green", "green_light"))
        rod(m, ar["bone"], (hx, hy - 1.0, hz - 2.0), (hx - 4.0, hy - 6.0, hz - 22.0), 2, GOLD, extend=0.4)
        spike(m, ar["bone"], (hx - 4.0, hy - 6.0, hz - 22.0), (-0.2, -0.25, -1), 2.0, 5.0, GOLD, tip=0.2)
        for nm in ("leg_left", "leg_right"):
            lg = a[nm]
            kn, ak = lg["knee"], lg["ankle"]
            for j in range(3):
                m.round_box(lg["bone"], kn[0], kn[2], 2.8, 2.8, 6.0 + j * 2.6, 7.0 + j * 2.6, STEEL, cut=1)
            sx = 1 if kn[0] > 0 else -1
            x0, x1 = sorted((ak[0] - sx * 1.0, ak[0] + sx * 1.0))
            m.box(lg["bone"], x0, 0.0, ak[2] - 9.0, x1, 7.0, ak[2] + 6.0, GOLD)  # axe-blade foot
            spike(m, lg["bone"], (ak[0], 3.0, ak[2] - 9.0), (0, 0.4, -1), 2.0, 4.0, GOLD, tip=0.2)
            spike(m, lg["bone"], (ak[0], 3.0, ak[2] + 6.0), (0, 0.4, 1), 2.0, 3.0, GOLD, tip=0.2)
        if hell:                                                              # black spikes everywhere
            for i in range(18):
                ang = i * 2.4
                y = 30.0 + (i * 7) % 24
                d = (math.sin(ang), 0.3, math.cos(ang))
                spike(m, bd, (5.6 * d[0], y, 4.2 * d[2]), d, 1.0, 4.0, BLACK, tip=0.2)
            tl = m.bone("tail", bd, (0, 32, 4))
            pts = [(0, 32.0, 4.0), (0, 22.0, 12.0), (2.0, 12.0, 18.0), (4.0, 4.0, 22.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, tl, p0, p1, 3 - j, BLACK, extend=0.5)
                spike(m, tl, p1, (0, 1, 0.5), 1.0, 3.0, BLACK, tip=0.2)
        return m
    return build
