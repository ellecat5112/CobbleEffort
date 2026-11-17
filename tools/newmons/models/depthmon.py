"""Depthmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the deep-sea hunter. A lean blue fish-man with a pale belly and a sharp fish-like head with a gold
eye, silver sickle fins sweeping from its back, elbows and calves, bony silver clawed hands and feet, and a long
forked shark tail. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import metal, scales, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean blue fish-man with a sharp fish head, silver sickle fins on its back, elbows and calves, silver claws "
        "and a long forked shark tail")
BASE = {"blue": (70, 110, 200), "blue_dark": (24, 46, 120), "blue_light": (150, 190, 250), "belly": (230, 240, 250),
        "belly_dark": (170, 190, 210), "silver": (210, 214, 226), "silver_dark": (110, 114, 130), "eye": (250, 200, 50),
        "black": (20, 20, 30)}
SHINY = {"blue": (70, 170, 150), "blue_dark": (20, 90, 80), "blue_light": (150, 230, 210)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = scales(P, "blue", "blue_dark", size=1.2, light="blue_light", rim_mix=0.3)
SILVER = metal(P, "silver", dark="silver_dark")


def fin(m, bone, base, d, length, w):
    """A sickle fin: a tapering curved blade along d, bending back."""
    pts = [base]
    for j in range(1, 4):
        t = j / 3
        pts.append((base[0] + d[0] * length * t, base[1] + d[1] * length * t + 1.6 * t * t,
                    base[2] + d[2] * length * t + 2.0 * t * t))
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, bone, p0, p1, 1, SILVER, extend=0.5, t2=max(1, round(w * (1 - j / 3))))


def build():
    m = Model("depthmon")
    mats = {"skin": HIDE, "chest": HIDE, "abs": skin(P, "belly", dark="belly_dark"), "pelvis": HIDE, "neck": HIDE,
            "deltoid": HIDE, "upper_arm": HIDE, "forearm": HIDE, "hand": SILVER, "finger": SILVER, "claw": SILVER,
            "thigh": HIDE, "knee": HIDE, "shin": HIDE, "calf": HIDE, "foot": SILVER, "talon": SILVER}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.85, leg_bulk=0.85, claws=True, talons=True, digitigrade=True,
                 name="depthmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -2.0, 2.4, 4.4, 53.0, 58.0, HIDE, cut=1)
    spike(m, hd, (0, 55.0, -6.0), (0, -0.1, -1), 2.4, 4.0, SILVER, tip=0.6)            # sharp snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.3, sx * 2.6), 56.0, -4.0, max(sx * 2.3, sx * 2.6), 57.2, -2.8, solid(P, "eye", glow=True))
    fin(m, hd, (0, 58.0, -1.0), (0, 0.6, 1), 8.0, 3)                                   # head fin
    for sx in (-1, 1):
        fin(m, bd, (sx * 3.0, 48.0, 3.0), (sx * 0.6, 0.6, 0.8), 12.0, 4)               # back sickle fins
    for nm in ("arm_left", "arm_right"):
        el = a[nm]["elbow"]
        fin(m, a[nm]["bone"], el, (0, 0.3, 1), 7.0, 3)
    for nm in ("leg_left", "leg_right"):
        kn = a[nm]["knee"]
        fin(m, a[nm]["bone"], (kn[0], kn[1] - 4.0, kn[2] + 1.0), (0, 0.2, 1), 6.0, 2)
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (0, 26.0, 10.0), (0, 22.0, 18.0), (0, 20.0, 26.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, 3 - j, HIDE, extend=0.6)
    for sgn in (-1, 1):                                                                # forked shark tail
        fin(m, tl, pts[-1], (0, sgn * 0.7, 0.7), 8.0, 3)
    return m
