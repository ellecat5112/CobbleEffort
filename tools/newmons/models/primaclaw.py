"""Primaclaw, the Primordial Imitator Pokémon (Bug/Ground), Crabgron evolved, after the art by @dude.dude.art (shown
there as a variant Crabgron; the name is ours) and the user's idea: its claws make up nine tenths of it. A tiny black
crab body with a spiky crown and glowing blue eyes rides on long white spider legs, and two long white arms hold up
two enormous claws: the left imitates the red, plated head of the continent Pokémon (black eye markings, a jaw of
jagged grey teeth), the right the blue head of the sea Pokémon (a white jaw and spot, red-tipped fins, grey teeth).

Shiny: a golden land-claw and a magenta sea-claw.

Front is -z, y is up. 34 units tall to the top of its claws; baseScale 0.75 (1.6 m).
"""
from __future__ import annotations

import math

from _boxmodel import Model, rod, spike
from _mimic import crab_body, crab_legs, solid
from _route import pal

SCALE = 0.45
HITBOX = [4.4, 3.6]
KIND = "quadruped"
K = 3
HEIGHT = 58
LOOK = ("a tiny black spiky crab on long white legs holding up two enormous claws: Groudon's head and Kyogre's head, "
        "borrowed from Mega Showdown's models")
# its claws: Groudon's head and Kyogre (its body without tail and fins) from Mega Showdown's models, facing
# forward and a little outward (rotation y: +90 points a snout to -x)
BORROW = [{"src": "groudon", "parent": "arm_left", "at": (-14.0, 40.0, -4.0), "rotation": (0, 35, 0), "prefix": "groudon_"},
          {"src": "kyogre", "parent": "arm_right", "at": (18.0, 30.0, 4.0), "rotation": (0, -35, 0), "prefix": "kyogre_"}]

BASE = {"shell": (40, 40, 46), "belly": (90, 92, 100), "brow": (14, 14, 18), "eye": (90, 200, 250), "eye_glow": True,
        "leg": (230, 230, 234)}
SHINY = {}


def P(v):
    return pal(BASE, SHINY, v)


def build() -> Model:
    m = Model("primaclaw")
    top = m.bone("primaclaw", None, (0, 0, 0))
    bd = m.bone("body", top, (0, 10, 0))
    crab_body(m, bd, P, 0, 0, 3.4, 3.0, 8.0, 13.6, 11.4, 1.3, -3.0, cut=1.3)    # the tiny body
    for i in range(5):                                                          # its spiky crown
        a = (i - 2) * 0.45
        spike(m, bd, (math.sin(a) * 1.8, 13.2, 0.2), (math.sin(a), 1, 0.2), 1.6, 3.0 + (i == 2) * 1.6,
              solid("shell", P), tip=1.0)
    crab_legs(m, P, top, 3, 0, 9.6, 3.0, 10.0, (-2.4, 0.4, 3.0), t=1.4)
    for nm, sx, to in (("arm_left", -1, (-12.0, 24.0, -2.0)), ("arm_right", 1, (13.0, 20.0, -2.0))):
        ar = m.bone(nm, bd, (sx * 3.0, 12.0, -0.6))                              # long white arms up to the heads
        mid = (sx * 7.0, 18.0, -1.2)
        rod(m, ar, (sx * 3.0, 12.0, -0.6), mid, 1.8, solid("leg", P), extend=0.3)
        rod(m, ar, mid, to, 1.8, solid("leg", P), extend=0.3)
    return m
