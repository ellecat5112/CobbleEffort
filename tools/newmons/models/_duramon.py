"""Shared builder for Duramon and Durandamon (CobbleEffort: Digital; hand-built after the official art on wikimon.net):
living holy swords. make(name, durandal=False):

- Duramon: a lean golden knight whose arms, crest and shoulders are all flared golden blades, a slit-visored helm,
  long blade-legs ending in golden talons, holding a huge golden broadsword, with a sweep of blue light round it.
- Durandamon: a slimmer black-and-gold sword knight with glowing rose eyes, a crown of curved blade horns, a long
  golden lance-sword taller than itself and a great ring of blue light circling it.
Shiny: silver.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

BASE = {"gold": (240, 200, 70), "gold_dark": (160, 110, 20), "gold_light": (255, 245, 180), "black": (34, 32, 40),
        "black_dark": (10, 10, 14), "black_light": (100, 96, 120), "steel": (220, 224, 236), "steel_dark": (110, 114, 128),
        "blue": (120, 220, 255, 170), "rose": (250, 120, 170), "eye": (80, 200, 255)}
SHINY = {"gold": (220, 224, 236), "gold_dark": (110, 114, 128), "gold_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light")
BLACK = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")


def blade(m, bone, base, d, length, w):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    tip = tuple(b + u_ * length for b, u_ in zip(base, u))
    rod(m, bone, base, tip, 1, GOLD, extend=0, t2=w)
    spike(m, bone, tip, u, 1.0, 2.0, GOLD)


def make(name, durandal=False):
    def build():
        m = Model(name)
        body = BLACK if durandal else GOLD
        mats = {"skin": body, "chest": GOLD, "abs": body, "pelvis": GOLD, "neck": body, "deltoid": GOLD,
                "upper_arm": body, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": body, "knee": GOLD,
                "shin": GOLD, "calf": body, "foot": GOLD, "toe": GOLD, "talon": GOLD}
        a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.9, talons=True, digitigrade=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, body, cut=1)
        eye = "rose" if durandal else "eye"
        m.box(hd, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, eye, glow=True))
        if durandal:                                                               # crown of curved blade horns
            for sx in (-1, 1):
                for j in range(2):
                    pts = [(sx * 1.6, 59.6, 0), (sx * (4.0 + j * 2.0), 64.0 + j * 2.0, 2.0),
                           (sx * (5.0 + j * 3.0), 68.0 + j * 2.0, 1.0)]
                    for p0, p1 in zip(pts, pts[1:]):
                        rod(m, hd, p0, p1, 1, GOLD, extend=0.4, t2=2)
        else:
            blade(m, hd, (0, 60.0, 0), (0, 1, 0.2), 9.0, 3)                         # blade crest
        for sx in (-1, 1):                                                         # flared shoulder blades
            blade(m, bd, (sx * 7.0, 51.0, 0), (sx, 0.8, 0.2), 12.0 if not durandal else 8.0, 3)
            blade(m, bd, (sx * 6.0, 48.0, 2.0), (sx, 0.3, 0.6), 9.0, 2)
        for nm in ("arm_left", "arm_right"):                                       # forearm blades
            el = a[nm]["elbow"]
            sx = 1 if el[0] > 0 else -1
            blade(m, a[nm]["bone"], el, (sx * 0.3, 0.4, 1), 8.0, 2)
        ar = a["arm_right"]                                                        # the great sword
        hx, hy, hz = ar["hand"]
        L = 40.0 if not durandal else 56.0
        rod(m, ar["bone"], (hx, hy - 6.0, hz), (hx, hy + L, hz), 1, GOLD, extend=0, t2=4 if not durandal else 3)
        m.box(ar["bone"], hx - 4.0, hy - 0.6, hz - 1.0, hx + 4.0, hy + 1.0, hz + 1.0, GOLD)
        spike(m, ar["bone"], (hx, hy + L, hz), (0, 1, 0), 3.0, 4.0, GOLD, tip=1.0)
        rb = m.bone("ring_light", bd, (0, 36, 0))                                  # sweep of blue light
        n = 20
        r = 20.0 if not durandal else 24.0
        span = 1.0 if durandal else 0.6
        for i in range(int(n * span)):
            a0 = 2 * math.pi * i / n
            a1 = 2 * math.pi * (i + 1) / n
            p0 = (r * math.cos(a0), 30.0 + 8.0 * math.sin(a0), r * math.sin(a0))
            p1 = (r * math.cos(a1), 30.0 + 8.0 * math.sin(a1), r * math.sin(a1))
            rod(m, rb, p0, p1, 1, solid(P, "blue", glow=True), extend=0.5, t2=2)
        return m
    return build
