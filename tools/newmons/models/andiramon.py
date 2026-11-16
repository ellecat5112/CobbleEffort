"""Andiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): one of the Twelve Devas, a rabbit-eared holy beast. A small pale face framed by enormous long
ears tipped pink, a white hooded mantle with a diamond mark, a red segmented chest, long brown sleeve-arms ending in
clawed cuffs that hang to the ground, and baggy pale pants gathered into pointed boots. 25 blocks tall.

Front is -z, y is up. 74 units tall (the ears); Perfect stage. Andiramon (Deva) adds a lilac scarf and lilac pants.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import armour, fabric, local, skin, solid
from _route import pal, tone

HEIGHT = 74
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a rabbit-eared holy beast: a small pale face, enormous pink-tipped ears, a white hooded mantle with a diamond "
        "mark, a red segmented chest, long brown sleeve-arms with clawed cuffs and baggy pale pants")
BASE = {"white": (246, 244, 244), "white_dark": (196, 190, 196), "pink": (244, 170, 200), "pink_dark": (200, 110, 150),
        "pants": (246, 226, 236), "pants_dark": (210, 180, 196), "brown": (150, 120, 100), "brown_dark": (90, 70, 56),
        "red": (190, 40, 40), "red_dark": (110, 16, 20), "face": (246, 236, 226), "eye": (40, 30, 30),
        "scarf": (160, 140, 210), "scarf_dark": (100, 80, 160), "claw": (240, 236, 230)}
SHINY = {"brown": (60, 60, 74), "brown_dark": (30, 30, 40), "red": (40, 150, 120), "red_dark": (16, 80, 60),
         "pink": (150, 220, 255), "pink_dark": (80, 150, 220)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, base, shiny, deva=False):
    def Pv(v):
        return pal(base, shiny, v)

    MANTLE = fabric(Pv, "white", "white_dark", axis="y", period=2.8)
    PANTS = fabric(Pv, "pants", "pants_dark", axis="y", period=3.0)
    SLEEVE = fabric(Pv, "brown", "brown_dark", axis="y", period=2.6)
    CHEST = armour(Pv, "red", "red_dark", seams=(1.6,))
    SCARF = fabric(Pv, "scarf", "scarf_dark", axis="x", period=1.6)

    def earf(x, y, z, face, variant, box=None, **k):
        p = Pv(variant)
        u, v, W, H = local(x, y, z, face, box)
        t = (box.lo[2] + box.size[2] - z) / max(box.size[2], 1e-6)
        if t > 0.75:
            return tone(p["pink"], face), None
        if face == "north" and min(u, W - u) > 0.5:
            return tone(p["pink_dark"] if t < 0.75 else p["pink"], face), None
        return tone(p["brown"], face), None

    def mantlef(x, y, z, face, variant, box=None, **k):
        p = Pv(variant)
        if face == "north" and abs(x) + abs(y - 46.0) < 1.6 and abs(x) + abs(y - 46.0) > 0.7:
            return tone(p["brown_dark"], face), None              # the diamond mark
        return MANTLE(x, y, z, face, variant, box=box, **k)

    def facef(x, y, z, face, variant, box=None, **k):
        p = Pv(variant)
        if face == "north":
            for sx in (-1, 1):
                if abs(x - sx * 0.9) < 0.5 and abs(y - 58.2) < 0.3:
                    return p["eye"], None
            if abs(x) < 0.3 and 56.4 < y < 57.2:
                return p["red"], None
        return skin(Pv, "face", dark="white_dark")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 30, 0))
        for i in range(6):                                       # red segmented chest under the mantle
            m.round_box(bd, 0, 0, 2.6 - abs(i - 2.5) * 0.15, 2.0, 32.0 + i * 2.6, 34.8 + i * 2.6, CHEST, cut=1)
        for i in range(10):                                      # the hooded mantle: a short cape of panels
            ang = math.radians(-162 + i * 36)
            c = (4.6 * math.sin(ang), 52.0, -4.0 * math.cos(ang))
            m.box(bd, c[0] - 1.8, 40.0, c[2], c[0] + 1.8, 53.0, c[2] + 0.8, mantlef,
                  rotation=(-12 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
        if deva:
            for i in range(8):                                   # the lilac scarf knotted at the throat
                ang = math.radians(-140 + i * 40)
                c = (4.0 * math.sin(ang), 51.0, -3.6 * math.cos(ang))
                m.box(bd, c[0] - 1.6, 49.0, c[2] - 0.6, c[0] + 1.6, 52.0, c[2] + 0.6, SCARF,
                      rotation=(0, -math.degrees(ang), 0), pivot=c)
            m.box(bd, -1.2, 42.0, -5.2, 1.2, 50.0, -4.4, SCARF)
        hd = m.bone("head", bd, (0, 54, 0))
        m.round_box(hd, 0, -0.6, 2.4, 2.4, 53.5, 60.5, facef, cut=1)
        m.round_box(hd, 0, 0.6, 3.4, 3.4, 54.0, 62.0, MANTLE, cut=1)                  # the hood behind the face
        for sx in (-1, 1):                                       # the enormous ears
            ear = m.bone("ear_left" if sx > 0 else "ear_right", hd, (sx * 1.8, 61.0, 0))
            rod(m, ear, (sx * 1.8, 61.0, 0.0), (sx * 10.0, 70.0, 2.0), 3, earf, extend=0.4, t2=2)
            rod(m, ear, (sx * 10.0, 70.0, 2.0), (sx * 18.0, 74.0, 3.0), 3, earf, extend=0.4, t2=2)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):     # long sleeve-arms hanging to the ground
            ab = m.bone(nm, bd, (sx * 4.6, 49.0, 0))
            pts = [(sx * 4.6, 49.0, 0.0), (sx * 7.0, 34.0, 0.4), (sx * 8.4, 18.0, 0.0), (sx * 9.0, 6.0, -0.6)]
            for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, ab, p0, p1, 4 + j, SLEEVE, extend=0.6)
            for f in range(4):                                   # clawed cuff fringe
                spike(m, ab, (sx * 9.0 + (f - 1.5) * 1.4, 4.0, -0.6), (0, -1, -0.2), 1.2, 3.0, solid(Pv, "claw"))
            m.box(ab, sx * 8.0 - 0.6, 24.0, -3.6, sx * 8.0 + 0.6, 26.0, -3.0, solid(Pv, "white"))
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):     # baggy pants into pointed boots
            lg = m.bone(nm, top, (sx * 2.2, 31.0, 0))
            m.round_box(lg, sx * 2.6, 0, 3.0, 3.0, 12.0, 32.0, PANTS, cut=1)
            m.round_box(lg, sx * 2.8, -0.4, 2.0, 2.0, 3.0, 12.6, PANTS, cut=1)
            m.box(lg, sx * 2.8 - 1.8, 0.0, -5.0, sx * 2.8 + 1.8, 3.0, 1.6, PANTS)
            spike(m, lg, (sx * 2.8, 1.2, -5.0), (0, 0.2, -1), 1.8, 2.6, PANTS)
        return m
    return build


build = make("andiramon", BASE, SHINY)
