"""Magna Kidmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the crimson demon dragon-knight: a lean figure in spiky crimson armour, a horned dragon helm,
great tattered black bat wings, a long silver blade-arm, a belt of brown straps looping round it and green flames
burning in its claws. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import humanoid
from _digidetail import armour, cutout, flame_inside, leather, local, metal, noise2, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a lean demon dragon-knight in spiky crimson armour with a horned helm, tattered black bat wings, a silver blade-arm and green flames"
BASE = {"red": (180, 30, 40), "red_dark": (90, 10, 14), "red_light": (240, 110, 110), "black": (30, 28, 34),
        "silver": (210, 214, 224), "silver_dark": (100, 104, 116), "brown": (130, 90, 60), "brown_dark": (70, 40, 20),
        "eye": (250, 220, 60), "fire": (120, 255, 120, 210), "fire_core": (230, 255, 220, 240)}
SHINY = {"red": (40, 60, 160), "red_dark": (14, 20, 80), "red_light": (120, 150, 240), "fire": (255, 120, 220, 210)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "red", "red_dark", light="red_light", trim="black", trim_w=0.25)


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.3 else p["fire"]
    return c, c[:3]


def tatter(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.14 * abs(math.sin(u * 0.8)) + 0.06 * noise2(u, 0.0, 4)


def build():
    m = Model("magnakidmon")
    mats = {"skin": ARM, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": ARM, "deltoid": ARM, "upper_arm": ARM,
            "forearm": ARM, "hand": ARM, "finger": ARM, "claw": solid(P, "black"), "thigh": ARM, "knee": ARM, "shin": ARM,
            "calf": ARM, "foot": ARM, "talon": solid(P, "black")}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.9, leg_bulk=0.9, claws=True, talons=True, digitigrade=True, name="magnakidmon")
    bd = a["body"]
    for nm in ("arm_left", "arm_right", "leg_left", "leg_right"):                    # spiky armour
        anc = a[nm]
        j = anc.get("elbow") or anc.get("knee")
        sx = 1 if j[0] > 0 else -1
        spike(m, anc["bone"], j, (sx, 0.3, 0.4), 1.2, 4.0, ARM, tip=0.8)
    hd = m.bone("head", bd, (0, 55, -1))
    m.round_box(hd, 0, -1.6, 2.6, 3.6, 53.6, 59.6, ARM, cut=1)
    m.round_box(hd, 0, -5.2, 1.6, 1.6, 53.8, 56.6, ARM, cut=1)
    m.box(hd, -1.6, 57.2, -5.1, 1.6, 57.8, -5.0, solid(P, "eye", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 59.0, 0), (sx * 0.5, 1, 0.6), 1.4, 6.0, ARM, tip=0.8)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.4))
        bat_wing(m, wb, (side * 3.0, 50.0, 3.4), 28.0, 22.0, 4, solid(P, "black"), cutout(tatter, solid(P, "black")),
                 side=side, sweep=20)
    hr = a["arm_right"]                                                              # silver blade-arm
    hx, hy, hz = hr["hand"]
    m.round_box(hr["bone"], hx, hz - 0.6, 1.4, 0.6, hy - 28.0, hy, metal(P, "silver", dark="silver_dark"), cut=0)
    spike(m, hr["bone"], (hx, hy - 28.0, hz - 0.6), (0, -1, 0), 2.0, 3.0, metal(P, "silver", dark="silver_dark"), tip=0.8)
    hl = a["arm_left"]                                                               # green flame
    lx, ly, lz = hl["hand"]
    for rot in (0, 90):
        m.box(hl["bone"], lx - 2.4, ly + 1.0, lz, lx + 2.4, ly + 8.0, lz, cutout(flame_inside(4, 0.1, 3), firef),
              rotation=(0, rot, 0), pivot=(lx, ly + 1.0, lz))
    for i in range(10):                                                              # looping belt straps
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        rod(m, bd, (10.0 * math.cos(a0), 36.0 + 3.0 * math.sin(a0), 6.0 * math.sin(a0)),
            (10.0 * math.cos(a1), 36.0 + 3.0 * math.sin(a1), 6.0 * math.sin(a1)), 1, leather(P, "brown", "brown_dark"),
            extend=0.2, t2=1)
    return m
