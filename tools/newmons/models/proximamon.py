"""Proximamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a dark knight bonded to its war-beast: a lean rider in black-and-gold armour with a crested helm
and a mane of red-and-white plumes, wielding a long golden halberd, astride a black armoured beast studded with gold
spikes and glowing violet seams and red lenses, a pale ragged cape spread behind and a tail of bone plates; a dark
violet mist swirls about its claws. 35 blocks.

Front is -z, y is up. 84 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import quadruped
from _digibody import cape, humanoid
from _digidetail import armour, metal, solid
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 84
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "a black-and-gold knight with a golden halberd astride a black armoured war-beast with violet seams, red lenses and gold spikes"
BASE = {"black": (36, 34, 42), "black_dark": (12, 12, 16), "gold": (230, 190, 70), "gold_dark": (150, 100, 20),
        "violet": (190, 80, 240), "red": (220, 40, 50), "white": (240, 240, 246), "white_dark": (180, 180, 196),
        "plume": (210, 40, 40), "mist": (70, 50, 130, 170), "bone": (220, 214, 196)}
SHINY = {"black": (200, 204, 216), "black_dark": (110, 114, 130), "violet": (60, 200, 240)}


def P(v):
    return pal(BASE, SHINY, v)


def platef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if abs((x * 0.5 + y * 0.7 + z * 0.3) % 6.0 - 3.0) < 0.15:
        return p["violet"], p["violet"]
    return armour(P, "black", "black_dark", trim="gold", trim_w=0.2)(x, y, z, face, variant, box=box, **k)


GOLD = metal(P, "gold", dark="gold_dark")


def capef(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    return tone(p["white_dark"] if face == "north" else p["white"], face), None


def build():
    m = Model("proximamon")
    mats = {"skin": platef, "claw": GOLD, "tooth": GOLD, "mouth": solid(P, "violet", glow=True)}
    a = quadruped(m, mats, "proximamon", length=34.0, body_y=20.0, body_rx=8.0, body_ry=7.0, neck=((0, 26, -18),
                  (0, 30, -24)), head_len=11.0, head_w=4.6, head_h=5.0, teeth=4, tail=((0, 22, 18), (0, 22, 28),
                  (0, 18, 36)), tail_r=(3.0, 2.2, 1.4))
    bd = a["body"]
    for j in range(8):                                                                   # gold spikes
        spike(m, bd, ((j % 2 * 2 - 1) * 6.0, 27.0, -12.0 + j * 3.4), ((j % 2 * 2 - 1) * 0.6, 1, 0.3), 1.6, 5.0, GOLD,
              tip=0.8)
    hd = a["head"]
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 4.4, sx * 4.8))
        m.box(hd, x0, 31.0, -29.0, x1, 32.4, -27.4, solid(P, "red", glow=True))
        spike(m, hd, (sx * 3.0, 34.0, -24.0), (sx * 0.4, 0.8, 0.6), 1.4, 6.0, GOLD, tip=0.8)
    for j in range(5):                                                                   # bone-plate tail
        spike(m, "tail", (0, 23.0 - j * 0.6, 20.0 + j * 3.6), (0, 1, 0.4), 1.4, 3.0, solid(P, "bone"), tip=0.8)
    for sx in (-1, 1):                                                                   # violet mist about the claws
        for zz in (-11.0, 11.0):
            m.round_box(bd, sx * 6.0, zz, 4.0, 4.0, 0.0, 2.0, solid(P, "mist"), cut=1)
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats_r = {"skin": platef, "neck": metal(P, "black", dark="black_dark"), "knee": GOLD, "hand": platef,
              "finger": GOLD}
    r = humanoid(m, mats_r, bulk=0.85, arm_bulk=0.85, leg_bulk=0.85, name="rider")
    rb = r["body"]
    hh = m.bone("head", rb, (0, 55, 0))
    m.round_box(hh, 0, -0.4, 2.4, 2.8, 54.0, 60.0, platef, cut=1)
    m.box(hh, -1.6, 57.0, -3.3, 1.6, 57.8, -3.1, solid(P, "violet", glow=True))
    for j in range(7):                                                                   # plume mane
        spike(m, hh, (0, 60.0, -2.0 + j * 0.9), ((j - 3) * 0.15, 0.6, 1), 1.0, 7.0 + (j % 2) * 2.0,
              solid(P, "plume" if j % 2 else "white"), tip=0.8)
    cape(m, rb, 52.0, 14.0, 26.0, capef, z=4.0, flare=1.6, panels=5, seed=9)
    w = r["arm_right"]["wrist"]                                                          # golden halberd
    rod(m, r["arm_right"]["bone"], (w[0], w[1] - 12.0, w[2] + 6.0), (w[0], w[1] + 14.0, w[2] - 14.0), 1, GOLD, extend=0.4)
    m.box(r["arm_right"]["bone"], w[0] - 0.4, w[1] + 10.0, w[2] - 16.0, w[0] + 0.4, w[1] + 16.0, w[2] - 10.0, GOLD,
          rotation=(-40, 0, 0), pivot=(w[0], w[1] + 13.0, w[2] - 13.0))
    mount(m, i_box, i_bone, 12.0, 2.0, bd)
    return m
