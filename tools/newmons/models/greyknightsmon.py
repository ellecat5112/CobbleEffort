"""Grey Knightsmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the dark knight dragon-rider: a black-and-gold armoured knight with a long black plume
and tattered black wings, riding low over a violet armoured dragon beast with a fanged maw, wielding a great silver
lance-drill and a round red-and-black shield, golden claws on the dragon's feet. 35 blocks tall.

Front is -z, y is up. 48 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, quadruped
from _digidetail import armour, metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a black-and-gold armoured knight with a black plume and tattered black wings riding a violet armoured dragon, "
        "wielding a great silver lance-drill and a round shield")
BASE = {"black": (36, 34, 40), "black_dark": (12, 12, 16), "black_light": (100, 96, 110), "gold": (230, 190, 70),
        "gold_dark": (150, 110, 20), "violet": (110, 90, 170), "violet_dark": (50, 40, 100), "steel": (214, 218, 228),
        "steel_dark": (110, 114, 126), "red": (190, 30, 40), "mouth": (120, 20, 40), "tooth": (250, 250, 240),
        "eye": (240, 220, 60)}
SHINY = {"black": (220, 220, 230), "black_dark": (150, 150, 166), "black_light": (255, 255, 255), "violet": (170, 60, 60)}


def P(v):
    return pal(BASE, SHINY, v)


KNIGHT = armour(P, "black", "black_dark", light="black_light", trim="gold", trim_w=0.3)
DRAGON = armour(P, "violet", "violet_dark", trim="black", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        cx, cy = box.lo[0] + box.size[0] / 2, box.lo[1] + box.size[1] / 2
        r = math.hypot(x - cx, y - cy)
        if r < 1.4:
            return p["red"], p["red"]
        if r < 2.6:
            return tone(p["gold"], face), None
    return KNIGHT(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("greyknightsmon")
    mats = {"skin": DRAGON, "head": DRAGON, "snout": DRAGON, "jaw": DRAGON, "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "claw": metal(P, "gold", dark="gold_dark"), "tail": scales(P, "violet", "violet_dark")}
    a = quadruped(m, mats, "greyknightsmon", length=30.0, body_y=16.0, body_rx=6.0, body_ry=5.4, chest_bulk=1.3,
                  neck=((0, 20, -13), (0, 22, -18)), head_len=10.0, head_w=3.6, head_h=3.6, snout=0.8, mouth_open=20,
                  teeth=6, leg_bulk=1.3, toes=3, tail=((0, 18, 15), (0, 20, 22), (2, 21, 28)), tail_r=(2.4, 1.8, 1.2))
    bd = a["body"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(a["head"], min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
              ez + 0.6, solid(P, "eye", glow=True))
    rb = m.bone("rider", bd, (0, 22, 0))                                                # the knight
    m.round_box(rb, 0, 0, 4.4, 3.4, 21.0, 32.0, KNIGHT, cut=1)
    hd = m.bone("rider_head", rb, (0, 32, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 32.0, 38.0, KNIGHT, cut=1)
    m.box(hd, -1.8, 35.0, -3.5, 1.8, 35.6, -3.3, solid(P, "eye", glow=True))
    for j in range(5):                                                                    # long black plume
        spike(m, hd, (0, 37.6 - j * 0.4, -1.0 + j * 1.4), (0.2, 0.4, 1), 1.6, 10.0 - j, solid(P, "black"), tip=0.8)
    for side in (1, -1):                                                                  # tattered black wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", rb, (side * 3.0, 30.0, 3.0))
        bat_wing(m, wb, (side * 3.0, 30.0, 3.0), 20.0, 12.0, 4, KNIGHT, metal(P, "black", dark="black_dark"), side=side,
                 sweep=30)
    rod(m, rb, (-5.0, 26.0, 2.0), (-8.0, 30.0, -26.0), 3, STEEL, extend=0)             # lance-drill
    spike(m, rb, (-8.0, 30.0, -26.0), (-0.1, 0.15, -1), 3.0, 8.0, STEEL, tip=1.0)
    m.round_box(rb, -6.0, -2.0, 1.6, 3.0, 24.0, 30.0, metal(P, "red", dark="black_dark"), cut=1)
    m.round_box(rb, 6.6, -3.0, 3.4, 0.8, 22.0, 30.0, shieldf, cut=0)                     # round shield
    return m
