"""Jupitermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net):  Wrath Mode. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _jupitermon.make(wrath=True).
"""
from __future__ import annotations

from _digi import sized
from _jupitermon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "Jupitermon in its wrath: heavier spiked golden armour, a huge golden sword wreathed in lightning and jagged bolts bursting from its back:a god in heavy spiked golden armour with a huge lightning sword and jagged bolts bursting from its back"
build = make("jupitermonwrathmode", wrath=True)
