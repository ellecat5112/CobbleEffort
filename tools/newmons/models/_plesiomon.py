"""Shared builder for Plesiomon and Plesiomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the great plesiosaur of the deep: a white body banded with blue-violet water marks, a long coiling
neck with a pale ridged throat, four long flippers, a dragon head with a spiky black mane and orange-red flame fins
along its spine and tail. X-Antibody: sleek and white, a blond mane, long whip-like blade fins sweeping from its head
and back, flippers dipped blue, a golden-banded belly. Shiny: pale gold with teal marks.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, lerp, slab_z
from _digidetail import fabric, skin, solid, strands
from _route import pal, tone

BASE = {"white": (240, 242, 246), "white_dark": (170, 176, 196), "blue": (90, 100, 200), "blue_dark": (50, 50, 130),
        "throat": (230, 220, 190), "black": (24, 24, 30), "flame": (240, 110, 40), "flame_tip": (250, 190, 60),
        "eye": (230, 50, 40), "mouth": (180, 60, 80), "tooth": (250, 250, 240), "blond": (220, 190, 120),
        "blond_dark": (150, 120, 60), "gold": (220, 190, 100)}
SHINY = {"white": (246, 232, 190), "white_dark": (190, 170, 120), "blue": (60, 170, 170), "blue_dark": (20, 110, 110)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, x=False):
    def bodyf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        w = math.sin(z * 0.45 + xx * 0.3) + math.sin(y * 0.6 - z * 0.2)
        if not x and face != "down" and w > 1.35:
            return tone(p["blue"] if w < 1.7 else p["blue_dark"], face), None
        if x and face == "down":
            return tone(p["gold"] if int(z) % 3 else p["throat"], face), None
        return skin(P, "white", dark="white_dark", var=0.03)(xx, y, z, face, variant, box=box, **k)

    def throatf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face in ("north", "down"):
            return tone(p["throat"] if int((y + z) * 1.2) % 2 else p["white_dark"], face), None
        return bodyf(xx, y, z, face, variant, box=box, **k)

    def flipf(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        if x and (abs(xx) > 13 or z > 18 or z < -14):
            return tone(p["blue"], face), None
        return bodyf(xx, y, z, face, variant, box=box, **k)

    def flamef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        return tone(p["flame_tip"] if (y % 3.0) > 1.8 else p["flame"], face), None

    BLADE = skin(P, "white", dark="blue", var=0.02)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 10, 0))
        for i in range(8):                                                             # body slices
            t = (i + 0.5) / 8
            r = 7.0 * math.sin(math.pi * (0.15 + 0.75 * t)) + 1.0
            slab_z(m, bd, 0, 11.0, -12.0 + i * 3.6, -12.0 + (i + 1) * 3.6 + 0.2, r * 1.1, r * 0.75, bodyf)
        fl = m.bone("flippers", bd, (0, 9, 0))
        for front, zz in ((True, -7.0), (False, 8.0)):
            for sx in (-1, 1):
                ln = 16.0 if x else 13.0
                tip = (sx * (7.0 + ln), 4.0, zz + (6.0 if front else 9.0))
                x0, x1 = sorted((sx * 6.0, tip[0]))
                m.box(fl, x0, 8.0, zz - 2.4, x1, 9.2, zz + 2.4, flipf,
                      rotation=(0, -sx * (25 if front else 35), sx * -18), pivot=(sx * 6.0, 9.0, zz))
        tl = m.bone("tail", bd, (0, 11, 16))
        pts = [(0, 11.0, 16.0), (0, 10.0, 22.0), (1.0, 9.0, 28.0), (2.0, 9.0, 33.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 5 - 2 * i if i < 2 else 1, bodyf, extend=0.6, t2=4 - i)
        nk = m.bone("neck", bd, (0, 14, -12))
        npts = [(0, 14.0, -12.0), (0, 22.0, -18.0), (0, 32.0, -18.0), (0, 40.0, -14.0), (0, 44.0, -18.0)]
        for i, (p0, p1) in enumerate(zip(npts, npts[1:])):
            rod(m, nk, p0, p1, 5 - (1 if i > 1 else 0), throatf, extend=0.8)
        hd = m.bone("head", nk, (0, 44, -18))
        m.round_box(hd, 0, -21.0, 2.6, 4.6, 42.6, 47.0, bodyf, cut=1)                   # skull
        m.round_box(hd, 0, -27.0, 1.8, 3.0, 42.6, 45.0, bodyf, cut=1)                   # snout
        m.box(hd, -1.6, 42.0, -29.6, 1.6, 42.8, -22.0, solid(P, "mouth"))
        jb = m.bone("jaw", hd, (0, 42, -18))
        m.round_box(jb, 0, -25.0, 1.6, 3.6, 40.6, 42.2, bodyf, cut=0)
        for j in range(5):
            for sx in (-1, 1):
                spike(m, hd, (sx * 1.4, 42.6, -28.4 + j * 1.4), (0, -1, 0), 0.8, 1.2, solid(P, "tooth"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 2.5, sx * 2.7), 45.0, -24.0, max(sx * 2.5, sx * 2.7), 46.0, -22.6,
                  solid(P, "eye", glow=True))
        if not x:
            for j in range(9):                                                           # spiky black mane
                ang = math.radians(-60 + j * 15)
                spike(m, hd, (0, 46.0, -17.0 + j * 0.6), (math.sin(ang) * 0.8, 1, 0.5 + 0.1 * j), 1.2,
                      5.0 + (j % 3) * 1.4, solid(P, "black"), tip=0.8)
            for j in range(7):                                                           # flame fins along the spine
                pz = -10.0 + j * 4.0
                spike(m, bd, (0, 18.0 - abs(j - 2) * 0.5, pz), (0, 1, 0.5), 1.4, 4.0 + (j % 2) * 1.6, flamef, tip=0.8)
            for p in npts[1:4]:
                spike(m, nk, (0, p[1], p[2] + 3.0), (0, 0.2, 1), 1.0, 3.0, flamef, tip=0.8)
        else:
            for j in range(5):                                                           # blond mane
                rod(m, hd, (0, 46.0, -16.0 + j * 0.8), (j - 2.0, 40.0 - j, -10.0 + j * 1.5), 1,
                    strands(P, "blond", "blond_dark"), extend=0.2, t2=2)
            for side in (-1, 1):                                                         # long whip blades
                for j, (o, L) in enumerate(((hd, 26.0), (bd, 30.0))):
                    root = (side * 1.4, 47.0, -18.0) if o is hd else (side * 2.0, 18.0, -2.0)
                    end = (root[0] + side * L * 0.5, root[1] + L * 0.45, root[2] + L * 0.6)
                    rod(m, o, root, end, 1, BLADE, extend=0.2, t2=2)
                    rod(m, o, end, (end[0] + side * 4.0, end[1] - 6.0, end[2] + 6.0), 1, BLADE, extend=0.2)
            spike(m, bd, (0, 18.0, 0.0), (0, 0.4, 1), 1.0, 9.0, BLADE, tip=0.8)
        return m

    return build
