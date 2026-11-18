"""Mihiramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the tiger of the Twelve Devas: a great golden tiger striped violet, with feathered white-and-gold
wings, a red hood knotted round its head, violet greaves on its legs with black paws and claws, two violet dharma
wheels mounted on its flanks on a steel axle, and a long violet-striped tail. 25 blocks long.

Front is -z, y is up. 34 units tall (the wings); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, quadruped
from _digidetail import armour, fabric, feathers, fur, metal, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a great golden tiger striped violet with white-and-gold feathered wings, a red hood, violet greaves and two "
        "violet dharma wheels on its flanks")
BASE = {"gold": (246, 200, 60), "gold_dark": (190, 130, 20), "stripe": (110, 60, 150), "white": (246, 246, 240),
        "white_dark": (190, 190, 180), "red": (200, 40, 40), "red_dark": (110, 14, 18), "violet": (120, 70, 170),
        "violet_dark": (60, 30, 100), "black": (34, 30, 40), "steel": (200, 204, 214), "eye": (60, 140, 60),
        "mouth": (150, 30, 40), "tooth": (250, 250, 240)}
SHINY = {"gold": (236, 236, 244), "gold_dark": (170, 170, 186), "stripe": (40, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "gold", "gold_dark", length=1.2)


def furf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and abs(((z * 0.5 + y * 0.3 + abs(x) * 0.2) % 3.2) - 1.6) < 0.4:
        return tone(p["stripe"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def wheelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(math.hypot(y - 18.0, z - 4.0) % 2.4 - 1.2) < 0.2:
        return tone(p["gold"], face), None
    return armour(P, "violet", "violet_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("mihiramon")
    mats = {"skin": furf, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "black")}
    a = quadruped(m, mats, "mihiramon", length=30.0, body_y=17.0, body_rx=6.0, body_ry=5.8, chest_bulk=1.3,
                  neck=((0, 21, -13), (0, 23, -16)), head_len=9.0, head_w=4.4, head_h=4.4, snout=0.6,
                  mouth_open=10, teeth=4, leg_bulk=1.5, toes=4,
                  tail=((0, 20, 15), (3, 24, 20), (6, 27, 23), (8, 28, 19)), tail_r=(1.6, 1.4, 1.2, 1.0))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
              ez + 0.6, solid(P, "eye"))
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2] + 3.4, 4.8, 3.0, ey + 1.6, ey + 3.6, fabric(P, "red", "red_dark"), cut=1)  # red hood
    for s in (-1, 1):
        m.box(hd, s * 1.0 - 1.0, ey - 6.0, hc[2] + 3.0, s * 1.0 + 1.0, ey - 1.0, hc[2] + 3.4, fabric(P, "red", "red_dark"),
              rotation=(20, 0, s * 15), pivot=(s * 1.0, ey - 1.0, hc[2] + 3.2))
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):          # violet greaves
        anc = a[nm]
        w = anc.get("wrist") or anc.get("ankle")
        if w:
            m.round_box(anc["bone"], w[0], w[2], 2.0, 2.0, w[1] + 0.5, w[1] + 5.0, armour(P, "violet", "violet_dark"),
                        cut=1)
    rod(m, bd, (-8.0, 18.0, 4.0), (8.0, 18.0, 4.0), 1, metal(P, "steel"), extend=0.4)            # axle
    for sx in (-1, 1):                                                                       # dharma wheels
        x0, x1 = sorted((sx * 7.0, sx * 8.6))
        for i in range(8):
            ang = 2 * math.pi * i / 8
            m.box(bd, x0, 18.0 + 4.0 * math.sin(ang) - 1.0, 4.0 + 4.0 * math.cos(ang) - 1.0, x1,
                  18.0 + 4.0 * math.sin(ang) + 1.0, 4.0 + 4.0 * math.cos(ang) + 1.0, wheelf)
        m.box(bd, x0, 15.0, 1.0, x1, 21.0, 7.0, wheelf)
        spike(m, bd, (sx * 8.6, 18.0, 4.0), (sx, 0, 0), 1.0, 2.0, metal(P, "steel"), tip=0.8)
    for side in (1, -1):                                                                     # feathered wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 23.0, -6.0))
        feather_wing(m, wb, (side * 3.0, 23.0, -6.0), 16.0, 9.0, 5, feathers(P, "white", "white_dark", tip="gold"),
                     side=side, sweep=30, droop=-6.0)
    return m
