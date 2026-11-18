"""Gaogamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
fighting wolf-beast: a hunched blue wolf with a great pale-blue mane, red fighting gloves on its forepaws, long red
ribbons trailing from its arms and a jointed pincer tail. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall. Built by _gaogamon.make(black=False).
"""
from __future__ import annotations

from _digi import sized
from _gaogamon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a hunched blue wolf-beast with a great pale mane, red fighting gloves and a jointed pincer tail"
build = make("gaogamon", "adult", black=False)
