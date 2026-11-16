"""Arkadimon Ultimate (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the bewitching beast grown huge. Grey-mint armour marked with crimson flame patterns,
a horned demon head framed in dark crimson tentacle-hair that hangs to its waist, violet membrane wings, crimson
claws on its hands and feet and tentacles hanging from its hips. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import bat_wing
from _digibody import dome, humanoid, shell
from _arkadi import CLAW, CRIMSON, MINT, P
from _digidetail import cutout, local, plane, solid
from _route import tone

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a huge armoured demon beast: grey-mint armour with crimson flame marks, a horned head framed in dark crimson "
        "tentacle-hair, violet membrane wings and crimson claws")


def flamed(x, y, z, face, variant, box=None, **k):
    """Mint armour with crimson flame-tongue marks."""
    p = P(variant)
    a, b = plane(x, y, z, face)
    if abs(math.sin(a * 0.8) * 1.6 - ((b * 0.5) % 3.0) + 1.5) < 0.35:
        return tone(p["crimson"], face), None
    return MINT(x, y, z, face, variant, box=box, **k)


def wingf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    u, v, W, H = local(x, y, z, face, box)
    return (p["wing_dark"] if (u * 0.9) % 2.0 < 0.3 else p["wing"]), None


def build():
    m = Model("arkadimonultimate")
    mats = {"skin": CRIMSON, "chest": flamed, "abs": flamed, "pelvis": flamed, "neck": CRIMSON, "deltoid": flamed,
            "upper_arm": flamed, "forearm": flamed, "hand": MINT, "finger": CLAW, "claw": CLAW, "thigh": flamed,
            "knee": MINT, "shin": flamed, "calf": flamed, "foot": MINT, "talon": CLAW}
    a = humanoid(m, mats, bulk=1.2, arm_bulk=1.3, leg_bulk=1.3, digitigrade=True, claws=True, talons=True,
                 name="arkadimonultimate", hand_pose="open")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, -0.8, 2.8, 3.0, 54.0, 60.6, flamed, cut=1)
    for sx in (-1, 1):
        m.box(hd, sx * 1.3 - 0.6, 57.4, -3.9, sx * 1.3 + 0.6, 58.0, -3.7, solid(P, "eye", glow=True))
        rod(m, hd, (sx * 2.4, 60.0, -0.5), (sx * 5.0, 64.0, 1.0), 2, MINT, extend=0.3)
        spike(m, hd, (sx * 5.0, 64.0, 1.0), (sx * 0.5, 1, 0.3), 1.4, 3.0, MINT)
    hr = m.bone("mane", hd, (0, 58, 1))
    for i in range(14):                                          # crimson tentacle-hair hanging to the waist
        ang = math.radians(-120 + i * (240 / 13))
        base = (3.0 * math.sin(ang), 59.0, -3.0 * math.cos(ang) * 0.4 + 1.0)
        tip = (6.0 * math.sin(ang), 34.0 + (i % 3) * 3, -4.0 * math.cos(ang) * 0.4 + 3.0)
        rod(m, hr, base, tip, 2, CRIMSON, extend=0.4)
    shell(m, bd, (0, 0, 0.6), 6.0, 42.0, 51.0, -85, 85, 9, 1.2, flamed)
    for sx, nm in ((1, "arm_left"), (-1, "arm_right")):
        ab, sh = a[nm]["bone"], a[nm]["shoulder"]
        dome(m, ab, (sh[0] + sx * 1.4, 50.0, 0.3), 4.6, 4.0, flamed, layers=3)
    for sx, nm in ((1, "wing_left"), (-1, "wing_right")):
        wb = m.bone(nm, bd, (sx * 3.0, 49.0, 3.0))
        bat_wing(m, wb, (sx * 3.0, 49.0, 3.0), 22.0, 14.0, 4, MINT, cutout(lambda *q: True, wingf), side=sx)
    for sx in (-1, 1):                                           # tentacles hanging from the hips
        for j in range(3):
            rod(m, bd, (sx * (3.0 + j), 31.0, -1.0 + j), (sx * (4.0 + j * 1.6), 14.0 + j * 2, -3.0 + j), 2, CRIMSON,
                extend=0.4)
    return m
