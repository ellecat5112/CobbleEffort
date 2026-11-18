"""Shared builder for Leviamon and Leviamon (X-Antibody) (CobbleEffort: Digital; hand-built at the detail standard after
the official art on wikimon.net): the Demon Lord of Envy: a colossal crimson crocodile-leviathan with a long armoured
snout full of teeth, blue-grey belly plates, a row of cyan spines down its back, short clawed legs, two long whip
antennae and a long tail, breathing rainbow mist. X-Antibody: dark violet armour, huge pink-and-cyan blade fins
flaring from its back, a jagged tail blade and a magic circle glowing above it. 45 blocks long.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, cutout, gem, local, scales, solid
from _route import pal, tone


def make(name, x=False):
    base = {"red": (190, 40, 40) if not x else (90, 50, 110), "red_dark": (100, 14, 14) if not x else (40, 20, 60),
            "red_light": (240, 110, 100) if not x else (160, 120, 190), "belly": (130, 140, 170), "belly_dark": (70, 76, 100),
            "cyan": (90, 220, 230), "cyan_light": (220, 255, 255), "pink": (250, 120, 190, 200), "pink_light": (255, 210, 235, 230),
            "mouth": (160, 30, 40), "tooth": (250, 248, 236), "eye": (250, 220, 60), "mist": (190, 220, 255, 170)}
    shiny = {"red": (40, 120, 60), "red_dark": (14, 60, 24), "red_light": (120, 200, 130)}

    def P(v):
        return pal(base, shiny, v)

    HIDE = scales(P, "red", "red_dark", size=1.8, light="red_light", belly_key="belly", belly=lambda xx, y, z, f: f == "down")
    BELLY = armour(P, "belly", "belly_dark")

    def bladef(xx, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(xx, y, z, face, box)
        c = p["pink_light"] if v / max(H, 1e-6) > 0.7 else p["pink"]
        return c, c[:3]

    def blade_in(xx, y, z, face, box):
        u, v, W, H = local(xx, y, z, face, box)
        a, b = u / max(W, 1e-6), v / max(H, 1e-6)
        return abs(a - 0.5) < 0.5 * (1 - b) + 0.03

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": BELLY,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": HIDE, "leg_lower": HIDE,
                "paw": HIDE, "claw": solid(P, "tooth"), "tail": HIDE}
        a = quadruped(m, mats, name, length=40.0, body_y=10.0, body_rx=6.0, body_ry=5.0, chest_bulk=1.15,
                      neck=((0, 12, -20), (0, 13, -25)), head_len=16.0, head_w=4.0, head_h=3.6, snout=1.6, mouth_open=24,
                      teeth=9, leg_bulk=1.2, toes=3,
                      tail=((0, 10, 21), (2, 9, 29), (5, 9, 37), (8, 10, 44)), tail_r=(3.6, 2.6, 1.8, 1.2))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.8,
                  solid(P, "eye", glow=True))
            pts = [(sx * 1.6, ey + 1.0, ez + 1.0), (sx * 5.0, ey + 8.0, ez + 8.0), (sx * 9.0, ey + 12.0, ez + 18.0)]   # antennae
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, hd, p0, p1, 1, HIDE, extend=0.2, t2=1)
        for i in range(12):                                                         # cyan back spines
            spike(m, bd, (0, 15.0, -18.0 + i * 3.4), (0, 1, 0.4), 1.4, 3.0, gem(P, "cyan", "cyan_light"), tip=0.8)
        for p in a["tail_pts"][1:]:
            spike(m, a["tail"], p, (0, 1, 0.3), 1.2, 2.4, gem(P, "cyan", "cyan_light"), tip=0.8)
        sn = (0, a["mouth_y"], a["snout_front"])                                     # rainbow mist
        m.round_box(hd, 0, sn[2] - 4.0, 3.0, 3.0, sn[1] - 2.0, sn[1] + 3.0, solid(P, "mist"), cut=1)
        if x:
            B = cutout(blade_in, bladef)
            for side in (1, -1):                                                     # huge blade fins
                wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 15.0, -4.0))
                for j in range(4):
                    x0, x1 = sorted((side * 3.0 - 2.0, side * 3.0 + 2.0))
                    m.box(wb, x0, 15.0, -4.0 + j * 3.0, x1, 15.0 + 18.0 - j * 3.0, -4.0 + j * 3.0, B,
                          rotation=(0, 0, side * -(30 + j * 14)), pivot=(side * 3.0, 15.0, -4.0 + j * 3.0))
            tp = a["tail_pts"][-1]
            m.box(a["tail"], tp[0] - 2.0, tp[1], tp[2], tp[0] + 2.0, tp[1] + 10.0, tp[2], B, rotation=(70, 0, 0), pivot=tp)
            rb = m.bone("ring_circle", bd, (0, 32, 0))                                 # magic circle above
            for i in range(16):
                a0, a1 = 2 * math.pi * i / 16, 2 * math.pi * (i + 1) / 16
                rod(m, rb, (12.0 * math.cos(a0), 32.0, 12.0 * math.sin(a0)), (12.0 * math.cos(a1), 32.0, 12.0 * math.sin(a1)), 1,
                    solid(P, "cyan", glow=True), extend=0.2, t2=1)
        return m

    return build
