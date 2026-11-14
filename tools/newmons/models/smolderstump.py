"""Smolderstump, the Burnt Stub Pokémon (Fire/Poison), Emberbutt evolved (the user's design): its papery armour has
burned away almost entirely, leaving a stubby, jagged, ash-crusted torso on a charred orange filter base, a thick
collar of acrid grey smoke round its neck, glowing ember eyes under a grumpy brow and a smouldering crown.

Shiny: white ash with a blue ember.

Front is -z, y is up. 15 units tall; baseScale 0.5 (0.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _nico import palette, puff, translucent
from _route import tone

SHINY = {"ash": (226, 224, 220), "ash_dark": (180, 178, 176), "ember": (80, 160, 255), "ember_hot": (180, 230, 255)}
P, solid, ramp = palette(SHINY)
SCALE = 0.5
HITBOX = [0.9, 0.95]
KIND = "biped"
K = 5
HEIGHT = 15
LOOK = "a stubby, jagged, ash-crusted burnt cigarette with a charred filter base, a collar of grey smoke and ember eyes"


def ashf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            if abs(x - sx * 1.3) < 0.6 and abs(y - 9.2 + sx * 0.0) < 0.35:
                return p["ember_hot"], p["ember_hot"]                         # glowing ember eyes
            if abs(x - sx * 1.3) < 0.9 and abs(y - 9.9 - (abs(x) - 1.3) * sx * 0.0 + abs(x) * 0.25 - 0.3) < 0.2:
                return p["ash_dark"], None                                    # a grumpy brow
    if math.sin(x * 2.1 + y * 1.7) * math.cos(z * 1.9) > 0.75:
        return p["ember"], p["ember"]                                         # embers glowing through cracks
    return tone(p["ash"] if (int(y * 2) % 3) else p["ash_dark"], face), None


def build() -> Model:
    m = Model("smolderstump")
    top = m.bone("smolderstump", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 3, 0))
    m.round_box(bd, 0, 0, 3.0, 3.0, 2.0, 5.4, solid("filter"), cut=1.0)       # the charred filter base
    m.round_box(bd, 0, 0, 3.1, 3.1, 4.8, 5.4, solid("gold_dark"), cut=1.0)
    m.round_box(bd, 0, 0, 2.8, 2.8, 5.4, 11.0, ashf, cut=0.9)                  # the ash-crusted torso
    hd = m.bone("head", bd, (0, 11, 0))
    for i in range(7):                                                         # a jagged, smouldering crown
        a = 2 * math.pi * i / 7
        spike(m, hd, (math.cos(a) * 1.9, 10.8, math.sin(a) * 1.9), (math.cos(a) * 0.3, 1, math.sin(a) * 0.3),
              1.0, 1.4 + (i % 3) * 0.7, ashf)
    puff(m, hd, (0, 11.6, 0), 1.0, lambda *a, **k: (P(k.get("variant"))["ember"], P(k.get("variant"))["ember"]))
    for i in range(8):                                                         # the collar of acrid smoke
        a = 2 * math.pi * i / 8
        puff(m, bd, (math.cos(a) * 3.2, 8.0 + (i % 2) * 0.6, math.sin(a) * 3.2), 1.3, translucent(P, "smoke"))
    for sx, side in ((-1, "left"), (1, "right")):
        ar = m.bone(f"arm_{side}", bd, (sx * 2.8, 8, 0))
        rod(m, ar, (sx * 2.8, 8.0, 0.0), (sx * 4.4, 5.6, -0.6), 1.2, solid("ash_dark"), extend=0.2)
        lb = m.bone(f"leg_{side}", top, (sx * 1.4, 2.4, 0))
        m.round_box(lb, sx * 1.4, -0.2, 0.9, 1.1, 0.0, 2.6, solid("filter_dark"), cut=0.4)
    return m
