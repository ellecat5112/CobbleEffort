"""Junomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the queen of the Olympos Twelve. 35 blocks tall. Built as officially drawn (clothed).

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _junomon.make(hysteric=False).
"""
from __future__ import annotations

from _digi import sized
from _junomon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = " a goddess in golden armour with a tall crown of golden spikes, a red double halo, a vast violet cape lined with blue scales and two golden staffs:a goddess in golden armour with a crown of spikes, a red double halo, a vast violet scaled cape and two golden staffs"
build = make("junomon", hysteric=False)
