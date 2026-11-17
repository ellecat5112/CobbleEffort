"""BEMmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a little alien raider. A glossy violet body and long curling tail, a pointed violet helmet with a red
triangle mark and a dark visor round one glowing green eye, a heavy chain collar, "01" on its chest, long steel
claws with a glowing yellow orb in one hand, and clawed feet. 1 block tall.

Front is -z, y is up. 40 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, gem, local, metal, plane, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(1.0, HEIGHT, 0.8)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("a little alien raider: a glossy violet body and curling tail, a pointed helmet with a red triangle and a dark "
        "visor round one green eye, a chain collar, long steel claws and a glowing yellow orb")
BASE = {"violet": (110, 60, 170), "violet_dark": (50, 24, 90), "violet_light": (180, 140, 230), "black": (26, 26, 34),
        "red": (220, 40, 40), "green": (90, 240, 140), "green_light": (220, 255, 230), "steel": (210, 214, 226),
        "steel_dark": (110, 114, 128), "orb": (255, 240, 90), "orb_light": (255, 255, 220), "white": (240, 240, 246)}
SHINY = {"violet": (60, 150, 90), "violet_dark": (20, 80, 40), "violet_light": (140, 220, 160), "green": (255, 120, 80)}


def P(v):
    return pal(BASE, SHINY, v)


BODY = skin(P, "violet", dark="violet_dark", light="violet_light", var=0.03)
STEEL = metal(P, "steel", dark="steel_dark")


def chestf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north" and 44.0 < y < 47.0 and 0.5 < x < 3.5 and ((x * 2) % 1.4 < 0.5 or abs(y - 45.5) > 1.0):
        return p["white"], None                                  # the "01"
    return BODY(x, y, z, face, variant, box=box, **k)


def helmf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        a, b = plane(x, y, z, face)
        if math.hypot(a, b - 57.0) < 1.6:
            return (p["green_light"] if math.hypot(a, b - 57.0) < 0.6 else p["green"]), p["green"]
        if abs(b - 57.0) < 2.6 and abs(a) < 2.4:
            return tone(p["black"], face), None                  # visor
        if b > 60.0 and abs(a) < (63.0 - b) * 0.5:
            return tone(p["red"], face), None                    # red triangle
    return armour(P, "violet", "violet_dark", light="violet_light")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("bemmon")
    mats = {"skin": BODY, "chest": chestf, "abs": chestf, "foot": BODY, "talon": STEEL, "claw": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="bemmon", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.6, 3.0, 3.4, 54.0, 61.0, helmf, cut=1)
    for i in range(4):                                           # pointed helmet sweeping back
        r = 2.8 - i * 0.6
        m.round_box(hd, 0, 2.0 + i * 2.0, r, r, 59.0 + i * 1.6, 62.0 + i * 1.6, helmf, cut=1)
    for i in range(10):                                          # chain collar
        ang = math.radians(i * 36)
        c = (3.6 * math.sin(ang), 52.0, -3.6 * math.cos(ang))
        m.box(bd, c[0] - 0.6, c[1] - 0.6, c[2] - 0.6, c[0] + 0.6, c[1] + 0.6, c[2] + 0.6, STEEL,
              rotation=(45 * (i % 2), 45, 0), pivot=c)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):         # long steel claws
        h = a[nm]["hand"]
        for f in range(3):
            spike(m, a[nm]["bone"], (h[0], h[1] - 2.0, h[2] + (f - 1) * 1.0), (sx * 0.3, -1, -0.2), 1.0, 6.0, STEEL,
                  tip=0.4)
    h = a["arm_left"]["hand"]
    ball(m, a["arm_left"]["bone"], (h[0] + 1.0, h[1] - 2.0, h[2] - 2.0), 1.6, gem(P, "orb", "orb_light"), layers=2)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32, 3), (3, 28, 10), (8, 32, 15), (12, 42, 15), (11, 50, 12), (8, 52, 9)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 4 - j), BODY, extend=0.4)
    return m
