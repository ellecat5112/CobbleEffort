"""Climbmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the climbing insect. A lean black ant-like insect-man in a hot-pink climbing harness with a gold
buckle, long golden antennae, four arms holding pickaxes and ropes, two enormous curved ice-axe blades wrapped in
white tape held above and below, and hooked clawed feet. 25 blocks tall.

Front is -z, y is up. 62 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import armour, leather, local, metal, solid
from _route import pal, tone

HEIGHT = 62
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a lean black insect-man in a hot-pink climbing harness, with golden antennae, four arms and two enormous "
        "tape-wrapped curved ice-axe blades")
BASE = {"black": (36, 36, 44), "black_dark": (14, 14, 18), "black_light": (100, 100, 116), "pink": (240, 60, 180),
        "pink_dark": (160, 20, 110), "gold": (230, 186, 60), "gold_dark": (160, 120, 20), "steel": (200, 204, 216),
        "steel_dark": (90, 94, 106), "tape": (240, 240, 236), "tape_dark": (190, 190, 184), "eye": (250, 220, 60),
        "green": (90, 140, 60)}
SHINY = {"black": (60, 100, 70), "black_dark": (24, 50, 30), "black_light": (130, 180, 140), "pink": (250, 180, 40),
         "pink_dark": (180, 110, 10)}


def P(v):
    return pal(BASE, SHINY, v)


SHELL = armour(P, "black", "black_dark", light="black_light")
HARNESS = leather(P, "pink", "pink_dark", stitch="gold")
STEEL = metal(P, "steel", dark="steel_dark")


def tapef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["tape_dark"] if (x + y + z) % 1.6 < 0.4 else p["tape"], face), None


def axe(m, bone, grip, up, side):
    """A huge curved ice-axe: tape-wrapped haft and a long curved blade."""
    top = tuple(g + u * 16.0 for g, u in zip(grip, up))
    rod(m, bone, tuple(g - u * 3.0 for g, u in zip(grip, up)), top, 2, tapef, extend=0)
    pts = [top]
    for j in range(1, 6):
        ang = j * 0.35
        pts.append((top[0] + side * 4.0 * math.sin(ang) * j * 0.6, top[1] + 2.0 * math.cos(ang) - j * 0.8,
                    top[2] - 4.0 * j * 0.7))
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, bone, p0, p1, 1, STEEL, extend=0.3, t2=3)


def build():
    m = Model("climbmon")
    mats = {"skin": SHELL, "chest": SHELL, "abs": HARNESS, "pelvis": HARNESS, "hand": SHELL, "finger": SHELL,
            "claw": solid(P, "black_light"), "foot": SHELL, "talon": solid(P, "black_light")}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, digitigrade=True, claws=True, talons=True,
                 name="climbmon")
    bd = a["body"]
    for sx in (-1, 1):                                                         # harness straps
        rod(m, bd, (sx * 4.0, 51.0, -3.8), (-sx * 2.0, 36.0, -4.2), 1, HARNESS, extend=0.2, t2=2)
    m.box(bd, -1.4, 42.0, -4.8, 1.4, 44.4, -4.0, metal(P, "gold", dark="gold_dark"))       # gold buckle
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -1.0, 2.4, 3.0, 54.6, 60.6, SHELL, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.2), 57.4, -4.1, max(sx * 0.6, sx * 2.2), 58.6, -3.9, solid(P, "eye", glow=True))
        pts = [(sx * 1.0, 60.0, -1.0), (sx * 5.0, 66.0, 0.0), (sx * 12.0, 66.0, 2.0), (sx * 16.0, 58.0, 2.0),
               (sx * 18.0, 50.0, 1.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 1, solid(P, "gold"), extend=0.2)
    for sx in (-1, 1):                                                         # second pair of arms
        ab = m.bone("arm2_left" if sx > 0 else "arm2_right", bd, (sx * 5.0, 44.0, 0))
        rod(m, ab, (sx * 5.0, 44.0, 0), (sx * 10.0, 40.0, -4.0), 2, SHELL, extend=0.3)
        rod(m, ab, (sx * 10.0, 40.0, -4.0), (sx * 11.0, 44.0, -9.0), 2, SHELL, extend=0.3)
        rod(m, ab, (sx * 11.0, 44.0, -9.0), (sx * 11.0, 50.0, -10.0), 1, STEEL, extend=0)        # a pickaxe
        m.box(ab, sx * 11.0 - 2.0, 49.6, -10.6, sx * 11.0 + 2.0, 50.6, -9.4, STEEL)
    axe(m, a["arm_left"]["bone"], a["arm_left"]["hand"], (0.2, 0.9, -0.3), 1)
    axe(m, a["arm_right"]["bone"], a["arm_right"]["hand"], (-0.2, -0.6, -0.8), -1)
    return m
