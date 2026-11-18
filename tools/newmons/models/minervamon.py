"""Minervamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the youngest Olympos warrior: a small fierce girl in a golden owl helm with white wings, long teal braids, a cream tunic over red-and-gold armour, a round golden shield and the great red sword Olympia, longer than she is tall. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built covered (a tunic over armour). Built by
_minervamon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _minervamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the youngest Olympos warrior: a small fierce girl in a golden owl helm with white wings, long teal braids, a cream tunic over red-and-gold armour, a round golden shield and the great red sword Olympia, longer than she is tall"
build = make("minervamon", x=False)
