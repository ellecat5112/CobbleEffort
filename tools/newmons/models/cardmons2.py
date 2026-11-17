"""Cardmon S2 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round black-and-white floating head with a black grid card, two grey cards and a dark blade. Ultimate stage.

Front is -z, y is up. 24 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 24
SCALE, HITBOX = sized(35.0, HEIGHT, 0.9)
KIND = "floater"
K = 4
LOOK = "a round black-and-white floating head with a black grid card, two grey cards and a dark blade"

build = make("cardmons2", "black", [((4.0, 9.0, 1.0), (0, 0, -30), (5.0, 8.0), 'black'), ((8.0, -3.0, 0), (0, 0, -80), (2.0, 7.0), 'grey'), ((-7.0, -7.0, 0), (0, 0, 50), (2.4, 7.0), 'grey'), ((6.0, -6.0, 0), (10.0, -9.0, 0), (1, 1), 'blade')], r=5.0)
