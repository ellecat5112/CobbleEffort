"""Shared builder for Toy Agumon and Toy Agumon (Black) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): Agumon built from toy bricks: studded blocks stacked into a dinosaur (a red-and-yellow head with a
round green eye, a green-and-blue body, red and green legs), grey brick hands with studded fingers, and a puff of
flame. Black: built from translucent grey bricks. Shiny: the bricks in other toy colours."""
from __future__ import annotations

import math

from _boxmodel import Model, spike
from _digibeast import ball
from _digidetail import gem, solid
from _route import pal, tone

COLOURS = {False: {"head": (220, 50, 40), "jaw": (250, 220, 50), "body": (60, 170, 70), "belly": (60, 90, 200),
                   "arm": (250, 220, 50), "leg_l": (220, 50, 40), "leg_r": (60, 170, 70), "hand": (180, 184, 196)},
           True: {k: c for k, c in (("head", (150, 150, 160)), ("jaw", (170, 170, 180)), ("body", (130, 130, 140)),
                                     ("belly", (150, 150, 162)), ("arm", (170, 170, 180)), ("leg_l", (140, 140, 150)),
                                     ("leg_r", (160, 160, 170)), ("hand", (180, 184, 196)))}}
SHINY = {"head": (60, 90, 200), "jaw": (250, 250, 250), "body": (240, 140, 40), "belly": (220, 50, 40),
         "arm": (250, 250, 250), "leg_l": (60, 90, 200), "leg_r": (240, 140, 40)}
COMMON = {"eye": (70, 190, 80), "eye_light": (200, 255, 200), "flame": (250, 120, 40, 220), "black": (20, 20, 20)}


def make(name, black=False):
    base = dict(COMMON, **COLOURS[black])
    shiny = dict(base, **SHINY)

    def P(v):
        return pal(base, shiny, v)

    def brickf(key):
        def f(x, y, z, face, variant, box=None, **k):
            p = P(variant)
            c = p[key]
            if box is not None and face != "up":
                if y < box.lo[1] + 0.4 or (face in ("north", "south") and (x - box.lo[0]) < 0.3):
                    c = tuple(int(v * 0.72) for v in c)
            return tone(c, face), None
        return f

    def brick(m, bone, x0, y0, z0, x1, y1, z1, key, studs=True):
        m.box(bone, x0, y0, z0, x1, y1, z1, brickf(key))
        if studs:
            nx = max(1, int((x1 - x0) / 2.4))
            nz = max(1, int((z1 - z0) / 2.4))
            for i in range(nx):
                for j in range(nz):
                    cx = x0 + (i + 0.5) * (x1 - x0) / nx
                    cz = z0 + (j + 0.5) * (z1 - z0) / nz
                    m.round_box(bone, cx, cz, 0.7, 0.7, y1, y1 + 0.8, brickf(key), cut=0)

    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        for sx, nm, key in ((1, "leg_left", "leg_l"), (-1, "leg_right", "leg_r")):
            lg = m.bone(nm, top, (sx * 2.6, 6.0, 0))
            brick(m, lg, sx * 2.6 - 2.2, 0.0, -4.0, sx * 2.6 + 2.2, 3.0, 2.0, key)
            brick(m, lg, sx * 2.6 - 1.8, 3.0, -1.6, sx * 2.6 + 1.8, 7.0, 1.6, key, studs=False)
        bd = m.bone("body", top, (0, 7, 0))
        brick(m, bd, -4.4, 7.0, -3.0, 4.4, 11.0, 3.0, "belly")
        brick(m, bd, -4.8, 11.0, -3.4, 4.8, 15.0, 3.4, "body")
        brick(m, bd, -2.0, 7.0, 3.0, 2.0, 10.0, 9.0, "body")                           # tail brick
        hd = m.bone("head", bd, (0, 15, 0))
        brick(m, hd, -4.2, 15.0, -7.0, 4.2, 18.6, 3.0, "jaw")
        brick(m, hd, -4.2, 18.6, -6.0, 4.2, 22.0, 3.0, "head")
        for sx in (-1, 1):
            ball(m, hd, (sx * 4.3, 20.4, -2.6), 1.3, gem(P, "eye", "eye_light", glow=False), layers=1)
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 4.8, 13.0, 0))
            brick(m, ab, sx * 5.4 - 1.4, 11.0, -2.0, sx * 5.4 + 1.4, 14.0, 1.0, "arm", studs=False)
            brick(m, ab, sx * 6.6 - 2.0, 9.0, -3.6, sx * 6.6 + 2.0, 11.6, -1.0, "hand")
            for f in range(3):
                m.round_box(ab, sx * 6.6 + (f - 1) * 1.2, -4.6, 0.5, 1.2, 9.4, 11.0, brickf("hand"), cut=0)
        fl = m.bone("flame", bd, (-7.0, 10.0, -6.0))
        for j in range(3):
            spike(m, fl, (-7.0, 8.0 + j, -7.0), (-0.4 + j * 0.2, 0.6, -1), 1.6, 4.0, solid(P, "flame", glow=True), tip=0.8)
        return m
    return build
