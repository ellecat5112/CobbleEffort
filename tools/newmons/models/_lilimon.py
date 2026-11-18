"""Shared builder for Lilimon and Lilimon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the flower fairy: a small fairy in a pink petal dress (a tulip-bell skirt and a petal top), a pink flower
bud hat with a curling tendril, green hair, long green leaf sleeves with yellow flower cuffs, green leaf boots with
yellow flowers, and four big green leaf wings. X-Antibody: a fuller ruffled pink-and-yellow petal skirt with long
trailing petals, longer green hair and a yellow lily held in one hand. Built as officially drawn, fully clothed.
Shiny: violet petals.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibody import humanoid
from _digidetail import cutout, fabric, local, skin, solid, strands
from _route import pal, tone

BASE = {"pink": (246, 170, 200), "pink_dark": (210, 100, 150), "green": (80, 170, 70), "green_dark": (30, 100, 30),
        "leaf": (90, 170, 80, 230), "leaf_dark": (40, 110, 40, 240), "yellow": (250, 220, 70), "yellow_dark": (200, 160, 20),
        "skin": (250, 226, 212), "skin_dark": (210, 170, 150), "eye": (40, 40, 60)}
SHINY = {"pink": (190, 160, 250), "pink_dark": (130, 100, 210)}


def P(v):
    return pal(BASE, SHINY, v)


def leaf_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6) - 0.5
    return abs(b) < 0.5 * math.sin(math.pi * min(1.0, a)) + 0.02


def leaff(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["leaf_dark"] if abs(v - H / 2) < 0.3 else p["leaf"]), None


def make(name, x=False):
    PETAL = fabric(P, "pink", "pink_dark", period=1.6)
    GREEN = fabric(P, "green", "green_dark")
    SK = skin(P, "skin", dark="skin_dark")

    def build():
        m = Model(name)
        mats = {"skin": SK, "chest": PETAL, "abs": PETAL, "pelvis": PETAL, "neck": SK, "deltoid": GREEN,
                "upper_arm": GREEN, "forearm": GREEN, "hand": SK, "finger": SK, "thigh": SK, "knee": GREEN,
                "shin": GREEN, "calf": GREEN, "foot": GREEN, "toe": GREEN}
        a = humanoid(m, mats, bulk=0.72, arm_bulk=0.72, leg_bulk=0.8, name=name)
        bd = a["body"]
        n = 8 if not x else 12                                                     # petal skirt
        for i in range(n):
            ang = 2 * math.pi * i / n
            spike(m, bd, (3.6 * math.cos(ang), 36.0, 3.0 * math.sin(ang)), (math.cos(ang) * 0.6, -1, math.sin(ang) * 0.6),
                  3.0, 9.0 if not x else 14.0, PETAL if (i % 3 or not x) else fabric(P, "yellow", "yellow_dark"), tip=0.8)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SK, cut=1)
        m.box(hd, -1.4, 57.4, -2.9, -0.4, 58.2, -2.8, solid(P, "eye"))
        m.box(hd, 0.4, 57.4, -2.9, 1.4, 58.2, -2.8, solid(P, "eye"))
        for i in range(9 if not x else 13):                                        # green hair
            ang = math.radians(-100 + i * (25 if not x else 17))
            rod(m, hd, (2.2 * math.sin(ang), 59.0, 0.8 + 1.2 * math.cos(ang)), (3.0 * math.sin(ang), 50.0 if not x else 40.0, 3.0),
                1, strands(P, "green", "green_dark"), extend=0.3, t2=2)
        for i in range(5):                                                         # bud hat
            ang = math.radians(i * 72)
            spike(m, hd, (1.6 * math.cos(ang), 59.6, 1.6 * math.sin(ang)), (math.cos(ang) * 0.3, 1, math.sin(ang) * 0.3), 1.8,
                  5.0, PETAL, tip=0.8)
        pts = [(0, 64.0, 0), (1.0, 67.0, 0), (2.4, 66.6, 0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "yellow"), extend=0.1, t2=1)
        for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):              # yellow flower cuffs
            anc = a[nm]
            j = anc.get("wrist") or anc.get("ankle")
            m.round_box(anc["bone"], j[0], j[2], 1.8, 1.8, j[1] - 0.4, j[1] + 1.0, solid(P, "yellow"), cut=1)
        L = cutout(leaf_in, leaff)
        for side in (1, -1):                                                       # four leaf wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.0, 48.0, 3.6))
            for j, rz in enumerate((30, -25)):
                x0, x1 = sorted((side * 2.0, side * 18.0))
                m.box(wb, x0, 45.0, 3.8 + j * 0.3, x1, 51.0, 3.8 + j * 0.3, L, rotation=(0, side * -15, side * rz),
                      pivot=(side * 2.0, 48.0, 3.8))
        if x:                                                                      # yellow lily in hand
            hx, hy, hz = a["arm_left"]["hand"]
            for j in range(5):
                spike(m, a["arm_left"]["bone"], (hx, hy + 1.0, hz), (math.cos(j * 1.26) * 0.6, 1, math.sin(j * 1.26) * 0.6),
                      1.2, 4.0, solid(P, "yellow"), tip=0.8)
        return m

    return build
