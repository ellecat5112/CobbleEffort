"""Anubimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the jackal god who judges the dead. A tall lavender-skinned figure with a black jackal head and
long black hair, a long white robe tied with a white sash and a patterned belt, red-and-gold banded bracelets,
black claws, white leg wraps and two vast wings of golden-brown feathers. 35 blocks tall.

Front is -z, y is up. 76 units tall (the wings); Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid, shell
from _digidetail import armour, fabric, feathers, local, metal, skin, solid, strands
from _route import pal, tone

HEIGHT = 76
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("the jackal god: lavender skin, a black jackal head with long black hair, a long white robe, red-and-gold "
        "bracelets, black claws and two vast golden-brown wings")
BASE = {"skin": (170, 170, 220), "skin_dark": (100, 100, 160), "skin_light": (220, 220, 250), "black": (30, 30, 40),
        "black_light": (90, 90, 110), "white": (246, 244, 236), "white_dark": (200, 194, 180), "red": (200, 40, 40),
        "gold": (230, 186, 60), "gold_dark": (160, 112, 26), "wing": (190, 160, 100), "wing_dark": (110, 86, 50),
        "eye": (255, 220, 60)}
SHINY = {"skin": (220, 190, 140), "skin_dark": (160, 130, 80), "skin_light": (250, 230, 190), "black": (230, 230, 240),
         "black_light": (255, 255, 255), "wing": (110, 110, 140), "wing_dark": (50, 50, 70)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "skin", dark="skin_dark", light="skin_light", var=0.03)
ROBE = fabric(P, "white", "white_dark", axis="y", period=2.6)
WING = feathers(P, "wing", "wing_dark", size=(1.6, 3.2), flow=(0, -1))
HAIR = strands(P, "black", "black", tip="black_light")


def bracelet(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    if t < 0.2 or t > 0.8:
        return tone(p["gold"], face), None
    zig = abs((u * 0.8) % 2 - 1)
    return tone(p["red"] if abs(t - 0.5) < 0.3 * zig else p["gold_dark"], face), None


def build():
    m = Model("anubimon")
    mats = {"skin": SKIN, "chest": ROBE, "abs": ROBE, "pelvis": ROBE, "neck": SKIN, "deltoid": SKIN,
            "upper_arm": SKIN, "forearm": SKIN, "hand": SKIN, "finger": SKIN, "claw": solid(P, "black"),
            "thigh": ROBE, "knee": ROBE, "shin": solid(P, "white"), "calf": ROBE, "foot": SKIN, "toe": SKIN}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.95, leg_bulk=0.85, name="anubimon", hand_pose="open", claws=True)
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.4, 2.6, 54.6, 60.6, solid(P, "black"), cut=1)
    m.box(hd, -1.4, 55.0, -7.0, 1.4, 58.0, -2.4, solid(P, "black"))                      # the jackal muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.5, 58.6, -2.7, sx * 1.4 + 0.5, 59.2, -2.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.6, 60.0, 0.4), (sx * 0.2, 1, 0.1), 1.6, 5.0, solid(P, "black"), tip=0.8)   # ears
    hr = m.bone("mane", hd, (0, 59, 2))
    for i in range(7):                                           # long black hair down its back
        x = -2.4 + i * 0.8
        rod(m, hr, (x, 59.0, 1.8), (x * 1.3, 26.0 - (i % 2) * 4, 5.0), 2, HAIR, extend=0.3)
    sk = m.bone("skirt", bd, (0, 32, 0))
    for i in range(10):                                          # the long robe to the ankles
        ang = math.radians(-162 + i * 36)
        c = (4.4 * math.sin(ang), 32.0, -3.8 * math.cos(ang))
        m.box(sk, c[0] - 1.6, 4.0, c[2], c[0] + 1.6, 32.0, c[2] + 0.8, ROBE,
              rotation=(-4 * math.cos(ang), -math.degrees(ang), 0), pivot=c)
    m.box(bd, -4.6, 31.0, -4.2, 4.6, 33.4, 4.0, bracelet)                                # patterned belt
    m.box(bd, -1.0, 16.0, -4.8, 1.0, 31.0, -4.2, ROBE)                                    # sash end
    for nm in ("arm_left", "arm_right"):
        w, el = a[nm]["wrist"], a[nm]["elbow"]
        p = tuple(ww + (e - ww) * 0.3 for ww, e in zip(w, el))
        rod(m, a[nm]["bone"], w, p, 4, bracelet, extend=0.2)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):        # vast golden wings
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        rod(m, wb, (sx * 3.0, 49.0, 3.0), (sx * 14.0, 66.0, 8.0), 3, WING, extend=0.3)
        rod(m, wb, (sx * 14.0, 66.0, 8.0), (sx * 20.0, 74.0, 10.0), 2, WING, extend=0.3)
        for i in range(12):
            t = i / 11
            base = (sx * (3.0 + 17.0 * t), 49.0 + 25.0 * t, 3.0 + 7.0 * t)
            ln = 18.0 + 22.0 * t
            m.box(wb, base[0] - 1.8, base[1] - ln, base[2], base[0] + 1.8, base[1], base[2], WING,
                  rotation=(-10, 0, -sx * (40 - 30 * t)), pivot=base)
    return m
