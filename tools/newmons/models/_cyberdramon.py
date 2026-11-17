"""Shared builder for Cyberdramon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a lean
dark-grey cyborg dragon-man in ribbed armour with a horned helmet visor, bare muscled grey arms bound with straps,
huge clawed hands, taloned feet with steel claws and tattered dark crimson wings. make(x=True): the X-Antibody form,
a sleek glossy black armoured dragon traced with glowing orange lines, a long-horned head, long clawed hands and
blade-like hexagon-patterned crimson-and-orange wings. Shiny: dark blue (base) / white (X).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import Bulge, armour, cutout, local, metal, skin, solid, torso_bulges
from _route import pal, tone

BASE = {"grey": (80, 82, 92), "grey_dark": (34, 34, 40), "grey_light": (150, 152, 166), "black": (24, 24, 30),
        "black_light": (90, 90, 104), "crimson": (120, 20, 40), "crimson_dark": (60, 6, 16), "orange": (250, 140, 40),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 128), "bone": (220, 210, 190), "eye": (250, 60, 60),
        "hex": (240, 110, 40, 200)}
SHINY = {"grey": (50, 70, 130), "grey_dark": (20, 30, 70), "grey_light": (110, 140, 210), "crimson": (60, 60, 70),
         "black": (230, 230, 240), "black_light": (255, 255, 255), "orange": (60, 160, 250)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def hexf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    edge = abs(((u * 0.8 + v * 0.46) % 2.0) - 1.0) < 0.12 or abs(((u * 0.8 - v * 0.46) % 2.0) - 1.0) < 0.12
    c = p["orange"] if edge else p["hex"]
    return (c[:3] + (255,) if edge else c), (c[:3] if edge else None)


def blade_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return b < 1 - a * 0.6 and b > a * 0.25


def make(name, x=False):
    if x:
        BODY = armour(P, "black", "black", light="black_light", trim="orange", trim_w=0.2, glow_key="orange")
    else:
        BODY = armour(P, "grey", "grey_dark", light="grey_light", seams=(36.0, 40.0, 44.0, 48.0))
    ARM = BODY if x else skin(P, "grey", dark="grey_dark", light="grey_light", var=0.03,
                              bulges=[Bulge("north", sx * 9.6, 42.0, 2.0, 3.8, light=0.3, shadow=0.45)
                                      for sx in (-1, 1)])

    def build():
        m = Model(name)
        mats = {"skin": BODY, "chest": BODY, "abs": BODY, "pelvis": BODY, "deltoid": BODY, "upper_arm": ARM,
                "forearm": ARM, "hand": BODY, "finger": STEEL, "claw": STEEL, "thigh": BODY, "knee": BODY,
                "shin": BODY, "calf": BODY, "foot": BODY, "talon": STEEL}
        a = humanoid(m, mats, bulk=1.1 if not x else 0.9, arm_bulk=1.3 if not x else 0.9, leg_bulk=1.1,
                     digitigrade=True, claws=True, talons=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.2, 54.2, 61.0, BODY, cut=1)
        m.box(hd, -1.6, 54.6, -6.0, 1.6, 57.0, -3.2, BODY)
        m.box(hd, -2.0, 57.6, -3.6, 2.0, 58.2, -3.2, solid(P, "eye" if not x else "orange", glow=True))
        for sx in (-1, 1):                                                       # horns
            spike(m, hd, (sx * 1.6, 60.6, -1.0), (sx * 0.3, 1, 0.4), 1.6, 8.0 if x else 5.0,
                  solid(P, "bone") if not x else BODY, tip=0.3)
        for nm in ("arm_left", "arm_right"):                                     # huge clawed hands
            h = a[nm]["hand"]
            for f in range(3):
                spike(m, a[nm]["bone"], (h[0] + (f - 1) * 1.2, h[1] - 3.0, h[2] - 1.0), (0, -1, -0.4), 1.2,
                      8.0 if x else 5.0, STEEL, tip=0.3)
            if not x:
                for j in range(3):                                               # arm straps
                    y = a[nm]["elbow"][1] + 2.0 + j * 2.4
                    m.round_box(a[nm]["bone"], a[nm]["elbow"][0], 0.0, 2.2, 2.2, y - 0.4, y + 0.4,
                                solid(P, "black"), cut=1)
        wb = m.bone("wings", bd, (0, 48, 4))
        for sx in (-1, 1):
            if x:                                                                # hexagon blade-wings
                for j, (ang, ln) in enumerate(((30, 28.0), (0, 24.0))):
                    x0, x1 = sorted((sx * 3.0, sx * ln))
                    m.box(wb, x0, 40.0, 5.0 + j, x1, 60.0, 5.0 + j, cutout(blade_in, hexf),
                          rotation=(0, sx * 15, sx * ang), pivot=(sx * 3.0, 50.0, 5.0 + j))
            else:                                                                # tattered crimson wings
                bat_wing(m, wb, (sx * 3.0, 50.0, 4.0), 20.0, 18.0, 4, solid(P, "crimson_dark"),
                         solid(P, "crimson"), side=sx, sweep=20)
        tl = m.bone("tail", bd, (0, 31, 3))
        pts = [(0, 31.0, 3.0), (2.0, 25.0, 8.0), (4.0, 18.0, 11.0), (6.0, 12.0, 12.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, max(1, 3 - j), BODY, extend=0.4)
        return m
    return build
