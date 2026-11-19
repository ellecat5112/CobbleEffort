"""Soloogarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a demon-beast enforcer: a black-armoured wolf-man with flame decals on its plates, a jackal-eared
helm with a red visor, a burning canister on its back spitting fire, a blue-flamed blowtorch lance in one hand, a heavy
gun-arm in the other, and clawed black boots. 25 blocks.

Front is -z, y is up. 66 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, metal, solid
from _route import pal, tone

HEIGHT = 66
SCALE, HITBOX = sized(25, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a black-armoured wolf-man with flame decals, a jackal-eared helm, a fire-spitting canister on its back and a blue-flamed torch lance"
BASE = {"black": (40, 38, 46), "black_dark": (12, 12, 16), "steel": (170, 174, 186), "steel_dark": (80, 84, 96),
        "flame": (250, 130, 40), "blue": (90, 150, 250), "red": (210, 40, 40), "violet": (110, 70, 170),
        "fire": (255, 150, 40, 220), "torch": (120, 190, 255, 220)}
SHINY = {"black": (200, 200, 214), "black_dark": (120, 120, 140)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "east", "west") and abs(math.sin(x * 1.3 + y * 0.6)) > 0.93 and y < 30.0:
        return tone(p["flame"] if y < 20.0 else p["blue"], face), None
    return armour(P, "black", "black_dark", trim="violet", trim_w=0.2)(x, y, z, face, variant, box=box, **k)


STEEL = metal(P, "steel", dark="steel_dark")
FIRE = cutout(flame_inside(tongues=4), solid(P, "fire", glow=True))


def build():
    m = Model("soloogarmon")
    mats = {"skin": platef, "talon": STEEL, "claw": STEEL}
    a = humanoid(m, mats, bulk=1.05, arm_bulk=1.05, leg_bulk=1.05, talons=True, claws=True, digitigrade=True,
                 name="soloogarmon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.4, 2.6, 3.6, 54.0, 60.0, platef, cut=1)
    m.round_box(hd, 0, -4.8, 1.6, 1.4, 54.4, 57.0, platef, cut=0)
    m.box(hd, -1.8, 57.6, -4.5, 1.8, 58.4, -4.3, solid(P, "red", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 1.6, 60.0, 0), (sx * 0.2, 1, 0.1), 1.4, 6.0, platef, tip=0.8)   # jackal ears
    rod(m, bd, (6.0, 46.0, 6.0), (10.0, 58.0, 6.0), 4, STEEL, extend=0.4)                     # fire canister
    m.box(bd, 6.0, 58.0, 4.0, 14.0, 70.0, 4.0, FIRE)
    w = a["arm_right"]["wrist"]                                                          # blue torch lance
    rod(m, a["arm_right"]["bone"], (w[0], w[1] - 2.0, w[2] + 6.0), (w[0] - 4.0, w[1] + 2.0, w[2] - 12.0), 1, STEEL,
        extend=0.2)
    spike(m, a["arm_right"]["bone"], (w[0] - 4.0, w[1] + 2.0, w[2] - 12.0), (-0.2, 0.1, -1), 1.6, 8.0,
          solid(P, "torch", glow=True), tip=0.8)
    w = a["arm_left"]["wrist"]                                                           # heavy gun-arm
    rod(m, a["arm_left"]["bone"], (w[0], w[1] + 4.0, w[2]), (w[0] + 1.0, w[1] - 10.0, w[2] - 4.0), 4, STEEL, extend=0.4)
    return m
