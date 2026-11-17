"""Divemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the hammerhead diver. A sleek, muscular blue shark-man with a white belly and a wide hammerhead,
patterned with fine dark tribal lines, tall swept dorsal and arm fins, a dark trunk band, webbed clawed hands and a
long shark tail in place of legs, built mid-dive. 25 blocks long.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digidetail import fabric, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.0)
KIND = "floater"
K = 3
LOOK = ("a sleek muscular blue hammerhead shark-man with a white belly, dark tribal lines, tall swept fins, webbed "
        "clawed hands and a long shark tail")
BASE = {"blue": (80, 140, 210), "blue_dark": (24, 60, 130), "blue_light": (160, 200, 250), "belly": (236, 244, 252),
        "belly_dark": (180, 200, 220), "line": (30, 40, 80), "band": (40, 40, 60), "band_dark": (14, 14, 24),
        "eye": (250, 220, 60), "claw": (230, 236, 246)}
SHINY = {"blue": (130, 130, 150), "blue_dark": (60, 60, 80), "blue_light": (200, 200, 220)}


def P(v):
    return pal(BASE, SHINY, v)


SKIN = skin(P, "blue", dark="blue_dark", light="blue_light")


def tribalf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and abs(math.sin(z * 0.8 + y * 0.6)) < 0.08:
        return tone(p["line"], face), None
    if face == "down":
        return tone(p["belly"], face), None
    return SKIN(x, y, z, face, variant, box=box, **k)


def fin(m, bone, base, d, length, w):
    pts = [base]
    for j in range(1, 4):
        t = j / 3
        pts.append((base[0] + d[0] * length * t, base[1] + d[1] * length * t, base[2] + d[2] * length * t + 2.0 * t * t))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, 1, tribalf, extend=0.5, t2=max(1, round(w * (1 - j / 3))))


def build():
    m = Model("divemon")
    top = m.bone("divemon", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 20, 0))
    m.round_box(bd, 0, -6.0, 5.0, 8.0, 16.0, 24.0, tribalf, cut=2)                     # diving torso (horizontal)
    m.round_box(bd, 0, 4.0, 3.6, 4.0, 15.0, 21.0, fabric(P, "band", "band_dark"), cut=1)  # trunk band
    hd = m.bone("head", bd, (0, 22, -14))
    m.round_box(hd, 0, -16.0, 3.0, 3.0, 18.0, 24.0, tribalf, cut=1)
    m.box(hd, -10.0, 20.0, -20.0, 10.0, 23.0, -16.0, tribalf)                          # wide hammerhead
    for sx in (-1, 1):
        m.box(hd, min(sx * 9.6, sx * 10.2), 21.0, -19.0, max(sx * 9.6, sx * 10.2), 22.4, -17.6,
              solid(P, "eye", glow=True))
    fin(m, bd, (0, 24.0, -4.0), (0, 1.0, 0.8), 9.0, 5)                                 # tall dorsal fin
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):                               # arms reaching forward
        ab = m.bone(nm, bd, (sx * 5.0, 21.0, -10.0))
        rod(m, ab, (sx * 5.0, 21.0, -10.0), (sx * 8.0, 20.0, -20.0), 3, tribalf, extend=0.6)
        rod(m, ab, (sx * 8.0, 20.0, -20.0), (sx * 8.0, 19.0, -28.0), 3, tribalf, extend=0.6)
        for j in range(4):
            spike(m, ab, (sx * 8.0 + (j - 1.5) * 0.8, 19.0, -29.0), (0, -0.2, -1), 0.8, 2.4, solid(P, "claw"), tip=0.2)
        fin(m, ab, (sx * 7.0, 21.0, -15.0), (sx * 0.6, 0.8, 0.4), 6.0, 3)              # arm fins
    tl = m.bone("tail", bd, (0, 20, 10))                                               # long shark tail
    pts = [(0, 20.0, 9.0), (0, 21.0, 17.0), (0, 23.0, 25.0), (0, 25.0, 32.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 6 - 2 * j, tribalf, extend=0.8)
    fin(m, tl, pts[-1], (0, 1.0, 0.6), 9.0, 4)
    fin(m, tl, pts[-1], (0, -0.8, 0.8), 7.0, 3)
    for sx in (-1, 1):
        fin(m, tl, (sx * 2.0, 21.0, 17.0), (sx, -0.4, 0.6), 5.0, 2)
    return m
