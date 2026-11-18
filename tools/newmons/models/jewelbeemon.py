"""Jewelbeemon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the jewel bee knight: a tall slender green insect warrior with a helmeted head, big red compound
eyes and long antennae, green carapace plates studded all over with round gold-and-amber jewels, red joint bands,
translucent wings, a long spear with a red star-shaped head and pointed insect feet. 25 blocks tall.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, gem, local, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall slender green insect knight with red compound eyes, carapace plates studded with gold-and-amber jewels, "
        "translucent wings and a spear with a red star head")
BASE = {"green": (90, 170, 60), "green_dark": (30, 90, 20), "green_light": (170, 230, 120), "gold": (240, 200, 70),
        "amber": (240, 150, 40), "amber_light": (255, 230, 150), "red": (210, 40, 40), "red_light": (250, 140, 120),
        "eye": (220, 40, 40), "wing": (200, 230, 250, 140), "wing_vein": (120, 170, 220, 200), "shaft": (210, 170, 90),
        "black": (24, 24, 30)}
SHINY = {"green": (60, 120, 210), "green_dark": (20, 50, 140), "green_light": (140, 190, 250)}


def P(v):
    return pal(BASE, SHINY, v)


CARA = armour(P, "green", "green_dark", light="green_light", trim="red", trim_w=0.2)


def jewelf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    cx, cy = round(x / 3.0) * 3.0, round(y / 3.0) * 3.0
    if face != "down" and math.hypot(x - cx if face in ("north", "south") else z - round(z / 3.0) * 3.0, y - cy) < 0.9:
        return tone(p["amber_light"] if y - cy > 0.3 else p["amber"], face), None
    return CARA(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["wing_vein"] if (u % 2.4) < 0.3 else p["wing"]), None


def wing_in(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    a, b = u / max(W, 1e-6) - 0.5, v / max(H, 1e-6) - 0.5
    return a * a / 0.25 + b * b / 0.25 < 1.0


def build():
    m = Model("jewelbeemon")
    mats = {"skin": jewelf, "chest": jewelf, "abs": CARA, "pelvis": jewelf, "neck": solid(P, "red"), "deltoid": jewelf,
            "upper_arm": jewelf, "forearm": jewelf, "hand": CARA, "finger": CARA, "thigh": jewelf, "knee": solid(P, "red"),
            "shin": jewelf, "calf": jewelf, "foot": CARA, "toe": CARA}
    a = humanoid(m, mats, bulk=0.82, arm_bulk=0.85, leg_bulk=0.9, digitigrade=True, name="jewelbeemon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, CARA, cut=1)
    for sx in (-1, 1):
        m.round_box(hd, sx * 1.6, -3.0, 1.2, 0.6, 56.6, 59.0, gem(P, "eye", "red_light"), cut=0)
        pts = [(sx * 1.0, 60.2, -1.0), (sx * 3.0, 66.0, -2.0), (sx * 6.0, 69.0, -1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "black"), extend=0.2, t2=1)
    for sx in (-1, 1):                                                               # jewel pauldrons
        m.round_box(bd, sx * 7.0, 0, 3.0, 3.0, 47.0, 53.0, gem(P, "amber", "amber_light", glow=False), cut=2)
    W = cutout(wing_in, wingf)
    for side in (1, -1):
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 2.0, 48.0, 3.6))
        for j, (ln, ang) in enumerate(((16.0, 25), (12.0, -15))):
            x0, x1 = sorted((side * 2.0, side * (2.0 + ln)))
            m.box(wb, x0, 46.0, 3.8, x1, 52.0, 3.8, W, rotation=(0, side * -25, side * ang), pivot=(side * 2.0, 48.0, 3.8))
    hl = a["arm_left"]                                                               # star-headed spear
    lx, ly, lz = hl["hand"]
    rod(m, hl["bone"], (lx, ly - 22.0, lz), (lx, ly + 18.0, lz), 1, solid(P, "shaft"), extend=0, t2=1)
    for j in range(5):
        ang = 2 * math.pi * j / 5
        spike(m, hl["bone"], (lx, ly + 20.0, lz), (math.sin(ang), math.cos(ang), 0), 1.2, 4.0, solid(P, "red"), tip=0.8)
    spike(m, hl["bone"], (lx, ly + 20.0, lz), (0, 1, 0), 1.2, 7.0, solid(P, "red"), tip=0.8)
    return m
