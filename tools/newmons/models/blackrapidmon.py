"""Black Rapidmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Rapidmon's dark twin: grey-and-steel armour, long rocket ears tipped red, cannon arms with red
spikes and a round hip plate. 25 blocks tall.

Front is -z, y is up. 72 units tall; Perfect stage. Built by _galgomon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _galgomon import make

HEIGHT = 72
SCALE, HITBOX = sized(25, HEIGHT, 2.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("Rapidmon's dark twin: grey-and-steel armour, long rocket ears tipped red, cannon arms with red spikes "
        'and a round hip plate')
build = make("blackrapidmon", "perfect", black=True)
