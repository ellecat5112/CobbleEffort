"""Tiger Vespamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a golden cyborg hornet-knight striped black like a tiger: a slim armoured body, a
horned golden helm with green eyes and a red scarf streaming behind, a fan of golden blade-wings and translucent
wings, and long stinger-lances on both forearms blazing with cyan energy. 35 blocks.

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _digi import sized
from _digibeast import ball
from _digibody import humanoid
from _digidetail import armour, metal, solid
from _route import pal, tone

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a golden tiger-striped cyborg hornet knight with blade-wings, a red scarf and cyan energy stinger-lances on its forearms"
BASE = {"gold": (240, 190, 50), "gold_dark": (160, 110, 20), "black": (36, 32, 30), "red": (220, 40, 40),
        "cyan": (120, 240, 255, 200), "wing": (200, 240, 255, 150), "eye": (90, 255, 120), "steel": (200, 204, 214)}
SHINY = {"gold": (200, 210, 230), "gold_dark": (120, 130, 160)}


def P(v):
    return pal(BASE, SHINY, v)


def stripedf(x, y, z, face, variant, box=None, **k):
    p = P(variant)
    if (y + abs(x) * 0.3) % 4.0 < 1.2:
        return tone(p["black"], face), None
    return metal(P, "gold", dark="gold_dark")(x, y, z, face, variant, box=box, **k)


ARM = armour(P, "gold", "gold_dark", trim="black", panel=(3.0, 3.0))


def build():
    m = Model("tigervespamon")
    mats = {"skin": stripedf, "chest": ARM, "abs": stripedf, "pelvis": ARM, "deltoid": ARM, "upper_arm": stripedf,
            "forearm": ARM, "hand": ARM, "thigh": stripedf, "knee": ARM, "shin": stripedf, "calf": stripedf,
            "foot": ARM, "talon": metal(P, "gold"), "neck": stripedf}
    a = humanoid(m, mats, bulk=1.0, arm_bulk=0.95, leg_bulk=0.95, talons=True, name="tigervespamon")
    bd = a["body"]
    hd = m.bone("head", bd, (0, 55, 0))
    m.round_box(hd, 0, 0, 3.0, 3.4, 54.0, 61.0, ARM, cut=1)
    for sx in (-1, 1):
        m.box(hd, min(sx * 0.6, sx * 2.2), 57.6, -3.9, max(sx * 0.6, sx * 2.2), 58.6, -3.5, solid(P, "eye", glow=True))
    spike(m, hd, (0, 60.6, -1.0), (0, 1, -0.5), 1.6, 6.0, ARM, tip=0.8)
    for j in range(4):                                                                  # red scarf
        m.box(hd, 2.0 + j * 2.6, 52.0 + j * 0.8, 2.0, 4.8 + j * 2.6, 54.0 + j * 0.8, 3.0, solid(P, "red"),
              rotation=(0, 0, 8), pivot=(2.0 + j * 2.6, 53.0, 2.5))
    wb = m.bone("wings", bd, (0, 48, 3))
    for sx in (-1, 1):
        for j in range(5):                                                             # blade-wing fan
            spike(m, wb, (sx * 2.0, 48.0, 3.6), (sx * (0.4 + j * 0.25), 1, 0.3), 1.4, 12.0 - j, metal(P, "gold"),
                  tip=0.8)
        m.box(wb, min(sx * 2.0, sx * 16.0), 36.0, 4.0, max(sx * 2.0, sx * 16.0), 50.0, 4.2, solid(P, "wing"),
              rotation=(0, 0, sx * 10), pivot=(sx * 2.0, 48.0, 4.0))
    for nm in ("arm_left", "arm_right"):                                                # stinger lances
        w = a[nm]["wrist"]
        ab = a[nm]["bone"]
        spike(m, ab, (w[0], w[1] + 1.0, w[2]), (0, -1, -0.15), 2.6, 10.0, metal(P, "gold"), tip=0.8)
        spike(m, ab, (w[0], w[1] - 8.0, w[2] - 1.2), (0, -1, -0.15), 1.6, 18.0, solid(P, "cyan", glow=True), tip=0.8)
    return m
