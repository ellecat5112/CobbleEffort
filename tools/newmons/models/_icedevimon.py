"""Shared builder for Ice Devimon and Ice Devimon Enhancement Absorbent (CobbleEffort: Digital; hand-built after the
official art on wikimon.net): the frozen fallen angel: a gaunt white Devimon of ice with pale-blue shadows, long
clawed arms, a blank mask face with red eyes, curling horns, a shock of frost-white hair and great tattered white bat
wings. Enhancement Absorbent: one arm swollen into a huge bandaged ice arm with crystal claws and spiked ice wings.
Shiny: midnight blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import cutout, fabric, gem, local, noise2, skin, solid, strands
from _route import pal, tone

BASE = {"white": (236, 242, 250), "white_dark": (140, 170, 210), "white_light": (255, 255, 255),
        "blue": (120, 170, 230), "ice": (170, 220, 255, 210), "ice_light": (240, 252, 255, 230),
        "membrane": (200, 220, 245), "membrane_dark": (120, 150, 200), "horn": (200, 200, 220),
        "eye": (230, 40, 40), "claw": (130, 170, 230), "bandage": (240, 236, 224), "bandage_dark": (190, 180, 160)}
SHINY = {"white": (60, 70, 140), "white_dark": (24, 28, 70), "white_light": (130, 140, 210),
         "membrane": (70, 80, 150), "membrane_dark": (30, 34, 90)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", light="white_light")


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.12 * abs(math.sin(u * 0.9)) + 0.06 * noise2(u, 0.0, 3)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["membrane_dark"] if v / max(H, 1e-6) < 0.3 else p["membrane"], face), None


def maskf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.1) < 0.6 and abs(y - 58.0) < 0.4:
                return tone(p["eye"], face), p["eye"]
    return SKIN(x, y, z, face, variant, box=box, **k)


def make(name, absorbent=False):
    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": SKIN, "abs": SKIN, "pelvis": SKIN, "neck": SKIN, "deltoid": SKIN,
                "upper_arm": SKIN, "forearm": SKIN, "hand": SKIN, "finger": SKIN, "claw": solid(P, "claw"),
                "thigh": SKIN, "knee": SKIN, "shin": SKIN, "calf": SKIN, "foot": SKIN, "toe": solid(P, "claw")}
        a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=0.88, claws=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.8, 54.0, 60.4, maskf, cut=1)
        for sx in (-1, 1):                                                       # curling horns
            pts = [(sx * 2.2, 59.6, 0.0), (sx * 4.0, 61.0, 1.0), (sx * 5.0, 63.4, 0.0), (sx * 4.0, 65.0, -1.0)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 2 if j < 1 else 1, solid(P, "horn"), extend=0.4)
        for i in range(9):                                                       # frost-white hair
            ang = math.radians(-100 + i * 25)
            rod(m, hd, (2.2 * math.sin(ang), 60.4, 0.8 + math.cos(ang)), (3.4 * math.sin(ang), 53.0, 3.6), 2,
                strands(P, "white_light", "blue"), extend=0.3, t2=1)
        for nm in ("arm_left", "arm_right"):
            ar = a[nm]
            hx, hy, hz = ar["hand"]
            big = absorbent and nm == "arm_right"
            if big:                                                               # huge bandaged ice arm
                el = ar["elbow"]
                rod(m, ar["bone"], el, (hx, hy - 6.0, hz - 2.0), 6, fabric(P, "bandage", "bandage_dark", period=1.2),
                    extend=0.8)
                m.round_box(ar["bone"], hx, hz - 2.0, 4.0, 4.0, hy - 12.0, hy - 5.0, gem(P, "ice", "ice_light", False),
                            cut=2)
                for j in range(4):
                    spike(m, ar["bone"], (hx + (j - 1.5) * 2.0, hy - 12.0, hz - 3.0), (0, -1, -0.3), 1.4, 6.0,
                          gem(P, "ice", "ice_light", False), tip=0.8)
            else:                                                                 # long arms reaching low
                rod(m, ar["bone"], (hx, hy, hz), (hx, hy - 8.0, hz - 1.0), 3, SKIN, extend=0.4)
                m.round_box(ar["bone"], hx, hz - 1.0, 1.8, 1.8, hy - 11.0, hy - 8.0, SKIN, cut=1)
                for j in range(4):
                    spike(m, ar["bone"], (hx + (j - 1.5) * 0.9, hy - 11.0, hz - 1.4), (0, -1, -0.2), 0.8, 3.6,
                          solid(P, "claw"), tip=0.8)
        for side in (1, -1):                                                      # tattered white bat wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
            bat_wing(m, wb, (side * 2.6, 50.0, 3.4), 28.0, 30.0, 4, SKIN, cutout(tatter, wingf), side=side, sweep=20)
            if absorbent:
                for j in range(4):
                    spike(m, wb, (side * (8.0 + j * 5.0), 56.0 - j * 1.5, 4.0), (side * 0.4, 1, 0.3), 1.4, 6.0,
                          gem(P, "ice", "ice_light", False), tip=0.8)
        return m

    return build
