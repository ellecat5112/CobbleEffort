"""Golemon (PS) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the PlayStation-era Golemon: a hulking golem built of black blocks outlined in a glowing green wireframe grid, a tall
block head, chunky arms and short block legs. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall.
"""
from __future__ import annotations

from _boxmodel import Model, rod
from _digi import sized
from _digidetail import local
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a hulking golem of black blocks outlined in a glowing green wireframe grid"
BASE = {"black": (12, 18, 14), "grid": (60, 255, 90)}
SHINY = {"grid": (80, 200, 255)}


def P(v):
    return pal(BASE, SHINY, v)


def gridf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if u < 0.4 or v < 0.4 or u > W - 0.4 or v > H - 0.4 or (u % 3.0) < 0.3 or (v % 3.0) < 0.3:
        return p["grid"], p["grid"]
    return tone(p["black"], face), None


def build():
    m = Model("golemonps")
    top = m.bone("golemonps", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 12, 0))
    m.box(bd, -8.0, 12.0, -5.0, 8.0, 26.0, 5.0, gridf)
    m.box(bd, -9.0, 26.0, -6.0, 9.0, 30.0, 6.0, gridf)
    hd = m.bone("head", bd, (0, 30, 0))
    m.box(hd, -5.0, 30.0, -5.0, 5.0, 40.0, 5.0, gridf)
    for sx in (-1, 1):
        ab = m.bone("arm_left" if sx > 0 else "arm_right", bd, (sx * 9.0, 28.0, 0))
        x0, x1 = sorted((sx * 9.0, sx * 15.0))
        m.box(ab, x0, 20.0, -3.0, x1, 28.0, 3.0, gridf, rotation=(0, 0, sx * 25), pivot=(sx * 9.0, 28.0, 0))
        x0, x1 = sorted((sx * 13.0, sx * 19.0))
        m.box(ab, x0, 12.0, -3.0, x1, 20.0, 3.0, gridf, rotation=(0, 0, sx * 10), pivot=(sx * 13.0, 20.0, 0))
        lg = m.bone("leg_left" if sx > 0 else "leg_right", top, (sx * 4.0, 12.0, 0))
        x0, x1 = sorted((sx * 1.0, sx * 8.0))
        m.box(lg, x0, 6.0, -4.0, x1, 12.0, 4.0, gridf)
        m.box(lg, x0, 0.0, -5.0, x1, 6.0, 4.0, gridf)
    return m
