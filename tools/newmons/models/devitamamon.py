"""Devitamamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the egg of darkness. A great cracked black eggshell from which bursts a lumpy brown fleshy demon:
a wide jagged maw of white fangs splitting the shell, a crest of yellow eyes running up its face, a black horn, bat
wings, gangly clawed arms and crouching clawed legs. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digidetail import cutout, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a great cracked black eggshell bursting with a lumpy brown fleshy demon: a jagged fanged maw, a crest of yellow "
        "eyes, a black horn, bat wings and gangly clawed limbs")
BASE = {"shell": (60, 60, 68), "shell_dark": (16, 16, 20), "shell_light": (150, 150, 164), "flesh": (140, 80, 50),
        "flesh_dark": (70, 34, 20), "flesh_light": (200, 140, 100), "eye": (250, 220, 60), "pupil": (40, 20, 10),
        "tooth": (250, 248, 240), "mouth": (40, 10, 10), "claw": (200, 160, 130)}
SHINY = {"shell": (220, 220, 230), "shell_dark": (150, 150, 160), "flesh": (120, 60, 120), "flesh_dark": (60, 20, 60)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = metal(P, "shell", dark="shell_dark", light="shell_light", streak=4.0)
FLESH = skin(P, "flesh", dark="flesh_dark", light="flesh_light", var=0.08)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 12.0 < y < 24.0:
        mx = abs(x)
        top = 21.0 - abs((x * 0.6) % 2.0 - 1.0) * 2.6                 # jagged upper teeth line
        bot = 15.0 + abs((x * 0.6 + 1.0) % 2.0 - 1.0) * 2.6
        if mx < 7.0:
            if bot - 1.6 < y < top + 1.6 and (y > top or y < bot):
                return tone(p["tooth"], face), None
            if bot <= y <= top:
                return tone(p["mouth"], face), None
    return SHELL(x, y, z, face, variant, box=box, **k)


def eyef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face == "north":
        r = math.hypot(u - W / 2, v - H / 2)
        if r < 0.3:
            return tone(p["pupil"], face), None
        if r < 0.65:
            return p["eye"], None
    return FLESH(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["flesh_dark"], face), None


def build():
    m = Model("devitamamon")
    top = m.bone("devitamamon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    ball(m, bd, (0, 20.0, 0), 10.0, shellf, layers=8, squash=0.9, ry=12.0)            # the black egg
    for i in range(7):                                                                 # crest of eyes
        t = i / 6
        y = 22.0 + 12.0 * t
        z = -9.0 + 7.0 * t * t
        m.round_box(bd, 0, z + 1.6, 2.6 - t, 2.4, y - 1.4, y + 1.6, FLESH, cut=1)
        m.box(bd, -0.7, y - 0.5, z - 0.9, 0.7, y + 0.9, z - 0.7, eyef)
    spike(m, bd, (0, 33.0, 0), (0, 1, 0.5), 3.0, 8.0, SHELL, tip=1.0)                  # black horn
    hd = m.bone("head", bd, (0, 32, -4))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                               # gangly arms
        ab = m.bone(nm, bd, (sx * 9.0, 24.0, 0))
        pts = [(sx * 9.0, 24.0, 0), (sx * 16.0, 20.0, -2.0), (sx * 17.0, 10.0, -5.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab, p0, p1, 3, FLESH, extend=0.6)
        for j in range(4):
            spike(m, ab, (sx * 17.0 + (j - 1.5) * 1.2, 9.0, -5.0), (0, -1, -0.4), 1.0, 4.0, solid(P, "claw"), tip=0.25)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                               # crouching legs
        lg = m.bone(nm, top, (sx * 6.0, 12.0, 2.0))
        pts = [(sx * 6.0, 12.0, 2.0), (sx * 12.0, 8.0, -2.0), (sx * 12.0, 1.0, 0.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, lg, p0, p1, 4, FLESH, extend=0.6)
        for j in range(4):
            spike(m, lg, (sx * 12.0 + (j - 1.5) * 1.4, 0.8, -1.0), (0, -0.2, -1), 1.0, 4.0, solid(P, "claw"), tip=0.25)
    for side in (1, -1):                                                              # bat wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 6.0, 28.0, 5.0))
        bat_wing(m, wb, (side * 6.0, 28.0, 5.0), 16.0, 14.0, 3, FLESH, cutout(lambda *a: True, wingf), side=side,
                 sweep=25)
    return m
