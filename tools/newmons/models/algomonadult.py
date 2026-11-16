"""Algomon (Adult) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a great glossy violet sphere crowned with three yellow-and-red tipped horns. Three small
red-eyed slits sit on green vein lines across its face over a zipped mouth leaking steam; stubby violet arms carry
mechanical gauntlets, a steel claw-drum on the left and a lamp-cup on the right, and a skirt of dozens of green
tentacles with steel caps hangs beneath it. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _algo import GREEN, P, STEEL, VIOLET, hornf, tentaclef
from _digidetail import eye, plane, solid
from _route import tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 2.2)
KIND = "floater"
K = 3
LOOK = ("a great glossy violet sphere with three yellow-and-red tipped horns, small eyes on green vein lines, a zipped "
        "mouth, steel claw and lamp gauntlets and a skirt of green tentacles with steel caps")
TENT = tentaclef()
EYES = [(-5.0, 33.0), (4.6, 31.0), (0.4, 26.6)]


def spheref(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        for ex, ey in EYES:
            du, dv = a - ex, b - ey
            if abs(du) < 1.8 and abs(dv) < 0.9 - 0.35 * abs(du):
                return (p["eye_r"] if math.hypot(du, dv) < 0.45 else p["eye_y"]), None
            if abs(du) < 2.2 and abs(dv) < 1.25 - 0.4 * abs(du):
                return tone(p["green"], face), None
        # green vein lines joining the eyes and running down to the zip
        for (x0, y0), (x1, y1) in ((EYES[0], EYES[2]), (EYES[1], EYES[2]), (EYES[2], (0.0, 19.0))):
            t = max(0, min(1, ((a - x0) * (x1 - x0) + (b - y0) * (y1 - y0)) / ((x1 - x0) ** 2 + (y1 - y0) ** 2)))
            if math.hypot(a - (x0 + t * (x1 - x0)), b - (y0 + t * (y1 - y0))) < 0.35:
                return tone(p["green"], face), None
        if abs(a + 0.25 * (b - 22)) < 0.9 and 16.0 < b < 25.0:     # the zipper
            return tone(p["steel"] if (b * 2.2) % 1 < 0.5 else p["steel_dark"], face), None
    return VIOLET(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("algomonadult")
    top = m.bone("algomonadult", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 26, 0))
    ball(m, bd, (0, 28.0, 0), 12.5, spheref, layers=9)
    for ang in (-34, 0, 34):                                     # the three horns
        r = math.radians(ang)
        base = (9.0 * math.sin(r), 38.0 - abs(ang) * 0.05, 1.0)
        rod(m, bd, base, (base[0] + 3.5 * math.sin(r), 48.0 - abs(ang) * 0.06, 2.0), 4, hornf, extend=0.4)
    for sx in (-1, 1):                                           # steam puffs from the zip
        m.box(bd, sx * 1.5 - 1.2, 18.0, -14.6, sx * 1.5 + 1.2, 20.0, -13.0, solid(P, "white"))
    sk = m.bone("skirt", bd, (0, 17, 0))
    for ring, (r0, y0, n) in enumerate(((10.0, 19.0, 16), (7.0, 17.0, 12))):
        for i in range(n):
            ang = math.radians(i * 360 / n + ring * 11)
            pts = [(r0 * math.sin(ang), y0, -r0 * math.cos(ang)),
                   ((r0 + 2.5) * math.sin(ang), y0 - 7, -(r0 + 2.5) * math.cos(ang)),
                   ((r0 + 3.5) * math.sin(ang + 0.1), y0 - 13, -(r0 + 3.5) * math.cos(ang + 0.1))]
            for a, b in zip(pts, pts[1:]):
                rod(m, sk, a, b, 2, TENT, extend=0.4)
            e = pts[-1]
            m.box(sk, e[0] - 1.0, e[1] - 2.0, e[2] - 1.0, e[0] + 1.0, e[1] - 0.2, e[2] + 1.0, STEEL)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 11.0, 27.0, 0))
        rod(m, ab, (sx * 11.0, 27.0, 0), (sx * 15.5, 30.0, -1.0), 4, VIOLET, extend=0.5)
        gx = sx * 18.5
        m.round_box(ab, gx, -1.0, 3.2, 3.2, 28.0, 34.5, STEEL, cut=1)     # gauntlet drum
        for j in range(3):
            m.box(ab, gx - 3.4, 28.6 + j * 2.0, -4.4, gx + 3.4, 29.2 + j * 2.0, 2.4, solid(P, "steel_dark"))
        if sx > 0:                                               # claw drum: three jointed steel fingers, yellow tips
            for j in range(3):
                ang = math.radians(-30 + j * 30)
                p0 = (gx + sx * 2.0 * math.cos(ang), 34.5, -1.0 + 2.0 * math.sin(ang))
                p1 = (p0[0] + sx * 2.5, 38.5, p0[2])
                rod(m, ab, p0, p1, 1, STEEL, extend=0.3)
                m.box(ab, p1[0] - 0.8, p1[1], p1[2] - 0.8, p1[0] + 0.8, p1[1] + 1.6, p1[2] + 0.8, solid(P, "horn_y"))
        else:                                                     # lamp cup: three glowing bulbs
            for j in range(3):
                ang = math.radians(j * 120)
                c = (gx + 2.0 * math.cos(ang), 36.0, -1.0 + 2.0 * math.sin(ang))
                ball(m, ab, c, 1.4, solid(P, "lamp", glow=True), layers=2)
    return m
