"""Parasaurmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a crested dinosaur: a hulking green dinosaur striped orange with a brown furry neck and limbs, a
long curved head crest spotted black and orange, a yellow feather headdress, a beaked face, and a long tail spotted
like its crest. 15 blocks long.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import fur, scales, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a hulking green dinosaur striped orange with brown fur, a long curved spotted head crest, a yellow feather headdress and a spotted tail"
BASE = {"green": (90, 180, 70), "green_dark": (40, 110, 30), "orange": (240, 130, 40), "brown": (120, 80, 50),
        "brown_dark": (70, 44, 24), "black": (40, 40, 44), "yellow": (250, 210, 60), "beak": (60, 60, 64),
        "eye": (60, 130, 200), "claw": (50, 50, 56)}
SHINY = {"green": (80, 140, 210), "green_dark": (30, 80, 150), "orange": (240, 210, 70)}


def P(v):
    return pal(BASE, SHINY, v)


SC0 = scales(P, "green", "green_dark", size=1.4)


def hidef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "down" and abs(((z * 0.45 + y * 0.2) % 3.6) - 1.8) < 0.45:
        return tone(p["orange"], face), None
    if face != "down" and math.sin(x * 1.1 + z * 0.8) * math.sin(y * 0.9) > 0.8:
        return tone(p["black"], face), None
    return SC0(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("parasaurmon")
    mats = {"skin": hidef, "mouth": solid(P, "beak"), "tooth": solid(P, "beak"), "claw": solid(P, "claw")}
    a = quadruped(m, mats, "parasaurmon", length=30.0, body_y=16.0, body_rx=6.4, body_ry=6.4, chest_bulk=1.2,
                  neck=((0, 22, -12), (0, 28, -14)), head_len=9.0, head_w=3.2, head_h=3.6, snout=0.6, mouth_open=8,
                  teeth=0, leg_bulk=1.5, toes=3,
                  tail=((0, 18, 15), (6, 14, 22), (14, 10, 24), (18, 8, 18)), tail_r=(3.0, 2.4, 1.8, 1.2))
    bd, hd = a["body"], a["head"]
    ex, ey, ez = a["eye"]
    hc = a["head_c"]
    for sx in (-1, 1):
        m.box(hd, min(sx * ex, sx * (ex + 0.3)), ey - 0.4, ez - 0.6, max(sx * ex, sx * (ex + 0.3)), ey + 0.4, ez + 0.6,
              solid(P, "eye"))
    pts = [(0, ey + 2.0, hc[2]), (0, ey + 7.0, hc[2] + 4.0), (0, ey + 9.0, hc[2] + 10.0), (0, ey + 7.0, hc[2] + 15.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):                                     # long curved crest
        rod(m, hd, p0, p1, 3 - j // 2, hidef, extend=0.4)
    for i in range(5):                                                                   # yellow feather headdress
        spike(m, hd, ((i - 2) * 0.8, ey + 1.4, hc[2] - 2.0), ((i - 2) * 0.3, 0.3, -1), 0.8, 4.0, solid(P, "yellow"),
              tip=0.8)
    for nm in ("leg_front_left", "leg_front_right"):                                     # brown furry forelimbs
        anc = a[nm]
        m.round_box(anc["bone"], anc["hip"][0], anc["hip"][2], 2.6, 2.6, anc["hip"][1] - 6.0, anc["hip"][1],
                    fur(P, "brown", "brown_dark"), cut=1)
    m.round_box(a["neck"], 0, -12.0, 3.6, 3.6, 20.0, 27.0, fur(P, "brown", "brown_dark"), cut=1)
    return m
