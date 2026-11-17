"""Dominimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the dominion angel. A tall knight in silver armour with gold filigree and a gold cross on its chest,
a silver helm with a spray of golden blades, long gold sash ribbons trailing from its waist, tall blue greaves, a
blade of green light in one hand, golden feather wings and two great blue shield-wings framed in gold standing at
its shoulders. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing
from _digibody import humanoid
from _digidetail import armour, fabric, feathers, local, metal, solid
from _route import pal, tone

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall silver-armoured angel knight with gold filigree, a helm of golden blades, gold sash ribbons, blue "
        "greaves, a green light blade, golden feather wings and two great gold-framed blue shield-wings")
BASE = {"silver": (220, 224, 236), "silver_dark": (120, 124, 140), "silver_light": (255, 255, 255),
        "gold": (240, 200, 70), "gold_dark": (170, 120, 20), "blue": (40, 70, 180), "blue_dark": (14, 26, 90),
        "blue_light": (110, 150, 240), "white": (246, 246, 250), "white_dark": (190, 194, 210),
        "green": (90, 250, 120, 220), "feather": (250, 220, 120), "feather_dark": (200, 150, 40)}
SHINY = {"blue": (150, 40, 60), "blue_dark": (70, 10, 20), "blue_light": (230, 120, 130)}


def P(v):
    return pal(BASE, SHINY, v)


SILVER = armour(P, "silver", "silver_dark", light="silver_light", trim="gold", trim_w=0.25)
BLUE = armour(P, "blue", "blue_dark", light="blue_light", trim="gold", trim_w=0.4)
GOLD = metal(P, "gold", dark="gold_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and ((abs(x) < 0.5 and 43.0 < y < 50.0) or (abs(y - 47.6) < 0.5 and abs(x) < 2.4)):
        return tone(p["gold"], face), None
    return SILVER(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("dominimon")
    mats = {"skin": SILVER, "chest": chestf, "abs": fabric(P, "white", "white_dark"), "pelvis": SILVER, "neck": SILVER,
            "deltoid": SILVER, "upper_arm": SILVER, "forearm": SILVER, "hand": SILVER, "finger": SILVER,
            "thigh": fabric(P, "white", "white_dark"), "knee": BLUE, "shin": BLUE, "calf": BLUE, "foot": BLUE,
            "toe": BLUE}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.9, leg_bulk=0.95, name="dominimon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.8, 54.0, 60.4, SILVER, cut=1)                       # helm
    for i in range(7):                                                                 # spray of golden blades
        ang = math.radians(-45 + i * 15)
        spike(m, hd, (0, 60.0, 0.0), (math.sin(ang), 1.0, 0.4), 1.0, 7.0 - abs(i - 3) * 0.8, GOLD, tip=0.25)
    for sx in (-1, 1):                                                                 # gold sash ribbons
        pts = [(sx * 3.0, 33.0, -3.0), (sx * 5.0, 22.0, -2.0), (sx * 7.0, 12.0, 1.0), (sx * 6.0, 2.0, 4.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, bd, p0, p1, 1, GOLD, extend=0.5, t2=3)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.6))
        feather_wing(m, wb, (side * 3.0, 50.0, 3.6), 18.0, 12.0, 2, feathers(P, "feather", "feather_dark"), side=side,
                     sweep=25, droop=-8.0)
        sb = m.bone("shield_" + ("left" if side > 0 else "right"), bd, (side * 8.0, 52.0, 2.0))
        x0, x1 = sorted((side * 9.0, side * 19.0))                                     # blue shield-wings
        m.box(sb, x0, 34.0, 0.6, x1, 66.0, 2.0, BLUE, rotation=(0, side * 20, side * 12), pivot=(side * 9.0, 52.0, 1.0))
    ar = a["arm_right"]                                                                # green light blade
    hx, hy, hz = ar["hand"]
    rod(m, ar["bone"], (hx, hy, hz), (hx - 2.0, hy - 24.0, hz - 8.0), 1, solid(P, "green", glow=True), extend=0, t2=2)
    return m
