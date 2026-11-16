"""Algomon (Ultimate) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a crouching armoured hunter in navy-black plate with green-lit edges, a horned helmet,
a great wild mane of lime-green spines streaming from its head and shoulders, heavy green claws, grey armoured legs
with glowing yellow knee lamps and a long whip-crest. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _algo import P, tentaclef
from _digidetail import armour, feathers, metal, solid, strands
from _route import tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 1.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a crouching armoured hunter in navy-black plate with green edges, a horned helmet, a wild mane of lime-green "
        "spines, heavy green claws and grey armoured legs with glowing yellow knee lamps")
NAVY = armour(P, "navy", "black", light="navy_light", trim="green")
NAVY_PLAIN = armour(P, "navy", "black", light="navy_light")
GREY = metal(P, "steel", dark="steel_dark", light="white")
GCLAW = metal(P, "green", dark="green_dark", light="green_light", streak=2.0)
MANE = strands(P, "feather", "feather_dark", tip="green_light")


def build():
    m = Model("algomonultimate")
    mats = {"skin": NAVY_PLAIN, "chest": NAVY, "abs": NAVY_PLAIN, "pelvis": NAVY, "neck": NAVY_PLAIN, "deltoid": NAVY,
            "upper_arm": NAVY_PLAIN, "forearm": NAVY, "hand": NAVY_PLAIN, "finger": GCLAW, "claw": GCLAW,
            "thigh": GREY, "knee": GREY, "shin": GREY, "calf": GREY, "foot": NAVY_PLAIN, "talon": GCLAW}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.25, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="algomonultimate", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 2.8, 3.2, 54.0, 60.6, NAVY, cut=1)
    m.box(hd, -1.8, 54.4, -6.8, 1.8, 57.6, -2.8, NAVY_PLAIN, rotation=(-6, 0, 0), pivot=(0, 56, -2.8))   # muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 58.0, -4.2, sx * 1.4 + 0.6, 58.8, -3.2, solid(P, "eye_y", glow=True))
        rod(m, hd, (sx * 2.0, 60.0, -1.0), (sx * 4.0, 64.5, 2.5), 1, GCLAW, extend=0.2)  # horns
    spike(m, hd, (0, 60.4, -3.0), (0, 1, -0.6), 1.6, 3.4, GCLAW, tip=0.5)
    mane = m.bone("mane", hd, (0, 58, 2))
    for i in range(22):                                          # the wild green mane streaming up and back
        ang = math.radians(-100 + i * (200 / 21))
        base = (3.0 * math.sin(ang), 57.0 + 2.0 * math.cos(ang), 2.0)
        ln = 14.0 + (i % 4) * 3
        tip = (base[0] + ln * 0.8 * math.sin(ang), base[1] + ln * 0.55 * abs(math.cos(ang)) + 3, base[2] + ln * 0.75)
        rod(m, mane, base, tip, 3 if i % 2 else 2, MANE, extend=0.3, t2=2)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):           # big shoulder plates with spines behind
        ab = a[nm]["bone"]
        sh = a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.0, 0.2), 4.4, 4.0, NAVY, layers=4)
        for j in range(4):
            spike(m, ab, (sh[0] + sx * 2.0, 52.0, 1.0 + j), (sx * 0.6, 0.6, 0.6), 2.0, 7.0 + j, MANE, tip=1.0)
        el, wr = a[nm]["elbow"], a[nm]["wrist"]
        shell(m, ab, (wr[0], 0, wr[2]), 2.2, 29.0, 36.0, -150 if sx < 0 else 30, -30 if sx < 0 else 150, 4, 1.0, NAVY)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):           # yellow knee lamps and green-lit knee plates
        lg, kn = a[nm]["bone"], a[nm]["knee"]
        dome(m, lg, (kn[0], 18.0, kn[2] - 0.6), 2.6, 2.4, NAVY, layers=2)
        m.round_box(lg, kn[0], kn[2] - 2.6, 1.2, 0.8, 17.4, 19.8, solid(P, "eye_y", glow=True), cut=1)
    shell(m, bd, (0, 0, 0.6), 5.2, 42.0, 51.0, -80, 80, 8, 1.0, NAVY)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32, 3), (0, 26, 10), (2, 18, 16), (5, 12, 22), (8, 8, 28)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - j * 0.5, NAVY_PLAIN, extend=0.5)
    spike(m, tl, pts[-1], (0.4, -0.3, 1), 1.6, 3.0, GCLAW)
    return m
