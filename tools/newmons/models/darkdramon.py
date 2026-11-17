"""Darkdramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the cyborg dragon general. A lean armoured dragon-man in navy plate with gold chevron stripes, a
crimson chest core, a long-snouted dragon helm with twisted silver horns, huge silver talon gauntlets, digitigrade
clawed legs, a whip of a tail and two great pale-blue energy wings streaming from its back. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, cutout, gem, local, metal, noise2, solid, twisted
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean navy-armoured cyborg dragon with gold chevrons, a crimson chest core, a dragon helm with twisted silver "
        "horns, silver talon gauntlets and great pale-blue energy wings")
BASE = {"navy": (40, 54, 120), "navy_dark": (14, 20, 54), "navy_light": (100, 120, 200), "gold": (240, 200, 60),
        "red": (200, 30, 60), "red_light": (255, 140, 170), "steel": (214, 218, 230), "steel_dark": (110, 114, 130),
        "wing": (190, 220, 250, 150), "wing_light": (240, 250, 255, 190), "mouth": (150, 20, 40),
        "tooth": (250, 250, 246), "eye": (250, 60, 60)}
SHINY = {"navy": (90, 40, 110), "navy_dark": (40, 10, 54), "navy_light": (160, 100, 190), "wing": (250, 200, 230, 150)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "navy", "navy_dark", light="navy_light", trim="gold", trim_w=0.3)
STEEL = metal(P, "steel", dark="steel_dark")


def chevf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("north", "south", "east", "west") and abs((y + abs(x) * 0.8) % 6.0 - 3.0) < 0.5:
        return tone(p["gold"], face), None
    return PLATE(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    n = noise2(u * 0.4, v * 0.15, 3)
    c = p["wing_light"] if n > 0.62 else p["wing"]
    return c, c[:3] if n > 0.75 else None


def wing_inside(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = u / max(W, 1e-6)
    return v / max(H, 1e-6) < 0.35 + 0.65 * (1 - t) + 0.08 * math.sin(u * 1.3)


def build():
    m = Model("darkdramon")
    mats = {"skin": chevf, "chest": chevf, "abs": PLATE, "pelvis": PLATE, "neck": PLATE, "deltoid": chevf,
            "upper_arm": PLATE, "forearm": STEEL, "hand": STEEL, "finger": STEEL, "claw": STEEL, "thigh": chevf,
            "knee": STEEL, "shin": PLATE, "calf": PLATE, "foot": STEEL, "talon": STEEL}
    a = humanoid(m, mats, bulk=0.9, arm_bulk=1.1, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="darkdramon")
    bd = a["body"]
    m.round_box(bd, 0, a["chest_front"] + 0.6, 2.4, 1.0, 45.0, 49.0, gem(P, "red", "red_light"), cut=1)   # chest core
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0.4, 2.8, 3.2, 54.0, 60.0, chevf, cut=1)
    m.round_box(hd, 0, -5.0, 1.8, 3.0, 54.6, 58.0, PLATE, cut=1)                       # long snout
    m.box(hd, -1.6, 53.4, -7.4, 1.6, 54.6, -2.6, PLATE)                                # lower jaw
    m.box(hd, -1.4, 54.4, -7.2, 1.4, 54.8, -2.6, solid(P, "mouth"))
    for i in range(3):
        for sx in (-1, 1):
            spike(m, hd, (sx * 1.2, 55.0, -7.0 + i * 1.4), (0, -1, 0), 0.6, 1.0, solid(P, "tooth"))
    for sx in (-1, 1):
        m.box(hd, min(sx * 2.4, sx * 2.9), 57.6, -3.2, max(sx * 2.4, sx * 2.9), 58.4, -1.6, solid(P, "eye", glow=True))
        pts = [(sx * 2.4, 59.4, 1.0)]
        for j in range(1, 6):                                                          # twisted silver horns
            t = j / 5
            pts.append((sx * (2.4 + 3.0 * t), 59.4 + 5.0 * t + math.sin(t * 6) * 0.8, 1.0 + 7.0 * t))
        for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
            rod(m, hd, p0, p1, 2 if j < 3 else 1, twisted(P, "steel", "steel_dark"), extend=0.4)
    for nm in ("arm_left", "arm_right"):                                               # talon gauntlets
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        for j in range(3):
            spike(m, ar["bone"], (hx + (j - 1) * 1.0, hy - 3.0, hz - 1.0), (0, -1, -0.3), 1.0, 6.0, STEEL, tip=0.3)
    for side in (1, -1):                                                               # energy wings
        wb = m.bone("wing_left" if side > 0 else "wing_right", bd, (side * 3.0, 50.0, 3.4))
        for j in range(3):
            x0, x1 = sorted((side * 3.0, side * (26.0 - j * 4.0)))
            m.box(wb, x0, 40.0 + j * 4.0, 3.6 + j * 0.4, x1, 64.0 + j * 2.0, 3.6 + j * 0.4, cutout(wing_inside, wingf),
                  rotation=(0, side * (24 + j * 10), side * (10 + j * 8)), pivot=(side * 3.0, 50.0, 3.4))
    tl = m.bone("tail", bd, (0, 32, 3))
    pts = [(0, 32.0, 3.0), (0, 26.0, 10.0), (3.0, 18.0, 16.0), (7.0, 12.0, 20.0), (10.0, 10.0, 26.0)]
    for j, (p0, p1) in enumerate(zip(pts, pts[1:])):
        rod(m, tl, p0, p1, max(1, 3 - j), chevf, extend=0.5)
    spike(m, tl, pts[-1], (0.4, 0, 1), 1.4, 3.0, STEEL)
    return m
