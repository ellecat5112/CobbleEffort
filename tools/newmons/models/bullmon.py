"""Bullmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the armoured fighting bull. A charging bull in navy-blue armour plates trimmed and riveted in gold,
brown hide at its joints, a red-masked head bowed low under two great curving ivory horns, a torn red cape with a
white emblem over its back, gold hoof-cuffs and a long tufted tail. 15 blocks tall.

Front is -z, y is up. 36 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, cutout, fabric, fur, local, metal, noise2, solid, strands
from _route import pal, tone

HEIGHT = 36
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("a charging bull in navy armour riveted in gold, brown hide at its joints, a red-masked head under two great "
        "ivory horns, a torn red cape and a tufted tail")
BASE = {"navy": (40, 60, 150), "navy_dark": (16, 24, 70), "navy_light": (110, 130, 220), "gold": (230, 190, 70),
        "gold_dark": (160, 120, 30), "brown": (150, 90, 40), "brown_dark": (90, 50, 20), "red": (210, 40, 40),
        "red_dark": (120, 14, 20), "white": (246, 244, 240), "horn": (240, 226, 180), "horn_dark": (190, 160, 100),
        "black": (30, 26, 30), "tuft": (246, 230, 210), "eye": (250, 220, 60), "mouth": (100, 30, 30)}
SHINY = {"navy": (40, 40, 46), "navy_dark": (14, 14, 18), "navy_light": (110, 110, 124), "red": (230, 200, 60),
         "red_dark": (160, 120, 20)}


def P(v):
    return pal(BASE, SHINY, v)


NAVY = armour(P, "navy", "navy_dark", light="navy_light", trim="gold", trim_w=0.4, rivets=True)
HIDE = fur(P, "brown", "brown_dark", length=1.0)
GOLD = metal(P, "gold", dark="gold_dark")
HORN = metal(P, "horn", dark="horn_dark", light="white")


def capef(x, y, z, face, variant, box=None, **k):
    """The red cape with a white chevron emblem."""
    p = P(variant)
    a, b = x, z
    if face in ("up", "down") and abs(abs(a) * 0.8 - (b + 2.0) * 0.4) < 0.5 and -10 < b < 4:
        return tone(p["white"], face), None
    return fabric(P, "red", "red_dark", axis="z", period=2.6)(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return u / max(W, 1e-6) < 0.85 + 0.15 * noise2((box.lo[2] + v) * 1.4, 2.0)


def build():
    m = Model("bullmon")
    mats = {"skin": NAVY, "belly": HIDE, "neck": NAVY, "head": solid(P, "red"), "snout": solid(P, "red"),
            "jaw": solid(P, "red_dark"), "mouth": solid(P, "mouth"), "tooth": solid(P, "white"), "leg_upper": HIDE,
            "leg_lower": NAVY, "paw": GOLD, "claw": GOLD, "tail": HIDE}
    a = quadruped(m, mats, "bullmon", length=26.0, body_y=19.0, body_rx=6.8, body_ry=7.4, chest_bulk=1.3,
                  neck=((0, 21, -14), (0, 17, -18)), head_len=9.0, head_w=3.6, head_h=4.2, snout=0.4, mouth_open=6,
                  teeth=0, leg_bulk=1.4, toes=2, claws=False,
                  tail=((0, 22, 16), (2, 16, 20), (4, 10, 22)), tail_r=(0.8, 0.7, 0.6))
    bd, hd = a["body"], a["head"]
    for sx in (-1, 1):                                                            # great curving horns
        pts = [(sx * 3.4, 19.0, -17.0), (sx * 8.0, 20.0, -18.0), (sx * 11.0, 17.0, -22.0), (sx * 10.0, 13.0, -25.0),
               (sx * 7.0, 11.0, -26.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, max(1, 3 - j // 2), HORN, extend=0.5)
        m.box(hd, sx * 2.0 - 0.6, 18.6, -21.4, sx * 2.0 + 0.6, 19.4, -21.0, solid(P, "eye", glow=True))
    m.box(hd, -1.6, 15.0, -23.0, 1.6, 16.0, -22.2, solid(P, "black"))             # nostrils band
    # armour bands on the knees
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        lg = a[nm]
        e = lg["elbow"]
        m.round_box(lg["bone"], e[0], e[2], 2.6, 2.6, e[1] - 1.6, e[1] + 1.6, GOLD, cut=1)
        w = lg["wrist"]
        m.round_box(lg["bone"], w[0], w[2], 2.4, 2.6, 2.4, 4.6, NAVY, cut=1)
    # the torn red cape over its back
    cb = m.bone("cap", bd, (0, 27, -6))
    for sx in (-1, 1):
        x0, x1 = sorted((0.0, sx * 9.0))
        m.box(cb, x0, 27.0, -10.0, x1, 27.0, 8.0, cutout(torn, capef), rotation=(0, 0, -sx * 35),
              pivot=(0, 27.0, 0))
    m.box(cb, -3.0, 26.4, -10.0, 3.0, 27.4, 8.0, capef)
    e = a["tail_pts"][-1]                                                         # tufted tail tip
    for d in ((0.3, -1, 0), (-0.3, -1, 0.3), (0, -1, -0.3)):
        spike(m, a["tail"], e, d, 1.4, 3.6, strands(P, "tuft", "brown"), tip=0.5)
    return m
