"""Bolgmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Hybrid mech of iron. A purple armoured war machine trimmed in gold: a horned helm with a yellow
visor, a great drum-shaped right shoulder of three gold-rimmed cannon ports round a yellow X emblem, back towers of
pincer horns, a rotary gatling cannon for a left arm, a heavy gold-ringed right gauntlet, and legs that end in steel
tank treads. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = ("a purple armoured war machine trimmed in gold: a horned helm with a yellow visor, a drum shoulder of cannon "
        "ports round a yellow X, a gatling-cannon arm and tank-tread feet")
BASE = {"purple": (90, 60, 170), "purple_dark": (36, 20, 80), "purple_light": (160, 130, 230), "gold": (246, 196, 50),
        "gold_dark": (170, 120, 20), "steel": (204, 208, 220), "steel_dark": (90, 94, 106), "black": (24, 22, 30),
        "yellow": (255, 230, 60), "under": (50, 46, 64)}
SHINY = {"purple": (60, 130, 90), "purple_dark": (20, 60, 36), "purple_light": (130, 210, 160), "gold": (220, 224, 236),
         "gold_dark": (130, 134, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PURPLE = armour(P, "purple", "purple_dark", light="purple_light", trim="gold", trim_w=0.4, rivets=True)
GOLD = metal(P, "gold", dark="gold_dark")
STEEL = metal(P, "steel", dark="steel_dark")
UNDER = solid(P, "under")


def treadf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    rib = ((z if face in ("east", "west", "up", "down") else y) % 1.8) < 0.7
    return tone(p["steel_dark"] if rib else p["steel"], face), None


def xf(x, y, z, face, variant, box=None, **k):
    """The yellow X emblem on the drum's face."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    if face in ("east", "west") and (abs(a - b) < 0.12 or abs(a + b) < 0.12) and abs(a) < 0.36:
        return tone(p["yellow"], face), None
    return PURPLE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bolgmon")
    mats = {"skin": UNDER, "chest": PURPLE, "abs": PURPLE, "pelvis": PURPLE, "neck": UNDER, "deltoid": PURPLE,
            "upper_arm": STEEL, "forearm": PURPLE, "hand": PURPLE, "finger": STEEL, "thigh": PURPLE, "knee": GOLD,
            "shin": PURPLE, "calf": PURPLE, "foot": treadf, "toe": treadf}
    a = humanoid(m, mats, bulk=1.3, arm_bulk=1.3, leg_bulk=1.4, name="bolgmon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.0, 2.8, 3.0, 54.0, 60.6, PURPLE, cut=1)
    m.box(hd, -2.2, 56.4, -3.4, 2.2, 57.8, -2.8, solid(P, "yellow", glow=True))
    for sx in (-1, 1):
        rod(m, hd, (sx * 1.6, 60.0, 0), (sx * 3.6, 65.0, 1.6), 1, GOLD, extend=0.3, t2=2)
    # the drum shoulder: a purple drum with three gold-rimmed cannon ports round a yellow X
    ar = a["arm_right"]
    sh = ar["shoulder"]
    c = (sh[0] - 3.4, 51.0, 0.6)
    m.round_box(ar["bone"], c[0], c[2], 4.0, 5.4, c[1] - 5.4, c[1] + 5.4, PURPLE, cut=2)
    m.box(ar["bone"], c[0] - 4.6, c[1] - 3.0, c[2] - 3.0, c[0] - 3.8, c[1] + 3.0, c[2] + 3.0, xf)
    for j, (dy, dz) in enumerate(((5.6, -2.4), (2.0, 6.0), (-4.0, 5.4))):
        pc = (c[0] - 1.0, c[1] + dy, c[2] + dz)
        m.round_box(ar["bone"], pc[0], pc[2], 2.6, 2.6, pc[1] - 2.6, pc[1] + 2.6, GOLD, cut=1)
        m.box(ar["bone"], pc[0] - 3.0, pc[1] - 1.4, pc[2] - 1.4, pc[0] - 2.4, pc[1] + 1.4, pc[2] + 1.4,
              solid(P, "black"))
    m.round_box(ar["bone"], ar["hand"][0], ar["hand"][2], 3.2, 3.2, ar["hand"][1] - 2.0, ar["hand"][1] + 4.0, GOLD,
                cut=1)
    # back towers ending in pincer horns
    for sx in (-1, 1):
        m.box(bd, sx * 3.6 - 1.4, 44.0, 3.6, sx * 3.6 + 1.4, 60.0, 6.4, PURPLE)
        for d in (-1, 1):
            rod(m, bd, (sx * 3.6 + d * 0.8, 60.0, 5.0), (sx * 3.6 + d * 1.6, 64.0, 4.0), 1, PURPLE, extend=0.2, t2=2)
    # the rotary gatling cannon on the left arm
    al = a["arm_left"]
    el, h = al["elbow"], al["hand"]
    gb = m.bone("spin_gun", al["bone"], el)
    m.round_box(gb, el[0], el[2] - 2.0, 3.4, 3.4, h[1] - 3.0, el[1], PURPLE, cut=1)
    for i in range(6):
        ang = math.radians(i * 60)
        bx, bz = el[0] + 1.8 * math.cos(ang), el[2] - 2.0 + 1.8 * math.sin(ang)
        rod(m, gb, (bx, h[1] - 2.0, bz), (bx, h[1] - 12.0, bz), 1, STEEL, extend=0)
    for yy in (h[1] - 6.0, h[1] - 11.0):
        m.round_box(gb, el[0], el[2] - 2.0, 3.0, 3.0, yy - 0.6, yy + 0.6, GOLD, cut=1)
    # tank treads round each leg
    for nm in ("leg_left", "leg_right"):
        lg = a[nm]
        k = lg["knee"]
        x0, x1 = k[0] - 2.4, k[0] + 2.4
        m.box(lg["bone"], x0, 0.0, -5.0, x1, 12.0, 4.0, treadf)
        m.box(lg["bone"], x0 - 0.6, 4.0, -3.6, x1 + 0.6, 8.0, 2.6, GOLD)
    return m
