"""Shared builder for Minervamon and Minervamon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): the youngest of the Olympos Twelve, a small fierce warrior girl in a golden owl helm with white wings,
long teal hair in two braids, a cream tunic over red-and-gold armour, red boots, a round golden shield on her left arm,
and the great sword Olympia, longer than she is tall, its red blade marked with a white double helix. The X-Antibody
("x"): gold and silver armour, a feathered crest, and two great blue spiked orbs swinging on beaded chains from
her shoulders, a ring of blue water swirling round the sword.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, local, metal, skin, solid, strands
from _route import pal, tone

BASE = {"skin": (244, 214, 194), "skin_dark": (196, 156, 134), "gold": (230, 190, 80), "gold_dark": (150, 110, 30),
        "red": (190, 40, 50), "red_dark": (100, 14, 20), "cream": (240, 228, 200), "cream_dark": (190, 176, 146),
        "hair": (90, 170, 170), "hair_dark": (40, 100, 100), "white": (246, 246, 250), "white_dark": (190, 190, 200),
        "steel": (210, 214, 226), "steel_dark": (110, 114, 126), "eye": (60, 150, 90), "orb": (40, 80, 160),
        "orb_dark": (14, 30, 90), "water": (110, 170, 255, 170)}
SHINY = {"gold": (200, 206, 220), "gold_dark": (120, 126, 140), "red": (60, 90, 190), "red_dark": (20, 40, 110),
         "hair": (240, 150, 190), "hair_dark": (180, 80, 120)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark")
GOLD = armour(P, "gold", "gold_dark", trim="red", trim_w=0.25)
TUNIC = fabric(P, "cream", "cream_dark")
RED = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
HAIR = strands(P, "hair", "hair_dark")


def bladef(x, y, z, face, variant, box=None, **k):
    """Olympia: red blade, steel edges, a white double helix down the middle."""
    p = P(variant)
    if box is None or face in ("up", "down"):
        return tone(p["steel"], face), None
    u, v, W, H = local(x, y, z, face, box)
    across, along = (u / max(W, 1e-6), v) if H >= W else (v / max(H, 1e-6), u)
    if across < 0.14 or across > 0.86:
        return tone(p["steel"], face), None
    s = 0.5 + 0.22 * math.sin(along * 0.9)
    if abs(across - s) < 0.06 or abs(across - (1 - s)) < 0.06:
        return tone(p["white"], face), None
    return tone(p["red"], face), None


def make(name, x=False):
    def build():
        m = Model(name)
        mats = {"skin": SKIN, "chest": GOLD, "abs": TUNIC, "pelvis": TUNIC, "neck": SKIN, "deltoid": GOLD,
                "upper_arm": TUNIC, "forearm": RED, "hand": SKIN, "finger": SKIN, "thigh": TUNIC, "knee": RED,
                "shin": RED, "calf": RED, "foot": RED, "toe": RED}
        a = humanoid(m, mats, bulk=0.8, arm_bulk=0.8, leg_bulk=0.85, name=name)
        bd = a["body"]
        for j in range(3):                                                             # cream tunic skirt
            r = 4.6 + j * 0.8
            m.round_box(bd, 0, 0.4, r, r * 0.8, 31.0 - (j + 1) * 3.6, 31.4 - j * 3.6, TUNIC, cut=1)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.4, SKIN, cut=1)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.6, sx * 1.6), 56.6, -2.9, max(sx * 0.6, sx * 1.6), 57.4, -2.8, solid(P, "eye"))
        m.round_box(hd, 0, -0.4, 3.0, 3.2, 57.6, 61.4, GOLD, cut=1)                    # golden owl helm
        m.round_box(hd, 0, -3.8, 1.6, 0.8, 58.6, 60.8, GOLD, cut=0)
        for sx in (-1, 1):                                                              # helm wings
            x0, x1 = sorted((sx * 2.6, sx * 7.0))
            m.box(hd, x0, 59.0, 0.0, x1, 63.0, 0.0, feathers(P, "white", "white_dark"),
                  rotation=(0, sx * 30, sx * 20), pivot=(sx * 2.6, 60.0, 0.0))
            pts = [(sx * 2.6, 57.0, 1.4), (sx * 4.0, 50.0, 3.0), (sx * 5.0, 42.0, 4.0), (sx * 5.4, 36.0, 4.0)]
            for p0, p1 in zip(pts, pts[1:]):                                            # two long braids
                rod(m, hd, p0, p1, 2, HAIR, extend=0.4)
        if x:
            for i in range(5):                                                          # feathered crest
                spike(m, hd, ((i - 2) * 0.7, 61.0, -1.0), ((i - 2) * 0.3, 1, 0.4), 1.0, 5.0, GOLD, tip=0.8)
        al = a["arm_left"]                                                             # round golden shield
        w = al["wrist"]
        for i in range(10):
            ang = 2 * math.pi * i / 10
            m.box(al["bone"], w[0] + 1.0 + 4.0 * math.cos(ang) - 1.2, w[1] + 2.0 + 4.0 * math.sin(ang) - 1.2,
                  w[2] - 3.4, w[0] + 1.0 + 4.0 * math.cos(ang) + 1.2, w[1] + 2.0 + 4.0 * math.sin(ang) + 1.2, w[2] - 2.2,
                  GOLD)
        ball(m, al["bone"], (w[0] + 1.0, w[1] + 2.0, w[2] - 3.2), 3.0, metal(P, "steel", dark="steel_dark"),
             layers=3, squash=0.4)
        ar = a["arm_right"]                                                            # the great sword Olympia
        h = ar["hand"]
        bx, bz = h[0] - 2.0, h[2] - 3.0
        m.box(ar["bone"], bx - 4.0, h[1] - 1.0, bz - 1.0, bx + 4.0, h[1] + 0.6, bz + 1.0, GOLD)
        rod(m, ar["bone"], (bx, h[1] + 0.6, bz), (bx, h[1] + 5.0, bz), 1, solid(P, "red_dark"), extend=0.2)
        for j in range(6):
            wdt = 3.6 - max(0, j - 4) * 1.4
            m.box(ar["bone"], bx - wdt, h[1] - 1.0 - (j + 1) * 7.0, bz - 0.6, bx + wdt, h[1] - 1.0 - j * 7.0, bz + 0.6,
                  bladef, rotation=(-35, 0, 0), pivot=(bx, h[1] - 1.0, bz))
        if x:
            for sx in (-1, 1):                                                          # blue spiked orbs on chains
                cb = m.bone("orb_left" if sx > 0 else "orb_right", bd, (sx * 6.0, 52.0, 2.0))
                pts = [(sx * 6.0, 52.0, 2.0), (sx * 9.0, 60.0, 3.0), (sx * 11.0, 68.0, 3.0)]
                for p0, p1 in zip(pts, pts[1:]):
                    for t in range(4):
                        q = tuple(p0[i] + (p1[i] - p0[i]) * (t + 0.5) / 4 for i in range(3))
                        ball(m, cb, q, 0.9, solid(P, "orb"), layers=1)
                c = pts[-1]
                ball(m, cb, (c[0], c[1] + 4.0, c[2]), 4.4, armour(P, "orb", "orb_dark"), layers=4)
                for j in range(6):
                    ang = j * math.pi / 3
                    spike(m, cb, (c[0], c[1] + 4.0, c[2]), (math.cos(ang), math.sin(ang), 0.2), 1.4, 6.6,
                          metal(P, "steel"), tip=0.8)
            for i in range(10):                                                         # swirling water ring
                ang = 2 * math.pi * i / 10
                m.box(bd, 9.0 * math.cos(ang) - 1.6, 6.0 + i * 0.6, 9.0 * math.sin(ang) - 0.4, 9.0 * math.cos(ang) + 1.6,
                      7.0 + i * 0.6, 9.0 * math.sin(ang) + 0.4, solid(P, "water"), rotation=(0, -math.degrees(ang) + 90, 0),
                      pivot=(9.0 * math.cos(ang), 6.5 + i * 0.6, 9.0 * math.sin(ang)))
        return m

    return build
