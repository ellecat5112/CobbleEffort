"""Bio Stegomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a Bio Hybrid stegosaur. A green body spotted with dark green, red-orange stripes and steel ring
bands on its legs, two rows of tall black-and-steel plates along its back, a red pointed head with a sharp beak, a
glass capsule on its back and a tail tipped with spikes. 15 blocks tall.

Front is -z, y is up. 38 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, gem, metal, plane, scales, skin, solid
from _route import pal, tone

HEIGHT = 38
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a Bio Hybrid stegosaur: a spotted green body with red-orange stripes, steel leg bands, two rows of tall black "
        "plates, a red pointed head, a glass capsule on its back and a spiked tail")
BASE = {"green": (60, 140, 50), "green_dark": (24, 80, 20), "spot": (30, 90, 30), "stripe": (230, 90, 40),
        "black": (40, 40, 48), "black_light": (150, 150, 170), "steel": (190, 194, 206), "steel_dark": (90, 94, 106),
        "red": (210, 40, 40), "red_dark": (130, 14, 20), "glass": (90, 200, 160, 200), "glass_light": (210, 255, 240),
        "mouth": (100, 20, 20), "tooth": (250, 250, 246), "eye": (255, 220, 60)}
SHINY = {"green": (140, 100, 190), "green_dark": (80, 40, 130), "spot": (90, 50, 130), "red": (60, 140, 220),
         "red_dark": (20, 70, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    a, b = plane(x, y, z, face)
    if face in ("east", "west") and abs(((z + y * 0.4) % 6.0) - 3.0) < 0.5:
        return tone(p["stripe"], face), None
    if math.hypot((a % 3.0) - 1.5, (b % 3.0) - 1.5) < 0.6 and (round(a / 3) + round(b / 3)) % 2:
        return tone(p["spot"], face), None
    return skin(P, "green", dark="green_dark")(x, y, z, face, variant, box=box, **k)


PLATE = armour(P, "black", "black", light="black_light")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("biostegomon")
    mats = {"skin": bodyf, "belly": bodyf, "neck": bodyf, "head": armour(P, "red", "red_dark"),
            "snout": armour(P, "red", "red_dark"), "jaw": armour(P, "red", "red_dark"), "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": bodyf, "leg_lower": bodyf, "paw": bodyf, "claw": PLATE,
            "tail": bodyf}
    a = quadruped(m, mats, "biostegomon", length=28.0, body_y=16.0, body_rx=7.0, body_ry=7.0, chest_bulk=0.9,
                  neck=((0, 12, -16), (0, 10, -19)), head_len=9.0, head_w=3.2, head_h=3.4, snout=0.9, mouth_open=6,
                  teeth=3, leg_bulk=1.5, toes=3, tail=((0, 16, 18), (0, 13, 24), (2, 11, 30)), tail_r=(2.4, 1.8, 1.2))
    bd = a["body"]
    for j in range(7):                                           # two rows of tall plates
        t = j / 6
        z = -12.0 + 24.0 * t
        h = 8.0 + 6.0 * math.sin(t * math.pi)
        for sx in (-1, 1):
            m.box(bd, sx * 1.6 - 0.5, 22.0, z - 2.4, sx * 1.6 + 0.5, 22.0 + h, z + 2.4, PLATE,
                  rotation=(0, 0, sx * 12), pivot=(sx * 1.6, 22.0, z))
    m.round_box(bd, -4.0, -6.0, 1.4, 1.4, 22.0, 27.0, gem(P, "glass", "glass_light"), cut=1)   # glass capsule
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):
        w = a[nm]["wrist"]
        m.round_box(a[nm]["bone"], w[0], w[2], 2.8, 2.8, 8.0, 9.4, STEEL, cut=1)
    tl = a["tail"]
    e = a["tail_pts"][-1]
    for d in ((1, 0.6, 0.4), (-1, 0.6, 0.4), (0.6, 1, 0.6), (-0.6, 1, 0.6)):
        spike(m, tl, e, d, 1.2, 4.0, STEEL)
    return m
