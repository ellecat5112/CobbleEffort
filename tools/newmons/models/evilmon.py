"""Evilmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
little devil. A squat, grey-green imp with a huge head that is mostly gaping fanged mouth and long red tongue, bulging
orange eyes, a wild crest of red-orange hair, shaggy white fur on its shoulders, long arms with yellow hooked claws, a
leather wristband, stubby clawed legs and two big ragged bat wings. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digidetail import cutout, fur, leather, local, noise2, skin, solid, strands
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a squat grey-green imp with a huge gaping fanged mouth and red tongue, bulging orange eyes, a red-orange hair "
        "crest, white shoulder fur, yellow hooked claws and ragged bat wings")
BASE = {"hide": (90, 110, 110), "hide_dark": (40, 54, 56), "hide_light": (150, 170, 170), "fur": (240, 240, 236),
        "fur_dark": (180, 180, 176), "hair": (230, 80, 40), "hair_dark": (150, 30, 20), "mouth": (130, 20, 30),
        "tongue": (220, 50, 60), "tooth": (250, 248, 240), "eye": (250, 160, 60), "pupil": (20, 20, 20),
        "claw": (240, 200, 90), "strap": (90, 60, 40), "strap_dark": (40, 26, 16), "wing": (110, 130, 130)}
SHINY = {"hide": (130, 90, 140), "hide_dark": (60, 30, 70), "hide_light": (190, 150, 200), "wing": (150, 110, 160)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "hide", dark="hide_dark", light="hide_light", var=0.07)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        if 18.0 < y < 28.0 and abs(x) < 6.0 - (y - 23.0) ** 2 * 0.15:
            fang = abs((x * 0.6) % 2.0 - 1.0) * 2.4
            if y > 26.0 - fang or y < 20.0 + fang:
                return tone(p["tooth"], face), None
            if abs(x) < 1.8 and y < 23.0:
                return tone(p["tongue"], face), None
            return tone(p["mouth"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    return tone(P(variant)["wing"], face), None


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return noise2(u * 0.6, v * 0.6, 51) < 0.82


def build():
    m = Model("evilmon")
    top = m.bone("evilmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 1.0, 5.0, 4.4, 8.0, 18.0, HIDE, cut=2)
    hd = m.bone("head", bd, (0, 18, -2))
    m.round_box(hd, 0, -1.0, 7.0, 6.0, 17.0, 31.0, headf, cut=2)                     # huge head, mostly mouth
    m.box(hd, -1.6, 15.0, -7.6, 1.6, 20.0, -6.8, solid(P, "tongue"), rotation=(-20, 0, 0), pivot=(0, 20.0, -7.2))
    for sx in (-1, 1):                                                               # bulging orange eyes
        m.round_box(hd, sx * 3.6, -6.0, 2.0, 1.4, 28.0, 32.0, solid(P, "eye"), cut=1)
        m.box(hd, sx * 3.6 - 0.6, 29.4, -7.6, sx * 3.6 + 0.6, 30.6, -7.2, solid(P, "pupil"))
        m.round_box(bd, sx * 5.4, 0, 3.0, 3.0, 15.0, 19.0, fur(P, "fur", "fur_dark", length=1.4), cut=1)
    for i in range(9):                                                               # wild hair crest
        ang = math.radians(-60 + i * 15)
        spike(m, hd, (3.0 * math.sin(ang), 31.0, 0.0), (math.sin(ang), 1, 0.3), 1.6, 5.0 + (i % 3),
              strands(P, "hair", "hair_dark"), tip=0.4)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                             # long arms, yellow claws
        ab = m.bone(nm, bd, (sx * 6.0, 16.0, 0))
        rod(m, ab, (sx * 6.0, 16.0, 0), (sx * 12.0, 10.0, -3.0), 2, HIDE, extend=0.5)
        rod(m, ab, (sx * 12.0, 10.0, -3.0), (sx * 14.0, 4.0, -5.0), 2, HIDE, extend=0.5)
        m.round_box(ab, sx * 12.0, -3.0, 1.6, 1.6, 9.0, 11.0, leather(P, "strap", "strap_dark"), cut=1)
        for j in range(4):
            spike(m, ab, (sx * 14.0 + (j - 1.5) * 0.9, 4.0, -5.0), (0, -1, -0.6), 0.8, 4.0, solid(P, "claw"), tip=0.2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 3.0, 8.0, 0))
        rod(m, lg, (sx * 3.0, 9.0, 0), (sx * 4.0, 2.0, -1.0), 3, HIDE, extend=0.5)
        for j in range(3):
            spike(m, lg, (sx * 4.0 + (j - 1) * 1.2, 1.0, -2.0), (0, -0.3, -1), 1.0, 3.0, solid(P, "claw"), tip=0.25)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 17.0, 4.0))
        bat_wing(m, wb, (side * 3.0, 17.0, 4.0), 18.0, 16.0, 3, HIDE, cutout(tatter, wingf), side=side, sweep=25)
    return m
