"""Takinmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a shaggy cream takin calf with a big grey muzzle, heavy grey horns curling out and back, a red
flame mark on its brow, rust-tipped ears, red bands round its legs, grey hooves and a rusty tail tuft. 1 block.

Front is -z, y is up. Child stage.
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import eye, fur, metal, plane, solid
from _route import pal, tone

HEIGHT = 32
SCALE, HITBOX = sized(1, HEIGHT, 1.2)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 18}
LOOK = "a shaggy cream takin calf with a grey muzzle, curling grey horns, a red brow mark and red leg bands"
BASE = {"fur": (246, 236, 196), "fur_dark": (200, 180, 130), "grey": (130, 130, 136), "grey_dark": (70, 70, 76),
        "rust": (210, 110, 50), "red": (190, 40, 40), "eye": (60, 140, 220), "pupil": (10, 10, 20),
        "white": (250, 250, 250), "horn": (150, 150, 156), "horn_dark": (80, 80, 86)}
SHINY = {"fur": (120, 80, 50), "fur_dark": (70, 44, 24)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="rust", length=1.4)


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if z < -17.6:
        return metal(P, "grey", dark="grey_dark")(x, y, z, face, variant, box=box, **k)
    if face == "north" and abs(x) < 1.4 and 30.0 < y < 32.0:
        return tone(p["red"], face), None
    if face in ("east", "west"):
        c = eye(p, z + 15.4, y - 28.6, 0.9, "eye")
        if c is not None:
            return c, None
    return FUR(x, y, z, face, variant, box=box, **k)


def legf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if y < 1.6:
        return tone(p["grey"], face), None
    if 4.6 < y < 6.0:
        return tone(p["red"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("takinmon")
    mats = {"skin": FUR, "belly": FUR, "neck": FUR, "head": headf, "leg": legf, "paw": legf, "shin": legf,
            "thigh": legf, "claw": solid(P, "grey"), "tail": FUR}
    a = quadruped(m, mats, "takinmon", length=24.0, body_y=14.0, body_rx=7.0, body_ry=7.0, chest_bulk=1.15,
                  neck=((0, 18, -12), (0, 22, -14)), head_len=10.0, head_w=4.6, head_h=7.0, snout=0.25, mouth_open=0,
                  tail=((0, 16, 12), (0, 13, 17), (0, 8, 20)), tail_r=(1.6, 1.2, 1.0), toes=0, claws=False)
    hd = a["head"]
    ball(m, hd, (0, 24.0, -19.6), 3.6, metal(P, "grey", dark="grey_dark"), layers=3)       # big grey muzzle
    for sx in (-1, 1):
        pts = [(sx * 3.4, 28.6, -14.0), (sx * 7.6, 30.6, -13.0), (sx * 10.0, 28.6, -10.6), (sx * 10.4, 26.0, -8.0)]
        for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 3 - i, metal(P, "horn", dark="horn_dark"), extend=0.6)
        m.round_box(hd, sx * 6.6, -11.6, 1.6, 1.0, 25.0, 27.4, FUR, cut=0)                 # ears
    tb = a.get("tail") or a["body"]
    ball(m, a["body"], (0, 7.4, 20.6), 1.8, solid(P, "rust"), layers=2)
    return m
