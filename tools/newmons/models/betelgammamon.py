"""Betel Gammamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a red dragon-man of explosive power. A lean red body with white stripes down its limbs, a horned
dragon head with yellow eyes, a blue scarf tied over its muzzle with long blue tails streaming behind like tattered
wings, white clawed hands and feet, a long red tail, and a blast of dark fire in its fist. 15 blocks tall.

Front is -z, y is up. 62 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, fabric, flame_inside, local, metal, skin, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(15, HEIGHT, 2.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a red dragon-man with white limb stripes, a horned head with yellow eyes, a blue scarf with long tattered "
        "tails, white claws, a long red tail and dark fire in its fist")
BASE = {"red": (210, 40, 40), "red_dark": (120, 14, 16), "red_light": (250, 130, 120), "white": (246, 244, 240),
        "blue": (50, 80, 190), "blue_dark": (20, 34, 110), "claw": (240, 240, 246), "eye": (255, 220, 60),
        "fire": (60, 40, 30, 230), "fire_core": (250, 180, 60, 240), "horn": (230, 230, 236)}
SHINY = {"red": (60, 60, 74), "red_dark": (24, 24, 30), "red_light": (130, 130, 150), "blue": (220, 140, 40),
         "blue_dark": (150, 80, 16)}


def P(v):
    return pal(BASE, SHINY, v)


def striped(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    if face in ("north", "south") and abs(u - W / 2) < W * 0.15:
        return tone(p["white"], face), None
    return skin(P, "red", dark="red_dark", light="red_light")(x, y, z, face, variant, box=box, **k)


def torn(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    return v / max(H, 1e-6) > 0.2 * abs(math.sin((box.lo[0] + u) * 2.6))


def firef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["fire_core"] if v / max(H, 1e-6) < 0.35 else p["fire"]
    return c, c[:3]


def build():
    m = Model("betelgammamon")
    RED = skin(P, "red", dark="red_dark", light="red_light")
    mats = {"skin": striped, "chest": RED, "abs": RED, "pelvis": RED, "neck": RED, "hand": RED,
            "finger": solid(P, "claw"), "claw": solid(P, "claw"), "foot": RED, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="betelgammamon", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.6, 3.0, 54.4, 60.6, RED, cut=1)
    m.box(hd, -1.8, 54.6, -7.0, 1.8, 57.6, -2.8, RED)                                    # snout
    m.box(hd, -2.2, 54.4, -6.0, 2.2, 57.0, -2.0, fabric(P, "blue", "blue_dark"))         # scarf over the muzzle
    for sx in (-1, 1):
        m.box(hd, sx * 1.4 - 0.6, 58.6, -3.9, sx * 1.4 + 0.6, 59.4, -3.7, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 60.0, 0.0), (sx * 0.4, 1, 0.6), 1.4, 4.0, solid(P, "horn"))
    sk = m.bone("skirt", bd, (0, 52, 3))                         # long scarf tails like tattered wings
    for j in range(3):
        rod(m, sk, (-1.0 + j, 53.0, 3.0), (-16.0 - j * 4, 62.0 - j * 3, 10.0 + j * 2), 1,
            cutout(torn, fabric(P, "blue", "blue_dark")), extend=0.3, t2=4)
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31, 3), (4, 24, 9), (10, 20, 12), (16, 22, 12), (19, 26, 10)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 4 - j), RED, extend=0.4)
    h = a["arm_right"]["hand"]                                   # dark fire in its fist
    for ang in (0, 60, 120):
        m.box(a["arm_right"]["bone"], h[0] - 4.0, h[1] - 2.0, h[2], h[0] + 4.0, h[1] + 10.0, h[2],
              cutout(flame_inside(4, -0.2, 2), firef), rotation=(0, ang, 0), pivot=h)
    return m
