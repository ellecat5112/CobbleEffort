"""Sagittarimon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Armor Digimon of light: a centaur archer: a black beast body on four clawed legs, a red-and-
gold armoured humanoid torso with dark-blue pauldrons and a horned helm, a quiver of arrows, a great red recurve bow
drawn in one hand, and two orange flame-orb shields. 15 blocks.

Front is -z, y is up. 60 units tall; Adult stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball, quadruped
from _digibody import humanoid
from _digidetail import armour, leather, metal, solid
from _dorbickmon import mount
from _route import pal, tone

HEIGHT = 60
SCALE, HITBOX = sized(15, HEIGHT, 6.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a centaur archer: a black beast body with a red-and-gold armoured torso, a horned helm, a great red recurve bow and flame-orb shields"
BASE = {"black": (40, 38, 46), "black_dark": (14, 12, 16), "red": (200, 40, 40), "red_dark": (110, 14, 14),
        "gold": (230, 190, 70), "gold_dark": (150, 100, 20), "blue": (40, 50, 110), "blue_dark": (14, 18, 50),
        "orange": (250, 150, 40), "steel": (220, 220, 230), "eye": (250, 200, 40), "claw": (240, 240, 236)}
SHINY = {"red": (40, 120, 200), "red_dark": (14, 60, 130), "black": (230, 230, 236), "black_dark": (160, 160, 176)}


def P(v):
    return pal(BASE, SHINY, v)


PLATE = armour(P, "red", "red_dark", trim="gold", trim_w=0.25)
HIDE = armour(P, "black", "black_dark", trim="red", trim_w=0.15)


def build():
    m = Model("sagittarimon")
    mats = {"skin": HIDE, "head": HIDE, "claw": solid(P, "claw")}
    a = quadruped(m, mats, "sagittarimon", length=28.0, body_y=18.0, body_rx=7.0, body_ry=6.4, neck=((0, 22, -14),
                  (0, 24, -15)), head_len=5.0, head_w=3.0, head_h=3.0, tail=((0, 20, 14), (0, 16, 20), (0, 12, 24)),
                  tail_r=(1.6, 1.2, 1.0))
    m.boxes[:] = [b for b in m.boxes if b.bone not in ("head", "jaw")]                 # the rider's torso is the head
    i_box, i_bone = len(m.boxes), len(m.bones)
    mats_r = {"skin": PLATE, "deltoid": armour(P, "blue", "blue_dark"), "neck": HIDE, "hand": HIDE, "finger": HIDE}
    r = humanoid(m, mats_r, bulk=0.9, arm_bulk=0.9, leg_bulk=0.6, name="rider")
    m.boxes[:] = m.boxes[:i_box] + [b for b in m.boxes[i_box:] if b.bone not in ("leg_left", "leg_right")]
    m.bones[:] = m.bones[:i_bone] + [b for b in m.bones[i_bone:] if b["name"] not in ("leg_left", "leg_right")]
    rb = r["body"]
    hh = m.bone("head", rb, (0, 55, 0))
    m.round_box(hh, 0, -0.6, 2.6, 3.0, 54.0, 60.0, HIDE, cut=1)
    m.box(hh, -1.8, 57.0, -3.7, 1.8, 57.8, -3.5, solid(P, "eye", glow=True))
    spike(m, hh, (0, 60.0, -1.0), (0, 1, -0.2), 1.4, 5.0, metal(P, "gold", dark="gold_dark"), tip=0.8)
    m.box(rb, -2.0, 38.0, 4.0, 2.0, 54.0, 7.0, leather(P, "black", "black_dark"))           # quiver
    for j in range(3):
        rod(m, rb, (-1.0 + j, 54.0, 5.5), (-1.0 + j, 58.0, 5.5), 1, metal(P, "steel"), extend=0.0)
    w = r["arm_left"]["wrist"]                                                           # great recurve bow
    bow = [(w[0] + 1.0, w[1] + 14.0, w[2] - 2.0), (w[0] + 3.0, w[1] + 6.0, w[2] - 4.0), (w[0] + 2.0, w[1], w[2] - 2.0),
           (w[0] + 3.0, w[1] - 6.0, w[2] - 4.0), (w[0] + 1.0, w[1] - 14.0, w[2] - 2.0)]
    for p0, p1 in zip(bow, bow[1:]):
        rod(m, r["arm_left"]["bone"], p0, p1, 2, PLATE, extend=0.3)
    rod(m, r["arm_left"]["bone"], bow[0], bow[-1], 1, solid(P, "steel"), extend=0.0, t2=1)
    for side in ("arm_left", "arm_right"):                                               # flame-orb shields
        e = r[side]["elbow"]
        ball(m, r[side]["bone"], (e[0] * 1.2, e[1], e[2]), 2.4, solid(P, "orange", glow=True), layers=2)
    mount(m, i_box, i_bone, -6.0, -12.0, a["body"])
    return m
