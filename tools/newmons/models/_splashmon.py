"""Shared builder for Splashmon and its Darkness Modes (CobbleEffort: Digital; hand-built after the official art on
wikimon.net). Splashmon: a slender water-man in a white bodysuit banded with gold and silver, long flowing lilac hair
like a wave, a pale face with a lilac visor-band, and a glassy bubble of water swirling in one hand. Darkness Mode
(Drippins): the same grown into a hulking pale-blue giant in a white bodysuit, huge arms and gold bands. Darkness Mode:
a raging water beast: a liquid tiger-dragon of white-blue water with a fanged maw, golden claws and splashing limbs.
Shiny: aqua / dark violet.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digibeast import ball, quadruped
from _digibody import humanoid
from _digidetail import armour, fabric, metal, skin, solid, strands
from _route import pal, tone


def make(name, mode="base"):
    base = {"white": (240, 244, 252), "white_dark": (180, 190, 214), "gold": (230, 190, 80), "silver": (200, 204, 216),
            "lilac": (200, 180, 240), "lilac_dark": (140, 120, 200), "face": (230, 220, 240), "blue": (170, 220, 250),
            "blue_dark": (100, 150, 210), "water": (180, 220, 250, 170), "claw": (240, 200, 70), "eye": (40, 60, 120),
            "mouth": (60, 80, 140), "tooth": (250, 250, 240)}
    shiny = {"white": (150, 230, 220), "white_dark": (80, 170, 160)} if mode != "beast" else {"blue": (130, 100, 200),
                                                                                           "blue_dark": (70, 50, 140)}

    def P(v):
        return pal(base, shiny, v)

    def suitf(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        if abs((y % 6.0) - 3.0) < 0.3:
            return tone(p["gold"], face), None
        return fabric(P, "white", "white_dark", axis="y", period=3.0)(x, y, z, face, variant, box=box, **k)

    def build():
        m = Model(name)
        if mode == "beast":
            WATER = skin(P, "blue", dark="blue_dark", var=0.06)
            mats = {"skin": WATER, "head": WATER, "snout": WATER, "jaw": WATER, "claw": solid(P, "claw"),
                    "tooth": solid(P, "tooth"), "mouth": solid(P, "mouth")}
            a = quadruped(m, mats, name, length=28.0, body_y=16.0, body_rx=7.0, body_ry=6.4, chest_bulk=1.3,
                          neck=((0, 22, -14), (0, 26, -18)), head_len=11.0, head_w=5.0, head_h=5.0, mouth_open=20,
                          teeth=8, tail=((0, 18, 14), (0, 20, 20), (0, 18, 26)), tail_r=(2.6, 2.0, 1.4))
            for j in range(10):                                                          # splashing droplets
                ang = 2 * math.pi * j / 10
                ball(m, a["body"], (12.0 * math.cos(ang), 6.0 + (j % 3) * 4.0, 12.0 * math.sin(ang)), 1.2,
                     solid(P, "water"), layers=1)
            return m
        big = mode == "drippins"
        mats = {"skin": suitf, "neck": skin(P, "face"), "hand": skin(P, "blue" if big else "face"),
                "finger": skin(P, "blue" if big else "face")}
        a = humanoid(m, mats, bulk=1.5 if big else 0.75, arm_bulk=1.7 if big else 0.75, leg_bulk=1.4 if big else 0.8,
                     name=name)
        bd = a["body"]
        hd = m.bone("head", bd, (0, 55, 0))
        m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.0, 60.0, skin(P, "face"), cut=1)
        m.round_box(hd, 0, -2.4, 2.4, 0.6, 57.0, 58.0, solid(P, "lilac"), cut=0)
        m.box(hd, -1.6, 56.4, -2.9, 1.6, 56.8, -2.7, solid(P, "eye"))
        for j in range(8):                                                               # flowing wave hair
            ang = math.radians(-70 + j * 20)
            rod(m, hd, (2.0 * math.sin(ang), 60.0, 0.6), (8.0 * math.sin(ang), 66.0 - abs(j - 3.5), 6.0 + j * 0.4), 2,
                strands(P, "lilac", "lilac_dark"), extend=0.3)
        if not big:
            h = a["arm_right"]["hand"]
            ball(m, a["arm_right"]["bone"], (h[0] - 1.0, h[1] + 4.0, h[2] - 3.0), 3.0, solid(P, "water"), layers=3)
        return m

    return build
