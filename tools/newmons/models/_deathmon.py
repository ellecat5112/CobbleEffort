"""Shared builder for Deathmon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a crouching
demon lord shaped like a grey dinosaur, its head a dark horned helm round one huge round yellow eye on each side, a
short fanged beak, fiery orange-to-red bat wings, a long whip tail, taloned feet with steel bands, and arms that end
in little bird-skull heads with eyes of their own. make(black=True): Deathmon (Black), the same body in charcoal.
Shiny: violet hide, blue wings.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, theropod
from _digidetail import armour, cutout, local, metal, noise2, skin, solid
from _route import pal, tone

BASE = {"hide": (200, 200, 206), "hide_dark": (120, 120, 130), "hide_light": (240, 240, 246), "black": (60, 58, 66),
        "black_dark": (20, 20, 26), "black_light": (130, 130, 144), "helm": (90, 90, 100), "helm_dark": (30, 30, 36),
        "eye": (250, 230, 120), "pupil": (20, 18, 16), "wing": (240, 120, 30), "wing_dark": (190, 30, 20),
        "wing_edge": (40, 20, 20), "steel": (200, 200, 210), "steel_dark": (100, 100, 110), "talon": (230, 226, 216),
        "mouth": (120, 20, 30), "tooth": (250, 250, 246), "band": (120, 30, 40)}
SHINY = {"hide": (170, 140, 210), "hide_dark": (100, 70, 150), "black": (80, 50, 110), "black_dark": (40, 20, 60),
         "wing": (80, 170, 250), "wing_dark": (40, 60, 200)}


def P(v):
    return pal(BASE, SHINY, v)


def make(name, black=False):
    key = "black" if black else "hide"
    HIDE = skin(P, key, dark=key + "_dark", light=key + "_light", var=0.05)
    HELM = armour(P, "helm", "helm_dark")
    STEEL = metal(P, "steel", dark="steel_dark")

    def eyef(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        r = math.hypot(u - W / 2, v - H / 2) / max(min(W, H) / 2, 1e-6)
        if face in ("east", "west"):
            if r < 0.35:
                return tone(p["pupil"], face), None
            if r < 0.95:
                return p["eye"], None
        return HELM(x, y, z, face, variant, box=box, **k)

    def wingf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        t = v / max(H, 1e-6)
        c = p["wing"] if t > 0.6 else p["wing_dark"] if t > 0.25 else p["wing_edge"]
        return tone(c, face), None

    def holes(x, y, z, face, box):
        u, v, W, H = local(x, y, z, face, box)
        return noise2(u * 0.6, v * 0.6, 11) < 0.82

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": HIDE, "neck": HIDE, "head": HELM, "snout": HIDE, "jaw": HIDE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE, "claw": STEEL,
                "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "talon"), "tail": HIDE, "tail_tip": HIDE}
        a = theropod(m, mats, name, hip_y=14.0, hip_z=3.0, chest=(0, 24.0, -3.0), body_r=6.0, chest_r=6.0,
                     neck_top=(0, 31.0, -6.0), head_len=10.0, head_w=4.6, head_h=5.0, mouth_open=12, teeth=4,
                     arm_len=10.0, arm_bulk=1.3, leg_bulk=1.5, stance=4.8,
                     tail=((0, 14, 9), (2, 13, 17), (5, 12, 25), (9, 12, 32), (14, 13, 37)),
                     tail_r=(3.6, 2.6, 1.8, 1.2, 0.8))
        bd, hd = a["body"], a["head"]
        ex, ey, ez = a["eye"]
        for sx in (-1, 1):                                                       # one huge eye each side
            x0, x1 = sorted((sx * (ex - 0.4), sx * (ex + 0.8)))
            m.box(hd, x0, ey - 2.4, ez - 2.4, x1, ey + 2.4, ez + 2.4, eyef)
            for j in range(3):                                                   # swept-back helm horns
                spike(m, hd, (sx * 2.6, ey + 2.6, ez + 1.0 + j * 1.6), (sx * 0.3, 0.6, 1), 2.0 - j * 0.4,
                      7.0 - j * 1.5, HELM, tip=0.25)
        for nm in ("arm_left", "arm_right"):                                     # bird-skull hands
            h = a[nm]["hand"]
            sb = a[nm]["bone"]
            m.round_box(sb, h[0], h[2] - 2.0, 2.0, 2.6, h[1] - 1.6, h[1] + 2.0, HELM, cut=1)
            spike(m, sb, (h[0], h[1], h[2] - 4.4), (0, -0.5, -1), 1.6, 3.4, solid(P, "talon"), tip=0.3)
            for sx in (-1, 1):
                x0, x1 = sorted((h[0] + sx * 2.0, h[0] + sx * 2.3))
                m.box(sb, x0, h[1] - 0.2, h[2] - 3.0, x1, h[1] + 1.2, h[2] - 1.6, solid(P, "eye"))
        for nm in ("leg_left", "leg_right"):                                     # steel ankle bands
            lg = a[nm]
            ak = lg["ankle"]
            m.round_box(lg["bone"], ak[0], ak[2], 2.4, 2.4, ak[1] + 0.6, ak[1] + 2.2, solid(P, "band"), cut=1)
        for side in (1, -1):                                                     # fiery bat wings
            wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 28.0, 4.0))
            bat_wing(m, wb, (side * 3.0, 28.0, 4.0), 18.0, 16.0, 4, HELM, cutout(holes, wingf), side=side, sweep=30)
        return m
    return build
