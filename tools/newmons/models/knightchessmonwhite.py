"""Knight Chessmon (White) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
chess knight in white lacquer: a horse-headed puppet with a flowing orange mane, gold rings at its joints, coiled spring
hocks, wheel hooves and a huge striped drill-lance on its back. 15 blocks tall. Built by _knightchess.make(white=True).

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

from _digi import sized
from _knightchess import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "quadruped"
K = 3
LOOK = "a white horse-headed chess knight puppet with an orange mane, gold rings, spring hocks, wheel hooves and a drill-lance on its back"
build = make("knightchessmonwhite", white=True)
