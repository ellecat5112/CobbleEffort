"""Arkadimon Perfect (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a hunched armoured beast. Mint-green plates over a crimson body, huge masses of dark
crimson tentacles curling from its shoulders, a fanged mint helm, mint gauntlets and great crimson claws on its
hands and digitigrade feet. 25 blocks tall.

Front is -z, y is up. 60 units tall; Perfect stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibody import dome, humanoid, shell
from _arkadi import CLAW, CRIMSON, MINT, P
from _digidetail import solid
from _route import tone

HEIGHT = 60
SCALE, HITBOX = sized(25, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a hunched armoured beast: mint plates over a crimson body, huge masses of dark crimson tentacles on its "
        "shoulders, a fanged mint helm and great crimson claws")


def tentacle_mass(m, bone, c, sx, n=8, size=1.0):
    """A bunch of thick tentacles curling outward and down from c."""
    for i in range(n):
        ang = math.radians(-80 + i * (160 / max(n - 1, 1)))
        p0 = c
        p1 = (c[0] + sx * 5.0 * size, c[1] + 6.0 * size * math.cos(ang), c[2] + 6.0 * size * math.sin(ang))
        p2 = (c[0] + sx * 10.0 * size, c[1] + 2.0 * size * math.cos(ang), c[2] + 8.0 * size * math.sin(ang))
        p3 = (c[0] + sx * 11.0 * size, c[1] - 4.0 * size, c[2] + 6.0 * size * math.sin(ang))
        for j, (a, b) in enumerate(((p0, p1), (p1, p2), (p2, p3))):
            rod(m, bone, a, b, max(1, round((4 - j) * size)), CRIMSON, extend=0.5)


def build():
    m = Model("arkadimonperfect")
    mats = {"skin": CRIMSON, "chest": MINT, "abs": CRIMSON, "pelvis": MINT, "neck": CRIMSON, "deltoid": MINT,
            "upper_arm": CRIMSON, "forearm": MINT, "hand": MINT, "finger": CLAW, "claw": CLAW, "thigh": MINT,
            "knee": MINT, "shin": MINT, "calf": CRIMSON, "foot": MINT, "talon": CLAW}
    a = humanoid(m, mats, bulk=1.1, arm_bulk=1.2, leg_bulk=1.2, digitigrade=True, claws=True, talons=True,
                 name="arkadimonperfect", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 54, -1))
    m.round_box(hd, 0, -1.6, 2.6, 3.0, 53.0, 59.0, MINT, cut=1)
    m.box(hd, -2.0, 52.6, -6.0, 2.0, 55.0, -3.0, MINT)
    for j in range(4):
        spike(m, hd, (-1.5 + j, 52.8, -5.6), (0, -1, 0), 0.8, 1.6, solid(P, "white"))
    for sx in (-1, 1):
        m.box(hd, sx * 1.2 - 0.5, 56.6, -4.7, sx * 1.2 + 0.5, 57.2, -4.5, solid(P, "eye", glow=True))
    shell(m, bd, (0, 0, 0.6), 5.6, 42.0, 51.0, -85, 85, 9, 1.2, MINT)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.2, 50.0, 0.3), 4.0, 3.6, MINT, layers=3)
        tentacle_mass(m, ab, (sh[0] + sx * 2.0, 52.0, 1.0), sx, n=9, size=1.1)
    for sx, nm in ((1, "leg_left"), (-1, "leg_right")):
        kn = a[nm]["knee"]
        dome(m, a[nm]["bone"], (kn[0], 18.0, kn[2] - 0.6), 2.8, 2.6, MINT, layers=2)
    return m
