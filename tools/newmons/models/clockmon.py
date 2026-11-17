"""Clockmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the clockwork soldier. A squat brass alarm-clock body with a white clock face, a winding key on top,
silver jointed legs with gold boots, a big grey hand-cannon on one side and a ring-mount on the other, ridden by a
little red-hooded imp in red gloves holding a long winding rod. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import fabric, local, metal, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a squat brass alarm-clock body with a clock face, silver jointed legs, a hand-cannon, ridden by a little "
        "red-hooded imp with a long winding rod")
BASE = {"brass": (230, 196, 100), "brass_dark": (160, 120, 40), "brass_light": (255, 236, 170), "face": (250, 250, 244),
        "hand": (30, 30, 36), "red": (210, 40, 40), "red_dark": (120, 14, 16), "steel": (200, 204, 216),
        "steel_dark": (100, 104, 116), "grey": (150, 152, 164), "eye": (90, 200, 90)}
SHINY = {"brass": (200, 204, 216), "brass_dark": (110, 114, 128), "brass_light": (255, 255, 255), "red": (60, 90, 200),
         "red_dark": (20, 40, 120)}


def P(v):
    return pal(BASE, SHINY, v)


BRASS = metal(P, "brass", dark="brass_dark", light="brass_light")
STEEL = metal(P, "steel", dark="steel_dark")


def facef(x, y, z, face, variant, box=None, **k):
    """The clock face: hour marks and two hands."""
    p = P(variant)
    if face != "north":
        return BRASS(x, y, z, face, variant, box=box, **k)
    a, b = x, y - 16.0
    r = math.hypot(a, b)
    if r > 6.6:
        return BRASS(x, y, z, face, variant, box=box, **k)
    ang = math.atan2(b, a)
    if r > 5.2 and abs(math.sin(ang * 6)) < 0.2:
        return tone(p["hand"], face), None
    if (abs(a) < 0.3 and 0 < b < 4.6) or (abs(b + a * 0.3) < 0.3 and 0 < a < 3.6):
        return tone(p["hand"], face), None
    return tone(p["face"], face), None


def build():
    m = Model("clockmon")
    top = m.bone("clockmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    for fy, fx in ((1.0, 0.42), (0.92, 0.72), (0.72, 0.92), (0.42, 1.0)):              # round clock body
        m.box(bd, -8.0 * fx, 16.0 - 8.0 * fy, -5.0, 8.0 * fx, 16.0 + 8.0 * fy, 5.0, facef)
    m.round_box(bd, 0, 0, 2.0, 2.0, 24.0, 26.0, BRASS, cut=1)                          # winding key
    m.box(bd, -3.0, 26.0, -0.6, 3.0, 29.0, 0.6, BRASS)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):                                # jointed legs
        lg = m.bone(nm, top, (sx * 4.0, 10.0, 0))
        rod(m, lg, (sx * 4.0, 10.0, 0), (sx * 6.0, 5.0, -1.0), 2, STEEL, extend=0.4)
        m.round_box(lg, sx * 6.0, -1.0, 1.4, 1.4, 4.0, 6.0, STEEL, cut=1)
        rod(m, lg, (sx * 6.0, 5.0, -1.0), (sx * 6.0, 2.0, -1.0), 2, STEEL, extend=0.4)
        m.box(lg, sx * 6.0 - 2.4, 0.0, -4.4, sx * 6.0 + 2.4, 2.6, 1.6, BRASS)
    ab = m.bone("arm_right", bd, (-8, 18, 0))                                           # hand-cannon
    rod(m, ab, (-8.0, 18.0, 0), (-12.0, 16.0, -2.0), 3, STEEL, extend=0.4)
    rod(m, ab, (-12.0, 16.0, -2.0), (-13.0, 15.0, -10.0), 4, solid(P, "grey"), extend=0)
    m.box(ab, -14.4, 13.6, -11.0, -11.6, 16.4, -10.0, solid(P, "hand"))                  # muzzle
    al = m.bone("arm_left", bd, (8, 18, 0))                                             # ring-mount
    rod(m, al, (8.0, 18.0, 0), (12.0, 15.0, 0), 3, STEEL, extend=0.4)
    for i in range(8):
        ang = i * math.pi / 4
        p0 = (13.0, 13.0 + 2.6 * math.sin(ang), 2.6 * math.cos(ang))
        p1 = (13.0, 13.0 + 2.6 * math.sin(ang + math.pi / 4), 2.6 * math.cos(ang + math.pi / 4))
        rod(m, al, p0, p1, 2, BRASS, extend=0.3)
    rd = m.bone("rider", bd, (0, 29, 2))                                                # the red-hooded imp
    m.round_box(rd, 0, 2.0, 2.0, 1.8, 29.0, 33.0, fabric(P, "red", "red_dark"), cut=1)
    m.round_box(rd, 0, 2.0, 2.0, 2.0, 33.0, 37.0, fabric(P, "red", "red_dark"), cut=1)
    m.box(rd, -0.6, 34.6, -0.1, 0.6, 35.4, 0.1, solid(P, "eye", glow=True))
    spike(m, rd, (0, 36.6, 2.0), (0, 1, 0.4), 1.6, 2.4, fabric(P, "red", "red_dark"))
    rod(m, rd, (-8.0, 31.0, -1.0), (8.0, 31.0, -1.0), 1, STEEL, extend=0)              # the winding rod
    m.round_box(rd, -9.0, -1.0, 1.4, 1.4, 30.0, 32.0, STEEL, cut=1)
    return m
