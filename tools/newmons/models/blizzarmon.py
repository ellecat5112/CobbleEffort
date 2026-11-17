"""Blizzarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Hybrid beast-warrior of ice. A crouching white-furred yeti with a shaggy mane swept back
from a black-masked face, a tribal headband of red-and-white cords, brown leather gloves and wrist wraps, brown
hooked claws on its feet, and a double-bladed steel battle-axe in each fist. 25 blocks tall.

Front is -z, y is up. 58 units tall; Perfect stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _digidetail import cutout, eye, fur, leather, local, metal, solid, strands
from _route import pal, tone

HEIGHT = 58
SCALE, HITBOX = sized(25, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a crouching white-furred yeti warrior with a shaggy swept mane, a black-masked face, a tribal headband, "
        "brown gloves and claws and a double-bladed battle-axe in each fist")
BASE = {"fur": (244, 244, 250), "fur_dark": (176, 180, 200), "fur_tip": (255, 255, 255), "mask": (40, 38, 46),
        "brown": (170, 104, 50), "brown_dark": (96, 54, 22), "claw": (110, 70, 40), "red": (210, 50, 40),
        "steel": (214, 218, 228), "steel_dark": (110, 114, 128), "gold": (220, 180, 60), "eye": (120, 200, 255),
        "pupil": (20, 20, 40), "white": (255, 255, 255)}
SHINY = {"fur": (180, 210, 250), "fur_dark": (100, 130, 190), "fur_tip": (230, 244, 255), "brown": (60, 60, 70),
         "brown_dark": (24, 24, 30), "red": (60, 160, 240)}


def P(v):
    return pal(BASE, SHINY, v)


FUR = fur(P, "fur", "fur_dark", tip="fur_tip", length=1.6)
MANE = strands(P, "fur", "fur_dark", tip="fur_tip")
GLOVE = leather(P, "brown", "brown_dark", stitch="red")
STEEL = metal(P, "steel", dark="steel_dark")


def facef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            c = eye(p, x - sx * 1.3, y - 54.2, 0.7, "eye")
            if c is not None:
                return c, None
        if abs(x) < 2.6 and 51.0 < y < 55.4:
            return tone(p["mask"], face), None
    return FUR(x, y, z, face, variant, box=box, **k)


def bladef(x, y, z, face, box):
    """A crescent axe blade: wide at the edge, narrow at the haft."""
    u, v, W, H = local(x, y, z, face, box)
    du, dv = u / max(W, 1e-6), v / max(H, 1e-6) - 0.5
    return abs(dv) < 0.18 + 0.42 * du and (du - 1.15) ** 2 + dv * dv * 1.4 > 0.12


def axe(m, bone, grip, up):
    """A double-bladed axe held at `grip`, haft along `up`."""
    top = tuple(g + u * 13.0 for g, u in zip(grip, up))
    rod(m, bone, tuple(g - u * 4.0 for g, u in zip(grip, up)), top, 1, leather(P, "brown_dark", "brown_dark"),
        extend=0)
    head = tuple(g + u * 10.0 for g, u in zip(grip, up))
    m.box(bone, head[0] - 0.8, head[1] - 2.0, head[2] - 0.8, head[0] + 0.8, head[1] + 2.0, head[2] + 0.8,
          solid(P, "gold"))
    for sx in (-1, 1):
        x0, x1 = sorted((head[0], head[0] + sx * 6.0))
        sh = cutout(lambda x, y, z, f, b, sx=sx: bladef(x if sx > 0 else 2 * head[0] - x, y, z, f, b), STEEL)
        m.box(bone, x0, head[1] - 4.6, head[2], x1, head[1] + 4.6, head[2], sh)
    spike(m, bone, top, up, 1.2, 2.4, STEEL)


def build():
    m = Model("blizzarmon")
    mats = {"skin": FUR, "hand": GLOVE, "finger": GLOVE, "foot": FUR, "talon": solid(P, "claw")}
    a = humanoid(m, mats, bulk=1.35, arm_bulk=1.45, leg_bulk=1.3, digitigrade=True, talons=True, name="blizzarmon",
                 hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 54, -1))
    m.round_box(hd, 0, -1.2, 3.0, 3.0, 50.6, 58.0, facef, cut=1)
    m.box(hd, -1.6, 50.8, -5.4, 1.6, 53.4, -3.8, FUR)                                    # muzzle
    m.box(hd, -0.6, 52.6, -5.6, 0.6, 53.4, -5.3, solid(P, "mask"))
    m.box(hd, -3.3, 56.4, -4.4, 3.3, 57.4, 2.0, solid(P, "red"))                          # headband
    for i in range(5):
        m.box(hd, -3.32, 56.6 + (i % 2) * 0.4, -4.0 + i * 1.3, 3.32, 56.9 + (i % 2) * 0.4, -3.6 + i * 1.3,
              solid(P, "white"))
    mane = m.bone("mane", hd, (0, 57, 1))
    for i in range(18):                                                                  # the swept mane
        ang = math.radians(-110 + i * 13)
        base = (3.0 * math.sin(ang), 56.5 + 1.4 * math.cos(ang), 0.5)
        tip = (base[0] * 2.4, base[1] + 2.0 * math.cos(ang) - 2.0, 10.0 + (i % 4) * 1.5)
        rod(m, mane, base, tip, 2, MANE, extend=0.3, t2=2)
    for i in range(3):                                                                   # the cords trailing back
        rod(m, mane, (2.0 - i * 2.0, 57.0, 2.0), (3.0 - i * 3.0, 54.0, 12.0), 1, solid(P, "red"), extend=0)
    for i in range(12):                                                                  # shaggy shoulder fur
        ang = math.radians(i * 30)
        spike(m, bd, (7.0 * math.sin(ang), 49.0, -7.0 * 0.5 * math.cos(ang)), (math.sin(ang) * 0.5, -1, 0), 2.4, 4.0,
              FUR)
    for nm, up in (("arm_left", (0.15, 0.6, -1)), ("arm_right", (-0.15, 0.6, -1))):
        ab = a[nm]
        w = ab["wrist"]
        rod(m, ab["bone"], w, (w[0], w[1] + 3.0, w[2] + 0.4), 4, GLOVE, extend=0)          # wrist wraps
        n = math.sqrt(sum(c * c for c in up))
        axe(m, ab["bone"], ab["hand"], tuple(c / n for c in up))
    return m
