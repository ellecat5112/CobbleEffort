"""Yaksamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Armor Digimon of sincerity: a lean blue-skinned demon warrior in a white one-horned mask with a
shock of red hair, a knotted green rope across its chest, ragged white hakama trousers, white furred clawed feet, and
two wooden club-staves each hung with a wooden board marked with a red seal. 15 blocks.

Front is -z, y is up. 66 units tall; Adult stage (Armor).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import fabric, fur, leather, plane, skin, solid, strands
from _route import pal, tone

HEIGHT = 65
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean blue demon warrior in a white one-horned mask with red hair, a green rope, ragged white hakama and two wooden staves with seal boards"
BASE = {"blue": (120, 170, 220), "blue_dark": (60, 100, 160), "white": (240, 240, 244), "white_dark": (180, 180, 190),
        "red": (210, 50, 40), "hair": (210, 60, 40), "hair_dark": (140, 24, 14), "green": (70, 150, 70),
        "wood": (160, 110, 60), "wood_dark": (100, 64, 30), "black": (30, 30, 34), "eye": (250, 60, 60)}
SHINY = {"blue": (200, 120, 200), "blue_dark": (130, 60, 130), "hair": (240, 220, 120), "hair_dark": (190, 160, 60)}


def P(v):
    return pal(BASE, SHINY, v)


BLUE = skin(P, "blue", dark="blue_dark")
HAKAMA = fabric(P, "white", "white_dark")


def boardf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south") and box is not None:
        cx = box.lo[0] + box.size[0] / 2
        cy = box.lo[1] + box.size[1] / 2
        if abs(abs(x - cx) - abs(y - cy)) < 0.4 and abs(x - cx) < 1.6:
            return tone(p["red"], face), None
    return fabric(P, "wood", "wood_dark")(x, y, z, face, variant, box=box, **k)


def build():
    m = Model("yaksamon")
    mats = {"skin": BLUE, "chest": BLUE, "abs": BLUE, "pelvis": leather(P, "black", "black"), "deltoid": BLUE,
            "upper_arm": BLUE, "forearm": BLUE, "hand": BLUE, "thigh": HAKAMA, "knee": HAKAMA, "shin": HAKAMA,
            "calf": HAKAMA, "foot": fur(P, "white", "white_dark"), "talon": solid(P, "white"), "neck": BLUE}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, talons=True, name="yaksamon")
    bd = a["body"]
    for nm in ("leg_left", "leg_right"):
        k = a[nm]["knee"]
        m.round_box(a[nm]["bone"], k[0], k[2], 3.4, 3.4, 6.0, 28.0, HAKAMA, cut=1)
    for j in range(8):                                                                  # knotted green rope
        t = j / 7
        ball(m, bd, (-5.0 + t * 10.0, 50.0 - t * 12.0, -4.0), 0.9, solid(P, "green"), layers=1)
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 2.8, 3.0, 54.0, 61.0, fabric(P, "white", "white_dark"), cut=1)       # white mask
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 1.8), 58.0, -3.2, max(sx * 0.6, sx * 1.8), 58.8, -3.0, solid(P, "eye", glow=True))
    spike(m, hd, (0, 61.0, -1.0), (0.1, 1, -0.2), 1.2, 6.0, solid(P, "white"), tip=0.8)
    for j in range(7):
        ang = (j - 3) * 0.4
        spike(m, hd, (math.sin(ang) * 2.4, 60.0, 2.0), (math.sin(ang) * 0.8, 0.2, 1), 1.4, 7.0,
              strands(P, "hair", "hair_dark"), tip=0.8)
    for nm in ("arm_left", "arm_right"):                                               # club-staves with seal boards
        h = a[nm]["hand"]
        sx = 1 if nm == "arm_left" else -1
        rod(m, a[nm]["bone"], (h[0] - sx * 6.0, h[1] - 3.0, h[2] - 8.0), (h[0] + sx * 4.0, h[1] + 2.0, h[2] + 6.0), 1,
            leather(P, "wood", "wood_dark"), extend=0.0)
        m.box(a[nm]["bone"], h[0] + sx * 1.0 - 2.4, h[1] + 2.0, h[2] - 0.6, h[0] + sx * 1.0 + 2.4, h[1] + 8.0, h[2] + 0.6,
              boardf)
    return m
