"""Atlur Ballistamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a beetle-robot heavyweight. Steel-grey plate armour with blue and red panels, a beetle
helm with a tall hooked horn, round red shoulder pods, a huge grey right fist and an electrified left hand holding a
crackling blue orb, hoses at its back and heavy grey boots. 25 blocks tall.

Front is -z, y is up. 70 units tall (the horn); Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid, shell
from _digidetail import armour, gem, metal, riveted, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a beetle-robot heavyweight: steel-grey armour with blue and red panels, a hooked beetle horn, red shoulder "
        "pods, a huge grey fist and an electrified hand holding a blue orb")
BASE = {"grey": (170, 174, 186), "grey_dark": (80, 84, 96), "grey_light": (230, 234, 244), "blue": (50, 90, 200),
        "blue_dark": (20, 40, 120), "blue_light": (120, 160, 250), "red": (210, 40, 50), "red_dark": (120, 14, 24),
        "red_light": (250, 120, 120), "orb": (120, 220, 255), "orb_light": (230, 250, 255), "black": (30, 30, 36),
        "eye": (255, 230, 80)}
SHINY = {"blue": (40, 150, 80), "blue_dark": (16, 80, 40), "blue_light": (120, 230, 150), "red": (240, 170, 40),
         "red_dark": (170, 100, 20), "red_light": (255, 220, 130)}


def P(v):
    return pal(BASE, SHINY, v)


GREY = riveted(P, "grey", "grey_dark", light="grey_light")
STEEL = metal(P, "grey", dark="grey_dark", light="grey_light")
BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="grey_light")
RED = armour(P, "red", "red_dark", light="red_light")


def build():
    m = Model("atlurballistamon")
    mats = {"skin": STEEL, "chest": BLUE, "abs": RED, "pelvis": GREY, "neck": STEEL, "deltoid": RED,
            "upper_arm": STEEL, "forearm": RED, "hand": GREY, "finger": GREY, "thigh": GREY, "knee": RED,
            "shin": GREY, "calf": STEEL, "foot": GREY, "toe": GREY}
    a = humanoid(m, mats, bulk=1.15, arm_bulk=1.3, leg_bulk=1.4, name="atlurballistamon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 54.6, 60.6, BLUE, cut=1)
    m.box(hd, -2.0, 56.8, -3.5, 2.0, 58.0, -3.1, solid(P, "eye", glow=True))
    pts = [(0, 60.0, -1.0), (0, 65.0, -2.0), (0, 69.0, 0.0), (0, 70.0, 3.0), (0, 68.0, 4.0)]   # hooked horn
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 3 - j // 2, STEEL, extend=0.3)
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 59.0, 0.0), (sx * 0.6, 0.6, 0.4), 1.2, 3.0, STEEL)
    shell(m, bd, (0, 0, 0.6), 5.8, 42.0, 51.0, -85, 85, 9, 1.2, BLUE)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        ball(m, ab, (sh[0] + sx * 2.2, 49.0, 0.3), 4.6, RED, layers=4)
    ar = a["arm_right"]                                          # huge grey fist
    h = ar["hand"]
    m.round_box(ar["bone"], h[0], h[2], 4.0, 4.0, h[1] - 5.0, h[1] + 3.0, GREY, cut=1)
    al = a["arm_left"]                                           # electrified hand with a blue orb
    h = al["hand"]
    ball(m, al["bone"], (h[0] + 1.0, h[1] + 4.0, h[2] - 4.0), 3.0, gem(P, "orb", "orb_light"), layers=3)
    for j in range(5):
        ang = math.radians(j * 72)
        rod(m, al["bone"], (h[0] + 1.0, h[1] + 4.0, h[2] - 4.0),
            (h[0] + 1.0 + 6.0 * math.cos(ang), h[1] + 4.0 + 6.0 * math.sin(ang), h[2] - 4.0), 1,
            solid(P, "orb", glow=True), extend=0)
    for sx in (-1, 1):                                           # hoses at its back
        rod(m, bd, (sx * 3.0, 48.0, 4.0), (sx * 7.0, 40.0, 6.0), 1, solid(P, "black"), extend=0.3)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        an = a[nm]["ankle"]
        m.round_box(a[nm]["bone"], an[0], an[2] - 1.0, 3.6, 5.0, 0.0, 6.0, GREY, cut=1)  # heavy boots
    return m
