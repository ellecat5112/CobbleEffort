"""Mercuremon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Hybrid warrior of steel: a tall green armoured jester whose head and body make one great cone
rising to a red tip, a round mirror for a face, gold-edged plates, jointed green limbs with ball joints, pointed
curled boots, a black cape and a great round mirror shield on each arm rimmed with red and green zigzags. 15 blocks
tall.

Front is -z, y is up. 72 units tall; Adult (Hybrid) stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import cape, humanoid
from _digidetail import armour, fabric, local, metal, solid
from _route import pal, tone

HEIGHT = 72
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall green armoured jester whose head and body make one great cone with a red tip, a round mirror face, "
        "pointed curled boots, a black cape and a round mirror shield on each arm")
BASE = {"green": (60, 150, 80), "green_dark": (20, 80, 40), "green_light": (140, 210, 150), "gold": (240, 200, 70),
        "gold_dark": (160, 120, 20), "red": (210, 40, 40), "mirror": (220, 234, 244), "mirror_dark": (150, 170, 190),
        "black": (30, 30, 36), "black_dark": (10, 10, 14)}
SHINY = {"green": (150, 70, 170), "green_dark": (70, 24, 90), "green_light": (210, 160, 230)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "green", "green_dark", light="green_light", trim="gold", trim_w=0.3)
JOINT = metal(P, "green_dark", dark="black")


def mirrorf(x, y, z, face, variant, box=None, **k):
    """A mirror: pale blue-white with a bright diagonal sheen."""
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    s = (u / max(W, 1e-6) + v / max(H, 1e-6))
    c = p["mirror"] if 0.7 < s < 1.0 or s > 1.4 else p["mirror_dark"]
    return c, None


def rimf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    t = (u + v) % 2.0
    return tone(p["red"] if t < 1.0 else p["green"], face), None


def shield(m, bone, c, r):
    """A round mirror shield facing -z: a zigzag rim ring and the mirror inside."""
    cx, cy, cz = c
    for i in range(16):
        ang = 2 * math.pi * i / 16
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
        m.box(bone, px - 1.2, py - 1.2, cz - 0.6, px + 1.2, py + 1.2, cz + 0.6, rimf)
    for i in range(4):                                                                  # mirror: stacked rows
        h = r - 0.8
        y0 = cy - h + i * h / 2
        w = math.sqrt(max(0.0, h * h - (y0 + h / 4 - cy) ** 2))
        m.box(bone, cx - w, y0, cz - 0.2, cx + w, y0 + h / 2, cz + 0.2, mirrorf)


def build():
    m = Model("mercuremon")
    mats = {"skin": JOINT, "chest": ARM, "abs": ARM, "pelvis": ARM, "neck": JOINT, "deltoid": ARM, "upper_arm": JOINT,
            "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": JOINT, "knee": ARM, "shin": ARM, "calf": ARM,
            "foot": ARM, "toe": ARM}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.8, leg_bulk=0.85, name="mercuremon")
    bd = a["body"]
    for j in range(9):                                                                   # the great cone body
        y0 = 36.0 + j * 4.2
        r = 8.6 - j * 0.95
        m.round_box(bd, 0, 0.2, r, r * 0.8, y0, y0 + 4.4, ARM, cut=max(1, int(r * 0.3)))
    spike(m, bd, (0, 73.6, 0.2), (0, 1, 0.1), 1.6, 4.0, solid(P, "red"), tip=0.8)
    hd = m.bone("head", bd, (0, 58, -4))
    for i in range(6):                                                                   # round mirror face
        h = 3.2
        y0 = 56.0 + i * 1.1
        w = math.sqrt(max(0.4, h * h - (y0 + 0.55 - 59.3) ** 2))
        m.box(hd, -w, y0, -6.6, w, y0 + 1.1, -6.2, mirrorf)
    m.box(hd, -1.6, 59.0, -6.7, 1.6, 59.5, -6.6, solid(P, "red"))
    for nm in ("arm_left", "arm_right"):                                                 # ball joints, shields
        anc = a[nm]
        ball(m, anc["bone"], anc["elbow"], 1.8, JOINT, layers=2)
        sx = 1 if anc["hand"][0] > 0 else -1
        shield(m, anc["bone"], (anc["wrist"][0] + sx * 1.0, anc["wrist"][1] + 2.0, anc["wrist"][2] - 3.0), 7.0)
    for nm in ("leg_left", "leg_right"):                                                 # pointed curled boots
        anc = a[nm]
        ball(m, anc["bone"], anc["knee"], 2.0, JOINT, layers=2)
        ank = anc["ankle"]
        rod(m, anc["bone"], (ank[0], 1.0, ank[2] - 3.0), (ank[0], 3.0, ank[2] - 8.0), 2, ARM, extend=0.3)
        spike(m, anc["bone"], (ank[0], 3.0, ank[2] - 8.0), (0, 1, -0.3), 1.2, 2.4, ARM, tip=0.8)
    cape(m, bd, 50.0, 14.0, 40.0, fabric(P, "black", "black_dark"), z=6.0, flare=0.6, panels=6)
    return m
