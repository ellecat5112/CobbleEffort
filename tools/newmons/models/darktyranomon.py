"""Dark Tyranomon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a dark grey tyrannosaur striped in red with a pale ribbed belly, green leaf-like dorsal spikes, steel claws and a leather belt. 15 blocks tall.

Front is -z, y is up. 46 units tall; Adult stage.
"""
from __future__ import annotations

from _darktyranomon import make
from _digi import sized

HEIGHT = 46
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a dark grey tyrannosaur striped in red with a pale ribbed belly, green leaf-like dorsal spikes, steel claws and a leather belt"

build = make("darktyranomon", x=False)
