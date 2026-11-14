"""Tearion, the Teary Bulb Pokémon (Grass), after the art of the A. Fakemon fanpage (the name is ours): a little white
onion on stubby legs with tiny arms, big watery eyes that never stop crying, a wobbly frown and a sprout of green
leaves bursting from its pointed top.

Shiny: a rose-red onion.

Front is -z, y is up. 21 units tall to its leaf tips; baseScale 0.36 (0.47 m).
"""
from __future__ import annotations

from _boxmodel import Model, rod, spike
from _onion import P, bulb, solid, teary_eye
from _route import tone

SCALE = 0.36
HITBOX = [0.75, 1.3]
KIND = "biped"
K = 5
HEIGHT = 21
LOOK = "a little white onion on stubby legs with big watery crying eyes, a wobbly frown and a sprout of green leaves"


def bulbf(x, y, z, face, variant, **k):
    p = P(variant)
    if face == "north":
        for sx in (-1, 1):
            e = teary_eye(p, x - sx * 1.5, y - 7.6, 0.85)
            if e:
                return e, None
        if abs(y - 5.6 + abs(x) * 0.35) < 0.18 and abs(x) < 1.0:
            return p["pupil"], None                                           # a wobbly frown
    return tone(p["white"], face), None


def build() -> Model:
    m = Model("tearion")
    top = m.bone("tearion", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 6, 0))
    bulb(m, bd, 7.0, 4.0, 9.0, bulbf)                                          # the onion bulb
    spike(m, bd, (0, 11.2, 0), (0, 1, 0), 1.6, 1.8, solid("white_shade"))      # its pointed top
    for d, h in (((0, 1, 0), 9.0), ((-0.5, 1, 0.2), 8.0), ((0.5, 1, -0.1), 8.0), ((0.2, 1, 0.6), 7.0),
                 ((-0.3, 1, -0.5), 6.5)):                                       # a sprout of green leaves
        rod(m, bd, (0, 11.6, 0), tuple(11.6 * (i == 1) + v * h for i, v in enumerate(d)), 1.6,
            ramp_leaf(), extend=0.3, t2=0.6)
    for sx, side in ((-1, "left"), (1, "right")):
        lb = m.bone(f"leg_{side}", top, (sx * 1.4, 3, 0))
        rod(m, lb, (sx * 1.4, 3.0, 0.0), (sx * 1.8, 0.8, -0.2), 1.4, solid("white_shade"), extend=0.3)
        m.round_box(lb, sx * 1.8, -0.6, 1.0, 1.4, 0.0, 1.2, solid("white"), cut=0.4)
        ar = m.bone(f"arm_{side}", bd, (sx * 3.6, 6.6, 0))
        rod(m, ar, (sx * 3.6, 6.6, 0.0), (sx * 5.2, 5.4, -0.8), 1.2, solid("white_shade"), extend=0.3)
    return m


def ramp_leaf():
    from _onion import ramp
    return ramp("green", "green_light", 0.5)
