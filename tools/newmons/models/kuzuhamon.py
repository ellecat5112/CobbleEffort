"""Kuzuhamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the fox priestess warrior, a slender figure in dark violet armour with blue plates, a fox-eared helm
with a black visor, a yin-yang emblem, a long tattered dark cloak and a silver shakujou staff hung with rings. 35
blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _kuzuha.make(miko=False).
"""
from __future__ import annotations

from _digi import sized
from _kuzuha import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender warrior in dark violet armour with a fox-eared helm, a yin-yang emblem, a tattered cloak and a silver ringed staff"
build = make("kuzuhamon", miko=False)
