"""Neo Vamdemon Darkness Mode (Vampire Army) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Neo Vamdemon empowered by its vampire army: violet-black blade-spined armour, great tattered black bat wings and red-lit joints. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _neovamdemon.make(mode="army").
"""
from __future__ import annotations

from _digi import sized
from _neovamdemon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Neo Vamdemon empowered by its vampire army: violet-black blade-spined armour, great tattered black bat wings and red-lit joints"
build = make("neovamdemondarknessmodevampirearmy", mode="army")
