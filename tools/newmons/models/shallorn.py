"""Shallorn, the Shallot Pokémon (Grass/Poison), Tearion evolved, after the art of the A. Fakemon fanpage (the name is
ours): a round brown shallot with long droopy green leaves hanging round it like hair, closed, forlorn eyes, a
drooping orange moustache of roots, a stalk on top ending in a green flower-bud, short legs, and a faint purple stink.

Shiny: a rose-red bulb.

Front is -z, y is up. 27 units tall to its bud; baseScale 0.55 (0.93 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _onion import P, bulb, ramp, solid, teary_eye
from _route import tone

SCALE = 0.55
HITBOX = [1.2, 1.7]
KIND = "biped"
K = 4
HEIGHT = 27
LOOK = ("a round brown shallot with droopy green leaves like hair, closed forlorn eyes, a drooping orange root "
        "moustache and a stalk with a green flower-bud")


def bulbf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = teary_eye(p, x - sx * 1.8, y - 11.2, 0.9, closed=True)
            if e and e != p["tear"]:
                return e, None
            dx, dy = x - sx * 1.8, y - 12.2
            if abs(dy - dx * sx * 0.3) < 0.18 and abs(dx) < 0.9:
                return p["brown_dark"], None                                  # sad brows
    if face == "up" and math.hypot(x, z) < 1.4:
        return p["brown_dark"], None
    return tone(p["brown"], face), None


def build() -> Model:
    m = Model("shallorn")
    top = m.bone("shallorn", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 9, 0))
    bulb(m, bd, 10.0, 6.4, 14.0, bulbf)                                        # the shallot bulb
    for sx in (-1, 1):                                                         # the drooping root moustache
        rod(m, bd, (0, 9.2, -6.2), (sx * 2.4, 8.6, -6.4), 1.4, solid("orange"), extend=0.3)
        rod(m, bd, (sx * 2.4, 8.6, -6.4), (sx * 3.4, 6.4, -6.0), 1.2, solid("orange"), extend=0.3)
        spike(m, bd, (sx * 3.4, 6.4, -6.0), (sx * 0.2, -1, 0.2), 1.0, 1.4, solid("orange_light"))
    hd = m.bone("head", bd, (0, 17, 0))
    rod(m, hd, (0, 16.4, 0), (0, 24.0, 0.4), 1.6, solid("green"), extend=0.4)  # the stalk
    for c in ((0, 25.0, 0.4), (-1.2, 24.4, 0.0), (1.2, 24.6, 0.8), (0, 24.2, -1.0), (0.2, 26.0, 0.0)):
        m.round_box(hd, c[0], c[2], 1.1, 1.1, c[1] - 1.0, c[1] + 1.0, solid("green_light"), cut=0.4)   # the bud
    for i in range(6):                                                         # long droopy leaves like hair
        a = 2 * math.pi * (i + 0.5) / 6
        sx, sz = math.sin(a), math.cos(a)
        rod(m, hd, (sx * 1.6, 16.0, sz * 1.6), (sx * 6.0, 18.4, sz * 6.0), 2.2, solid("green"), extend=0.4, t2=0.8)
        rod(m, hd, (sx * 6.0, 18.4, sz * 6.0), (sx * 8.4, 12.0, sz * 7.6), 2.0, ramp("green", "green_dark"),
            extend=0.4, t2=0.8)
    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 2.4, 4, 0))
        rod(m, lb, (sx * 2.4, 4.0, 0.0), (sx * 2.8, 1.0, -0.4), 1.8, solid("brown_dark"), extend=0.3)
        m.round_box(lb, sx * 2.8, -1.0, 1.4, 2.0, 0.0, 1.4, solid("brown_dark"), cut=0.5)
    return m
