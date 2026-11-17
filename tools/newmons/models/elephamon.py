"""Elephamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the armoured war elephant. A sturdy white elephant in blue armour plates with silver trim, a blue
helmet with a crest, a long trunk tipped with a steel plate, big grey toenails, a little tufted tail, and on each
shoulder a huge round silver turbine disc with red vanes. 15 blocks tall.

Front is -z, y is up. 34 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a sturdy white elephant in blue armour with silver trim, a crested helmet, a steel-tipped trunk, grey toenails "
        "and a huge silver turbine disc with red vanes on each shoulder")
BASE = {"white": (240, 240, 246), "white_dark": (170, 172, 190), "blue": (40, 70, 160), "blue_dark": (14, 26, 80),
        "blue_light": (110, 150, 230), "silver": (210, 214, 226), "silver_dark": (110, 114, 128), "red": (220, 40, 40),
        "red_dark": (130, 14, 18), "grey": (150, 150, 160), "eye": (30, 30, 36), "mouth": (130, 40, 50),
        "tooth": (250, 248, 240)}
SHINY = {"blue": (40, 130, 90), "blue_dark": (10, 60, 40), "blue_light": (110, 210, 170), "red": (240, 180, 40)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "white", dark="white_dark", var=0.03)
BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="silver", trim_w=0.4)
SILVER = metal(P, "silver", dark="silver_dark")


def turbinef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        u, v, W, H = local(x, y, z, face, box)
        cu, cv = u - W / 2, v - H / 2
        r = math.hypot(cu, cv)
        if r > min(W, H) / 2 - 0.8:
            return tone(p["silver_dark"], face), None
        a = math.atan2(cv, cu)
        if r > 1.2 and (a * 4 / math.pi) % 1.0 < 0.55:
            return tone(p["red"], face), None
        return tone(p["silver"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("elephamon")
    mats = {"skin": SKIN, "belly": SKIN, "neck": SKIN, "head": BLUE, "snout": SKIN, "jaw": SKIN,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": SKIN, "leg_lower": BLUE,
            "paw": BLUE, "claw": solid(P, "grey"), "tail": SKIN}
    a = quadruped(m, mats, "elephamon", length=30.0, body_y=16.0, body_rx=8.0, body_ry=7.4, chest_bulk=1.1,
                  neck=((0, 19, -14), (0, 20, -17)), head_len=7.0, head_w=4.6, head_h=5.0, snout=0.3, mouth_open=4,
                  teeth=0, leg_bulk=2.0, toes=3, tail=((0, 18, 15), (0, 14, 18)), tail_r=(1.0, 0.8))
    bd, hd = a["body"], a["head"]
    m.round_box(bd, 0, -2.0, 8.4, 9.0, 18.0, 24.6, BLUE, cut=3)                      # armour saddle plate
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.5, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.5,
              solid(P, "eye"))
        x0, x1 = sorted((sx * 8.0, sx * 9.6))                                         # turbine discs
        m.box(bd, x0, 16.0, -9.0, x1, 28.0, 3.0, turbinef)
    spike(m, hd, (0, ey + 2.6, ez + 1.0), (0, 1, -0.3), 1.6, 3.0, BLUE, tip=0.5)      # helmet crest
    pts = [(0, ey - 1.0, a["snout_front"]), (0, ey - 6.0, a["snout_front"] - 3.0), (0, 4.0, a["snout_front"] - 3.0),
           (0, 2.0, a["snout_front"] - 6.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # long trunk
        rod(m, hd, p0, p1, 3 - j // 2, SKIN, extend=0.5)
    m.round_box(hd, 0, pts[-1][2], 1.4, 1.4, 1.0, 3.0, SILVER, cut=0)
    e = a["tail_pts"][-1]
    m.round_box(a["tail"], e[0], e[2], 1.0, 1.0, e[1] - 2.0, e[1], solid(P, "grey"), cut=0)
    return m
