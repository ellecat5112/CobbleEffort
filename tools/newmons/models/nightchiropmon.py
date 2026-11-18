"""Night Chiropmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the bat assassin grown up: a lean figure in a black-and-navy bodysuit with pink-lit
seams, a sleek silver bat helm with pointed ears, long swept scythe-blades at its forearms and hips, dark armoured
boots with pink trim, and violet sonar rings glowing round its open hands. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean bat assassin in a black-and-navy bodysuit with pink-lit seams, a sleek silver bat helm, long scythe-"
        "blades at its forearms and hips and violet sonar rings round its hands")
BASE = {"navy": (40, 50, 90), "navy_dark": (14, 18, 40), "black": (30, 28, 36), "pink": (240, 80, 150),
        "silver": (210, 214, 226), "silver_dark": (110, 116, 130), "violet": (170, 110, 250, 190), "eye": (240, 60, 120)}
SHINY = {"navy": (110, 40, 70), "navy_dark": (50, 14, 30), "pink": (90, 230, 200)}


def P(v):
    return pal(BASE, SHINY, v)


SUIT0 = armour(P, "navy", "navy_dark", trim="black", trim_w=0.3)
BLADE = metal(P, "silver", dark="silver_dark")


def suitf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(((y + abs(x) * 0.6) % 5.0) - 2.5) < 0.12:
        return p["pink"], p["pink"]
    return SUIT0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("nightchiropmon")
    mats = {"skin": suitf, "neck": solid(P, "black"), "hand": solid(P, "black"), "finger": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, name="nightchiropmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.4, 2.8, 54.0, 60.0, armour(P, "silver", "silver_dark"), cut=1)   # bat helm
    m.box(hd, -1.8, 57.4, -3.5, 1.8, 58.2, -3.3, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 60.0, 0), (sx * 0.3, 1, 0.2), 1.6, 6.0, BLADE, tip=0.8)        # pointed ears
    for nm in ("arm_left", "arm_right"):                                                 # forearm scythe-blades
        anc = a[nm]
        el = anc["elbow"]
        sx = 1 if el[0] > 0 else -1
        x0, x1 = sorted((el[0], el[0] + sx * 1.0))
        m.box(anc["bone"], x0, el[1] - 18.0, el[2] + 0.4, x1, el[1] + 2.0, el[2] + 4.0, BLADE,
              rotation=(10, 0, sx * 10), pivot=(el[0], el[1], el[2]))
        h = anc["hand"]
        for i in range(10):                                                              # sonar rings
            ang = 2 * math.pi * i / 10
            m.box(anc["bone"], h[0] + 3.0 * math.cos(ang) - 0.5, h[1] + 3.0 * math.sin(ang) - 0.5, h[2] - 2.0,
                  h[0] + 3.0 * math.cos(ang) + 0.5, h[1] + 3.0 * math.sin(ang) + 0.5, h[2] - 1.6,
                  solid(P, "violet", glow=True))
    for sx in (-1, 1):                                                                   # hip scythes
        x0, x1 = sorted((sx * 4.4, sx * 5.4))
        m.box(bd, x0, 10.0, 0.0, x1, 32.0, 3.0, BLADE, rotation=(-15, 0, sx * 15), pivot=(sx * 4.9, 32.0, 1.0))
    return m
