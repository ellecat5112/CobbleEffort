"""Surfimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the surfing cyborg: a lean blue-armoured dragon-warrior striped white-and-blue with a horned crest of
gold fins, red claws and a red spine, riding a sleek violet jet-surfboard with orange fins and a blazing booster.
35 blocks.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a lean blue-armoured dragon-warrior with a gold-finned crest and red claws riding a sleek violet jet-surfboard with a blazing booster"
BASE = {"blue": (40, 90, 200), "blue_dark": (14, 34, 110), "white": (240, 244, 252), "gold": (240, 200, 70),
        "red": (210, 40, 40), "violet": (120, 110, 200), "violet_dark": (60, 50, 130), "orange": (250, 140, 40),
        "jet": (255, 200, 90, 210), "eye": (250, 220, 60)}
SHINY = {"blue": (200, 60, 80), "blue_dark": (110, 20, 30)}


def P(v):
    return pal(BASE, SHINY, v)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs(math.sin(y * 0.8 + abs(x) * 0.4)) > 0.85:
        return tone(p["white"], face), None
    return armour(P, "blue", "blue_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("surfimon")
    top = m.bone("surfimon", None, (0, 0, 0))
    sb = m.bone("board", top, (0, 2, 0))
    m.round_box(sb, 0, 0, 5.0, 16.0, 1.0, 3.0, armour(P, "violet", "violet_dark"), cut=2)     # jet-surfboard
    spike(m, sb, (0, 2.0, -16.0), (0, 0.1, -1), 3.0, 5.0, armour(P, "violet", "violet_dark"), tip=0.8)
    for sx in (-1, 1):
        spike(m, sb, (sx * 4.0, 2.0, 12.0), (sx * 0.6, 0.6, 0.6), 1.2, 4.0, solid(P, "orange"), tip=0.8)
    spike(m, sb, (0, 2.0, 16.0), (0, 0, 1), 2.4, 7.0, solid(P, "jet", glow=True), tip=0.8)
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats = {"skin": stripef, "claw": solid(P, "red"), "talon": solid(P, "red")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="rider")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.6, 3.6, 54.0, 60.0, stripef, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.5, sx * 2.7), 57.4, -3.8, max(sx * 2.5, sx * 2.7), 58.2, -2.4, solid(P, "eye", glow=True))
    for j in range(6):                                                                   # gold-finned crest
        ang = math.radians(-60 + j * 24)
        spike(m, hd, (2.4 * math.sin(ang), 60.0, 0), (math.sin(ang) * 0.6, 1, 0.5), 1.2, 6.0, solid(P, "gold"), tip=0.8)
    for j in range(6):
        spike(m, bd, (0, 52.0 - j * 3.6, 4.0), (0, 0.4, 1), 1.0, 3.0, solid(P, "red"), tip=0.8)
    mount(m, i_box, i_bone, 3.0, 0.0, top)
    return m
