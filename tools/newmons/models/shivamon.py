"""Shivamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the insect deity of destruction and creation: a lean blue-and-black armoured mantis-god with six arms
raised in a dancing pose, a pointed magenta crest-helm, white ribbon sashes, golden accents, seated on a great pink
lotus of blade petals above a rainbow halo, a small sun blazing over its head. 35 blocks.

Front is -z, y is up. 78 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 78
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "a lean six-armed blue-and-black mantis-god with a magenta crest-helm, seated on a pink lotus of blade petals above a rainbow halo"
BASE = {"blue": (50, 70, 170), "blue_dark": (14, 20, 70), "black": (30, 28, 36), "magenta": (220, 60, 160),
        "pink": (240, 120, 180), "pink_dark": (170, 50, 110), "gold": (240, 200, 70), "gold_dark": (160, 110, 20),
        "white": (246, 246, 252), "sun": (255, 230, 120), "rainbow": (255, 255, 255, 170)}
SHINY = {"blue": (150, 40, 60), "blue_dark": (70, 10, 20), "pink": (120, 220, 240), "pink_dark": (40, 140, 170)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "blue", "blue_dark", trim="gold", trim_w=0.2)
PETAL = armour(P, "pink", "pink_dark")


def rainbowf(x, y, z, face, variant, box=None, **k):
    r = math.hypot(x, z)
    cols = [(240, 60, 60), (250, 160, 40), (250, 230, 60), (80, 200, 90), (60, 130, 230), (150, 80, 220)]
    c = cols[int(r) % 6]
    return c + (200,), c


def build():
    m = Model("shivamon")
    top = m.bone("shivamon", None, (0, 0, 0))
    hb = m.bone("halo", top, (0, 2, 0))
    m.round_box(hb, 0, 0, 14.0, 14.0, 1.0, 2.0, rainbowf, cut=4)                             # rainbow halo
    lb = m.bone("lotus", top, (0, 8, 0))
    for j in range(10):                                                                  # lotus blade petals
        ang = 2 * math.pi * j / 10
        spike(m, lb, (3.0 * math.cos(ang), 6.0, 3.0 * math.sin(ang)), (math.cos(ang), 0.8, math.sin(ang)), 3.0, 10.0,
              PETAL, tip=0.8)
    spike(m, lb, (0, 4.0, 0), (0, -1, 0), 2.0, 4.0, PETAL, tip=0.8)
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats = {"skin": ARM, "hand": solid(P, "black"), "finger": solid(P, "black"), "claw": metal(P, "gold")}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.75, leg_bulk=0.8, claws=True, name="god")
    from _dorbickmon import mount
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 3.0, 54.0, 60.0, ARM, cut=1)
    spike(m, hd, (0, 60.0, -1.0), (0, 1, 0.2), 2.0, 9.0, solid(P, "magenta"), tip=0.8)        # pointed crest
    m.box(hd, -1.6, 57.0, -3.7, 1.6, 57.8, -3.5, solid(P, "magenta", glow=True))
    for sx in (-1, 1):                                                                   # four extra raised arms
        for j in range(2):
            sh = (sx * 6.0, 48.0 - j * 4.0, 1.0)
            el = (sx * (14.0 + j * 2.0), 58.0 - j * 10.0, 2.0)
            wr = (sx * (12.0 + j * 6.0), 70.0 - j * 18.0, 2.0)
            rod(m, bd, sh, el, 2, ARM, extend=0.4)
            rod(m, bd, el, wr, 2, ARM, extend=0.4)
            spike(m, bd, wr, (sx * 0.2, 1, 0), 1.0, 3.0, metal(P, "gold"), tip=0.8)
        rod(m, bd, (sx * 3.0, 46.0, -3.0), (sx * 8.0, 30.0, -6.0), 1, solid(P, "white"), extend=0.2, t2=3)   # ribbons
    ball(m, hd, (0, 72.0, 0), 2.6, solid(P, "sun", glow=True), layers=2)                    # little sun
    mount(m, i_box, i_bone, 6.0, 0.0, top)
    return m
