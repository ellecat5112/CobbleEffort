"""Brigadramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the airborne cyborg dragon. A crouching blue armoured dragon-man with a red-crested helm and an
orange visor, a huge rotor pack on its back (twin rotor booms with yellow-ringed engine pods and tail fins), a long
anti-materiel rifle held low, black hoses coiled round its hip, armoured clawed feet and dark grey joints.
35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a blue armoured cyborg dragon-man with a red-crested helm and orange visor, a rotor pack of twin booms and "
        "engine pods, a long rifle and coiled black hoses")
BASE = {"blue": (40, 100, 190), "blue_dark": (14, 44, 110), "blue_light": (110, 170, 240), "grey": (90, 92, 104),
        "grey_dark": (40, 42, 50), "steel": (204, 208, 220), "steel_dark": (90, 94, 106), "red": (210, 40, 40),
        "yellow": (250, 210, 40), "orange": (250, 140, 40), "black": (30, 30, 36), "white": (240, 240, 246)}
SHINY = {"blue": (60, 140, 70), "blue_dark": (20, 70, 30), "blue_light": (130, 210, 140), "yellow": (240, 120, 200)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = armour(P, "blue", "blue_dark", light="blue_light", rivets=True)
GREY = metal(P, "grey", dark="grey_dark")
STEEL = metal(P, "steel", dark="steel_dark")


def build():
    m = Model("brigadramon")
    mats = {"skin": GREY, "chest": BLUE, "abs": GREY, "pelvis": BLUE, "deltoid": BLUE, "upper_arm": GREY,
            "forearm": BLUE, "hand": GREY, "finger": GREY, "claw": STEEL, "thigh": BLUE, "knee": STEEL,
            "shin": BLUE, "calf": BLUE, "foot": BLUE, "talon": STEEL}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.3, digitigrade=True, claws=True, talons=True,
                 name="brigadramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.0, 2.8, 3.2, 54.4, 60.6, BLUE, cut=1)
    m.box(hd, -2.0, 54.4, -6.8, 2.0, 57.0, -3.6, BLUE)                                   # dragon snout
    m.box(hd, -2.4, 57.2, -4.4, 2.4, 58.6, -3.6, solid(P, "orange", glow=True))         # visor
    for i in range(5):                                                                  # red crest
        spike(m, hd, (0, 60.4, -2.6 + i * 1.4), (0, 1, 0.6), 1.2, 3.4 - abs(i - 2) * 0.5, solid(P, "red"))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.6, 59.0, 0.8), (sx * 0.5, 0.6, 1), 1.4, 4.0, STEEL)
    # the rotor pack: a hump on the back, twin booms out to engine pods, tail fins
    m.round_box(bd, 0, 6.0, 5.0, 3.0, 40.0, 54.0, BLUE, cut=2)
    for sx in (-1, 1):
        rod(m, bd, (sx * 4.0, 54.0, 6.0), (sx * 20.0, 60.0, 6.0), 2, STEEL, extend=0.4)
        pod = (sx * 13.0, 58.0, 6.0)
        m.round_box(bd, pod[0], pod[2], 3.4, 4.6, pod[1] - 3.0, pod[1] + 3.4, BLUE, cut=1)
        for dz in (-2.0, 2.0):
            m.box(bd, pod[0] - 3.6, pod[1] - 2.0, pod[2] + dz - 0.6, pod[0] + 3.6, pod[1] + 2.0, pod[2] + dz + 0.6,
                  solid(P, "yellow"))
        tip = (sx * 21.0, 60.0, 6.0)
        m.round_box(bd, tip[0], tip[2], 1.2, 1.2, tip[1] - 1.0, tip[1] + 1.0, solid(P, "black"), cut=1)
        for d in ((0, 1, 0), (0, -1, 0), (0, 0, 1)):
            spike(m, bd, (sx * 19.0, 60.0, 6.0), d, 0.6, 3.0, STEEL)
    rot = m.bone("spin_rotor", bd, (0, 56, 6))
    m.box(rot, -0.6, 55.0, 5.4, 0.6, 58.0, 6.6, STEEL)
    for ang in (0, 90):
        m.box(rot, -18.0, 57.8, 5.6, 18.0, 58.2, 6.4, solid(P, "grey_dark"), rotation=(0, ang, 0), pivot=(0, 58, 6))
    for sx in (-1, 1):                                                                  # back jet fins
        spike(m, bd, (sx * 3.0, 50.0, 8.0), (sx * 0.4, 0.8, 1), 2.4, 6.0, BLUE)
    # black hoses coiled round its right hip
    for i in range(10):
        ang = math.radians(i * 36)
        c = (-6.0 + 3.0 * math.cos(ang), 30.0 + 3.0 * math.sin(ang), 3.0)
        n = (-6.0 + 3.0 * math.cos(ang + 0.63), 30.0 + 3.0 * math.sin(ang + 0.63), 3.0)
        rod(m, bd, c, n, 1, solid(P, "black"), extend=0.3)
    # the long rifle held low across the body
    ar = a["arm_right"]
    h = ar["hand"]
    gb = m.bone("rifle", ar["bone"], h)
    rod(m, gb, (h[0], h[1] + 2.0, h[2] + 6.0), (h[0] + 6.0, h[1] - 10.0, h[2] - 16.0), 2, solid(P, "black"),
        extend=0)
    m.box(gb, h[0] - 1.4, h[1] - 2.0, h[2] - 2.0, h[0] + 1.4, h[1] + 2.6, h[2] + 4.0, GREY)
    rod(m, gb, (h[0] + 6.0, h[1] - 10.0, h[2] - 16.0), (h[0] + 8.0, h[1] - 14.0, h[2] - 24.0), 1, STEEL, extend=0)
    return m
