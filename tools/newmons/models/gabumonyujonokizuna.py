"""Gabumon -Yujo no Kizuna- (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after
the official art on wikimon.net): Gabumon's "Bond of Friendship" form: a lean wolf-knight in navy-blue armour
streaked with pink circuit lines, a wolf helm with a fierce snout, arm-mounted cannons, a long segmented armoured tail,
clawed feet, and two glowing golden discs on a staff held high, with homing missiles at its back. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, local, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean wolf-knight in navy armour with pink circuit lines, a wolf helm, arm cannons, a segmented tail and two "
        "glowing golden discs on a staff")
BASE = {"navy": (40, 50, 110), "navy_dark": (16, 20, 50), "navy_light": (110, 130, 200), "pink": (240, 80, 170),
        "steel": (200, 206, 220), "steel_dark": (90, 96, 110), "gold": (250, 220, 90), "gold_core": (255, 250, 200),
        "eye": (250, 220, 60), "claw": (230, 230, 240), "flame": (250, 160, 40)}
SHINY = {"navy": (230, 232, 240), "navy_dark": (150, 152, 170), "navy_light": (255, 255, 255), "pink": (60, 160, 250)}


def P(v):
    return pal(BASE, SHINY, v)


ARM0 = armour(P, "navy", "navy_dark", light="navy_light", trim="steel", trim_w=0.25)
STEEL = metal(P, "steel", dark="steel_dark")


def armf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (abs((x * 0.5 + y * 0.3) % 4.0 - 2.0) < 0.15 or abs((y * 0.7) % 5.0 - 2.5) < 0.12):
        return p["pink"], p["pink"]
    return ARM0(x, y, z, face, variant, box=box, **k)


def discf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    c = p["gold_core"] if math.hypot(u - W / 2, v - H / 2) < min(W, H) * 0.2 else p["gold"]
    return c, c


def build():
    m = Model("gabumonyujonokizuna")
    mats = {"skin": armf, "claw": solid(P, "claw"), "talon": solid(P, "claw"), "hand": STEEL, "finger": STEEL}
    a = humanoid(m, mats, bulk=0.85, arm_bulk=0.95, leg_bulk=0.95, claws=True, talons=True, digitigrade=True,
                 name="gabumonyujonokizuna")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.8, 3.0, 53.6, 59.6, armf, cut=1)
    m.round_box(hd, 0, -4.6, 1.8, 1.8, 53.8, 56.8, armf, cut=1)                      # wolf snout
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.8, sx * 2.2), 57.4, -3.5, max(sx * 0.8, sx * 2.2), 58.2, -3.3, solid(P, "eye", glow=True))
        spike(m, hd, (sx * 2.0, 59.0, 0.4), (sx * 0.4, 1, 0.5), 1.6, 5.0, armf, tip=0.8)   # ears
        for j in range(4):                                                             # shoulder missiles
            spike(m, bd, (sx * (4.0 + j * 1.6), 50.0, 5.0), (sx * 0.3, 0.8, 0.6), 1.2, 4.0,
                  solid(P, "steel"), tip=0.8)
    for nm in ("arm_left", "arm_right"):                                               # arm cannons
        arm = a[nm]
        w = arm["wrist"]
        rod(m, arm["bone"], (w[0], w[1] + 2.0, w[2]), (w[0], w[1] + 2.0, w[2] - 9.0), 3, STEEL, extend=0)
        m.box(arm["bone"], w[0] - 0.6, w[1] + 1.4, w[2] - 9.6, w[0] + 0.6, w[1] + 2.6, w[2] - 9.0,
              solid(P, "flame", glow=True))
    tb = m.bone("tail", bd, (0, 32, 3))                                                # segmented armoured tail
    pts = [(0, 32.0, 3.0), (2.0, 24.0, 9.0), (5.0, 16.0, 13.0), (9.0, 9.0, 14.0), (13.0, 4.0, 12.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tb, p0, p1, 3 - j // 2, armf, extend=0.4)
    ar, h = a["arm_right"]["bone"], a["arm_right"]["hand"]                             # staff + two golden discs
    rod(m, ar, (h[0], h[1] - 2.0, h[2] - 1.0), (h[0] - 2.0, h[1] + 30.0, h[2] - 1.0), 1, STEEL, extend=0)
    for j, (dy, dx) in enumerate(((30.0, -2.0), (22.0, 8.0))):
        m.box(ar, h[0] + dx - 4.0, h[1] + dy - 4.0, h[2] - 1.5, h[0] + dx + 4.0, h[1] + dy + 4.0, h[2] - 0.5, discf)
    return m
