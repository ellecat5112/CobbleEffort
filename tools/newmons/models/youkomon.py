"""Youkomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a bewitching fox: a slender violet fox with a white-tufted face, long ears bound with striped green
cords ending in green bells, a great bushy violet tail tipped with flame, and fox-fire flickering round it. 15 blocks.

Front is -z, y is up. Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, fur, metal, solid
from _route import pal, tone

HEIGHT = 28
SCALE, HITBOX = sized(15, HEIGHT, 4.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = "a slender violet fox with a white-tufted face, ears bound with striped green cords and bells, a great flame-tipped tail and fox-fire"
BASE = {"violet": (130, 110, 190), "violet_dark": (70, 50, 130), "white": (240, 240, 246), "white_dark": (190, 190, 210),
        "green": (60, 130, 110), "bell": (200, 230, 90), "flame": (255, 170, 60, 210), "eye": (250, 220, 60),
        "pupil": (20, 10, 30)}
SHINY = {"violet": (230, 160, 70), "violet_dark": (170, 100, 20)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "violet", "violet_dark", length=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west"):
        c = eye(p, z + 16.0, y - 21.0, 0.8, "eye", slit=True)
        if c is not None:
            return c, None
    return FUR(x, y, z, face, variant, box=box, **k)


def cordf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["green"] if int((x + y + z) * 1.2) % 2 else p["white"], face), None


def build():
    m = Model("youkomon")
    mats = {"skin": FUR, "belly": fur(P, "white", "white_dark"), "neck": fur(P, "white", "white_dark"), "head": headf,
            "leg": FUR, "paw": FUR, "claw": solid(P, "white"), "tail": FUR}
    a = quadruped(m, mats, "youkomon", length=18.0, body_y=11.0, body_rx=4.0, body_ry=4.0, chest_bulk=1.1,
                  neck=((0, 15, -9), (0, 19, -11)), head_len=8.0, head_w=3.0, head_h=3.6, snout=0.7, mouth_open=0,
                  tail=((0, 13, 9),), tail_r=(2.0,), toes=0, claws=False)
    hd, bd = a["head"], a["body"]
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 22.0, -10.0), (sx * 0.4, 1, 0.3), 1.8, 5.0, FUR, tip=0.8)
        pts = [(sx * 2.4, 23.0, -9.6), (sx * 5.0, 20.0, -12.0), (sx * 7.0, 16.0, -14.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, cordf, extend=0.2)
        ball(m, hd, pts[-1], 1.2, metal(P, "bell"), layers=1)
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.6, 19.0, -14.0), ((j - 2) * 0.4, -0.2, 0.4), 1.0, 3.0, fur(P, "white", "white_dark"),
              tip=0.8)
    tl = m.bone("brush", bd, (0, 14, 9))                                                # great bushy tail
    for j in range(6):
        ball(m, tl, (0, 15.0 + j * 1.6, 11.0 + j * 1.4), 3.4 - abs(j - 2.5) * 0.3, FUR, layers=2)
    for j in range(4):
        spike(m, tl, ((j - 1.5) * 1.2, 24.0, 18.0), ((j - 1.5) * 0.3, 1, 0.4), 1.6, 6.0, solid(P, "flame", glow=True),
              tip=0.8)
    for i in range(5):                                                                  # fox-fire
        ang = i * 2 * math.pi / 5
        ball(m, bd, (10.0 * math.cos(ang), 18.0 + 2.0 * math.sin(ang * 2), 10.0 * math.sin(ang)), 1.2,
             solid(P, "flame", glow=True), layers=1)
    return m
