"""Arma Lizamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): an armoured lizard. Overlapping magenta plates edged in lime-green spikes from snout to tail, a
black under-hide, a ridged head crest, glowing yellow-veined forelimb plates, heavy black claws tipped gold and a long
plated tail curling up over its back to a green spear-tip. 15 blocks tall.

Front is -z, y is up. 44 units tall (the curled tail); Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, eye, local, metal, mix, skin, solid
from _route import pal, tone

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("an armoured lizard: overlapping magenta plates edged in lime-green spikes, a black under-hide, glowing "
        "yellow-veined forelimb plates, black gold-tipped claws and a plated tail curling over its back")
BASE = {"mag": (200, 30, 110), "mag_dark": (110, 10, 56), "mag_light": (250, 110, 180), "green": (120, 230, 80),
        "green_dark": (50, 150, 30), "black": (34, 30, 40), "black_light": (90, 86, 100), "gold": (250, 200, 50),
        "vein": (255, 240, 90), "eye": (250, 220, 40), "pupil": (20, 16, 10), "white": (250, 250, 250),
        "mouth": (90, 10, 30), "tongue": (200, 60, 90)}
SHINY = {"mag": (40, 120, 200), "mag_dark": (16, 60, 130), "mag_light": (120, 190, 250), "green": (250, 170, 60),
         "green_dark": (190, 110, 20)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "mag", "mag_dark", light="mag_light", trim="green", trim_w=0.4)
HIDE = skin(P, "black", light="black_light")
CLAW = metal(P, "black", dark="black", light="gold", streak=2.0)
SPIKE = metal(P, "green", dark="green_dark")


def veined(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if abs(u - W / 2) < 0.3 or abs(abs(u - W / 2) - (v % 2.4) * 0.8) < 0.18:
        return p["vein"], p["vein"]
    return PLATE(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 11.6, y - 33.6, 0.9, "eye", slit=True)
        if c is not None:
            return c, None
    return PLATE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("armalizamon")
    mats = {"skin": PLATE, "belly": HIDE, "neck": PLATE, "head": headf, "snout": PLATE, "jaw": HIDE,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "white"), "tongue": solid(P, "tongue"), "arm": veined,
            "hand": PLATE, "claw": CLAW, "thigh": PLATE, "shin": PLATE, "foot": HIDE, "talon": CLAW,
            "tail": PLATE, "tail_tip": PLATE}
    a = theropod(m, mats, "armalizamon", hip_y=16.0, hip_z=4.0, chest=(0, 25.0, -4.0), body_r=6.0, chest_r=6.2,
                 neck_top=(0, 30.0, -8.0), head_len=10.0, head_w=3.6, head_h=4.0, mouth_open=12, arm_len=11.0,
                 arm_bulk=1.5, leg_bulk=1.3, stance=4.6,
                 tail=((0, 18, 12), (1, 24, 18), (2, 32, 19), (2, 39, 14), (1, 42, 7)), tail_r=(4, 3.4, 2.8, 2.2, 1.6))
    bd = a["body"]
    for i in range(7):                                           # green spike ridges down its back and flanks
        t = i / 6
        p = (0, 16.0 + 12.0 * t, 6.0 - 12.0 * t)
        spike(m, bd, (0, p[1] + 5.0, p[2]), (0, 1, 0.5), 1.6, 3.0, SPIKE)
        for sx in (-1, 1):
            spike(m, bd, (sx * 5.6, p[1] + 1.0, p[2]), (sx, 0.5, 0.4), 1.4, 2.6, SPIKE)
    hd = a["head"]
    for j in range(4):                                           # ridged head crest
        spike(m, hd, (0, a["skull_top"], a["skull_z"][0] + j * 1.6), (0, 1, 0.6), 1.4, 3.0 - j * 0.4, SPIKE)
    for nm in ("arm_left", "arm_right"):
        ab = a[nm]
        spike(m, ab["bone"], ab["elbow"], (1 if nm == "arm_left" else -1, 0.4, 0.4), 1.4, 3.0, SPIKE)
    tl = a["tail_tip"]
    e = a["tail_pts"][-1]
    spike(m, tl, e, (0, -0.2, -1), 2.0, 5.0, SPIKE, tip=0.8)                           # green spear-tip
    for j, p in enumerate(a["tail_pts"][1:-1]):
        spike(m, a["tail"] if j < 2 else tl, (p[0], p[1] + 2.0, p[2]), (0, 1, 0.2), 1.2, 2.4, SPIKE)
    return m
