"""Ceresmon Medium (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Olympus goddess of the harvest in her medium form. A figure crowned with a great coral-pink
flower and violet blossoms in pink hair, wearing a green leaf bodice and a long armoured skirt of golden leaves with
golden leaf pauldrons, curling green vines winding round her arms and down to the ground, standing on stones. Its
official design is kept as drawn. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid, shell
from _digidetail import armour, cutout, fabric, local, skin, solid, strands
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a harvest goddess crowned with a coral-pink flower in pink hair, in a green leaf bodice and a long skirt of "
        "golden leaves, with green vines curling round her")
BASE = {"skin": (226, 214, 200), "skin_dark": (180, 160, 146), "hair": (240, 150, 190), "hair_dark": (190, 90, 140),
        "flower": (240, 120, 120), "flower_light": (255, 200, 190), "violet": (150, 100, 200), "leaf": (90, 180, 90),
        "leaf_dark": (40, 110, 40), "gold": (230, 210, 140), "gold_dark": (170, 140, 70), "vine": (60, 150, 60),
        "stone": (170, 150, 120), "eye": (60, 140, 80)}
SHINY = {"hair": (200, 220, 250), "hair_dark": (120, 150, 210), "gold": (210, 214, 230), "gold_dark": (130, 134, 160),
         "flower": (250, 220, 90)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", trim="leaf", trim_w=0.25)
LEAF = armour(P, "leaf", "leaf_dark")
SKIN = skin(P, "skin", dark="skin_dark", var=0.03)


def petal_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    du, t = abs(u / max(W, 1e-6) - 0.5) * 2, v / max(H, 1e-6)
    return du < math.sin(math.pi * min(1.0, t)) ** 0.6


def petalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return tone(p["flower_light"] if v / max(H, 1e-6) > 0.7 else p["flower"], face), None


def build():
    m = Model("ceresmonmedium")
    mats = {"skin": SKIN, "chest": LEAF, "abs": SKIN, "pelvis": LEAF, "deltoid": GOLD, "thigh": GOLD, "knee": GOLD,
            "shin": GOLD, "calf": GOLD, "foot": GOLD, "toe": GOLD}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.85, leg_bulk=0.95, name="ceresmonmedium")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.6, 54.4, 60.6, SKIN, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.0 - 0.4, 57.6, -2.9, sx * 1.0 + 0.4, 58.2, -2.7, solid(P, "eye"))
    hair = strands(P, "hair", "hair_dark")
    for i in range(12):                                                      # long pink hair
        ang = math.radians(-120 + i * 22)
        rod(m, hd, (2.4 * math.sin(ang), 60.0, -2.0 * math.cos(ang) + 0.6),
            (3.4 * math.sin(ang), 46.0, 2.4 + abs(math.sin(ang))), 2, hair, extend=0.3, t2=1)
    fl = m.bone("crown", hd, (0, 61, 0))                                     # the great flower crown
    for i in range(7):
        ang = -60 + i * 20
        m.box(fl, -2.6, 61.0, 1.0, 2.6, 71.0, 1.0, cutout(petal_in, petalf), rotation=(-20, 0, ang),
              pivot=(0, 61.0, 1.0))
    for sx in (-1, 1):
        for j in range(3):
            m.round_box(hd, sx * (2.8 + j * 0.8), -1.0 + j, 0.9, 0.9, 59.0 - j * 1.4, 60.6 - j * 1.4,
                        solid(P, "violet"), cut=1)
    for sx in (-1, 1):                                                       # golden leaf pauldrons
        for j in range(3):
            m.box(bd, min(sx * 4.0, sx * (11.0 - j)), 46.0 + j * 2.0, -3.0, max(sx * 4.0, sx * (11.0 - j)),
                  48.0 + j * 2.0, 3.0, GOLD, rotation=(0, 0, -sx * (20 + j * 12)), pivot=(sx * 5.0, 50.0, 0))
    shell(m, bd, (0, 0, 0.4), 5.6, 6.0, 34.0, -170, 170, 12, 1.0, GOLD, tilt=-6)  # the golden leaf skirt
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                      # curling vines
        ab = a[nm]
        h = ab["hand"]
        pts = [ab["shoulder"]] + [(h[0] + sx * 3.0 * math.cos(t), h[1] - t * 5.0, h[2] + 3.0 * math.sin(t))
                                  for t in (0.6, 1.6, 2.6, 3.6, 4.6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab["bone"], p0, p1, 1, solid(P, "vine"), extend=0.3)
    for sx in (-1, 1):                                                       # standing on stones
        m.round_box(bd, sx * 4.0, -1.0, 3.6, 3.0, -34.0 + 34.0, 2.0, solid(P, "stone"), cut=1)
    return m
