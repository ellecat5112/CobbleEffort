"""Cardmon S1 (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a round yellow-and-white floating head ringed by four hollow golden card frames with pink rings. Ultimate stage.

Front is -z, y is up. 25 units tall (head and cards).
"""
from __future__ import annotations

from _cardmon import make
from _digi import sized

HEIGHT = 25
SCALE, HITBOX = sized(35.0, HEIGHT, 0.94)
KIND = "floater"
K = 4
LOOK = "a round yellow-and-white floating head ringed by four hollow golden card frames with pink rings"

build = make("cardmons1", "yellow", [((-9.0, 6.0, 0), (0, 0, 40), (5.0, 7.0), 'frame'), ((9.0, 8.0, 0), (0, 0, -30), (6.0, 8.0), 'frame'), ((-8.0, -8.0, 0), (0, 0, -40), (5.0, 7.0), 'frame'), ((9.0, -8.0, 0), (0, 0, 40), (6.0, 8.0), 'frame')], r=5.0)
