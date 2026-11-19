"""Volcdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a living volcano dragon: a hulking four-legged body of black lava rock split by glowing orange
magma veins, flames licking up from its back under a cloud of black smoke, blue crystal studs on its shoulders, purple
obsidian hooves, and a small fierce teal dragon head with a spiked crest. 25 blocks.

Front is -z, y is up. Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digidetail import gem, metal, scales, solid
from _route import pal, tone

HEIGHT = 45
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a hulking lava-rock dragon split by glowing magma veins, flames and black smoke on its back and a small teal dragon head"
BASE = {"rock": (50, 40, 40), "rock_dark": (20, 14, 14), "magma": (255, 130, 30), "flame": (255, 170, 50, 210),
        "smoke": (40, 38, 44, 200), "teal": (60, 150, 160), "teal_dark": (20, 80, 90), "crystal": (90, 130, 240),
        "crystal_light": (190, 210, 255), "hoof": (110, 80, 150), "eye": (255, 230, 80), "steel": (200, 204, 214)}
SHINY = {"magma": (90, 220, 255), "flame": (120, 220, 255, 210), "teal": (200, 90, 60), "teal_dark": (120, 40, 20)}


def P(v):
    return pal(BASE, SHINY, v)


def lavaf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    v = abs(math.sin(x * 0.7 + z * 0.4) + math.cos(y * 0.6 - x * 0.3) * 0.8)
    if v < 0.16:
        return p["magma"], p["magma"]
    if y < 2.2:
        return tone(p["hoof"], face), None
    return tone(p["rock"] if (int(x + 40) + int(y) + int(z + 40)) % 3 else p["rock_dark"], face), None


def headf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west") and abs(z + 22.0) < 0.8 and abs(y - 33.0) < 0.6:
        return p["eye"], p["eye"]
    return scales(P, "teal", "teal_dark", size=0.9)(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("volcdramon")
    mats = {"skin": lavaf, "belly": lavaf, "neck": lavaf, "head": headf, "leg": lavaf, "paw": lavaf,
            "claw": solid(P, "hoof"), "tail": lavaf}
    a = quadruped(m, mats, "volcdramon", length=26.0, body_y=18.0, body_rx=9.0, body_ry=9.0, chest_bulk=1.15,
                  neck=((0, 26, -14), (0, 31, -18)), head_len=9.0, head_w=3.0, head_h=3.4, snout=0.6, mouth_open=14,
                  teeth=4, tail=((0, 18, 14), (0, 14, 18)), tail_r=(3.0, 2.0), toes=3, claws=True)
    bd, hd = a["body"], a["head"]
    for j in range(5):
        spike(m, hd, ((j - 2) * 0.6, 34.0, -17.0 + abs(j - 2) * 0.4), ((j - 2) * 0.3, 0.6, 1), 0.9, 4.0,
              metal(P, "steel"), tip=0.8)
    for sx in (-1, 1):
        for j in range(2):
            ball(m, bd, (sx * 8.6, 22.0 - j * 3.0, -8.0 + j * 2.0), 1.2, gem(P, "crystal", "crystal_light"), layers=1)
    fl = m.bone("flames", bd, (0, 26, 0))
    for i in range(10):
        ang = i * 2.4
        x, z = 5.0 * math.cos(ang), 5.0 * math.sin(ang)
        spike(m, fl, (x, 25.0, z), (x * 0.05, 1, z * 0.05), 2.4, 8.0 + (i % 3) * 3.0, solid(P, "flame", glow=True),
              tip=0.8)
    for i in range(6):
        ang = i * 1.1
        ball(m, fl, (7.0 * math.cos(ang), 38.0 + (i % 2) * 3.0, 7.0 * math.sin(ang)), 4.0, solid(P, "smoke"), layers=1)
    return m
