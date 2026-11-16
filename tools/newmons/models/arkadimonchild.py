"""Arkadimon Child (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a lean pink imp. Hairless pink skin over wiry muscle, three steel horn-spikes on its
head, crimson bat-wing blades growing from its forearms, bands at its wrists, a whip tail and pointed crimson feet.
1 block tall.

Front is -z, y is up. 40 units tall; Child stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import humanoid
from _arkadi import CLAW, CRIMSON, GREY, P, PINK
from _digidetail import cutout, local, metal, solid
from _route import tone

HEIGHT = 40
SCALE, HITBOX = sized(1.0, HEIGHT, 0.7)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = ("a lean pink imp with three steel horn-spikes, crimson bat-wing blades on its forearms, a whip tail and "
        "pointed crimson feet")


def blade_shape(x, y, z, face, box):
    u, v, W, H = local(x, y, z, face, box)
    t = v / max(H, 1e-6)
    return abs(u / max(W, 1e-6) - 0.3 - 0.2 * t) < 0.5 * math.sin(math.pi * min(1.0, t * 1.05))


def build():
    m = Model("arkadimonchild")
    mats = {"skin": PINK, "foot": CRIMSON, "toe": CRIMSON, "talon": CLAW}
    a = humanoid(m, mats, bulk=0.8, arm_bulk=0.85, leg_bulk=0.8, digitigrade=True, talons=True,
                 name="arkadimonchild", hand_pose="fist")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.4, 2.4, 2.6, 54.4, 60.8, PINK, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.1 - 0.6, 57.6, -3.1, sx * 1.1 + 0.6, 58.2, -2.9, solid(P, "red", glow=True))
    for ang in (-25, 0, 25):                                     # three steel horn-spikes
        r = math.radians(ang)
        spike(m, hd, (2.0 * math.sin(r), 60.6, 0.4), (math.sin(r) * 0.5, 1, 0.3), 1.4, 7.0 - abs(ang) * 0.06, GREY,
              tip=0.6)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):          # crimson wing-blades on the forearms
        el, wr = a[nm]["elbow"], a[nm]["wrist"]
        x0, x1 = sorted((wr[0], wr[0] + sx * 9.0))
        m.box(a[nm]["bone"], x0, wr[1] - 2.0, wr[2] - 0.5, x1, wr[1] + 14.0, wr[2] - 0.5,
              cutout(blade_shape, CRIMSON), rotation=(0, 0, sx * 10), pivot=wr)
        rod(m, a[nm]["bone"], wr, (wr[0], wr[1] + 1.6, wr[2]), 4, GREY, extend=0)
    tl = m.bone("tail", bd, (0, 31, 3))
    pts = [(0, 31, 3), (2, 24, 8), (5, 16, 11), (9, 8, 12)]
    for p0, p1 in zip(pts, pts[1:]):
        rod(m, tl, p0, p1, 1, PINK, extend=0.3)
    spike(m, tl, pts[-1], (0.5, -0.5, 0.4), 1.4, 2.6, CRIMSON)
    return m
