"""Daipenmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the ice-pop penguin. A plump violet penguin with a white belly, a yellow beak and feet, half-closed
sleepy eyes, a little propeller cap, and a giant translucent blue ice-pop paddle held in one flipper and a pink one in
the other. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import local, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a plump violet penguin with a white belly, a yellow beak, sleepy eyes, a little propeller cap and giant "
        "translucent blue and pink ice-pop paddles")
BASE = {"violet": (80, 60, 150), "violet_dark": (36, 24, 80), "violet_light": (150, 130, 210), "white": (250, 250, 252),
        "yellow": (250, 210, 50), "yellow_dark": (200, 150, 20), "eye": (24, 24, 30), "lid": (60, 44, 120),
        "ice": (170, 210, 250, 170), "ice_light": (240, 250, 255, 200), "pink": (250, 160, 190, 170),
        "pink_light": (255, 230, 240, 200), "stick": (230, 210, 170), "grey": (150, 152, 164)}
SHINY = {"violet": (40, 130, 120), "violet_dark": (14, 70, 60), "violet_light": (120, 210, 190)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 3.0) < 1.4 and 27.4 < y < 28.4:
                return tone(p["lid"] if y > 27.9 else p["eye"], face), None
        if y < 24.0 and abs(x) < 7.0 - max(0.0, (y - 16.0) * 0.4):
            return tone(p["white"], face), None
    return skin(P, "violet", dark="violet_dark", light="violet_light", var=0.03)(x, y, z, face, variant, box=box, **k)


def popf(key, light):
    def s(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        u, v, W, H = local(x, y, z, face, box)
        c = p[light] if (u / max(W, 1e-6)) < 0.25 else p[key]
        return c, None
    return s


def build():
    m = Model("daipenmon")
    top = m.bone("daipenmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 4, 0))
    ball(m, bd, (0, 18.0, 0), 10.0, bodyf, layers=8, squash=1.0)
    m.round_box(bd, 0, 0, 7.0, 6.0, 26.0, 32.0, bodyf, cut=2)                          # head bulge
    m.box(bd, -2.0, 24.0, -9.6, 2.0, 26.0, -6.0, solid(P, "yellow"))                   # beak
    hd = m.bone("head", bd, (0, 32, 0))                                                # propeller cap
    m.round_box(hd, 0, 0, 2.4, 2.4, 31.6, 33.4, solid(P, "grey"), cut=1)
    rod(m, hd, (0, 33.4, 0), (0, 35.0, 0), 1, solid(P, "grey"), extend=0)
    sp = m.bone("spin_prop", hd, (0, 35, 0))
    m.box(sp, -3.0, 35.0, -0.4, 3.0, 35.6, 0.4, solid(P, "yellow"))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 4.0, 4.0, 0))
        m.box(lg, sx * 4.0 - 2.6, 0.0, -4.4, sx * 4.0 + 2.6, 4.6, 1.6, solid(P, "yellow_dark"))
    for sx, nm, key, light in ((1, "arm_right", "pink", "pink_light"), (-1, "arm_left", "ice", "ice_light")):
        ab = m.bone(nm, bd, (sx * 9.0, 18.0, 0))
        m.box(ab, min(sx * 8.0, sx * 13.0), 12.0, -1.6, max(sx * 8.0, sx * 13.0), 20.0, 1.6,
              skin(P, "violet", dark="violet_dark"), rotation=(0, 0, sx * 20), pivot=(sx * 9.0, 18.0, 0))
        rod(m, ab, (sx * 13.0, 14.0, -2.0), (sx * 15.0, 20.0, -2.0), 1, solid(P, "stick"), extend=0)
        m.box(ab, min(sx * 12.0, sx * 24.0), 20.0, -3.0, max(sx * 12.0, sx * 24.0), 38.0, -1.0, popf(key, light),
              rotation=(0, 0, -sx * 15), pivot=(sx * 15.0, 20.0, -2.0))                # the ice-pop paddle
    return m
