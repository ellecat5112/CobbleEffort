"""Hi-Commandramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the heavy trooper dragon: a squat dark-green armoured dragon soldier in digital camo,
a red helmet with a black horn and a sunburst crest, goggles, a big riot shield with yellow sawtooth markings, a heavy
grenade-launcher rifle and steel claws on its feet. 15 blocks tall.

Front is -z, y is up. 48 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import theropod
from _digidetail import armour, metal, riveted, scales, solid
from _route import pal, tone

HEIGHT = 48
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a squat dark-green armoured dragon soldier in digital camo with a red horned helmet, a riot shield with yellow "
        "sawtooth markings and a heavy grenade-launcher rifle")
BASE = {"green": (40, 70, 60), "green_dark": (16, 30, 26), "green_light": (90, 130, 120), "camo": (70, 110, 150),
        "red": (190, 40, 40), "red_dark": (110, 14, 18), "black": (30, 28, 32), "yellow": (240, 200, 40),
        "steel": (170, 174, 186), "steel_dark": (80, 84, 96), "eye": (250, 200, 40), "mouth": (90, 20, 30),
        "tooth": (250, 250, 240)}
SHINY = {"green": (150, 130, 80), "green_dark": (90, 70, 30), "camo": (180, 150, 100)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "green", "green_dark", light="green_light", trim="black", trim_w=0.3)


def camof(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (int(x * 0.8) * 3 + int(y * 0.8) * 7 + int(z * 0.8) * 5) % 5 == 0:
        return tone(p["camo"], face), None
    return ARM0(x, y, z, face, variant, box=box, **k)


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        u = y - box.lo[1]
        if abs(((u * 0.7) % 2.0) - 1.0) * 1.6 > abs(x - box.lo[0] - box.size[0] / 2) - 1.0 and abs(x - box.lo[0] - box.size[0] / 2) < 3.0:
            return tone(p["yellow"], face), None
    return riveted(P, "green", "green_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("hicommandramon")
    mats = {"skin": camof, "belly": camof, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"),
            "claw": metal(P, "steel", dark="steel_dark"), "talon": metal(P, "steel", dark="steel_dark")}
    a = theropod(m, mats, "hicommandramon", hip_y=14.0, chest=(0, 26.0, -1.0), body_r=6.6, chest_r=6.4,
                 neck_top=(0, 32.0, -3.0), head_len=8.0, head_w=3.6, head_h=4.0, mouth_open=10, teeth=4, arm_len=8.0,
                 leg_bulk=1.3, tail=((0, 14, 7), (0, 11, 14), (2, 9, 20)), tail_r=(3.6, 2.6, 1.4), digitigrade=False)
    hd, bd = a["head"], a["body"]
    hc = a["head_c"]
    m.round_box(hd, hc[0], hc[2], 4.4, 5.0, hc[1] + 0.4, hc[1] + 5.4, armour(P, "red", "red_dark", trim="black"), cut=1)
    spike(m, hd, (0, hc[1] + 3.0, hc[2] - 5.0), (0, 0.6, -1), 2.4, 6.0, solid(P, "black"), tip=0.9)
    for j in range(6):
        spike(m, hd, (0, hc[1] + 4.6, hc[2] + 2.0 + j * 0.6), ((j - 2.5) * 0.3, 1, 0.6), 0.8, 3.0, solid(P, "yellow"), tip=0.8)
    al = a["arm_left"]                                                                    # riot shield
    m.box(al["bone"], al["hand"][0] + 1.0, 14.0, -10.0, al["hand"][0] + 2.0, 38.0, 2.0, shieldf,
          rotation=(0, -70, 0), pivot=(al["hand"][0] + 1.5, 26.0, -4.0))
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                                 # grenade launcher
    rod(m, ar, (h[0] + 4.0, h[1] + 2.0, h[2] + 4.0), (h[0] - 2.0, h[1], h[2] - 16.0), 3,
        metal(P, "steel", dark="steel_dark"), extend=0)
    m.round_box(ar, h[0], h[2] - 4.0, 2.0, 3.0, h[1] - 2.0, h[1] + 2.0, metal(P, "black"), cut=1)
    return m
