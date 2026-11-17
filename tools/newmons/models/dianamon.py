"""Dianamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Olympus goddess of the moon. A slender knight in white and pale-silver armour with deep-blue
crescent trims, a helm crowned by two tall rabbit-ear blades and a crescent moon, a white veil streaming behind, a
long staff ending in great curved crescent blades, crescent blades sweeping from its back like a halo and tall
pointed armoured boots. Its official design is kept as drawn. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import cape, humanoid
from _digidetail import armour, fabric, metal, skin, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a slender moon knight in white and silver armour with blue crescent trims, a helm with rabbit-ear blades and a "
        "crescent moon, a white veil, a crescent-bladed staff and crescent blades fanning from its back")
BASE = {"white": (240, 242, 248), "white_dark": (170, 176, 196), "white_light": (255, 255, 255), "blue": (40, 60, 160),
        "blue_dark": (14, 20, 80), "silver": (210, 214, 226), "silver_dark": (110, 114, 130), "black": (30, 30, 36),
        "skin": (240, 220, 210), "skin_dark": (190, 160, 150), "gold": (240, 200, 70), "eye": (60, 80, 200)}
SHINY = {"blue": (120, 40, 160), "blue_dark": (50, 10, 80), "white": (250, 236, 220)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "white", "white_dark", light="white_light", trim="blue", trim_w=0.35)
SILVER = metal(P, "silver", dark="silver_dark")
BLUE = armour(P, "blue", "blue_dark")


def crescent(m, bone, c, r, a0, a1, n, t, shader, plane="xy"):
    """A crescent blade: rods along an arc of radius r from angle a0 to a1 (degrees), thinning toward the tips."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        if plane == "xy":
            pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]))
        else:
            pts.append((c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)))
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        mid = 1 - abs(i / max(n - 1, 1) - 0.5) * 2
        rod(m, bone, p0, p1, 1, shader, extend=0.5, t2=max(1, round(1 + t * mid)))


def build():
    m = Model("dianamon")
    mats = {"skin": PLATE, "chest": PLATE, "abs": solid(P, "black"), "pelvis": PLATE, "neck": solid(P, "black"),
            "deltoid": PLATE, "upper_arm": solid(P, "black"), "forearm": PLATE, "hand": PLATE, "finger": PLATE,
            "thigh": PLATE, "knee": BLUE, "shin": PLATE, "calf": PLATE, "foot": PLATE, "toe": PLATE}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.85, leg_bulk=0.95, name="dianamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.2, 2.4, 2.8, 54.0, 60.0, PLATE, cut=1)                       # helm
    m.box(hd, -1.6, 56.6, -3.0, 1.6, 57.4, -2.8, solid(P, "eye", glow=True))
    for sx in (-1, 1):                                                                 # rabbit-ear blades
        pts = [(sx * 1.6, 59.6, 0.4), (sx * 3.0, 64.0, 1.0), (sx * 4.0, 70.0, 2.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 1, PLATE, extend=0.4, t2=3 - j)
    crescent(m, hd, (0, 61.0, -2.4), 2.6, 200, 340, 6, 2, solid(P, "gold"))            # crescent crown
    cape(m, bd, 58.0, 9.0, 34.0, fabric(P, "white", "white_dark"), z=3.2, flare=0.8)   # veil
    for side in (1, -1):                                                               # crescent halo blades
        crescent(m, bd, (0, 48.0, 5.0), 16.0, 90 - side * 20, 90 - side * 80, 7, 3, SILVER)
        crescent(m, bd, (0, 40.0, 6.0), 20.0, 90 - side * 40, 90 - side * 100, 7, 3, SILVER)
    ar = a["arm_right"]                                                                # crescent staff
    hx, hy, hz = ar["hand"]
    rod(m, ar["bone"], (hx, hy - 20.0, hz), (hx, hy + 22.0, hz), 1, BLUE, extend=0)
    crescent(m, ar["bone"], (hx, hy + 22.0, hz), 7.0, 200, 340, 6, 3, SILVER)
    crescent(m, ar["bone"], (hx, hy - 20.0, hz), 6.0, 20, 160, 6, 3, SILVER)
    for nm in ("leg_left", "leg_right"):                                               # pointed boots
        ak = a[nm]["ankle"]
        spike(m, a[nm]["bone"], (ak[0], 1.0, ak[2] - 3.0), (0, 0, -1), 1.6, 4.0, PLATE, tip=0.4)
    return m
