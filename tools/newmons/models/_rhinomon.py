"""Shared builder for Rhinomon and Rhinomon (X-Antibody) (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Rhinomon (the Armor Digimon of knowledge): a sturdy golden-armoured rhinoceros with a long silver drill
horn, scrolled gold plates set with red gems, black joints and golden hooves, and a spiked tail. X-Antibody: a heavier
bronze war rhino bristling with silver spikes, cyan-lit plates and a great broadsword mounted along its back.
Shiny: silver / dark steel.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, gem, metal, solid
from _route import pal, tone


def make(name, x=False):
    base = {"gold": (240, 210, 100) if not x else (190, 140, 70), "gold_dark": (170, 130, 40) if not x else (110, 70, 30),
            "steel": (210, 214, 226), "steel_dark": (110, 114, 126), "black": (30, 30, 36), "red": (210, 40, 40),
            "white": (255, 230, 230), "cyan": (90, 230, 230), "eye": (250, 60, 40)}
    shiny = {"gold": (210, 214, 226), "gold_dark": (110, 114, 126)} if not x else {"gold": (80, 84, 96),
                                                                                   "gold_dark": (30, 32, 40)}

    def P(v):
        return pal(base, shiny, v)

    PLATE = armour(P, "gold", "gold_dark", trim="steel" if x else None, trim_w=0.2)
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        mats = {"skin": PLATE, "head": PLATE, "snout": PLATE, "jaw": PLATE, "leg_lower": PLATE,
                "paw": PLATE, "claw": PLATE, "belly": solid(P, "black")}
        a = quadruped(m, mats, name, length=28.0, body_y=14.0, body_rx=7.0, body_ry=6.4, neck=((0, 18, -14),
                      (0, 19, -18)), head_len=10.0, head_w=4.0, head_h=4.4, snout=0.4, mouth_open=4,
                      tail=((0, 16, 14), (0, 18, 19), (0, 19, 23)), tail_r=(1.6, 1.2, 1.0))
        bd = a["body"]
        hd = a["head"]
        spike(m, hd, (0, 20.0, -24.0), (0, 0.4, -1), 2.4, 10.0, STEEL, tip=0.8)              # drill horn
        spike(m, hd, (0, 22.0, -19.0), (0, 1, -0.3), 1.4, 4.0, STEEL, tip=0.8)
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 4.0, sx * 4.3))
            m.box(hd, x0, 20.0, -20.0, x1, 21.0, -18.6, solid(P, "eye", glow=True))
            for j in range(3):                                                           # gem studs
                m.box(bd, min(sx * 7.2, sx * 7.6), 15.0, -8.0 + j * 7.0, max(sx * 7.2, sx * 7.6), 17.0, -6.6 + j * 7.0,
                      gem(P, "red", "white", glow=False))
        spike(m, "tail", (0, 19.0, 23.0), (0, 0.4, 1), 1.4, 4.0, STEEL, tip=0.8)
        if x:
            for j in range(8):                                                           # silver spikes
                spike(m, bd, ((j % 2 * 2 - 1) * 5.0, 20.0, -10.0 + j * 2.8), ((j % 2 * 2 - 1) * 0.5, 1, 0.2), 1.4,
                      4.0, STEEL, tip=0.8)
            m.box(bd, -1.0, 21.0, -6.0, 1.0, 24.0, 22.0, STEEL, rotation=(-28, 0, 0), pivot=(0, 22.0, 4.0))   # broadsword
            m.box(bd, -3.0, 20.0, -7.0, 3.0, 22.0, -5.0, PLATE, rotation=(-28, 0, 0), pivot=(0, 22.0, 4.0))
            for sx in (-1, 1):
                m.box(bd, min(sx * 6.6, sx * 7.0), 10.0, -4.0, max(sx * 6.6, sx * 7.0), 11.0, 6.0,
                      solid(P, "cyan", glow=True))
        return m

    return build
