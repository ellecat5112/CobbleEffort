"""Metal Etemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Etemon recast in chrome Chrondigizoit: a muscle-bound monkey of polished silver striking a flexing
pose, dark sunglasses, a smug grin, a red-and-gold chest emblem, a microphone in one fist, a little brown teddy bear
hanging at its hip, big flat feet and a long curling tail. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a muscle-bound chrome-silver monkey with dark sunglasses, a smug grin, a red-and-gold chest emblem, a "
        "microphone, a little teddy bear at its hip and a long curling tail")
BASE = {"chrome": (206, 212, 226), "chrome_dark": (110, 116, 136), "chrome_light": (250, 252, 255),
        "black": (24, 24, 30), "red": (210, 40, 40), "gold": (240, 200, 70), "bear": (150, 100, 60),
        "bear_dark": (90, 56, 30), "mouth": (110, 30, 40), "tooth": (250, 230, 120)}
SHINY = {"chrome": (240, 200, 90), "chrome_dark": (160, 110, 30), "chrome_light": (255, 240, 180)}


def P(v):
    return pal(BASE, SHINY, v)


CHROME = metal(P, "chrome", dark="chrome_dark", light="chrome_light")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and abs(x) < 2.2 and 44.0 < y < 48.4:
        return tone(p["gold"] if abs(x) > 1.2 or y > 47.4 else p["red"], face), None
    return CHROME(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("metaletemon")
    mats = {"skin": CHROME, "chest": chestf}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.4, leg_bulk=1.2, hand_pose="fist", name="metaletemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    ball(m, hd, (0, 58.0, -0.2), 3.4, CHROME, layers=5, ry=3.4)
    m.round_box(hd, 0, -3.2, 2.2, 1.0, 55.0, 57.6, CHROME, cut=0)                         # muzzle
    m.box(hd, -2.6, 58.2, -3.5, 2.6, 59.4, -3.2, solid(P, "black"))                         # sunglasses
    m.box(hd, -1.6, 55.6, -4.3, 1.6, 56.4, -4.2, solid(P, "tooth"))                         # gold-toothed grin
    for sx in (-1, 1):
        ball(m, hd, (sx * 3.6, 58.6, 0.0), 1.4, CHROME, layers=2, squash=0.5)              # ears
    ar = a["arm_right"]                                                                    # microphone
    h = ar["hand"]
    rod(m, ar["bone"], (h[0], h[1], h[2] - 1.0), (h[0], h[1] + 4.0, h[2] - 2.0), 1, solid(P, "black"), extend=0.2)
    ball(m, ar["bone"], (h[0], h[1] + 5.0, h[2] - 2.2), 1.2, metal(P, "chrome"), layers=2)
    bb = m.bone("bear", bd, (4.0, 31.0, -3.0))                                             # teddy bear at the hip
    ball(m, bb, (5.0, 28.0, -4.6), 1.8, fur(P, "bear", "bear_dark"), layers=3)
    ball(m, bb, (5.0, 31.2, -4.6), 1.4, fur(P, "bear", "bear_dark"), layers=2)
    for sx in (-1, 1):
        ball(m, bb, (5.0 + sx * 1.0, 32.4, -4.6), 0.6, fur(P, "bear", "bear_dark"), layers=1)
    tb = m.bone("tail", bd, (0, 31, 3))                                                    # curling tail
    pts = [(0, 31.0, 3.0)]
    for i in range(1, 10):
        t = i / 9
        pts.append((6.0 * math.sin(t * 2.4), 31.0 - 10.0 * t + 6.0 * math.sin(t * 5.0), 3.0 + 9.0 * t))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tb, p0, p1, 1, CHROME, extend=0.3, t2=1)
    for nm in ("leg_left", "leg_right"):                                                   # big flat feet
        anc = a[nm]
        ank = anc["ankle"]
        m.round_box(anc["bone"], ank[0], ank[2] - 3.0, 2.6, 4.4, 0.0, 1.6, CHROME, cut=1)
    return m
