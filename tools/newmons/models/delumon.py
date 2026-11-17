"""Delumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the flower-bush bird. A plump little blue bird with a white belly, a big yellow beak, a gold crown
and a red bow tie, standing in red sneakers, and carrying on its back an enormous round green bush dotted with pink
blossoms. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a plump blue bird with a white belly, a yellow beak, a gold crown, a red bow tie and red sneakers, carrying an "
        "enormous round green bush dotted with pink blossoms")
BASE = {"blue": (60, 110, 200), "blue_dark": (20, 50, 120), "blue_light": (150, 190, 250), "white": (246, 248, 252),
        "white_dark": (190, 200, 220), "yellow": (240, 190, 50), "gold": (240, 200, 60), "gold_dark": (160, 120, 20),
        "red": (220, 40, 40), "green": (50, 140, 60), "green_dark": (20, 70, 30), "green_light": (120, 200, 110),
        "pink": (250, 160, 190), "pink_core": (240, 90, 120), "eye": (30, 30, 40), "sole": (240, 240, 244)}
SHINY = {"blue": (240, 170, 60), "blue_dark": (160, 90, 20), "blue_light": (255, 230, 150), "green": (140, 60, 140),
         "green_dark": (70, 20, 70), "green_light": (200, 130, 200)}


def P(v):
    return pal(BASE, SHINY, v)


FEATH = skin(P, "blue", dark="blue_dark", light="blue_light", var=0.03)
BUSH = fur(P, "green", "green_dark", tip="green_light", length=1.4, density=1.6)


def bodyf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if math.hypot(x - sx * 2.6, y - 25.6) < 0.8:
                return tone(p["eye"], face), None
        if y < 20.0 and abs(x) < 6.0 - max(0.0, (y - 14.0) * 0.5):
            return tone(p["white"], face), None
    return FEATH(x, y, z, face, variant, box=box, **k)


def bushf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    cx = (x * 0.35) % 3.0 - 1.5
    cy = (y * 0.35 + (x * 0.2) // 1 * 0.5) % 3.0 - 1.5
    r = math.hypot(cx, cy)
    if face in ("north", "east", "west", "south", "up") and r < 0.9:
        a = math.atan2(cy, cx)
        if r < 0.3:
            return tone(p["pink_core"], face), None
        if r < 0.55 + 0.35 * abs(math.cos(2.5 * a)):
            return tone(p["pink"], face), None
    return BUSH(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("delumon")
    top = m.bone("delumon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 5, 0))
    ball(m, bd, (0, 18.0, -3.0), 8.0, bodyf, layers=8, squash=0.9, ry=11.0)          # plump body
    hd = m.bone("head", bd, (0, 28, -3))
    spike(m, hd, (0, 24.0, -10.0), (0, -0.3, -1), 3.0, 6.0, solid(P, "yellow"), tip=1.0)   # big beak
    for i in range(5):                                                                # gold crown
        ang = math.radians(-60 + i * 30)
        spike(m, hd, (2.4 * math.sin(ang), 28.6, -3.0 - 2.4 * math.cos(ang)), (0, 1, 0), 1.2, 3.0,
              metal(P, "gold", dark="gold_dark"), tip=0.5)
    m.round_box(hd, 0, -3.0, 2.8, 2.8, 28.0, 29.4, metal(P, "gold", dark="gold_dark"), cut=1)
    for sx in (-1, 1):                                                                # red bow tie
        m.box(bd, min(sx * 0.6, sx * 3.0), 19.0, -11.4, max(sx * 0.6, sx * 3.0), 22.0, -10.6, solid(P, "red"),
              rotation=(0, 0, sx * 10), pivot=(0, 20.5, -11.0))
    m.box(bd, -0.8, 19.6, -11.6, 0.8, 21.4, -10.6, solid(P, "red"))
    bb = m.bone("bush", bd, (0, 20, 6))                                               # the blossom bush
    ball(m, bb, (2.0, 22.0, 9.0), 13.0, bushf, layers=8, squash=0.8)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 8.0, 18.0, -3.0))
        m.box(ab, min(sx * 7.0, sx * 10.0), 12.0, -4.6, max(sx * 7.0, sx * 10.0), 20.0, -1.4, FEATH,
              rotation=(0, 0, sx * 20), pivot=(sx * 8.0, 18.0, -3.0))
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                              # red sneakers
        lg = m.bone(nm, top, (sx * 3.6, 6.0, -3.0))
        rod(m, lg, (sx * 3.6, 8.0, -3.0), (sx * 3.6, 4.0, -3.0), 2, FEATH, extend=0.4)
        m.round_box(lg, sx * 3.6, -5.0, 2.6, 4.4, 1.0, 5.0, solid(P, "red"), cut=1)
        m.box(lg, sx * 3.6 - 2.6, 0.0, -9.4, sx * 3.6 + 2.6, 1.0, -0.6, solid(P, "sole"))
    return m
