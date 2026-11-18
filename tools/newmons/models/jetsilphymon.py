"""Jet Silphymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Silphymon boosted with jet power: a slender warrior in white armour with a white feathered
helm with pointed ears, short blue hair and a red visor, lilac trim, white flight wings folded at her back, white boots
with lilac soles, and a long pole ending in a giant blue-and-white pinwheel. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, cutout, feathers, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender warrior in white armour with a feathered helm, short blue hair, a red visor, white folded wings and "
        "a long pole with a giant blue-and-white pinwheel")
BASE = {"white": (244, 244, 250), "white_dark": (170, 172, 196), "lilac": (190, 160, 230), "blue": (60, 100, 210),
        "blue_dark": (20, 40, 130), "red": (220, 40, 50), "skin": (240, 214, 196), "skin_dark": (190, 160, 140),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "gold": (240, 200, 70)}
SHINY = {"white": (60, 60, 76), "white_dark": (20, 20, 30), "blue": (220, 90, 140), "blue_dark": (140, 30, 80)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="lilac", trim_w=0.25)


def pinf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["blue"] if u / max(W, 1e-6) > 0.5 else p["white"], face), None


def pin_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6), v / max(H, 1e-6)
    return a < 1.0 - b * 0.6


def build():
    m = Model("jetsilphymon")
    mats = {"skin": WHITE, "chest": WHITE, "abs": WHITE, "pelvis": WHITE, "neck": WHITE, "deltoid": WHITE,
            "upper_arm": WHITE, "forearm": WHITE, "hand": WHITE, "finger": WHITE, "thigh": WHITE, "knee": WHITE,
            "shin": WHITE, "calf": WHITE, "foot": solid(P, "lilac"), "toe": solid(P, "lilac")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.82, leg_bulk=0.86, name="jetsilphymon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 59.6, skin(P, "skin", dark="skin_dark"), cut=1)
    m.round_box(hd, 0, -2.8, 2.2, 0.4, 56.6, 57.8, solid(P, "red", glow=True), cut=0)
    m.round_box(hd, 0, 0.4, 2.8, 2.8, 58.0, 61.6, WHITE, cut=1)                              # feathered helm
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.4, 60.6, 0.4), (sx * 0.4, 1, 0.4), 1.4, 5.0, WHITE, tip=0.8)    # pointed ears
        for j in range(3):
            rod(m, hd, (sx * (1.0 + j * 0.6), 58.6, -2.4), (sx * (1.6 + j * 0.8), 55.6, -2.6), 1,
                strands(P, "blue", "blue_dark"), extend=0.2, t2=1)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.6, 50.0, 3.4))
        feather_wing(m, wb, (side * 2.6, 50.0, 3.4), 16.0, 9.0, 2, feathers(P, "white", "white_dark", tip="lilac"),
                     side=side, sweep=50, droop=-14.0)
    hr = a["arm_right"]                                                              # pinwheel pole
    hx, hy, hz = hr["hand"]
    end = (hx - 26.0, hy + 4.0, hz - 2.0)
    rod(m, hr["bone"], (hx + 6.0, hy - 1.0, hz), end, 1, metal(P, "steel", dark="steel_dark"), extend=0, t2=1)
    pb = m.bone("spin_pinwheel", hr["bone"], end)
    m.round_box(pb, end[0], end[2] - 1.0, 1.4, 1.0, end[1] - 1.4, end[1] + 1.4, solid(P, "gold"), cut=0)
    for i in range(4):
        m.box(pb, end[0], end[1], end[2] - 1.4, end[0] + 10.0, end[1] + 10.0, end[2] - 1.4, cutout(pin_in, pinf),
              rotation=(0, 0, i * 90), pivot=(end[0], end[1], end[2] - 1.4))
    return m
