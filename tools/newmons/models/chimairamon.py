"""Chimairamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the patchwork chimera. A stitched-together beast on four mismatched legs: a striped white
Garurumon-like body, a black Greymon-like skull head and an orange Airdramon-like head side by side, one red Kuwagamon
pincer arm and one skeletal arm, white angel wings and red-and-orange devil wings, and a tail. 25 blocks tall.

Front is -z, y is up. 40 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing, feather_wing, quadruped
from _digidetail import armour, feathers, fur, metal, skin, solid
from _route import pal, tone

HEIGHT = 40
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a stitched patchwork chimera: a striped white body, a black skull head and an orange dragon head, a red "
        "pincer arm, a skeletal arm, angel wings and devil wings")
BASE = {"white": (240, 240, 246), "white_dark": (180, 184, 200), "stripe": (100, 80, 160), "black": (40, 40, 48),
        "black_light": (110, 110, 124), "orange": (240, 150, 50), "orange_dark": (180, 90, 20), "red": (210, 40, 40),
        "red_dark": (120, 14, 16), "bone": (236, 232, 220), "bone_dark": (170, 164, 150), "pink": (230, 120, 150),
        "wing": (246, 246, 250), "wing_dark": (200, 204, 214), "fire": (250, 140, 40), "eye": (250, 220, 60),
        "tooth": (250, 250, 246), "mouth": (110, 20, 30), "stitch": (60, 40, 30)}
SHINY = {"white": (60, 60, 70), "white_dark": (24, 24, 30), "orange": (90, 200, 220), "red": (60, 160, 90)}


def P(v):
    return pal(BASE, SHINY, v)


def stripedfur(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if face in ("east", "west", "up") and (z + 0.4 * y) % 4.0 < 1.0:
        return tone(p["stripe"], face), None
    if face == "north" and abs(x) < 0.25:
        return tone(p["stitch"], face), None
    return fur(P, "white", "white_dark", length=1.0)(x, y, z, face, variant, box=box, **k)


BONE = metal(P, "bone", dark="bone_dark")
RED = armour(P, "red", "red_dark")


def build():
    m = Model("chimairamon")
    mats = {"skin": stripedfur, "belly": stripedfur, "neck": stripedfur, "head": solid(P, "black"),
            "snout": solid(P, "black"), "jaw": solid(P, "black"), "mouth": solid(P, "mouth"),
            "tooth": solid(P, "tooth"), "leg_upper": stripedfur, "leg_lower": stripedfur,
            "paw": skin(P, "pink"), "claw": solid(P, "bone"), "tail": stripedfur}
    a = quadruped(m, mats, "chimairamon", length=24.0, body_y=15.0, body_rx=6.0, body_ry=6.4, chest_bulk=1.3,
                  neck=((-2, 20, -12), (-3, 25, -15)), head_len=10.0, head_w=3.6, head_h=3.8, snout=0.5,
                  mouth_open=14, teeth=4, leg_bulk=1.4, toes=3, tail=((0, 18, 15), (3, 20, 22), (6, 18, 27)),
                  tail_r=(1.8, 1.4, 1.0))
    bd = a["body"]
    st = a["skull_top"]
    for sx in (-1, 1):                                                       # horns on the black skull head
        spike(m, a["head"], (-3.0 + sx * 2.4, st - 0.4, -15.0), (sx * 0.3, 1, 0.3), 1.6, 4.0, solid(P, "bone"))
    m.box(a["head"], -6.7, st - 2.0, -19.0, -6.6, st - 1.4, -18.0, solid(P, "eye", glow=True))
    nk2 = m.bone("head_2", bd, (3, 21, -11))                                 # the orange dragon head beside it
    rod(m, nk2, (3.0, 21.0, -11.0), (5.0, 26.0, -14.0), 4, skin(P, "orange", dark="orange_dark"), extend=0.6)
    m.round_box(nk2, 5.6, -16.0, 2.6, 3.0, 25.0, 29.0, skin(P, "orange", dark="orange_dark"), cut=1)
    m.box(nk2, 3.8, 25.4, -22.0, 7.4, 27.6, -17.0, skin(P, "orange", dark="orange_dark"))
    for i in range(6):                                                       # its red mane
        spike(m, nk2, (5.6, 29.0, -16.0 + i * 1.0), (0.3, 1, 0.4), 1.2, 3.0, RED)
    m.box(nk2, 8.1, 27.6, -18.6, 8.2, 28.4, -17.6, solid(P, "eye", glow=True))
    ar = m.bone("arm_right", bd, (-6, 18, -9))                               # red pincer arm
    rod(m, ar, (-6.0, 18.0, -9.0), (-11.0, 13.0, -14.0), 3, RED, extend=0.4)
    for d in (-1, 1):
        rod(m, ar, (-11.0, 13.0, -14.0), (-12.0 + d * 1.6, 9.0, -19.0), 2, RED, extend=0.4)
        spike(m, ar, (-12.0 + d * 1.6, 9.0, -19.0), (-d * 0.6, -0.3, -0.6), 1.2, 2.6, RED)
    al = m.bone("arm_left", bd, (6, 18, -9))                                 # skeletal arm
    rod(m, al, (6.0, 18.0, -9.0), (11.0, 13.0, -14.0), 1, BONE, extend=0.4)
    rod(m, al, (11.0, 13.0, -14.0), (12.0, 9.0, -18.0), 1, BONE, extend=0.4)
    for j in range(3):
        rod(m, al, (12.0, 9.0, -18.0), (12.0 + (j - 1) * 1.2, 6.0, -20.0), 1, BONE, extend=0.2)
    feather_wing(m, bd, (-3.0, 21.0, 0.0), 16.0, 8.0, 2, feathers(P, "wing", "wing_dark", size=(1.4, 2.6)), side=-1,
                 sweep=25)
    bat_wing(m, bd, (3.0, 21.0, 0.0), 16.0, 12.0, 3, RED, solid(P, "fire"), side=1, sweep=20)
    return m
