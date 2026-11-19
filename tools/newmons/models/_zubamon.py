"""Shared builder for Zubamon and Zubaeagermon (CobbleEffort: Digital; hand-built after the official art on
wikimon.net): the blade beasts: a lithe golden armoured beast of sword-edged plates with a long blade-crested head,
red eyes, a fanged jaw, silver-tipped claws and steel spikes at its joints. Zubamon (Child): small, with a great
ragged white mane and tail like torn banners and a sword-tail trailing a blue slash. Zubaeagermon (Adult): bigger and
sleeker, its tail one huge curved golden blade trailing a blue arc. Shiny: silver."""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import quadruped
from _digidetail import armour, fur, metal, solid
from _route import pal, tone

BASE = {"gold": (236, 196, 80), "gold_dark": (160, 120, 30), "steel": (210, 214, 226), "steel_dark": (110, 114, 130),
        "white": (240, 240, 246), "white_dark": (180, 184, 200), "black": (34, 30, 30), "eye": (255, 50, 50),
        "arc": (120, 210, 255, 190)}
SHINY = {"gold": (210, 214, 226), "gold_dark": (120, 124, 140)}


def make(name, adult=False):
    def P(v):
        return pal(BASE, SHINY, v)

    GOLD = armour(P, "gold", "gold_dark", trim="black", panel=(2.4, 2.4))
    STEEL = metal(P, "steel", dark="steel_dark")

    def build():
        m = Model(name)
        mats = {"skin": GOLD, "belly": GOLD, "neck": GOLD, "head": GOLD, "leg": GOLD, "paw": GOLD, "claw": STEEL,
                "tail": GOLD}
        L = 22.0 if adult else 16.0
        a = quadruped(m, mats, name, length=L, body_y=10.0, body_rx=3.6, body_ry=3.6, chest_bulk=1.1,
                      neck=((0, 14, -L / 2 - 2), (0, 16, -L / 2 - 4)), head_len=9.0, head_w=2.6, head_h=3.2, snout=0.8,
                      mouth_open=14, teeth=4, tail=((0, 12, L / 2),), tail_r=(1.4,), toes=3, claws=True)
        bd, hd = a["body"], a["head"]
        hz = -L / 2 - 4
        m.box(hd, -0.4, 18.0, hz - 6.0, 0.4, 24.0, hz + 6.0, STEEL, rotation=(-25, 0, 0), pivot=(0, 18.0, hz))  # blade crest
        for sx in (-1, 1):
            m.box(hd, min(sx * 1.6, sx * 2.7), 17.0, hz - 3.4, max(sx * 1.6, sx * 2.7), 17.8, hz - 2.8,
                  solid(P, "eye", glow=True))
        for i in range(4):
            spike(m, bd, (0, 14.0, -L / 2 + 2.0 + i * L / 5), (0, 1, 0.4), 1.2, 3.4, STEEL, tip=0.8)
        tl = m.bone("blade_tail", bd, (0, 12, L / 2))
        if adult:                                                                      # one huge curved blade tail
            for j in range(6):
                ang = j * 0.25
                c = (0, 14.0 + 16.0 * math.sin(ang), L / 2 + 14.0 * (1 - math.cos(ang)) + j * 1.4)
                m.box(tl, -0.5, c[1] - 1.0, c[2] - 3.0, 0.5, c[1] + 3.6, c[2] + 0.6, GOLD,
                      rotation=(math.degrees(ang) * -1.0, 0, 0), pivot=c)
            for j in range(8):
                ang = j * 0.25
                m.box(tl, -0.3, 16.0 + 18.0 * math.sin(ang), L / 2 + 18.0 * (1 - math.cos(ang)) + 2.0, 0.3,
                      17.4 + 18.0 * math.sin(ang), L / 2 + 18.0 * (1 - math.cos(ang)) + 4.0, solid(P, "arc", glow=True))
        else:                                                                          # ragged white mane and tail
            for j in range(7):
                ang = (j - 3) * 0.4
                spike(m, hd, (math.sin(ang) * 2.0, 18.0, hz + 2.0), (math.sin(ang) * 0.6, 0.7, 1), 1.6, 8.0,
                      fur(P, "white", "white_dark"), tip=0.8)
            for j in range(4):
                spike(m, tl, (0, 12.0, L / 2), ((j - 1.5) * 0.4, 0.6, 1), 2.0, 12.0, fur(P, "white", "white_dark"),
                      tip=0.8)
            spike(m, tl, (0, 12.0, L / 2), (0, 0.2, 1), 1.0, 8.0, STEEL, tip=0.8)
        return m
    return build
