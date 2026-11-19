"""Shared builder for Triceramon and Triceramon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art
on wikimon.net): a hulking teal triceratops reared up on thick legs: a spiked frill round its head, a long nose horn
banded red and black and two brow horns, a toothy beak, an olive belly, studded plates down its back and tail, and
huge ivory claws. X-Antibody: a broad green frill fringed with spikes, three long drill horns blazing with fire,
steel-blue riveted armour plates studded with spikes over its body and legs. Shiny: purple / orange."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, theropod
from _digidetail import armour, eye, riveted, scales, skin, solid
from _route import pal, tone

BASE = {"teal": (60, 120, 130), "teal_dark": (24, 60, 70), "olive": (110, 110, 60), "olive_dark": (60, 60, 24),
        "ivory": (250, 240, 210), "red": (210, 40, 40), "black": (30, 30, 34), "eye": (60, 140, 220),
        "pupil": (10, 10, 20), "white": (255, 255, 255), "green": (80, 140, 70), "green_dark": (30, 80, 30),
        "steel": (110, 130, 170), "steel_dark": (40, 50, 90), "drill": (240, 200, 110), "flame": (255, 150, 40, 200),
        "mouth": (150, 20, 30)}
SHINY = {"teal": (120, 80, 160), "teal_dark": (60, 30, 100), "green": (220, 130, 50), "green_dark": (140, 70, 20)}


def make(name, x=False):
    def P(v):
        return pal(BASE, SHINY, v)

    HIDE = scales(P, "green" if x else "teal", "green_dark" if x else "teal_dark", size=1.4)
    ARM = riveted(P, "steel", "steel_dark") if x else armour(P, "teal", "teal_dark", panel=(3.0, 3.0))

    def build():
        m = Model(name)
        mats = {"skin": HIDE, "belly": skin(P, "olive", dark="olive_dark"), "head": HIDE, "neck": HIDE,
                "thigh": ARM, "shin": ARM, "foot": ARM, "talon": solid(P, "ivory"), "claw": solid(P, "ivory"),
                "arm": ARM, "tail": HIDE}
        a = theropod(m, mats, name, hip_y=16.0, chest=(0, 24.0, -4.0), body_r=7.4, chest_r=7.0)
        hd = a["head"]
        hx, hy, hz = 0, a["skull_top"] - 3.0, a["skull_z"][1]
        for i in range(9):                                                         # frill
            ang = (i - 4) * 0.36
            fx, fy = math.sin(ang) * 8.0, hy + 2.0 + math.cos(ang) * 6.0
            m.round_box(hd, fx, hz + 3.0, 2.2, 0.8, fy - 2.0, fy + 2.0, solid(P, "green" if x else "teal"), cut=0)
            spike(m, hd, (fx * 1.15, fy + math.cos(ang) * 1.4, hz + 3.0), (math.sin(ang), math.cos(ang), 0.2), 1.0,
                  2.6, solid(P, "ivory" if not x else "ivory"), tip=0.8)
        sf = a["snout_front"]
        if x:
            for k, (dx, dy, L) in enumerate(((0, -1.0, 12.0), (-2.4, 3.0, 16.0), (2.4, 3.0, 16.0))):
                base_pt = (dx, hy + dy, sf + 2.0 if k == 0 else hz - 2.0)
                spike(m, hd, base_pt, (dx * 0.05, 0.25, -1), 2.2, L, solid(P, "drill"), tip=0.8)
                spike(m, hd, (dx, hy + dy + 0.5, base_pt[2] - L * 0.7), (dx * 0.05, 0.25, -1), 1.6, 6.0,
                      solid(P, "flame", glow=True), tip=0.8)
        else:
            for j in range(4):                                                     # banded nose horn
                spike(m, hd, (0, hy - 0.6 + j * 0.9, sf + 2.0 - j * 2.0), (0, 0.45, -1), 2.0 - j * 0.4, 2.6,
                      solid(P, "red" if j % 2 else "black"), tip=0.8)
            for sx in (-1, 1):
                spike(m, hd, (sx * 2.4, hy + 2.6, hz - 2.0), (sx * 0.2, 0.5, -1), 1.4, 6.0, solid(P, "ivory"), tip=0.8)
        bd = a["body"]
        for j in range(8):                                                         # back plates / spikes
            z = -2.0 + j * 3.4
            spike(m, bd, (0, 30.0 - j * 1.6, z), (0, 1, 0.2), 1.6, 3.0, solid(P, "ivory" if x else "teal_dark"),
                  tip=0.8)
            if x:
                for sx in (-1, 1):
                    spike(m, bd, (sx * 5.0, 26.0 - j * 1.2, z), (sx, 0.6, 0), 1.0, 3.0, solid(P, "ivory"), tip=0.8)
        return m
    return build
