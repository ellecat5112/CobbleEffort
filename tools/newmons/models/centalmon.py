"""Centalmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the centaur hunter. An orange-hided centaur covered in rounded violet-blue armour plates, a steel
helm on its human-like upper body, a steel arm-cannon crackling with energy on its right, a chained shackle on its
left wrist, silver hooves and a flaming tail. 15 blocks tall.

Front is -z, y is up. 50 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digidetail import armour, cutout, flame_inside, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 50
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 14}
LOOK = ("an orange-hided centaur covered in violet-blue armour plates, a steel helm, a crackling steel arm-cannon, a "
        "chained shackle, silver hooves and a flaming tail")
BASE = {"orange": (240, 160, 50), "orange_dark": (180, 100, 20), "plate": (80, 80, 190), "plate_dark": (30, 30, 110),
        "plate_light": (150, 150, 240), "steel": (200, 204, 216), "steel_dark": (90, 94, 106), "eye": (250, 60, 40),
        "flame": (255, 150, 40, 220), "flame_core": (255, 240, 160, 240), "bolt": (255, 250, 150)}
SHINY = {"orange": (200, 200, 210), "orange_dark": (130, 130, 146), "plate": (190, 60, 60), "plate_dark": (110, 20, 20),
         "plate_light": (250, 140, 140)}


def P(v):
    return pal(BASE, SHINY, v)


STEEL = metal(P, "steel", dark="steel_dark")


def spotted(x, y, z, face, variant, box=None, **k):
    """Orange hide covered in rounded violet-blue plates (a grid of oval patches)."""
    p = P(variant)
    a, b = (x, y) if face in ("north", "south") else (z, y) if face in ("east", "west") else (x, z)
    du = ((a + 1.0) % 3.6) - 1.8
    dv = ((b + 0.6) % 3.0) - 1.5
    if (du / 1.5) ** 2 + (dv / 1.2) ** 2 < 1.0:
        return armour(P, "plate", "plate_dark", light="plate_light")(x, y, z, face, variant, box=box, **k)
    return skin(P, "orange", dark="orange_dark", var=0.03)(x, y, z, face, variant, box=box, **k)


def flamef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["flame_core"] if v / max(H, 1e-6) < 0.3 else p["flame"]
    return c, c[:3]


def build():
    m = Model("centalmon")
    mats = {"skin": spotted, "belly": spotted, "neck": spotted, "head": STEEL, "snout": STEEL, "jaw": STEEL,
            "leg_upper": spotted, "leg_lower": spotted, "paw": STEEL, "claw": STEEL, "tail": spotted}
    a = quadruped(m, mats, "centalmon", length=22.0, body_y=18.0, body_rx=5.4, body_ry=5.4, chest_bulk=1.1,
                  neck=((0, 26, -10), (0, 34, -11)), head_len=4.0, head_w=2.0, head_h=2.0, snout=0.2, mouth_open=0,
                  teeth=0, leg_bulk=1.3, toes=2, claws=False, tail=((0, 22, 14), (0, 26, 18)), tail_r=(1.2, 0.8))
    bd, nk = a["body"], a["neck"]
    # the upper body rising from the front of the horse body
    m.round_box(nk, 0, -10.0, 4.6, 3.4, 24.0, 38.0, spotted, cut=1)
    m.round_box(nk, 0, -10.0, 5.6, 3.8, 34.0, 40.0, spotted, cut=1)
    hd = a["head"]
    m.round_box(hd, 0, -10.6, 2.6, 2.8, 40.0, 47.0, STEEL, cut=1)                     # steel helm
    m.box(hd, -2.0, 43.6, -13.5, 2.0, 44.2, -13.3, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 46.4, -10.0), (sx * 0.3, 1, 0.3), 1.2, 3.0, STEEL)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab = m.bone(nm, nk, (sx * 5.6, 38.0, -10.0))
        el = (sx * 8.0, 32.0, -12.0)
        hand = (sx * 8.4, 26.0, -16.0)
        rod(m, ab, (sx * 5.6, 38.0, -10.0), el, 3, spotted, extend=0.5)
        if sx < 0:                                                                    # the arm-cannon
            rod(m, ab, el, (sx * 9.0, 30.0, -24.0), 4, STEEL, extend=0.5)
            for j in range(4):
                spike(m, ab, (sx * 9.0, 30.0, -24.0), (math.cos(j * 1.6), math.sin(j * 1.6), -1), 0.6, 3.0,
                      solid(P, "bolt", glow=True))
        else:                                                                         # the chained shackle
            rod(m, ab, el, hand, 3, spotted, extend=0.5)
            m.round_box(ab, hand[0], hand[2], 2.0, 2.0, hand[1] - 1.0, hand[1] + 1.4, STEEL, cut=1)
            for j in range(5):
                y0 = hand[1] - 1.4 - j * 1.8
                m.box(ab, hand[0] - 0.5, y0 - 1.4, hand[2] - 0.5, hand[0] + 0.5, y0, hand[2] + 0.5, STEEL,
                      rotation=(0, 90 * (j % 2), 0), pivot=(hand[0], y0, hand[2]))
    tl = a["tail"]                                                                    # the flaming tail
    e = a["tail_pts"][-1]
    for ang in (0, 90):
        m.box(tl, e[0] - 3.0, e[1], e[2], e[0] + 3.0, e[1] + 9.0, e[2], cutout(flame_inside(4, 0.2, 2), flamef),
              rotation=(-30, ang, 0), pivot=e)
    return m
