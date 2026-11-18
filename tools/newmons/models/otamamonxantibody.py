"""Otamamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Otamamon changed by the X-Antibody: a much fatter round violet body with a tiny gold crown, gold armbands and a thin finned tail below. 1 block tall.

Front is -z, y is up. 24 units tall; Child stage. Built by _otamamon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _otamamon import make

HEIGHT = 24
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "floater"
K = 3
LOOK = "Otamamon changed by the X-Antibody: a much fatter round violet body with a tiny gold crown, gold armbands and a thin finned tail below"
build = make("otamamonxantibody", look="x")
