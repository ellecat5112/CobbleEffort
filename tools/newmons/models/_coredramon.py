"""Shared builder for Coredramon (CobbleEffort: Digital; hand-built after the official art on wikimon.net): a crouching
scaly dragon with a cream belly, a fanged red-mouthed head crowned with red spikes, thick clawed arms and legs with
white talons, a spiked tail and great bat wings with pale tattered membranes. make("blue") is the blue Coredramon,
make("green") the green one. Shiny: crimson (blue) / gold (green).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import bat_wing, theropod
from _digidetail import scales, skin, solid
from _route import pal, tone

COMMON = {"belly": (230, 220, 190), "belly_dark": (180, 166, 130), "red": (210, 40, 40), "claw": (240, 236, 220),
          "membrane": (236, 226, 200), "mouth": (200, 40, 50), "tooth": (250, 250, 246), "eye": (250, 220, 60)}
BLUE = {"hide": (50, 70, 160), "hide_dark": (20, 30, 90), "hide_light": (110, 140, 220)}
GREEN = {"hide": (70, 110, 50), "hide_dark": (30, 60, 20), "hide_light": (140, 180, 100)}
SHINY = {"blue": {"hide": (160, 30, 40), "hide_dark": (80, 10, 16), "hide_light": (230, 110, 110)},
         "green": {"hide": (200, 160, 50), "hide_dark": (130, 90, 10), "hide_light": (240, 210, 130)}}


def make(name, colour="blue"):
    base = dict(COMMON, **(BLUE if colour == "blue" else GREEN))

    def P(v):
        return pal(base, dict(base, **SHINY[colour]), v)

    HIDE = scales(P, "hide", "hide_dark", size=1.4, light="hide_light", rim_mix=0.4)
    BELLY = skin(P, "belly", dark="belly_dark", var=0.03)

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": BELLY, "neck": HIDE, "head": HIDE, "snout": HIDE, "jaw": HIDE,
                "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "arm": HIDE, "hand": HIDE,
                "claw": solid(P, "claw"), "thigh": HIDE, "shin": HIDE, "foot": HIDE, "talon": solid(P, "claw"),
                "tail": HIDE, "tail_tip": HIDE}
        a = theropod(m, mats, name, hip_y=17.0, hip_z=2.0, chest=(0, 28.0, -2.0), body_r=6.0, chest_r=6.2,
                     neck_top=(0, 36.0, -6.0), head_len=10.0, head_w=3.6, head_h=4.0, mouth_open=22, teeth=5,
                     arm_len=11.0, arm_bulk=1.4, leg_bulk=1.4, stance=5.4,
                     tail=((0, 14, 10), (4, 10, 16), (9, 8, 21), (14, 9, 25)), tail_r=(3.4, 2.4, 1.6, 1.0))
        hd = a["head"]
        st = a["skull_top"]
        for i in range(5):                                                   # red head spikes
            spike(m, hd, ((i - 2) * 0.9, st - 0.4, -6.0 + abs(i - 2) * 0.6), ((i - 2) * 0.25, 1, 0.5), 1.2,
                  4.0 - abs(i - 2) * 0.6, solid(P, "red"), tip=0.3)
        for sx in (-1, 1):
            spike(m, hd, (sx * 3.4, st - 1.6, -4.0), (sx * 0.6, 0.6, 0.6), 1.2, 3.0, solid(P, "claw"))
            ex, ey, ez = a["eye"]
            m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.8, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
                  ez + 0.8, solid(P, "eye", glow=True))
        for p in a["tail_pts"][1:]:
            spike(m, a["tail"], p, (0, 1, 0.4), 1.4, 2.4, HIDE)
        for side in (1, -1):                                                # great bat wings
            bat_wing(m, a["body"], (side * 4.0, 31.0, 3.0), 22.0, 16.0, 4, HIDE, solid(P, "membrane"), side=side,
                     sweep=25)
        return m
    return build
