"""Meramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a leaner, taller man of flame with an olive-gold core, long clawed fingers and toes, a burning clenched fist and a crown of flames over a pale blue face. 15 blocks tall.

Front is -z, y is up. 64 units tall; Adult stage. Built by _meramon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _meramon import make

HEIGHT = 64
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a leaner, taller man of flame with an olive-gold core, long clawed fingers and toes, a burning clenched fist and a crown of flames over a pale blue face"
build = make("meramonxantibody", x=True)
