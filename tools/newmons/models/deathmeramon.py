"""Death Meramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the blue-flame brawler. A hulking man of flesh-toned flame whose head is a wild crown of dark
blue fire round a scowling face, his torso and arms bound in heavy steel chains, fists wreathed in pale blue fire,
black trousers with red flame patterns, black-and-white striped shins and big steel boots with skull caps. Its
official design is kept as drawn. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fabric, flame_inside, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a hulking flame man with a crown of dark blue fire, steel chains round his torso and arms, fists wreathed in "
        "blue fire, flame-patterned black trousers, striped shins and skull-capped steel boots")
BASE = {"flesh": (220, 150, 120), "flesh_dark": (150, 80, 70), "flesh_light": (250, 200, 170), "blue": (60, 80, 200),
        "blue_dark": (20, 24, 90), "flame": (150, 190, 255, 210), "flame_core": (235, 245, 255, 240),
        "black": (34, 34, 40), "black_dark": (10, 10, 14), "red": (220, 60, 30), "white": (240, 240, 244),
        "steel": (200, 204, 216), "steel_dark": (100, 104, 116), "eye": (250, 240, 120), "mouth": (40, 10, 20)}
SHINY = {"flesh": (150, 160, 200), "flesh_dark": (80, 90, 140), "blue": (220, 90, 40), "blue_dark": (120, 30, 10),
         "flame": (255, 180, 80, 210)}


def P(v):
    return pal(BASE, SHINY, v)


FLESH = skin(P, "flesh", dark="flesh_dark", light="flesh_light", var=0.06)
STEEL = metal(P, "steel", dark="steel_dark")
PANTS = fabric(P, "black", "black_dark", axis="y")


def pantsf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "north") and abs((y * 0.8 + abs(x) * 1.4) % 5.0 - 2.5) < 0.5 and y > 20:
        return tone(p["red"], face), None
    return PANTS(x, y, z, face, variant, box=box, **k)


def stripef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["white"] if y % 2.4 < 1.2 else p["black"], face), None


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.2) < 0.7 and abs(y - 58.4) < 0.35:
                return p["eye"], p["eye"]
        if abs(y - 56.0) < 0.35 and abs(x) < 1.6:
            return tone(p["mouth"], face), None
    return FLESH(x, y, z, face, variant, box=box, **k)


def chain_loop(m, bone, cy, rx, rz, n, tilt=0.0):
    for i in range(n):
        ang = 2 * math.pi * i / n
        x, z = rx * math.sin(ang), -rz * math.cos(ang)
        y = cy + tilt * math.sin(ang)
        a, b = (0.5, 0.9) if i % 2 else (0.9, 0.5)
        m.box(bone, x - a, y - 0.6, z - b, x + a, y + 0.6, z + b, STEEL)


def build():
    m = Model("deathmeramon")
    mats = {"skin": FLESH, "chest": FLESH, "abs": FLESH, "pelvis": pantsf, "neck": FLESH, "deltoid": FLESH,
            "upper_arm": FLESH, "forearm": FLESH, "hand": FLESH, "finger": FLESH, "thigh": pantsf, "knee": pantsf,
            "shin": stripef, "calf": stripef, "foot": STEEL, "toe": STEEL}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.4, leg_bulk=1.1, name="deathmeramon")
    bd = a["body"]
    for j in range(5):                                                               # chains round the torso
        chain_loop(m, bd, 37.0 + j * 3.2, 6.6 + j * 0.3, 4.6, 18, tilt=1.6 * (-1) ** j)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.0, 60.0, headf, cut=1)
    for i in range(9):                                                               # crown of dark blue fire
        ang = math.radians(-120 + i * 30)
        spike(m, hd, (2.4 * math.sin(ang), 59.0, -2.4 * math.cos(ang) + 1.0),
              (math.sin(ang) * 0.6, 1.0, -math.cos(ang) * 0.4 + 0.3), 2.2, 6.0 + (i % 3) * 1.6,
              solid(P, "blue_dark"), tip=0.3)
    for nm in ("arm_left", "arm_right"):
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        el = ar["elbow"]
        for j in range(3):                                                           # chained arms
            chain_loop(m, ar["bone"], el[1] - 2.0 - j * 2.4, 2.8, 2.8, 10, tilt=0.6)
        m.round_box(ar["bone"], hx, hz, 2.4, 2.4, hy - 2.0, hy + 2.0, FLESH, cut=1)
        for ang in (0, 60, 120):                                                     # blue fire fists
            m.box(ar["bone"], hx - 3.4, hy - 2.0, hz, hx + 3.4, hy + 7.0, hz, cutout(flame_inside(4, 0, ang), flamef),
                  rotation=(0, ang, 0), pivot=(hx, hy, hz))
    for nm in ("leg_left", "leg_right"):
        lg = a[nm]
        ak = lg["ankle"]
        m.round_box(lg["bone"], ak[0], ak[2] - 1.0, 3.0, 4.4, 0.0, 6.0, STEEL, cut=1)    # big boots
        m.round_box(lg["bone"], ak[0], ak[2] - 5.4, 2.0, 0.8, 1.6, 4.6, solid(P, "white"), cut=0)  # skull caps
        for sx in (-1, 1):
            m.box(lg["bone"], ak[0] + sx * 0.8 - 0.4, 3.0, ak[2] - 6.4, ak[0] + sx * 0.8 + 0.4, 3.8, ak[2] - 6.0,
                  solid(P, "black"))
    return m
