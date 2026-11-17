"""Cho·Hakkaimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the pig warrior of the Journey to the West quartet. A pilot in a rounded pink pig-shaped mech
suit with big pig ears and a snout, a glass porthole showing the green-haired pilot inside, stickers on its plating,
and a huge spiked steel rake-hammer on a long black chain-shaft. Its official design is kept as drawn. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a pilot in a rounded pink pig-shaped mech suit with big ears and a snout, a glass porthole, stickers and a "
        "huge spiked steel rake-hammer")
BASE = {"pink": (240, 150, 190), "pink_dark": (190, 90, 140), "pink_light": (255, 210, 230), "steel": (140, 146, 170),
        "steel_dark": (60, 64, 86), "steel_light": (210, 214, 230), "glass": (160, 210, 220), "glass_light": (240, 250, 255),
        "hair": (60, 160, 120), "skin": (246, 226, 214), "sticker": (230, 220, 150), "black": (34, 34, 42),
        "snout": (250, 180, 210)}
SHINY = {"pink": (170, 210, 240), "pink_dark": (100, 150, 200), "pink_light": (230, 245, 255)}


def P(v):
    return pal(BASE, SHINY, v)


PINK = armour(P, "pink", "pink_dark", light="pink_light", rivets=True)
STEEL = metal(P, "steel", dark="steel_dark", light="steel_light")


def stickered(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and (abs((x + z) % 9.0 - 4.5) < 1.0) and (abs(y % 11.0 - 5.5) < 1.4):
        return tone(p["sticker"], face), None
    return PINK(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("chohakkaimon")
    top = m.bone("chohakkaimon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 22, 0))
    ball(m, bd, (0, 36.0, 0), 11.0, stickered, layers=7)                         # the round pig mech body
    m.round_box(bd, 0, -9.0, 4.0, 3.0, 34.0, 40.0, gem(P, "glass", "glass_light", glow=False), cut=1)  # porthole
    m.round_box(bd, 0, -8.6, 2.4, 1.6, 35.0, 39.0, skin(P, "skin"), cut=1)       # the pilot's face
    m.box(bd, -2.6, 38.4, -9.4, 2.6, 40.0, -7.4, solid(P, "hair"))
    hd = m.bone("head", bd, (0, 46, 0))
    m.round_box(hd, 0, -3.0, 6.0, 5.0, 44.0, 52.0, PINK, cut=2)                   # pig head
    m.round_box(hd, 0, -8.6, 2.4, 1.4, 45.0, 48.6, solid(P, "snout"), cut=1)      # snout
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.4, 46.2, -10.1, sx * 1.0 + 0.4, 47.4, -9.9, solid(P, "black"))
        spike(m, hd, (sx * 4.4, 51.0, -2.0), (sx * 0.5, 1, -0.3), 3.6, 5.0, PINK, tip=0.8)   # big pig ears
        m.box(hd, sx * 3.0 - 0.6, 49.0, -8.1, sx * 3.0 + 0.6, 50.0, -7.9, solid(P, "black"))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 10.0, 38.0, 0))
        rod(m, ab, (sx * 10.0, 38.0, 0), (sx * 13.0, 30.0, -3.0), 5, PINK, extend=0.6)
        m.round_box(ab, sx * 13.4, -3.4, 3.0, 3.0, 25.0, 30.0, PINK, cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 5.0, 26.0, 0))
        rod(m, lg, (sx * 5.0, 27.0, 0), (sx * 5.6, 6.0, 0), 5, PINK, extend=0.6)
        m.round_box(lg, sx * 5.8, -1.6, 3.4, 4.6, 0.0, 6.0, STEEL, cut=1)
    rb = m.bone("rake", "arm_right", (-13.4, 27.0, -3.4))                       # spiked rake-hammer
    rod(m, rb, (-13.4, 27.0, 4.0), (-14.0, 34.0, -26.0), 1, solid(P, "black"), extend=0)
    hh = (-14.0, 34.0, -28.0)
    m.box(rb, hh[0] - 4.0, hh[1] - 8.0, hh[2] - 3.0, hh[0] + 4.0, hh[1] + 8.0, hh[2] + 3.0, STEEL)
    for j in range(4):
        spike(m, rb, (hh[0], hh[1] - 6.0 + j * 4.0, hh[2] - 3.0), (0, 0, -1), 2.2, 5.0, STEEL, tip=0.5)
    return m
