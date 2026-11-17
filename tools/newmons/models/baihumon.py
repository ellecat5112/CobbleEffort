"""Baihumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the White Tiger of the West, one of the Four Holy Beasts. A white tiger with violet stripes, steel
blade spines along its back and shoulders, violet armour on its forelegs marked with the kanji 虎, spiked black
collars on its legs and tail, steel claws and a ring of floating golden orbs at its back. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import armour, fur, gem, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("the White Tiger holy beast: white fur with violet stripes, steel blade spines, violet foreleg armour, spiked "
        "collars, steel claws and a ring of floating golden orbs")
BASE = {"white": (246, 246, 250), "white_dark": (190, 190, 206), "stripe": (130, 100, 190), "violet": (110, 80, 180),
        "violet_dark": (60, 40, 120), "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "black": (34, 34, 40),
        "gold": (240, 200, 60), "gold_light": (255, 240, 170), "mouth": (110, 20, 30), "tooth": (250, 250, 246),
        "tongue": (210, 80, 90), "eye": (255, 200, 40)}
SHINY = {"white": (240, 220, 160), "white_dark": (190, 160, 100), "stripe": (60, 40, 30), "violet": (40, 100, 70),
         "violet_dark": (16, 60, 40)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.4)
STEEL = metal(P, "steel", dark="steel_dark")
VIOLET = armour(P, "violet", "violet_dark", trim="steel")


def tigerf(x, y, z, face, variant, box=None, **k):
    """White fur with violet tiger stripes running round the body."""
    p = P(variant)
    t = (z * 0.5 + abs(x) * 0.25 + y * 0.12) % 3.0
    if t < 0.55 and face not in ("down",):
        return tone(p["stripe"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("baihumon")
    mats = {"skin": tigerf, "belly": FUR, "neck": tigerf, "head": tigerf, "snout": FUR, "jaw": FUR,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": VIOLET, "leg_lower": tigerf,
            "paw": FUR, "claw": STEEL, "tail": tigerf}
    a = quadruped(m, mats, "baihumon", length=30.0, body_y=17.0, body_rx=7.0, body_ry=7.0, chest_bulk=1.3,
                  neck=((0, 22, -15), (0, 25, -18)), head_len=10.0, head_w=4.8, head_h=5.0, snout=0.35,
                  mouth_open=18, teeth=4, leg_bulk=1.6, toes=3,
                  tail=((0, 22, 18), (0, 26, 24), (2, 30, 28)), tail_r=(1.8, 1.4, 1.2))
    bd = a["body"]
    for i in range(6):                                           # steel blade spines down the back
        z = -12.0 + i * 4.0
        spike(m, bd, (0, 24.0, z), (0, 1, 0.5), 1.4, 5.0 - i * 0.4, STEEL)
    for sx in (-1, 1):
        for j in range(3):
            spike(m, bd, (sx * 6.0, 22.0, -10.0 + j * 2.0), (sx, 0.8, 0.4), 1.4, 5.0, STEEL, tip=0.5)
    hd = a["head"]
    for sx in (-1, 1):
        m.box(hd, sx * 2.0 - 0.6, 27.0, -22.4, sx * 2.0 + 0.6, 27.8, -22.2, solid(P, "eye", glow=True))
        m.box(hd, min(sx * 4.6, sx * 5.4), 20.0, -22.0, max(sx * 4.6, sx * 5.4), 26.0, -18.0, STEEL)   # face guards
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):   # spiked collars
        lg = a[nm]
        w = lg["wrist"]
        m.round_box(lg["bone"], w[0], w[2], 2.6, 2.6, 5.0, 7.0, solid(P, "black"), cut=1)
        for j in range(4):
            ang = math.radians(j * 90 + 45)
            spike(m, lg["bone"], (w[0] + 2.6 * math.cos(ang), 6.0, w[2] + 2.6 * math.sin(ang)),
                  (math.cos(ang), 0, math.sin(ang)), 0.8, 1.6, STEEL)
    ring = m.bone("ring_orbs", bd, (0, 28, 4))                   # floating golden orbs
    for i in range(9):
        ang = math.radians(i * 40)
        ball(m, ring, (9.0 * math.cos(ang), 28.0 + 9.0 * math.sin(ang), 6.0), 1.6, gem(P, "gold", "gold_light"),
             layers=2)
    return m
