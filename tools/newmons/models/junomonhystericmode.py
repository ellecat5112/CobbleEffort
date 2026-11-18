"""Junomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net):  Hysteric Mode. 35 blocks tall. Built as officially drawn (clothed).

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _junomon.make(hysteric=True).
"""
from __future__ import annotations

from _digi import sized
from _junomon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = "Junomon in a jealous rage: a huge tattered violet mantle spread wide, two great golden peacock-feather blades tipped with spikes, a burst of needles for a crown and swinging golden chains:a raging goddess in a huge tattered violet mantle with two great golden peacock-feather blades and swinging chains"
build = make("junomonhystericmode", hysteric=True)
