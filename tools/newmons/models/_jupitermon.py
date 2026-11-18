"""Shared builder for Jupitermon and Jupitermon: Wrath Mode (CobbleEffort: Digital; hand-built at the detail standard
after the official art on wikimon.net): the king of the Olympos Twelve. Jupitermon: a god in ornate golden armour
with a crested helm, a red halo, a white feathered cape-wing on one side, two golden hammers (the thunder-drum
mallets) in its hands and a crackling ring of yellow lightning round it. Wrath Mode: heavier spiked golden armour, a
huge golden sword wreathed in lightning and jagged lightning bolts bursting from its back. Shiny: silver and blue.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, feathers, gem, metal, solid
from _route import pal, tone

BASE = {"gold": (240, 200, 80), "gold_dark": (150, 110, 24), "gold_light": (255, 240, 180), "white": (246, 246, 250),
        "white_dark": (180, 184, 204), "red": (220, 40, 50), "bolt": (255, 240, 90), "bolt_core": (255, 255, 230),
        "black": (30, 30, 36), "eye": (120, 220, 255), "blade": (230, 236, 246), "blade_dark": (130, 140, 160)}
SHINY = {"gold": (210, 216, 232), "gold_dark": (110, 118, 140), "gold_light": (255, 255, 255), "bolt": (120, 200, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="black", trim_w=0.2, rivets=True)
METAL = metal(P, "gold", dark="gold_dark", light="gold_light")
BOLT = solid(P, "bolt", glow=True)


def bolt(m, bone, p0, p1, segs=4, r=1, seed=0):
    """A jagged lightning bolt from p0 to p1."""
    pts = [p0]
    for i in range(1, segs):
        t = i / segs
        off = 2.4 * (1 if (i + seed) % 2 else -1)
        pts.append((p0[0] + (p1[0] - p0[0]) * t + off, p0[1] + (p1[1] - p0[1]) * t, p0[2] + (p1[2] - p0[2]) * t))
    pts.append(p1)
    for a, b in zip(pts, pts[1:]):
        rod(m, bone, a, b, r, BOLT, extend=0.3, t2=1)


def make(name, wrath=False):
    def build():
        m = Model(name)
        mats = {"skin": GOLD, "chest": GOLD, "abs": GOLD, "pelvis": GOLD, "neck": GOLD, "deltoid": GOLD,
                "upper_arm": GOLD, "forearm": GOLD, "hand": GOLD, "finger": GOLD, "thigh": GOLD, "knee": GOLD,
                "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
        a = humanoid(m, mats, bulk=1.25 if wrath else 1.05, arm_bulk=1.15, leg_bulk=1.1, name=name)
        bd = a["body"]
        m.round_box(bd, 0, -4.4, 1.6, 0.5, 45.0, 48.0, gem(P, "red", "bolt"), cut=0)
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, GOLD, cut=1)
        m.round_box(hd, 0, -3.2, 2.0, 0.4, 56.6, 57.8, solid(P, "black"), cut=0)
        m.box(hd, -1.6, 57.0, -3.7, 1.6, 57.6, -3.6, solid(P, "eye", glow=True))
        for j in range(5):                                                          # crested helm
            spike(m, hd, (0, 60.0, -1.6 + j * 1.0), (0, 1, 0.4 + j * 0.2), 1.4, 6.0 - j * 0.6, METAL, tip=0.8)
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.6, 58.6, 0), (sx, 0.6, 0.3), 1.0, 4.0, METAL, tip=0.8)
        hb = m.bone("ring_halo", hd, (0, 67, 1))                                     # red halo
        for i in range(12):
            a0, a1 = 2 * math.pi * i / 12, 2 * math.pi * (i + 1) / 12
            rod(m, hb, (3.4 * math.cos(a0), 67.0, 1.0 + 3.4 * math.sin(a0)), (3.4 * math.cos(a1), 67.0,
                1.0 + 3.4 * math.sin(a1)), 1, solid(P, "red", glow=True), extend=0.2, t2=1)
        for sx in (-1, 1):                                                          # great pauldrons
            m.round_box(bd, sx * 8.4, 0, 3.8, 4.0, 46.0, 53.4, GOLD, cut=2)
            if wrath:
                for j in range(3):
                    spike(m, bd, (sx * 9.4, 53.0, -2.0 + j * 2.0), (sx * 0.5, 1, 0), 1.4, 6.0, METAL, tip=0.8)
        if not wrath:
            wb = m.bone("wing_left", bd, (4.0, 50.0, 3.6))                            # one white feathered wing
            feather_wing(m, wb, (4.0, 50.0, 3.6), 24.0, 14.0, 3, feathers(P, "white", "white_dark"), side=1, sweep=20,
                         droop=-18.0)
            for nm in ("arm_left", "arm_right"):                                     # two golden hammers
                hx, hy, hz = a[nm]["hand"]
                sx = 1 if hx > 0 else -1
                rod(m, a[nm]["bone"], (hx, hy - 1.0, hz), (hx + sx * 6.0, hy + 2.0, hz - 2.0), 1, METAL, extend=0, t2=1)
                m.round_box(a[nm]["bone"], hx + sx * 8.0, hz - 2.0, 3.2, 3.2, hy - 2.0, hy + 6.0, GOLD, cut=1)
            rb = m.bone("ring_bolt", bd, (0, 40, 4))                                   # ring of lightning
            for i in range(10):
                a0 = 2 * math.pi * i / 10
                a1 = 2 * math.pi * (i + 1) / 10
                r0, r1 = 26.0 + (2.0 if i % 2 else -2.0), 26.0 + (-2.0 if i % 2 else 2.0)
                rod(m, rb, (r0 * math.cos(a0), 40.0 + r0 * math.sin(a0), 6.0), (r1 * math.cos(a1), 40.0 + r1 * math.sin(a1),
                    6.0), 1, BOLT, extend=0.3, t2=1)
        else:
            hr = a["arm_right"]                                                      # huge golden sword
            hx, hy, hz = hr["hand"]
            m.round_box(hr["bone"], hx, hz, 1.0, 1.0, hy - 2.0, hy + 3.0, METAL, cut=0)
            m.round_box(hr["bone"], hx, hz, 4.4, 1.4, hy - 3.6, hy - 2.0, GOLD, cut=0)
            m.round_box(hr["bone"], hx, hz - 0.4, 2.6, 0.6, hy - 40.0, hy - 3.6, metal(P, "blade", dark="blade_dark"), cut=0)
            m.round_box(hr["bone"], hx, hz - 1.0, 0.6, 0.2, hy - 38.0, hy - 6.0, BOLT, cut=0)
            spike(m, hr["bone"], (hx, hy - 40.0, hz - 0.4), (0, -1, 0), 3.0, 5.0, metal(P, "blade", dark="blade_dark"),
                  tip=0.8)
            for j in range(5):                                                      # lightning from its back
                ang = math.radians(-70 + j * 35)
                bolt(m, bd, (2.0 * math.sin(ang), 50.0, 4.0), (24.0 * math.sin(ang), 50.0 + 22.0 * math.cos(ang), 10.0),
                     segs=4, r=1, seed=j)
        return m

    return build
