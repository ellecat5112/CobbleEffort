"""Black Seraphimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a fallen seraph. Silver armour edged in green and gold, a helm with a red crest and a
dark visor, gold star emblems, ten violet bat-wings spread behind it and orbs of violet dark energy blazing in both
hands. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, bat_wing
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, gem, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a fallen seraph in silver armour edged in green and gold, a red-crested helm, gold star emblems, ten violet "
        "bat-wings and orbs of violet dark energy in both hands")
BASE = {"silver": (200, 204, 216), "silver_dark": (100, 104, 116), "silver_light": (246, 248, 255),
        "green": (60, 170, 90), "gold": (236, 196, 60), "red": (210, 30, 40), "black": (30, 30, 36),
        "violet": (120, 60, 190, 235), "violet_dark": (60, 24, 110), "orb": (200, 60, 230), "orb_light": (255, 200, 255)}
SHINY = {"silver": (70, 70, 84), "silver_dark": (30, 30, 36), "silver_light": (140, 140, 160), "violet": (200, 40, 60, 235),
         "violet_dark": (110, 14, 24), "orb": (255, 80, 80)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="green", trim_w=0.35)


def build():
    m = Model("blackseraphimon")
    mats = {"skin": SILVER, "hand": SILVER, "finger": SILVER, "foot": SILVER, "toe": solid(P, "gold"),
            "talon": solid(P, "gold")}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.1, digitigrade=True, talons=True,
                 name="blackseraphimon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 2.8, 54.6, 60.6, SILVER, cut=1)
    m.box(hd, -2.0, 56.8, -3.4, 2.0, 58.6, -3.0, solid(P, "black"))
    for j in range(5):
        spike(m, hd, (0, 60.4, -1.6 + j * 1.0), (0, 1, 0.5), 1.0, 3.4 - j * 0.4, solid(P, "red"))
    shell(m, bd, (0, 0, 0.6), 5.4, 42.0, 51.0, -85, 85, 9, 1.2, SILVER)
    for j, (x, y) in enumerate(((0, 46.5), (-3.0, 40.0), (3.0, 40.0))):              # gold star emblems
        for ang in (0, 36, 72):
            m.box(bd, x - 1.2, y - 0.3, -6.6, x + 1.2, y + 0.3, -6.2, solid(P, "gold"),
                  rotation=(0, 0, ang), pivot=(x, y, -6.4))
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        sh = a[nm]["shoulder"]
        dome(m, a[nm]["bone"], (sh[0] + sx * 1.4, 50.0, 0.3), 4.0, 3.6, SILVER, layers=3)
        h = a[nm]["hand"]
        ball(m, a[nm]["bone"], (h[0] + sx * 1.0, h[1] - 1.0, h[2] - 3.0), 3.0, gem(P, "orb", "orb_light"), layers=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # ten bat-wings, five a side
        wb = m.bone(nm, bd, (sx * 3.0, 48.0, 4.0))
        for w in range(5):
            ang = math.radians(50 - w * 25)
            root = (sx * 3.0, 48.0 - w * 1.4, 4.0 + w * 0.6)
            for f, (span, hgt) in enumerate(((14.0, 6.0),)):
                tip = (root[0] + sx * span * math.cos(ang), root[1] + span * math.sin(ang), root[2] + 2.0)
                rod(m, wb, root, tip, 1, solid(P, "violet_dark"), extend=0.3)
                x0, x1 = sorted((root[0], tip[0]))
                y0, y1 = sorted((root[1], tip[1]))
                m.box(wb, x0, y0 - 3.0, root[2] + 1.0, x1, y1 + 1.0, root[2] + 1.0,
                      lambda x, y, z, face, variant=None, box=None, **k: (P(variant)["violet"], None))
    return m
