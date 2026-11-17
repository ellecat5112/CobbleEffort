"""Ballistamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a beetle-robot bruiser. A boxy blue armoured body with red panels and gold bolts, a speaker-grille
face and a tall two-pronged horn, grey piston arms ending in huge red fists with round gauntlets, and stubby blue
legs with wide feet. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage. make("mc"): Ballistamon MC (a walking fortress: a round armoured
dome with towers, cannons and windows, 35 blocks); make("sr"): Ballistamon SR (a war-machine form with a drill arm and
twin cannons on its back, 25 blocks).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a beetle-robot bruiser: a boxy blue body with red panels and gold bolts, a grille face, a two-pronged horn, "
        "grey piston arms with huge red fists and stubby legs")
BASE = {"blue": (40, 60, 170), "blue_dark": (16, 24, 90), "blue_light": (110, 140, 240), "red": (210, 30, 40),
        "red_dark": (120, 10, 20), "red_light": (250, 120, 120), "grey": (170, 174, 186), "grey_dark": (80, 84, 96),
        "gold": (240, 200, 60), "black": (30, 30, 36), "window": (120, 200, 250), "eye": (255, 220, 60)}
SHINY = {"blue": (40, 140, 80), "blue_dark": (16, 70, 40), "blue_light": (120, 220, 150), "red": (240, 170, 40),
         "red_dark": (170, 100, 20), "red_light": (255, 220, 140)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="red", trim_w=0.4)
BLUE_PLAIN = armour(P, "blue", "blue_dark", light="blue_light")
RED = armour(P, "red", "red_dark", light="red_light")
GREY = riveted(P, "grey", "grey_dark")
STEEL = metal(P, "grey", dark="grey_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        u, v, W, H = local(x, y, z, face, box)
        if v < H * 0.45 and (u % 1.2) < 0.4:
            return tone(p["black"], face), None                  # grille slots
        if abs(v - H * 0.7) < 0.4 and abs(u - W / 2) < W * 0.3:
            return p["eye"], p["eye"]
    return GREY(x, y, z, face, variant, box=box, **k)


def fist(m, bone, c, s):
    m.round_box(bone, c[0], c[2], 3.6 * s, 3.4 * s, c[1] - 3.0 * s, c[1] + 3.0 * s, RED, cut=1)
    for f in range(4):
        m.box(bone, c[0] - 3.8 * s, c[1] - 2.6 * s + f * 1.4 * s, c[2] - 3.8 * s, c[0] + 3.8 * s,
              c[1] - 1.8 * s + f * 1.4 * s, c[2] - 3.2 * s, RED)
    m.round_box(bone, c[0], c[2] + 3.4 * s, 3.0 * s, 1.2 * s, c[1] - 3.0 * s, c[1] + 3.0 * s, STEEL, cut=1)


def make(name, variant=None):
    def build():
        m = Model(name)
        top = m.bone(name, None, (0, 0, 0))
        bd = m.bone("body", top, (0, 14, 0))
        if variant == "mc":                                      # the walking fortress
            ball(m, bd, (0, 24.0, 0), 18.0, BLUE_PLAIN, layers=8, squash=0.9)
            m.box(bd, -12.0, 18.0, -17.0, 12.0, 26.0, -14.0, facef)                       # the great grille face
            for sx in (-1, 1):
                for j in range(3):                               # windows
                    m.box(bd, sx * (6.0 + j * 3.0) - 1.0, 30.0, -16.0 + j * 2.0, sx * (6.0 + j * 3.0) + 1.0,
                          33.0, -15.4 + j * 2.0, solid(P, "window", glow=True))
                m.round_box(bd, sx * 10.0, 4.0, 4.0, 4.0, 36.0, 46.0, GREY, cut=1)        # towers
                m.round_box(bd, sx * 10.0, 4.0, 4.6, 4.6, 46.0, 48.0, RED, cut=1)
                rod(m, bd, (sx * 6.0, 40.0, -6.0), (sx * 8.0, 44.0, -18.0), 3, STEEL, extend=0)   # cannons
            for sx in (-1, 1):
                rod(m, bd, (sx * 4.0, 42.0, 0.0), (sx * 6.0, 52.0, 2.0), 3, BLUE_PLAIN, extend=0.3)   # horn prongs
            for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
                lg = m.bone(nm, top, (sx * 8.0, 8.0, 0))
                m.round_box(lg, sx * 9.0, 0, 5.0, 6.0, 0.0, 9.0, BLUE_PLAIN, cut=1)
            return m
        s = 1.25 if variant == "sr" else 1.0
        m.box(bd, -7.0 * s, 16.0, -5.0 * s, 7.0 * s, 32.0, 5.0 * s, BLUE)                 # boxy torso
        m.box(bd, -4.0 * s, 20.0, -5.6 * s, 4.0 * s, 27.0, -4.8 * s, RED)                 # red chest panel
        m.box(bd, -1.4, 22.4, -6.2 * s, 1.4, 25.0, -5.4 * s, solid(P, "gold"))
        for sx in (-1, 1):
            m.box(bd, sx * 7.0 * s - 1.0, 28.0, -2.0, sx * 7.0 * s + 1.0, 30.0, 2.0, solid(P, "gold"))
        m.box(bd, -5.0 * s, 12.0, -4.0 * s, 5.0 * s, 16.4, 4.0 * s, BLUE_PLAIN)           # hips
        hd = m.bone("head", bd, (0, 32, 0))
        m.box(hd, -4.0, 32.0, -4.0, 4.0, 38.0, 3.0, facef)
        for sx in (-1, 1):                                       # the two-pronged horn
            rod(m, hd, (sx * 1.6, 37.0, -0.5), (sx * 2.4, 48.0, 0.0), 3, BLUE_PLAIN, extend=0.3)
            spike(m, hd, (sx * 2.4, 48.0, 0.0), (sx * 0.4, 1, 0), 1.6, 2.0, solid(P, "gold"))
        for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
            ab = m.bone(nm, bd, (sx * 8.0 * s, 29.0, 0))
            ball(m, ab, (sx * 8.6 * s, 29.0, 0), 3.0 * s, RED, layers=3)
            el = (sx * 13.0 * s, 24.0, -1.0)
            rod(m, ab, (sx * 9.0 * s, 28.0, 0), el, 2, STEEL, extend=0.4)
            rod(m, ab, el, (sx * 17.0 * s, 20.0, -4.0), 2, STEEL, extend=0.4)
            if variant == "sr" and sx < 0:                       # SR: drill arm
                for j in range(4):
                    c = (sx * 18.0 * s, 20.0, -6.0 - j * 3.0)
                    r = 4.0 - j * 0.9
                    m.box(ab, c[0] - r, c[1] - r, c[2] - 3.0, c[0] + r, c[1] + r, c[2], GREY,
                          rotation=(0, 0, 45 * (j % 2)), pivot=c)
            else:
                fist(m, ab, (sx * 18.0 * s, 20.0, -5.0), s)
        if variant == "sr":                                      # twin cannons on its back
            for sx in (-1, 1):
                rod(m, bd, (sx * 4.0, 30.0, 5.0), (sx * 6.0, 46.0, 10.0), 4, STEEL, extend=0)
        for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
            lg = m.bone(nm, top, (sx * 3.6 * s, 12.0, 0))
            m.box(lg, sx * 3.8 * s - 2.4, 4.0, -2.6, sx * 3.8 * s + 2.4, 12.0, 2.6, BLUE_PLAIN)
            m.box(lg, sx * 3.8 * s - 3.4, 0.0, -6.0, sx * 3.8 * s + 3.4, 4.0, 3.0, BLUE)
        return m
    return build


build = make("ballistamon")
