"""Deathmon (C'mon Digimon Version) (a Digimon of the CobbleEffort: Digital crossover; after the manga art on
wikimon.net, the C'mon Digimon story): the shapeshifting demon in its own form. A massive crouching beast with a pale
hide covered in black leopard-like blotches, a broad head ringed with ridges, a huge maw of ivory tusks and fangs, a
cluster of curved horn-claws sweeping forward round its face, thick clawed limbs and a long blotched tail. 35 blocks
tall.

Front is -z, y is up. 34 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fbm, skin, solid
from _route import pal, tone

HEIGHT = 34
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a massive crouching beast with a pale hide covered in black blotches, a ridged head, a huge maw of ivory tusks "
        "and a cluster of curved horn-claws sweeping forward round its face")
BASE = {"hide": (236, 232, 222), "hide_dark": (170, 166, 156), "spot": (30, 28, 30), "ivory": (246, 240, 220),
        "ivory_dark": (190, 180, 150), "mouth": (110, 20, 30), "tooth": (250, 248, 240), "eye": (250, 200, 40)}
SHINY = {"hide": (240, 200, 120), "hide_dark": (180, 140, 60), "spot": (90, 40, 20)}


def P(v):
    return pal(BASE, SHINY, v)


HIDE = skin(P, "hide", dark="hide_dark", var=0.04)
IVORY = skin(P, "ivory", dark="ivory_dark", var=0.03)


def spotf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    n = fbm(x * 0.35, y * 0.35, z * 0.35, 21)
    if n > 0.62:
        return tone(p["spot"], face), None
    return HIDE(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("deathmoncmondigimonversion")
    mats = {"skin": spotf, "belly": HIDE, "neck": spotf, "head": spotf, "snout": spotf, "jaw": spotf,
            "mouth": solid(P, "mouth"), "tooth": solid(P, "tooth"), "leg_upper": spotf, "leg_lower": spotf,
            "paw": spotf, "claw": IVORY, "tail": spotf}
    a = quadruped(m, mats, "deathmoncmondigimonversion", length=36.0, body_y=18.0, body_rx=9.0, body_ry=8.4,
                  chest_bulk=1.4, neck=((0, 22, -18), (0, 24, -22)), head_len=10.0, head_w=6.0, head_h=6.0,
                  snout=0.6, mouth_open=22, teeth=6, leg_bulk=2.0, toes=4,
                  tail=((0, 20, 18), (3, 16, 26), (7, 12, 32), (12, 10, 36)), tail_r=(3.0, 2.4, 1.8, 1.2))
    hd = a["head"]
    for j in range(4):                                                         # ridges round the head
        m.round_box(hd, 0, -22.0 + j * 1.6, 6.4 - j * 0.6, 0.8, 26.0 + j * 0.8, 30.0 + j * 0.6, spotf, cut=0)
    for sx in (-1, 1):
        m.box(hd, min(sx * 4.6, sx * 5.2), 27.0, -28.0, max(sx * 4.6, sx * 5.2), 28.0, -26.4,
              solid(P, "eye", glow=True))
        spike(m, hd, (sx * 3.0, 21.0, -31.0), (sx * 0.2, -0.3, -1), 1.8, 6.0, IVORY, tip=0.25)   # ivory tusks
        for j in range(3):                                                      # curved horn-claws
            base = (sx * (6.0 + j * 1.0), 26.0 - j * 3.0, -22.0 + j * 1.4)
            pts = [base, (base[0] + sx * 3.0, base[1] + 2.0, base[2] - 4.0),
                   (base[0] + sx * 1.0, base[1] + 1.0, base[2] - 9.0), (base[0] - sx * 2.0, base[1] - 1.0, base[2] - 12.0)]
            for k_, (p0, p1) in enumerate(zip(pts, pts[1:])):
                rod(m, hd, p0, p1, 2 if k_ == 0 else 1, IVORY, extend=0.4)
    return m
