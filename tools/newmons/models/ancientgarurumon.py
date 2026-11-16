"""Ancient Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the ancient warrior of light, a wolf knight. White-and-silver plate armour with lavender
under-plates, a wolf helm with jagged ears, a fanged snout and a purple face, huge clawed gauntlets, a long gold
blade-shield on its left arm, black fur at its neck and a tail of plates. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _digidetail import armour, cutout, fur, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a wolf knight in white-and-silver plate with lavender under-plates, a wolf helm with jagged ears and a purple "
        "face, clawed gauntlets, a long gold blade-shield on its arm and black fur at its neck")
BASE = {"white": (240, 242, 248), "white_dark": (160, 164, 186), "silver": (190, 194, 210), "silver_dark": (90, 94, 112),
        "lav": (170, 150, 210), "lav_dark": (100, 80, 150), "gold": (236, 190, 60), "gold_dark": (160, 112, 26),
        "gold_light": (255, 240, 170), "black": (30, 30, 40), "black_light": (80, 80, 96), "face": (110, 70, 150),
        "eye": (255, 220, 60), "claw": (236, 236, 244)}
SHINY = {"white": (60, 62, 74), "white_dark": (24, 26, 34), "silver": (110, 112, 130), "silver_dark": (40, 42, 54),
         "lav": (220, 80, 90), "lav_dark": (140, 30, 40), "face": (180, 40, 50)}


def P(v):
    return pal(BASE, SHINY, v)


WHITE = armour(P, "white", "white_dark", trim="lav")
WHITE_PLAIN = armour(P, "white", "white_dark", seams=(4.0,))
LAV = armour(P, "lav", "lav_dark")
SILVER = metal(P, "silver", dark="silver_dark", light="white")
GOLD = metal(P, "gold", dark="gold_dark", light="gold_light")
FUR = fur(P, "black", "black", tip="black_light", length=1.2)


def blade(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    uu = u / max(W, 1e-6)
    return uu < 0.55 + 0.45 * t if t > 0.15 else uu < 0.55 + 3 * t


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 57.0 < y < 58.0 and 0.6 < abs(x) < 2.0:
        return p["eye"], p["eye"]
    return WHITE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("ancientgarurumon")
    mats = {"skin": LAV, "chest": WHITE, "abs": LAV, "pelvis": WHITE, "neck": FUR, "deltoid": WHITE,
            "upper_arm": LAV, "forearm": WHITE, "hand": SILVER, "finger": SILVER, "claw": solid(P, "claw"),
            "thigh": WHITE, "knee": SILVER, "shin": WHITE, "calf": WHITE_PLAIN, "foot": SILVER, "talon": GOLD}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.25, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="ancientgarurumon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.6, 60.6, helmf, cut=1)
    m.box(hd, -1.7, 54.6, -7.4, 1.7, 57.4, -2.6, solid(P, "face"))                     # purple snout
    m.box(hd, -2.0, 57.0, -7.0, 2.0, 58.6, -2.6, WHITE_PLAIN)                            # helm brow over it
    for sx in (-1, 1):
        for j in range(3):
            spike(m, hd, (sx * 1.2, 54.8, -6.6 + j * 1.3), (0, -1, 0), 0.8, 1.2, solid(P, "claw"))
        for j in range(3):                                       # jagged ears
            spike(m, hd, (sx * (2.0 + j * 0.6), 60.0 - j * 0.6, 0.4 + j), (sx * 0.3, 1, 0.3), 1.6, 4.0 - j, WHITE)
    for i in range(10):                                          # black fur ruff
        ang = math.radians(-160 + i * 35.5)
        c = (4.0 * math.sin(ang), 52.0, -3.6 * math.cos(ang))
        spike(m, bd, c, (math.sin(ang), -0.6, -math.cos(ang)), 2.0, 4.0, FUR, tip=1.0)
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, WHITE)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.6, 50.0, 0.3), 4.8, 4.6, WHITE, layers=4)
        for j in range(3):
            spike(m, ab, (sh[0] + sx * 3.0, 53.0, -1.0 + j * 1.6), (sx * 0.5, 1, 0.2), 1.4, 4.0 + j, WHITE)
        wr, el = a[nm]["wrist"], a[nm]["elbow"]
        shell(m, ab, (wr[0], 0, wr[2]), 2.4, 29.0, 37.0, -180, 180, 6, 1.0, WHITE)       # gauntlet
    al = a["arm_left"]                                           # the gold blade-shield along its left forearm
    w = al["wrist"]
    sb = m.bone("shield", al["bone"], w)
    m.box(sb, w[0] + 2.4, 14.0, w[2] - 7.0, w[0] + 2.4, 44.0, w[2] + 4.0, cutout(blade, GOLD))
    m.box(sb, w[0] + 2.0, 26.0, w[2] - 1.0, w[0] + 3.0, 34.0, w[2] + 1.0, SILVER)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg, kn = a[nm]["bone"], a[nm]["knee"]
        dome(m, lg, (kn[0], 18.0, kn[2] - 0.8), 2.8, 2.6, WHITE, layers=2)
        spike(m, lg, (kn[0], 18.5, kn[2] - 3.0), (0, 0.4, -1), 1.8, 3.0, WHITE)
    tl = m.bone("tail", bd, (0, 31, 3.5))
    pts = [(0, 31, 3.5), (0, 26, 9), (0, 19, 13), (0, 12, 15)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 4 - j, WHITE, extend=0.5)
    return m
