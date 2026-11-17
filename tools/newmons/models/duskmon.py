"""Duskmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the warrior of darkness. A tall knight in jagged black armour striped with red, staring red eyes set
all over it (on its shoulders, knees, chest and the skull-like sabatons of its feet), a long flowing blonde mane
streaming from a horned black helm, and a blade of red light held out from each hand. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage (Hybrid).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid
from _digidetail import armour, local, solid, strands
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ("a tall knight in jagged red-striped black armour covered in staring red eyes, a horned black helm with a long "
        "blonde mane, skull sabatons and red light blades")
BASE = {"black": (36, 34, 42), "black_dark": (10, 10, 14), "black_light": (110, 106, 130), "red": (180, 20, 30),
        "white": (240, 240, 240), "pupil": (200, 20, 30), "blonde": (250, 220, 120), "blonde_dark": (200, 160, 60),
        "blade": (255, 60, 60, 220), "tooth": (230, 230, 230)}
SHINY = {"black": (220, 220, 230), "black_dark": (140, 140, 156), "black_light": (255, 255, 255), "blonde": (120, 90, 200),
         "blonde_dark": (60, 40, 140)}


def P(v):
    return pal(BASE, SHINY, v)


ARM = armour(P, "black", "black_dark", light="black_light")


def striped(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face != "up" and (y % 3.0) < 0.6:
        return tone(p["red"], face), None
    return ARM(x, y, z, face, variant, box=box, **k)


def eye(m, bone, c, r):
    """A staring red eye on a front-facing plate at c."""
    def f(x, y, z, face, variant, box=None, **k):
        p = P(variant)
        d = math.hypot(x - c[0], y - c[1])
        if face == "north":
            if d < r * 0.4:
                return p["pupil"], p["pupil"]
            if d < r:
                return tone(p["white"], face), None
        return ARM(x, y, z, face, variant, box=box, **k)
    m.box(bone, c[0] - r - 0.4, c[1] - r - 0.4, c[2] - 0.6, c[0] + r + 0.4, c[1] + r + 0.4, c[2] + 0.4, f)


def build():
    m = Model("duskmon")
    mats = {"skin": striped, "chest": ARM, "abs": striped, "pelvis": ARM, "neck": ARM, "deltoid": ARM,
            "upper_arm": striped, "forearm": ARM, "hand": ARM, "finger": ARM, "thigh": striped, "knee": ARM,
            "shin": striped, "calf": striped, "foot": ARM, "toe": ARM}
    a = humanoid(m, mats, bulk=0.95, arm_bulk=0.95, leg_bulk=1.0, name="duskmon")
    bd = a["body"]
    eye(m, bd, (0, 46.0, a["chest_front"] - 0.4), 1.6)                                  # chest eye
    for sx in (-1, 1):
        dome(m, bd, (sx * 8.0, 49.0, 0), 3.8, 3.4, ARM)
        eye(m, bd, (sx * 8.0, 49.0, -4.0), 1.6)                                          # shoulder eyes
        for j in range(3):
            spike(m, bd, (sx * 8.6, 52.0, -1.0 + j * 1.6), (sx * 0.5, 1, 0), 1.2, 4.0, ARM, tip=0.3)
    for nm in ("leg_left", "leg_right"):
        lg = a[nm]
        kn, ak = lg["knee"], lg["ankle"]
        eye(m, lg["bone"], (kn[0], kn[1] - 2.0, kn[2] - 2.6), 1.4)                        # knee eyes
        m.round_box(lg["bone"], ak[0], ak[2] - 2.0, 2.6, 3.4, 0.0, 4.0, ARM, cut=1)       # skull sabatons
        eye(m, lg["bone"], (ak[0], 2.2, ak[2] - 5.6), 1.2)
        for j in range(3):
            m.box(lg["bone"], ak[0] - 1.6 + j * 1.2, 0.0, ak[2] - 5.8, ak[0] - 1.0 + j * 1.2, 0.8, ak[2] - 5.4,
                  solid(P, "tooth"))
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.6, 3.0, 54.0, 60.4, ARM, cut=1)
    m.box(hd, -1.8, 56.8, -3.5, 1.8, 57.6, -3.3, solid(P, "pupil", glow=True))
    for sx in (-1, 1):
        spike(m, hd, (sx * 2.0, 59.8, 0), (sx * 0.4, 1, 0.3), 1.2, 4.0, ARM, tip=0.3)    # helm horns
    for i in range(12):                                                                   # long blonde mane
        ang = math.radians(-110 + i * 20)
        pts = [(2.4 * math.sin(ang), 59.6, 0.8 + math.cos(ang)), (5.0 * math.sin(ang), 50.0, 6.0),
               (7.0 * math.sin(ang), 40.0, 10.0)]
        for p0, p1 in zip(pts, pts[1:]):
            rod(m, hd, p0, p1, 2, strands(P, "blonde", "blonde_dark"), extend=0.3, t2=1)
    for nm in ("arm_left", "arm_right"):                                                  # red light blades
        ar = a[nm]
        hx, hy, hz = ar["hand"]
        sx = 1 if hx > 0 else -1
        rod(m, ar["bone"], (hx, hy, hz), (hx + sx * 6.0, hy + 4.0, hz - 18.0), 1, solid(P, "blade", glow=True),
            extend=0, t2=2)
    return m
