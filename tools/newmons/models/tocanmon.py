"""Tocanmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a little brown toucan bird hatched only halfway: its round body still sits in a jagged red eggshell
with white spots, a huge banana-shaped beak in blue, yellow and orange, a blue cap of feathers, green eyes, brown wing
hands, and big yellow-and-orange feet. 15 blocks.

Front is -z, y is up. Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digidetail import eye, feathers, plane, skin, solid
from _route import pal, tone

HEIGHT = 23
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a little brown toucan in a jagged red eggshell with a huge blue, yellow and orange beak, a blue feather cap and big yellow feet"
BASE = {"brown": (90, 60, 50), "brown_dark": (50, 30, 24), "red": (220, 40, 40), "red_dark": (140, 16, 16),
        "white": (250, 250, 250), "blue": (70, 140, 220), "yellow": (250, 210, 50), "orange": (240, 130, 40),
        "eye": (130, 210, 70), "pupil": (20, 20, 10), "black": (30, 30, 30)}
SHINY = {"brown": (60, 60, 70), "brown_dark": (30, 30, 40), "red": (240, 200, 60), "red_dark": (180, 130, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def shellf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    for cx, cy in ((-3.0, 6.0), (3.4, 8.0), (0, 4.0), (-4.4, 10.0), (4.6, 4.6)):
        if face == "north" and math.hypot(x - cx, y - cy) < 0.9:
            return tone(p["white"], face), None
    return skin(P, "red", dark="red_dark")(x, y, z, face, variant, box=box, **k)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 1.6, y - 18.0, 1.0, "eye")
        if c is not None:
            return c, None
    return feathers(P, "brown", "brown_dark")(x, y, z, face, variant, box=box, **k)


def beakf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    t = -z
    if t < 7.0:
        c = p["blue"]
    elif (t + y * 0.4) % 3.0 < 1.4 and t < 13.0:
        c = p["yellow"] if (t % 6.0) < 3.0 else p["blue"]
    else:
        c = p["orange"] if t > 13.0 else p["yellow"]
    return tone(c, face), None


def build():
    m = Model("tocanmon")
    top = m.bone("tocanmon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    ball(m, bd, (0, 12.0, 0), 5.6, feathers(P, "brown", "brown_dark"), layers=5)
    ball(m, bd, (0, 7.0, 0), 5.8, shellf, layers=4, squash=0.9)                         # eggshell
    for i in range(10):                                                                 # jagged rim
        ang = i * 2 * math.pi / 10
        spike(m, bd, (5.4 * math.sin(ang), 11.0, 5.4 * math.cos(ang)), (0, 1, 0), 1.8, 2.6, shellf, tip=0.8)
    hd = m.bone("head", bd, (0, 17, 0))
    ball(m, hd, (0, 18.0, 0), 4.0, headf, layers=4)
    m.round_box(hd, 0, 1.0, 3.6, 3.6, 20.6, 22.6, feathers(P, "blue", "blue"), cut=1)       # blue cap
    spike(m, hd, (0, 21.6, 4.0), (0, 0.3, 1), 2.0, 3.0, solid(P, "blue"), tip=0.8)
    pts = [(0, 18.6, -3.0), (0, 18.6, -9.0), (0, 17.0, -14.0), (0, 13.6, -17.0)]          # banana beak
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, hd, p0, p1, 3 - i, beakf, extend=0.6, t2=4 - i)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, bd, (sx * 5.0, 12.0, 0))
        for j in range(4):
            spike(m, ab, (sx * 5.0, 12.0, 0), (sx, -0.3 + j * 0.25, 0.2), 1.2, 5.0, feathers(P, "brown", "brown_dark"),
                  tip=0.8)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        lg = m.bone(nm, top, (sx * 2.4, 3.0, 0))
        m.round_box(lg, sx * 2.6, -2.4, 1.8, 3.4, 0.0, 2.4, solid(P, "yellow"), cut=1)
        m.box(lg, sx * 2.6 - 1.9, 0.0, -6.4, sx * 2.6 + 1.9, 1.6, -5.4, solid(P, "orange"))
    return m
