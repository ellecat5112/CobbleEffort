"""Gundramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the gun dragon: a towering grey-steel mech dragon-man bristling with giant revolvers and
cannons that fan out from its back and arms like wings, every barrel spitting fire, its armour plated and riveted,
smoke curling round its clawed feet. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, local, metal, riveted, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a towering grey-steel mech dragon-man bristling with giant revolvers and cannons fanning out from its back and "
        "arms, every barrel spitting fire")
BASE = {"steel": (170, 174, 186), "steel_dark": (80, 84, 96), "steel_light": (230, 232, 240), "gun": (110, 112, 124),
        "gun_dark": (40, 42, 50), "red": (210, 40, 40), "eye": (240, 60, 40), "fire": (255, 170, 40, 215),
        "fire_core": (255, 245, 180, 240)}
SHINY = {"steel": (200, 170, 90), "steel_dark": (130, 100, 30), "steel_light": (250, 230, 160)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "steel", "steel_dark", light="steel_light", trim="gun_dark", trim_w=0.3, rivets=True)
GUN = riveted(P, "gun", "gun_dark")


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if u / max(W, 1e-6) < 0.35 else p["fire"]
    return c, c[:3]


def gun(m, bone, base, d, length, r):
    n = math.sqrt(sum(v * v for v in d))
    u = tuple(v / n for v in d)
    end = tuple(b + v * length for b, v in zip(base, u))
    rod(m, bone, base, end, r, GUN, extend=0)
    mid = tuple(b + v * length * 0.25 for b, v in zip(base, u))
    rod(m, bone, mid, tuple(b + v * length * 0.4 for b, v in zip(base, u)), r + 2, metal(P, "steel", dark="steel_dark"),
        extend=0)
    spike(m, bone, end, d, r + 1, 5.0, firef)


def build():
    m = Model("gundramon")
    mats = {"skin": ARM, "claw": metal(P, "gun", dark="gun_dark"), "talon": metal(P, "gun", dark="gun_dark")}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.2, leg_bulk=1.15, claws=True, talons=True, digitigrade=True,
                 name="gundramon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 3.0, 3.6, 53.4, 60.0, ARM, cut=1)
    m.round_box(hd, 0, -5.0, 2.0, 1.6, 54.0, 57.4, ARM, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.4), 57.6, -4.7, max(sx * 0.8, sx * 2.4), 58.4, -4.5, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 59.6, 0), (sx * 0.4, 1, 0.4), 1.4, 5.0, ARM, tip=0.8)
    for side in (1, -1):                                                                # revolver wings
        for j, (dy, ln) in enumerate(((0.4, 26.0), (0.0, 24.0), (-0.4, 20.0))):
            gun(m, bd, (side * 5.0, 50.0 - j * 4.0, 4.0), (side * 1.0, dy + 0.3, 0.4), ln, 2)
    for nm in ("arm_left", "arm_right"):                                                 # arm cannons
        w = a[nm]["wrist"]
        sx = 1 if w[0] > 0 else -1
        gun(m, a[nm]["bone"], (w[0], w[1] + 2.0, w[2]), (sx * 0.6, 0.1, -1), 16.0, 3)
    return m
