"""Pawn Chessmon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a black chess-pawn soldier with a knight's helm and gold barred visor, a round gold-rimmed shield and a steel spear. 1 block tall.

Front is -z, y is up. 30 units tall; Child stage. Built by _pawnchess.make(white=False).
"""
from __future__ import annotations

from _digi import sized
from _pawnchess import make

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a black chess-pawn soldier with a knight's helm and gold barred visor, a round gold-rimmed shield and a steel spear"
build = make("pawnchessmonblack", white=False)
