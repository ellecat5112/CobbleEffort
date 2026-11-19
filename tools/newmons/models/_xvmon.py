"""Shared builder for XV-mon and XV-mon (Black) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a muscular blue dragon-man of the V-mon line: a horned head with a long silver nose horn and a yellow V
on its brow, a pale chest marked with a great white X scar, heavy clawed arms, small white bat wings, digitigrade legs
with long silver claws and a thick tail. Black: charcoal-black hide. Shiny: green / violet."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import metal, plane, skin, solid
from _route import pal, tone


def make(name, black=False):
    base = {"hide": (60, 120, 220) if not black else (50, 50, 62), "hide_dark": (20, 60, 140) if not black else (16, 16, 22),
            "pale": (230, 236, 246), "white": (250, 250, 255), "yellow": (250, 210, 50), "silver": (220, 224, 236),
            "silver_dark": (120, 124, 140), "eye": (200, 40, 40), "wing": (240, 240, 250), "bar": (180, 186, 200)}
    shiny = {"hide": (70, 170, 90), "hide_dark": (24, 100, 40)} if not black else {"hide": (110, 60, 150),
                                                                                    "hide_dark": (60, 24, 90)}

    def P(v):
        return pal(base, shiny, v)

    HIDE = skin(P, "hide", dark="hide_dark")

    def chestf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(x) < 5.0:
            if abs(abs(x) - abs(y - 45.0) * 0.6) < 0.5 and abs(y - 45.0) < 6.0:
                return tone(p["white"], face), None
            return skin(P, "pale", dark="hide")(x, y, z, face, variant, box=box, **k)
        return HIDE(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "chest": chestf, "abs": chestf, "pelvis": HIDE, "deltoid": HIDE, "upper_arm": HIDE,
                "forearm": HIDE, "hand": HIDE, "finger": HIDE, "claw": metal(P, "silver"), "thigh": HIDE, "knee": HIDE,
                "shin": HIDE, "calf": HIDE, "foot": HIDE, "talon": metal(P, "silver"), "neck": HIDE}
        a = humanoid(m, mats, bulk=1.3, arm_bulk=1.35, leg_bulk=1.2, digitigrade=True, claws=True, talons=True, name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -1.0, 3.2, 4.4, 54.0, 61.0, HIDE, cut=1)
        m.round_box(hd, 0, -5.6, 2.2, 1.8, 54.4, 57.6, skin(P, "pale", dark="hide"), cut=1)
        spike(m, hd, (0, 58.0, -5.4), (0, 0.6, -1), 1.6, 6.0, metal(P, "silver", dark="silver_dark"), tip=0.8)
        for sx in (-1, 1):
            m.box(hd, min(sx * 0.8, sx * 2.6), 58.6, -4.6, max(sx * 0.8, sx * 2.6), 59.4, -4.2, solid(P, "eye", glow=True))
            m.box(hd, min(0.0, sx * 1.8), 60.0, -4.3, max(0.0, sx * 1.8), 60.8, -4.0, solid(P, "yellow"),
                  rotation=(0, 0, -sx * 30), pivot=(0, 60.0, -4.1))
            spike(m, hd, (sx * 2.6, 60.6, 0.6), (sx * 0.6, 0.8, 0.6), 1.6, 6.0, HIDE, tip=0.8)
            wb = m.bone("wing_left" if sx > 0 else "wing_right", bd, (sx * 3.0, 48.0, 4.0))
            bat_wing(m, wb, (sx * 3.0, 48.0, 4.0), 14.0, 12.0, 3, solid(P, "bar"), solid(P, "wing"), side=sx, sweep=20)
        tl = m.bone("tail", bd, (0, 30, 4))
        pts = [(0, 30.0, 4.0), (0, 22.0, 12.0), (2.0, 16.0, 18.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, tl, p0, p1, 3 - i, HIDE, extend=0.6)
        return m
    return build
