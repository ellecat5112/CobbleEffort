"""Crossmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the golden cyborg bird. A hunched bird-machine in segmented golden armour with a helmeted head and a
pointed crest, a great golden wing of layered blades, two long arms ending in black hooked pincer claws, and thick
golden legs with black talons. 35 blocks tall.

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a hunched golden cyborg bird in segmented armour with a helmeted head, a great wing of golden blades, black "
        "hooked pincer claws and black talons")
BASE = {"gold": (230, 196, 80), "gold_dark": (160, 120, 30), "gold_light": (255, 240, 170), "black": (40, 40, 46),
        "black_light": (110, 110, 124), "eye": (220, 40, 40), "grey": (150, 152, 164)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (110, 120, 150), "gold_light": (255, 255, 255)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", seams=(10.0, 18.0, 26.0, 34.0))
CLAW = metal(P, "black", dark="black", light="black_light")


def build():
    m = Model("crossmon")
    top = m.bone("crossmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 18, 0))
    for i, (r, y0, y1, cz) in enumerate(((6.0, 16.0, 22.0, 0.0), (7.0, 22.0, 30.0, -1.0), (6.4, 30.0, 36.0, -2.6),
                                         (5.0, 36.0, 40.0, -4.0))):
        m.round_box(bd, 0, cz, r, r * 0.86, y0, y1, GOLD, cut=max(1, round(r * 0.3)))
    hd = m.bone("head", bd, (0, 40, -6))                                           # helmeted head, thrust forward
    m.round_box(hd, 0, -10.0, 3.0, 4.0, 36.0, 42.0, GOLD, cut=1)
    m.box(hd, -2.0, 36.6, -17.0, 2.0, 39.4, -13.0, GOLD)
    spike(m, hd, (0, 38.0, -17.0), (0, -0.3, -1), 2.4, 3.0, CLAW, tip=0.4)
    for sx in (-1, 1):
        m.box(hd, min(sx * 3.0, sx * 3.3), 39.4, -12.4, max(sx * 3.0, sx * 3.3), 40.4, -11.2, solid(P, "eye", glow=True))
    spike(m, hd, (0, 42.0, -9.0), (0, 0.8, 1), 2.0, 6.0, GOLD, tip=0.4)
    wb = m.bone("wings", bd, (0, 36, 4))                                           # great wing of golden blades
    for sx in (-1, 1):
        for j, ang in enumerate((40, 25, 10, -5)):
            x0, x1 = sorted((sx * 3.0, sx * (22.0 - j * 2.0)))
            m.box(wb, x0, 35.0, 4.0 + j * 0.8, x1, 38.0, 5.0 + j * 0.8, GOLD, rotation=(0, sx * 25, sx * ang),
                  pivot=(sx * 3.0, 36.0, 4.0 + j * 0.8))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                            # long arms, pincer claws
        ab = m.bone(nm, bd, (sx * 6.0, 32.0, -2.0))
        el = (sx * 10.0, 26.0, -8.0)
        hand = (sx * 9.0, 22.0, -16.0)
        rod(m, ab, (sx * 6.0, 32.0, -2.0), el, 3, GOLD, extend=0.5)
        rod(m, ab, el, hand, 3, GOLD, extend=0.5)
        for d in (-1, 1):
            pts = [hand, (hand[0] + d * 2.4, hand[1] + 1.0, hand[2] - 3.0), (hand[0] + d * 1.0, hand[1] + 1.0, hand[2] - 6.0)]
            for p0, p1 in zip(pts, pts[1:]):
                rod(m, ab, p0, p1, 1, CLAW, extend=0.3, t2=2)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                            # thick golden legs
        lg = m.bone(nm, top, (sx * 4.0, 18.0, 0))
        rod(m, lg, (sx * 4.0, 18.0, 0), (sx * 5.0, 9.0, -3.0), 5, GOLD, extend=0.6)
        rod(m, lg, (sx * 5.0, 9.0, -3.0), (sx * 5.0, 2.0, 0.0), 4, GOLD, extend=0.6)
        for d in ((-0.5, 0, -1), (0, 0, -1), (0.5, 0, -1)):
            spike(m, lg, (sx * 5.0 + d[0] * 2.0, 1.4, -2.0), (d[0], -0.4, -1), 1.6, 3.6, CLAW, tip=0.4)
    return m
