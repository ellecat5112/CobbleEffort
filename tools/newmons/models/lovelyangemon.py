"""Lovely Angemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the idol warrior angel: a fighter in a pink-and-white armoured dress with gold trim and a gold
helm-visor, two huge golden twin-tails tied with violet ribbons swinging out like wings, pink-and-gold greaves, a
glowing pink energy burst in her raised fist, and long translucent ribbon streamers trailing behind. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built as officially drawn (armoured dress).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, cutout, fabric, gem, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an idol warrior angel in a pink-and-white armoured dress, a gold visor, huge golden twin-tails with violet ribbons and a glowing fist"
BASE = {"pink": (240, 140, 180), "pink_dark": (180, 60, 110), "pink_light": (255, 210, 230), "white": (250, 248, 250),
        "white_dark": (200, 196, 210), "gold": (240, 200, 70), "gold_dark": (170, 120, 20), "violet": (150, 90, 200),
        "skin": (250, 226, 212), "skin_dark": (210, 170, 150), "glow": (255, 160, 200), "glow_light": (255, 240, 250),
        "ribbon": (200, 230, 255, 170), "ribbon_light": (240, 250, 255, 200)}
SHINY = {"pink": (130, 200, 240), "pink_dark": (50, 120, 190), "gold": (220, 220, 236), "gold_dark": (130, 130, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = armour(P, "pink", "pink_dark", light="pink_light", trim="gold", trim_w=0.3)
WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.25)


def ribbonf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["ribbon_light"] if (u % 2.0) < 0.4 else p["ribbon"]
    return c, None


def build():
    m = Model("lovelyangemon")
    SK = skin(P, "skin", dark="skin_dark")
    mats = {"skin": WHITE, "chest": PINK, "abs": WHITE, "pelvis": PINK, "neck": SK, "deltoid": PINK, "upper_arm": WHITE,
            "forearm": PINK, "hand": PINK, "finger": PINK, "thigh": WHITE, "knee": armour(P, "gold", "gold_dark"),
            "shin": PINK, "calf": PINK, "foot": PINK, "toe": armour(P, "gold", "gold_dark")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.82, leg_bulk=0.86, name="lovelyangemon")
    bd = a["body"]
    for i in range(8):                                                               # armoured dress skirt
        ang = 2 * math.pi * i / 8
        spike(m, bd, (3.6 * math.cos(ang), 34.0, 3.0 * math.sin(ang)), (math.cos(ang) * 0.5, -1, math.sin(ang) * 0.5), 3.0,
              8.0, PINK if i % 2 else WHITE, tip=0.8)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.0, 60.0, SK, cut=1)
    m.round_box(hd, 0, -0.2, 2.6, 2.8, 57.0, 61.0, armour(P, "gold", "gold_dark"), cut=1)          # gold helm-visor
    m.round_box(hd, 0, -2.9, 2.2, 0.3, 56.8, 58.0, solid(P, "gold"), cut=0)
    for sx in (-1, 1):                                                               # huge golden twin-tails
        pts = [(sx * 2.4, 60.0, 1.0), (sx * 8.0, 64.0, 3.0), (sx * 14.0, 60.0, 4.0), (sx * 16.0, 50.0, 3.0), (sx * 14.0, 42.0, 2.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 3 - j // 2, strands(P, "gold", "gold_dark"), extend=0.6)
        m.round_box(hd, sx * 4.0, 2.0, 1.4, 1.4, 60.0, 62.6, solid(P, "violet"), cut=0)
    hr = a["arm_right"]                                                              # glowing fist
    hx, hy, hz = hr["hand"]
    ball(m, hr["bone"], (hx, hy - 1.0, hz - 1.0), 2.6, gem(P, "glow", "glow_light"), layers=3)
    for side in (1, -1):                                                             # ribbon streamers
        x0, x1 = sorted((side * 2.0, side * 14.0))
        m.box(bd, x0, 10.0, 4.0, x1, 34.0, 4.0, ribbonf, rotation=(0, side * -20, side * 15), pivot=(side * 2.0, 34.0, 4.0))
    return m
