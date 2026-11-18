"""Metallife Kuwagamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a stag beetle turned to living metal: a lean golden armoured insect-warrior with blue
crystal joints, a horned beetle helm with two great mandible horns, a narrow red-eyed face, clawed golden hands and
feet, and a huge right arm cannon of three round golden barrels glowing blue inside. 25 blocks tall.

Front is -z, y is up. 70 units tall (the horns); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, gem, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a lean golden metal stag-beetle warrior with blue crystal joints, two great mandible horns and a huge arm cannon "
        "of three round barrels glowing blue")
BASE = {"gold": (220, 180, 70), "gold_dark": (130, 96, 24), "gold_light": (250, 230, 150), "blue": (80, 180, 250),
        "blue_light": (210, 240, 255), "brown": (110, 60, 30), "eye": (240, 40, 60), "black": (30, 28, 34)}
SHINY = {"gold": (200, 206, 220), "gold_dark": (110, 116, 130), "gold_light": (250, 250, 255), "blue": (250, 90, 140),
         "blue_light": (255, 210, 230)}


def P(v):
    return pal(BASE, SHINY, v)


GOLD = armour(P, "gold", "gold_dark", light="gold_light", trim="gold_dark", trim_w=0.2)
JOINT = gem(P, "blue", "blue_light")


def build():
    m = Model("metallifekuwagamon")
    mats = {"skin": GOLD, "neck": metal(P, "brown"), "upper_arm": metal(P, "brown"), "claw": GOLD, "talon": GOLD}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, claws=True, talons=True, name="metallifekuwagamon")
    bd = a["body"]
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                            # blue crystal joints
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        ball(m, anc["bone"], (j[0], j[1], j[2] - 1.4), 1.0, JOINT, layers=2)
    ball(m, bd, (0, 46.0, -3.8), 1.2, JOINT, layers=2)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.2, 2.8, 54.0, 60.0, GOLD, cut=1)                              # beetle helm
    m.box(hd, -1.4, 56.6, -3.3, 1.4, 57.4, -3.1, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                                     # mandible horns
        pts = [(sx * 1.4, 59.0, -1.0), (sx * 3.6, 63.0, -1.6), (sx * 4.0, 67.0, -1.0), (sx * 2.6, 70.0, -0.4)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if j < 2 else 1, GOLD, extend=0.3)
        spike(m, hd, (sx * 3.8, 65.0, -1.4), (-sx, 0.3, 0), 1.0, 2.4, GOLD, tip=0.8)
    for sx in (-1, 1):                                                                     # shoulder spikes
        spike(m, bd, (sx * 6.0, 51.0, 0), (sx * 0.8, 0.8, 0.3), 1.4, 4.0, GOLD, tip=0.8)
    ar = a["arm_right"]                                                                    # triple-barrel cannon
    el, wr = ar["elbow"], ar["wrist"]
    c = (wr[0] - 4.0, wr[1] + 10.0, wr[2] - 2.0)
    rod(m, ar["bone"], el, c, 4, GOLD, extend=0.6)
    for ang in (90, 210, 330):
        a_ = math.radians(ang)
        bx, by = c[0] + 3.6 * math.cos(a_), c[1] + 3.6 * math.sin(a_)
        m.round_box(ar["bone"], bx, c[2] - 3.0, 2.8, 4.0, by - 2.6, by + 2.6, GOLD, cut=1)
        m.box(ar["bone"], bx - 1.6, by - 1.6, c[2] - 7.1, bx + 1.6, by + 1.6, c[2] - 6.9, solid(P, "blue", glow=True))
    return m
