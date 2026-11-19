"""Whamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a colossal blue whale with a grey-brown armoured ram of a head, a huge gaping toothed
mouth, ragged fins and a broad fluked tail. 15 blocks.

Front is -z, y is up. Adult stage. Built by _whamon.make.
"""
from __future__ import annotations

from _digi import sized
from _whamon import make

HEIGHT = 21
SCALE, HITBOX = sized(15, HEIGHT, 8.0)
KIND = "floater"
K = 3
LOOK = "a colossal blue whale with a grey-brown armoured head, a huge gaping toothed mouth, ragged fins and a fluked tail"
build = make("whamon")
