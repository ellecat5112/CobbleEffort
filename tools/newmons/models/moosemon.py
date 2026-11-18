"""Moosemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of kindness: a white moose striped with flowing blue markings, a long black
mane down its neck, a white horse-like head with a red gem on its brow, huge sweeping blue antlers banded dark, small
white feathered wings, brown leather straps on its legs and shaggy blue fetlocks over its hooves. 15 blocks tall.

Front is -z, y is up. 50 units tall (the antlers); Adult (Armor) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import feather_wing, quadruped
from _digidetail import feathers, fur, gem, leather, solid, strands
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a white moose striped with flowing blue markings, a long black mane, a red brow gem, huge sweeping blue antlers, "
        "small feathered wings and shaggy blue fetlocks")
BASE = {"white": (240, 242, 248), "white_dark": (170, 176, 196), "blue": (60, 120, 210), "blue_dark": (20, 50, 130),
        "black": (30, 30, 36), "red": (220, 40, 50), "leather": (150, 100, 60), "leather_dark": (90, 56, 30),
        "eye": (40, 40, 60), "mouth": (110, 60, 70), "tooth": (250, 250, 240)}
SHINY = {"blue": (200, 70, 160), "blue_dark": (120, 20, 90)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "white", "white_dark", length=1.0)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and abs(math.sin(z * 0.5 + y * 0.35 + abs(x) * 0.3)) > 0.86:
        return tone(p["blue"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def antlerf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["blue_dark"] if (y * 0.8) % 3.0 < 0.8 else p["blue"], face), None


def build():
    m = Model("moosemon")
    mats = {"skin": hidef, "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "claw": solid(P, "blue_dark")}
    a = quadruped(m, mats, "moosemon", length=28.0, body_y=19.0, body_rx=5.4, body_ry=5.6, chest_bulk=1.25,
                  neck=((0, 26, -13), (0, 32, -15)), head_len=10.0, head_w=3.0, head_h=3.4, snout=0.9,
                  mouth_open=4, teeth=0, leg_bulk=1.1, toes=2,
                  tail=((0, 22, 14), (0, 20, 17)), tail_r=(1.2, 0.8))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4,
              ez + 0.6, solid(P, "eye"))
        root = (sx * 2.0, ey + 2.4, hc[2] + 2.0)
        pts = [root, (sx * 7.0, ey + 6.0, hc[2] + 3.0), (sx * 11.0, ey + 12.0, hc[2] + 2.0),
               (sx * 10.0, ey + 17.0, hc[2] + 1.0)]
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                 # sweeping antlers
            rod(m, hd, p0, p1, max(1, 2 - j // 2), antlerf, extend=0.3)
        for j in range(3):
            q = pts[1 + j]
            spike(m, hd, q, (sx * 0.3, 1, -0.3 + j * 0.2), 1.2, 4.0 - j * 0.6, antlerf, tip=0.8)
    ball_gem = gem(P, "red", "white")
    m.box(hd, -0.7, ey + 1.2, hc[2] - 3.2, 0.7, ey + 2.4, hc[2] - 2.9, ball_gem)
    for j in range(8):                                                                   # long black mane
        spike(m, a["neck"], (0, 30.0 - j * 1.4, -13.0 + j * 0.8), (0, 0.3, 1), 1.6, 5.0, strands(P, "black", "black"),
              tip=0.8)
    for side in (1, -1):                                                                 # small feathered wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 4.0, 24.0, -4.0))
        feather_wing(m, wb, (side * 4.0, 24.0, -4.0), 8.0, 6.0, 3, feathers(P, "white", "white_dark"), side=side,
                     sweep=30, droop=-3.0)
    for nm in ("leg_front_left", "leg_front_right", "leg_back_left", "leg_back_right"):  # straps + fetlocks
        anc = a[nm]
        w = anc.get("wrist") or anc.get("ankle")
        if w:
            m.round_box(anc["bone"], w[0], w[2], 1.8, 1.8, w[1] + 4.0, w[1] + 5.0, leather(P, "leather", "leather_dark"),
                        cut=0)
            m.round_box(anc["bone"], w[0], w[2], 2.4, 2.4, 0.4, 3.0, fur(P, "blue", "blue_dark", length=1.4), cut=1)
    return m
