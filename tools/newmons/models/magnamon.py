"""Magnamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Royal Knight of miracles: a sturdy blue dragon-man in gleaming golden armour with angular spiked plates, a horned golden helm with a V crest, huge golden greaves and gauntlets and a blue tail. 35 blocks tall. Built by _magnamon.make(x=False).

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _magnamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a sturdy blue dragon-man in gleaming golden armour with angular spiked plates, a horned golden helm with a V crest, huge golden greaves and gauntlets and a blue tail"
build = make("magnamon", x=False)
