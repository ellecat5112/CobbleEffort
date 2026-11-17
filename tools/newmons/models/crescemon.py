"""Crescemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the moon huntress. A lithe figure in sleek silver-and-black armour and a black bodysuit, a white
rabbit-eared helm with a gold face crest and long pink ribbons streaming from it, a pair of great curved crescent
moon blades on its arms, and round gold-rimmed shields on its hips. Its official design is kept as drawn.
25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, fabric, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lithe moon huntress in sleek silver-and-black armour, a white rabbit-eared helm with long pink ribbons, "
        "great crescent moon blades on its arms and round gold-rimmed hip shields")
BASE = {"silver": (210, 214, 226), "silver_dark": (110, 114, 130), "silver_light": (255, 255, 255),
        "black": (30, 30, 38), "black_light": (90, 90, 104), "white": (246, 246, 250), "white_dark": (190, 194, 210),
        "gold": (240, 200, 70), "gold_dark": (170, 130, 20), "pink": (240, 170, 200), "pink_dark": (200, 110, 150),
        "visor": (250, 230, 120), "violet": (170, 150, 230)}
SHINY = {"silver": (240, 200, 120), "silver_dark": (170, 120, 40), "black": (40, 30, 70), "pink": (150, 210, 250)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="black", trim_w=0.25)
SUIT = fabric(P, "black", "black_light", axis="y", period=2.2)


def build():
    m = Model("crescemon")
    mats = {"skin": SUIT, "chest": SILVER, "abs": SUIT, "pelvis": SILVER, "deltoid": SILVER, "forearm": SILVER,
            "hand": SILVER, "finger": SILVER, "thigh": SUIT, "knee": SILVER, "shin": SILVER, "calf": SILVER,
            "foot": SILVER, "toe": SILVER}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, name="crescemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.6, 3.0, 54.4, 61.0, armour(P, "white", "white_dark"), cut=1)
    m.box(hd, -2.0, 57.0, -3.3, 2.0, 58.0, -3.0, solid(P, "visor", glow=True))
    spike(m, hd, (0, 58.6, -3.2), (0, 1, -0.4), 1.6, 3.0, metal(P, "gold", dark="gold_dark"), tip=0.3)
    for sx in (-1, 1):                                                      # rabbit-eared helm
        rod(m, hd, (sx * 1.6, 60.6, 0), (sx * 3.4, 70.0, 3.0), 2, armour(P, "white", "white_dark"), extend=0.3, t2=3)
        pts = [(sx * 2.4, 59.0, 2.6), (sx * 6.0, 58.0, 9.0), (sx * 10.0, 60.0, 15.0), (sx * 14.0, 56.0, 20.0)]
        for p0, p1 in zip(pts, pts[1:]):                                    # long pink ribbons
            rod(m, hd, p0, p1, 1, fabric(P, "pink", "pink_dark", axis="x"), extend=0.3, t2=3)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                     # crescent moon blades
        ab = a[nm]
        el, h = ab["elbow"], ab["hand"]
        pts = []
        for i in range(9):
            ang = math.radians(-80 + i * 20)
            pts.append((el[0] + sx * 3.0 + sx * 6.0 * math.cos(ang) * 0.4, el[1] - 4.0 + 14.0 * math.sin(ang),
                        el[2] - 3.0 - 9.0 * math.cos(ang)))
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, ab["bone"], p0, p1, 1, metal(P, "silver", dark="silver_dark", light="silver_light"), extend=0.4,
                t2=3)
    for sx in (-1, 1):                                                      # round gold-rimmed hip shields
        for fy, fz in ((1.0, 0.42), (0.92, 0.72), (0.72, 0.92), (0.42, 1.0)):
            m.box(bd, min(sx * 4.6, sx * 6.0), 28.0 - 4.0 * fy, 0.4 - 4.0 * fz, max(sx * 4.6, sx * 6.0),
                  28.0 + 4.0 * fy, 0.4 + 4.0 * fz, SILVER)
        m.box(bd, min(sx * 6.0, sx * 6.6), 26.0, -1.6, max(sx * 6.0, sx * 6.6), 30.0, 2.4,
              metal(P, "gold", dark="gold_dark"))                                   # gold boss
    return m
