"""Vikemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the viking beast of the frozen seas: a huge white-furred walrus-yeti with a stern bearded face and
tusks, a horned helm, a heavy golden fur mantle, leather straps and a red loincloth, a round studded shield, two
spiked morning-star flails on chains slung over its back, and great clawed fists and feet. 35 blocks.

Front is -z, y is up. Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, leather, metal, plane, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a huge white-furred viking beast with a horned helm, a golden fur mantle, a round studded shield and two spiked flails"
BASE = {"white": (240, 242, 248), "white_dark": (180, 184, 200), "gold": (220, 190, 110), "gold_dark": (150, 120, 50),
        "leather": (90, 60, 40), "leather_dark": (50, 30, 18), "red": (190, 40, 30), "iron": (80, 84, 96),
        "iron_dark": (30, 32, 40), "brass": (230, 190, 80), "eye": (90, 160, 230), "claw": (50, 50, 56),
        "tusk": (250, 246, 230)}
SHINY = {"white": (190, 170, 140), "white_dark": (130, 110, 80), "gold": (150, 160, 190), "gold_dark": (90, 100, 130)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=2.0)
MANTLE = fur(P, "gold", "gold_dark", length=2.4)
IRON = metal(P, "iron", dark="iron_dark")


def shieldf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if box is not None and face in ("east", "west"):
        cy = box.lo[1] + box.size[1] / 2
        cz = box.lo[2] + box.size[2] / 2
        d = math.hypot(y - cy, z - cz)
        if d < 2.0 or abs(d - 4.6) < 0.5:
            return tone(p["brass"], face), None
        if abs(d - 3.4) < 0.5 and int(math.atan2(y - cy, z - cz) * 3.0) % 2 == 0:
            return tone(p["brass"], face), None
    return metal(P, "iron", dark="iron_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("vikemon")
    mats = {"skin": FUR, "chest": FUR, "abs": FUR, "pelvis": leather(P, "leather", "leather_dark"), "deltoid": FUR,
            "upper_arm": FUR, "forearm": FUR, "hand": FUR, "finger": FUR, "claw": solid(P, "claw"), "thigh": FUR,
            "knee": FUR, "shin": FUR, "calf": FUR, "foot": FUR, "talon": solid(P, "claw"), "neck": FUR}
    a = humanoid(m, mats, bulk=1.6, arm_bulk=1.5, leg_bulk=1.5, claws=True, talons=True, name="vikemon")
    bd = a["body"]
    m.box(bd, -2.4, 18.0, -6.0, 2.4, 31.0, -5.0, fabric(P, "red", "red"))                  # loincloth
    m.round_box(bd, 0, 0, 7.6, 5.6, 29.6, 32.0, leather(P, "leather", "leather_dark"), cut=1)
    m.round_box(bd, 0, 1.0, 9.0, 6.6, 46.0, 55.0, MANTLE, cut=3)                          # golden fur mantle
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.6, 3.6, 54.0, 61.0, FUR, cut=1)
    m.round_box(hd, 0, 0, 3.8, 3.8, 59.0, 62.4, IRON, cut=1)                              # horned helm
    for sx in (-1, 1):
        pts = [(sx * 3.6, 61.0, 0), (sx * 6.0, 63.0, 0), (sx * 6.6, 66.0, -0.6)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "tusk"), extend=0.3)
        m.box(hd, min(sx * 0.8, sx * 2.2), 58.0, -4.3, max(sx * 0.8, sx * 2.2), 58.8, -4.0, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 1.2, 55.0, -4.0), (0, -1, -0.3), 1.0, 3.6, solid(P, "tusk"), tip=0.8)
    h = a["arm_left"]["hand"]                                                           # round shield
    m.box(a["arm_left"]["bone"], h[0] + 2.0, h[1] - 3.0, h[2] - 6.0, h[0] + 3.4, h[1] + 9.0, h[2] + 6.0, shieldf)
    fb = m.bone("flails", bd, (0, 52, 6))                                               # two morning stars
    for sx in (-1, 1):
        rod(m, fb, (sx * 2.0, 44.0, 6.0), (sx * 8.0, 62.0, 7.0), 1, solid(P, "leather"), extend=0.0)
        for j in range(3):
            ball(m, fb, (sx * (8.6 + j * 0.8), 63.0 + j * 1.6, 7.0), 0.6, IRON, layers=1)
        c = (sx * 11.0, 69.0, 7.0)
        ball(m, fb, c, 2.6, IRON, layers=2)
        for j in range(8):
            ang = j * math.pi / 4
            spike(m, fb, (c[0] + 2.2 * math.cos(ang), c[1] + 2.2 * math.sin(ang), c[2]), (math.cos(ang), math.sin(ang), 0),
                  0.9, 1.8, IRON, tip=0.8)
    return m
