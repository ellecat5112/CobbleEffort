"""Metallicdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a sleek sky dragon of polished silver alloy: a slender armoured body with cyan-lit seams,
a long narrow head with a blade crest, thin clawed limbs, a long segmented tail ending in a rail-gun barrel, and two
vast wings of translucent blue-violet crystal panes on silver frames. 35 blocks tall.

Front is -z, y is up. 60 units tall (the wings); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = ("a sleek silver sky dragon with cyan-lit seams, a blade crest, thin clawed limbs, a rail-gun tail and vast "
        "wings of translucent blue-violet crystal panes")
BASE = {"silver": (210, 216, 230), "silver_dark": (110, 116, 136), "silver_light": (250, 252, 255),
        "cyan": (90, 230, 250), "pane": (160, 170, 250, 140), "pane_light": (230, 220, 255, 170), "eye": (90, 230, 250)}
SHINY = {"silver": (60, 60, 70), "silver_dark": (24, 24, 30), "silver_light": (130, 130, 150),
         "pane": (250, 160, 90, 140), "pane_light": (255, 230, 180, 170), "cyan": (250, 140, 60)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "silver", "silver_dark", light="silver_light", trim="silver_dark", trim_w=0.2)
STEEL = metal(P, "silver", dark="silver_dark", light="silver_light")


def armf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(((y + z * 0.4) % 3.0) - 1.5) < 0.12:
        return p["cyan"], p["cyan"]
    return ARM0(x, y, z, face, variant, box=box, **k)


def panef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if u < 0.4 or v < 0.4 or u > W - 0.4 or v > H - 0.4:
        return tone(p["silver"], face), None
    c = p["pane_light"] if (u / max(W, 1e-6) + v / max(H, 1e-6)) > 1.3 else p["pane"]
    return c, None


def build():
    m = Model("metallicdramon")
    top = m.bone("metallicdramon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 30, 0))
    pts = [(0, 40.0, -6.0), (0, 34.0, -2.0), (0, 28.0, 0.0), (0, 23.0, 2.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # slender armoured body
        rod(m, bd, p0, p1, 5 - j, armf, extend=0.8)
    nk = m.bone("neck", bd, (0, 40, -6))
    rod(m, nk, (0, 40.0, -6.0), (0, 46.0, -10.0), 3, armf, extend=0.6)
    hd = m.bone("head", nk, (0, 46, -10))
    m.round_box(hd, 0, -14.0, 1.8, 4.0, 45.4, 48.0, armf, cut=1)                           # long narrow head
    m.round_box(hd, 0, -11.4, 2.4, 2.4, 46.0, 49.0, armf, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 2.6), 47.6, -12.6, max(sx * 2.4, sx * 2.6), 48.2, -11.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 49.0, -10.0), (0, 0.5, 1), 1.4, 8.0, STEEL, tip=0.8)                    # blade crest
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                                    # thin clawed arms
        ab = m.bone(nm, bd, (sx * 3.0, 37.0, -4.0))
        rod(m, ab, (sx * 3.0, 37.0, -4.0), (sx * 5.0, 31.0, -8.0), 2, STEEL, extend=0.3)
        for f in range(3):
            spike(m, ab, (sx * 5.0 + (f - 1) * 0.6, 31.0, -8.0), (0, -1, -0.4), 0.8, 3.0, solid(P, "cyan"), tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, bd, (sx * 2.6, 24.0, 2.0))
        rod(m, lg, (sx * 2.6, 24.0, 2.0), (sx * 4.0, 18.0, -2.0), 2, STEEL, extend=0.3)
        rod(m, lg, (sx * 4.0, 18.0, -2.0), (sx * 3.6, 13.0, 0.0), 2, STEEL, extend=0.3)
        for f in range(3):
            spike(m, lg, (sx * 3.6 + (f - 1) * 0.7, 13.0, 0.0), (0, -1, -0.6), 0.8, 3.0, solid(P, "cyan"), tip=0.8)
    tb = m.bone("tail", bd, (0, 23, 2))                                                    # segmented tail
    tp = [(0, 23.0, 2.0), (-2.0, 16.0, 6.0), (-4.0, 9.0, 6.0), (-8.0, 4.0, 2.0)]
    for j, (p0, p1) in enumerate(zip(tp, tp[1:])):
        rod(m, tb, p0, p1, 3 - j // 2, armf, extend=0.4)
    rod(m, tb, tp[-1], (-16.0, 2.0, 0.0), 2, STEEL, extend=0.4)                             # rail-gun barrel
    for side in (1, -1):                                                                   # crystal-pane wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 38.0, 2.0))
        root = (side * 3.0, 38.0, 2.0)
        for j in range(5):                                                                 # fan of panes
            ang = 30 - j * 16
            ln = 30.0 - j * 3.0
            a_ = math.radians(ang)
            tip = (root[0] + side * ln * math.cos(a_), root[1] + ln * math.sin(a_), root[2] + 2.0 + j * 0.8)
            rod(m, wb, root, tip, 1, STEEL, extend=0.3)
            x0, x1 = sorted((root[0], root[0] + side * ln))
            m.box(wb, x0, root[1] - 5.0, root[2] + 2.4 + j * 0.8, x1, root[1], root[2] + 2.4 + j * 0.8, panef,
                  rotation=(0, 0, side * ang), pivot=(root[0], root[1], root[2] + 2.4 + j * 0.8))
    return m
