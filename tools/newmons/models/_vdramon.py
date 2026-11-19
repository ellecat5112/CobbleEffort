"""Shared builder for V-dramon and Red V-dramon (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): a stocky upright dragon of the Veemon line: a horned head with a big nose horn and two swept horns, a
pale muzzle and belly marked with a V, thick arms with long white claws, digitigrade legs with clawed feet and a
short heavy tail. Red: crimson hide. Blue (V-dramon): blue hide. Shiny: green / gold.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import theropod
from _digidetail import skin, solid
from _route import pal, tone


def make(name, red=False, colours=None, shiny_colours=None):
    hide = (200, 60, 70) if red else (60, 110, 210)
    hide_dark = (120, 20, 30) if red else (20, 50, 140)
    base = {"hide": hide, "hide_dark": hide_dark, "belly": (240, 230, 200), "belly_dark": (190, 176, 140),
            "claw": (230, 230, 236), "eye": (200, 30, 30), "white": (250, 250, 250), "mouth": (170, 40, 50),
            "tooth": (250, 250, 240), "horn": (230, 230, 236)}
    shiny = {"hide": (70, 160, 80), "hide_dark": (24, 90, 30)} if red else {"hide": (230, 180, 60), "hide_dark": (160, 110, 20)}
    base.update(colours or {})
    shiny = dict(shiny, **(shiny_colours or {}))

    def P(v):
        return pal(base, shiny, v)

    HIDE = skin(P, "hide", dark="hide_dark")

    def bellyf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if face == "north" and abs(abs(x) - (y - 30.0) * 0.4) < 0.5 and 30.0 < y < 38.0:
            return tone(p["hide_dark"], face), None
        return skin(P, "belly", dark="belly_dark")(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": bellyf, "snout": bellyf, "jaw": bellyf, "claw": solid(P, "claw"),
                "talon": solid(P, "claw"), "tooth": solid(P, "tooth"), "mouth": solid(P, "mouth")}
        a = theropod(m, mats, name, chest=(0, 34.0, -1.0), body_r=7.0, chest_r=6.6, neck_top=(0, 44.0, -3.0),
                     head_len=9.0, head_w=4.4, head_h=4.6, mouth_open=12, teeth=6, arm_len=12.0, arm_bulk=1.6,
                     leg_bulk=1.3, tail=((0, 18, 8), (0, 13, 14), (0, 9, 19)), tail_r=(4.6, 3.4, 2.0))
        hd = a["head"]
        sf, st = a["snout_front"], a["skull_top"]
        z0, z1 = a["skull_z"]
        spike(m, hd, (0, st - 1.0, sf + 2.0), (0, 1, -0.3), 1.8, 5.0, solid(P, "horn"), tip=0.8)        # nose horn
        for sx in (-1, 1):
            spike(m, hd, (sx * 2.4, st, z1 - 1.0), (sx * 0.5, 1, 0.5), 1.6, 6.0, solid(P, "horn"), tip=0.8)
            e = a["eye"]
            m.box(hd, min(sx * e[0], sx * (e[0] + 0.2)), e[1] - 0.6, e[2] - 0.8, max(sx * e[0], sx * (e[0] + 0.2)),
                  e[1] + 0.6, e[2] + 0.8, solid(P, "eye"))
        return m

    return build
