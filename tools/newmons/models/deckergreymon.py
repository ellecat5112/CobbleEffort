"""Decker Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Greymon and Deckerdramon combined. An armoured blue dragon warrior rising out of a brown tracked
tank chassis, its head a blue Greymon helm with steel horns and a red visor, a steel bolt-studded chest, a cannon on
each arm, a fan of red spikes and missile tubes on its back, and huge blue crescent claw-blades on its shoulders.
25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, metal, riveted, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("an armoured blue dragon warrior rising out of a brown tracked tank chassis, with a Greymon helm, arm cannons, red "
        "back spikes, missile tubes and blue crescent shoulder blades")
BASE = {"blue": (40, 80, 180), "blue_dark": (14, 30, 90), "blue_light": (120, 160, 240), "brown": (120, 96, 70),
        "brown_dark": (60, 44, 30), "brown_light": (190, 160, 120), "steel": (200, 204, 214), "steel_dark": (90, 94, 104),
        "black": (40, 40, 46), "black_dark": (12, 12, 16), "red": (220, 40, 40), "green": (80, 230, 120)}
SHINY = {"blue": (170, 40, 40), "blue_dark": (80, 10, 10), "blue_light": (240, 130, 120)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="steel", trim_w=0.3)
HULL = armour(P, "brown", "brown_dark", light="brown_light", rivets=True)
STEEL = metal(P, "steel", dark="steel_dark")
TRACK = riveted(P, "black", "black_dark", spacing=1.6)


def build():
    m = Model("deckergreymon")
    mats = {"skin": BLUE, "chest": riveted(P, "steel", "steel_dark"), "abs": BLUE, "pelvis": HULL, "neck": BLUE,
            "deltoid": BLUE, "upper_arm": BLUE, "forearm": STEEL, "hand": BLUE, "finger": BLUE, "claw": STEEL,
            "thigh": HULL, "knee": HULL, "shin": HULL, "calf": HULL, "foot": TRACK, "toe": TRACK}
    a = humanoid(m, mats, bulk=1.25, arm_bulk=1.3, leg_bulk=1.5, claws=True, name="deckergreymon")
    bd = a["body"]
    top = a["top"]
    m.round_box(top, 0, 0, 9.0, 10.0, 8.0, 18.0, HULL, cut=2)                          # tank chassis
    for sx in (-1, 1):                                                                 # tracks with road wheels
        x0, x1 = sorted((sx * 8.0, sx * 11.0))
        m.round_box(top, (x0 + x1) / 2, 0, 1.6, 11.0, 0.0, 8.0, TRACK, cut=1)
        for j in range(5):
            x0, x1 = sorted((sx * 11.0, sx * 11.6))
            m.round_box(top, (x0 + x1) / 2, -8.0 + j * 4.0, 0.3, 1.6, 2.4, 5.6, STEEL, cut=0)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -2.0, 3.4, 5.0, 53.0, 60.0, BLUE, cut=1)                         # Greymon helm
    m.box(hd, -3.0, 56.0, -7.2, 3.0, 57.0, -6.6, solid(P, "red", glow=True))             # visor
    spike(m, hd, (0, 58.0, -6.0), (0, 0.6, -1), 1.6, 4.0, STEEL, tip=0.4)                # nose horn
    for sx in (-1, 1):
        spike(m, hd, (sx * 3.0, 59.0, 0), (sx * 0.6, 1, 0.5), 1.6, 6.0, STEEL, tip=0.3)
    for nm in ("arm_left", "arm_right"):                                               # arm cannons
        ar = a[nm]
        el, hx = ar["elbow"], ar["hand"]
        rod(m, ar["bone"], (el[0], el[1] - 2.0, el[2] - 1.0), (hx[0], hx[1] + 2.0, hx[2] - 12.0), 3, STEEL, extend=0.5)
        m.round_box(ar["bone"], hx[0], hx[2] - 12.0, 1.0, 1.0, hx[1] + 1.4, hx[1] + 2.8, solid(P, "black"), cut=0)
    for sx in (-1, 1):                                                                 # crescent shoulder blades
        pts = [(sx * 8.0, 52.0, 0), (sx * 13.0, 56.0, -3.0), (sx * 16.0, 54.0, -8.0), (sx * 15.0, 50.0, -12.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, BLUE, extend=0.5, t2=4)
        dome(m, bd, (sx * 8.0, 50.0, 0), 4.0, 3.0, BLUE)
    for i in range(6):                                                                 # back spikes + missile tubes
        ang = math.radians(-50 + i * 20)
        spike(m, bd, (2.0 * math.sin(ang), 48.0, 3.6), (math.sin(ang), 0.8, 0.6), 1.4, 7.0, solid(P, "red"), tip=0.3)
    for sx in (-1, 1):
        for j in range(2):
            rod(m, bd, (sx * (3.0 + j * 2.0), 44.0, 4.0), (sx * (4.0 + j * 2.0), 60.0, 8.0), 2, STEEL, extend=0)
    return m
