"""King Chessmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the chess king: a small round puppet knight in a white enamel body with a gold collar and belt buckle, a visored
silver helm under a tall golden crown, a black handlebar moustache, a long violet-lined black cape, white gloves and
pointed boots, and a golden sceptre with a faceted head. 35 blocks tall.

Front is -z, y is up. 40 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape
from _digidetail import armour, fabric, gem, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a small round chess-king puppet in white enamel with a visored helm, a tall golden crown, a moustache, a black cape and a golden sceptre"
BASE = {"white": (246, 246, 250), "white_dark": (170, 172, 190), "gold": (250, 200, 60), "gold_dark": (170, 120, 20),
        "gold_light": (255, 240, 170), "silver": (210, 214, 224), "silver_dark": (90, 94, 106), "black": (30, 28, 34),
        "violet": (90, 50, 160), "red": (210, 40, 40)}
SHINY = {"white": (40, 40, 48), "white_dark": (12, 12, 18), "violet": (200, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="gold", trim_w=0.25)
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "south":
        return fabric(P, "black", "black")(x, y, z, face, variant, box=box, **k)
    return fabric(P, "violet", "black")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("kingchessmon")
    top = m.bone("kingchessmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 8, 0))
    m.round_box(bd, 0, 0, 5.6, 4.6, 8.0, 20.0, WHITE, cut=2)
    m.round_box(bd, 0, 0, 5.8, 4.8, 11.0, 12.6, GOLD, cut=2)                                # belt
    m.round_box(bd, 0, -4.8, 1.2, 0.4, 10.6, 13.0, GOLD, cut=0)
    m.round_box(bd, 0, 0, 4.0, 3.6, 19.4, 21.0, GOLD, cut=1)                                # collar
    cape(m, bd, 20.0, 12.0, 18.0, capef, z=3.6, flare=0.8, panels=6)
    hd = m.bone("head", bd, (0, 21, 0))
    m.round_box(hd, 0, 0, 3.4, 3.4, 21.0, 27.4, metal(P, "silver", dark="silver_dark"), cut=1)   # visored helm
    for j in range(4):
        m.box(hd, -2.4, 23.0 + j * 0.9, -3.5, 2.4, 23.4 + j * 0.9, -3.3, solid(P, "black"))
    for sx in (-1, 1):                                                               # handlebar moustache
        rod(m, hd, (0, 22.4, -3.6), (sx * 3.6, 23.0, -3.4), 1, solid(P, "black"), extend=0.2, t2=1)
    m.round_box(hd, 0, 0, 3.6, 3.6, 27.0, 29.0, GOLD, cut=1)                                # crown band
    m.round_box(hd, 0, -3.7, 1.8, 0.3, 27.4, 28.6, solid(P, "red"), cut=0)
    for i in range(8):                                                               # crown points
        ang = 2 * math.pi * i / 8
        spike(m, hd, (3.0 * math.cos(ang), 28.6, 3.0 * math.sin(ang)), (math.cos(ang) * 0.1, 1, math.sin(ang) * 0.1), 1.2,
              4.4, GOLD, tip=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.6, 18.0, 0))
        rod(m, ab, (sx * 5.6, 18.0, 0), (sx * 7.6, 13.0, -2.0), 2, WHITE, extend=0.4)
        m.round_box(ab, sx * 8.0, -2.4, 1.8, 1.8, 10.6, 13.6, solid(P, "white"), cut=1)
    rod(m, "arm_left", (8.0, 2.0, -2.4), (8.0, 30.0, -2.4), 1, GOLD, extend=0, t2=1)           # sceptre
    m.round_box("arm_left", 8.0, -2.4, 2.0, 2.0, 30.0, 35.0, gem(P, "gold", "gold_light", glow=False), cut=1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.6, 8.0, 0))
        rod(m, lg, (sx * 2.6, 8.4, 0), (sx * 2.8, 2.0, 0), 2, WHITE, extend=0.4)
        m.round_box(lg, sx * 2.8, -2.0, 2.0, 3.4, 0.0, 2.4, solid(P, "white"), cut=1)
        spike(m, lg, (sx * 2.8, 1.0, -5.0), (0, 0.6, -1), 1.2, 2.4, solid(P, "white"), tip=0.8)
    return m
