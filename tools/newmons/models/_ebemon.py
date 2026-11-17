"""Shared builder for EBEmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): the grey alien
cyborg. A small white-and-chrome body with a gold V on its chest, a long white domed alien head with a dark brown
visor and a red eye-lens, an orange gem at its waist, a laser gun in one hand, a probe arm with a dish on the other
and a skirt of ribbed steel hoses for legs. make(x=True): EBEmon (X-Antibody), bigger and heavier: a chrome skull
head with a grim mouth grille, a broad white shield-body with a gold chevron, coloured capsule tanks (red, blue, green)
on its shoulders, a green circuit board, a red cannon arm, ribbed hose tentacles and a crackle of teal lightning.
Shiny: gold chrome.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digidetail import armour, gem, local, metal, skin, solid
from _route import pal, tone

BASE = {"white": (240, 240, 244), "white_dark": (170, 172, 186), "white_light": (255, 255, 255),
        "chrome": (200, 204, 216), "chrome_dark": (100, 104, 118), "visor": (100, 70, 50), "visor_light": (190, 150, 120),
        "red": (220, 50, 40), "red_light": (255, 160, 150), "gold": (240, 196, 60), "orange": (250, 150, 40),
        "orange_light": (255, 210, 150), "blue": (60, 110, 220), "green": (30, 110, 70), "green_light": (120, 230, 160),
        "black": (30, 30, 36), "teal": (80, 240, 220, 210)}
SHINY = {"white": (250, 230, 170), "white_dark": (190, 160, 90), "chrome": (230, 200, 120), "chrome_dark": (140, 110, 40)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", light="white_light")
CHROME = metal(P, "chrome", dark="chrome_dark")


def hosef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y + x * 0.2 + z * 0.2) % 1.2 < 0.35:
        return tone(p["chrome_dark"], face), None                    # ribbed hose
    return CHROME(x, y, z, face, variant, box=box, **k)


def hose(m, bone, pts, t=2):
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, t, hosef, extend=0.5)


def chevf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(abs(x) * 0.8 - (y - box.lo[1] - 1.0)) < 0.5 and y - box.lo[1] < 5.0:
        return tone(p["gold"], face), None
    return WHITE(x, y, z, face, variant, box=box, **k)


def make(name, x=False):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 16, 0))
        if not x:
            m.round_box(bd, 0, 0, 4.0, 3.4, 16.0, 26.0, chevf, cut=1)                          # body
            m.round_box(bd, 0, -3.6, 1.2, 0.6, 17.0, 19.0, gem(P, "orange", "orange_light"), cut=0)
            hd = m.bone("head", bd, (0, 27, 0))
            m.round_box(hd, 0, -0.4, 3.0, 3.4, 26.0, 33.0, WHITE, cut=1)                       # domed head
            m.round_box(hd, 0, 2.4, 2.6, 4.4, 30.0, 36.0, WHITE, cut=1)                       # long dome back
            m.box(hd, -2.6, 30.0, -4.0, 2.6, 32.4, -3.6, metal(P, "visor", dark="visor"))       # dark visor
            m.round_box(hd, 0, -3.8, 0.8, 0.4, 27.6, 29.0, gem(P, "red", "red_light"), cut=0)  # eye-lens
            ar = m.bone("arm_right", bd, (-4, 24, 0))                                          # laser gun
            hose(m, ar, [(-4.0, 24.0, 0), (-8.0, 22.0, -2.0), (-9.0, 24.0, -6.0)])
            rod(m, ar, (-9.0, 24.0, -6.0), (-10.0, 32.0, -10.0), 2, CHROME, extend=0)
            al = m.bone("arm_left", bd, (4, 24, 0))                                            # probe arm with a dish
            hose(m, al, [(4.0, 24.0, 0), (9.0, 26.0, -1.0), (13.0, 25.0, -2.0)])
            m.round_box(al, 14.0, -2.0, 1.6, 1.6, 24.0, 27.0, CHROME, cut=1)
            m.box(al, 15.6, 24.0, -4.0, 16.2, 28.0, 0.0, CHROME)
            for j in range(10):                                                                # hose skirt
                ang = 2 * math.pi * j / 10
                base = (2.4 * math.cos(ang), 16.0, 2.0 * math.sin(ang))
                tip = (5.6 * math.cos(ang), 1.0, 4.6 * math.sin(ang))
                hose(m, bd if j % 2 else top, [base, ((base[0] + tip[0]) / 2, 8.0, (base[2] + tip[2]) / 2), tip])
                m.round_box(bd if j % 2 else top, tip[0], tip[2], 1.0, 1.0, 0.0, 1.4, CHROME, cut=0)
            for nm, sx in (("leg_left", 1), ("leg_right", -1)):
                m.bone(nm, top, (sx * 2.0, 16.0, 0))
        else:
            m.round_box(bd, 0, 0, 8.0, 5.0, 18.0, 34.0, chevf, cut=2)                         # broad shield-body
            hd = m.bone("head", bd, (0, 35, 0))
            m.round_box(hd, 0, 0, 4.4, 4.4, 33.0, 42.0, CHROME, cut=1)                         # chrome skull head
            m.round_box(hd, 0, 2.6, 3.0, 4.4, 40.0, 46.0, CHROME, cut=1)
            for sx in (-1, 1):
                m.box(hd, min(sx * 1.0, sx * 3.0), 38.0, -4.6, max(sx * 1.0, sx * 3.0), 39.4, -4.2, solid(P, "black"))
            for j in range(5):                                                                 # mouth grille
                m.box(hd, -2.0 + j * 0.9, 34.0, -4.6, -1.6 + j * 0.9, 36.4, -4.2, solid(P, "black"))
            for i, key in enumerate(("red", "blue", "green")):                                 # capsule tanks
                sx = -1 if i == 0 else 1
                cx = sx * (10.0 + (i == 2) * 2.0)
                cy = 38.0 - (i == 2) * 6.0
                m.round_box(bd, cx, 2.0, 2.2, 2.2, cy - 4.0, cy + 4.0, gem(P, key, key + "_light" if key + "_light"
                            in BASE else "white", glow=False), cut=1)
            m.box(bd, 8.0, 20.0, -5.0, 14.0, 30.0, -4.0, gem(P, "green", "green_light", glow=False))   # circuit board
            ar = m.bone("arm_right", bd, (-8, 30, 0))                                          # red cannon arm
            hose(m, ar, [(-8.0, 30.0, 0), (-14.0, 32.0, -1.0), (-18.0, 36.0, -2.0)], t=3)
            m.round_box(ar, -20.0, -2.0, 3.0, 3.0, 34.0, 44.0, armour(P, "red", "red"), cut=1)
            al = m.bone("arm_left", bd, (8, 26, 0))
            hose(m, al, [(8.0, 26.0, 0), (12.0, 20.0, -4.0), (12.0, 12.0, -8.0)], t=3)
            for j in range(4):                                                                 # teal lightning
                rod(m, al, (12.0 + (j % 2) * 2.0, 12.0 - j * 2.6, -8.0), (12.0 + ((j + 1) % 2) * 2.0,
                    9.4 - j * 2.6, -8.0), 1, solid(P, "teal", glow=True), extend=0.3)
            for j in range(12):                                                                # hose tentacles
                ang = 2 * math.pi * j / 12
                base = (5.0 * math.cos(ang), 18.0, 3.6 * math.sin(ang))
                tip = (10.0 * math.cos(ang), 1.0, 7.0 * math.sin(ang))
                hose(m, bd if j % 2 else top, [base, ((base[0] + tip[0]) / 2, 9.0, (base[2] + tip[2]) / 2), tip], t=3)
            for nm, sx in (("leg_left", 1), ("leg_right", -1)):
                m.bone(nm, top, (sx * 3.0, 18.0, 0))
        return m
    return build
