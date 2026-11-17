"""Black Growmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Growmon's dark twin: a big charcoal-grey dinosaur with red markings, a white belly with the
Hazard emblem, a white mane, bat-wing ears, white elbow blades and claws. 15 blocks tall.

Front is -z, y is up. 44 units tall; Adult stage. Built by _guilmon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 44
SCALE, HITBOX = sized(15, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = ("a big charcoal-grey dinosaur with red markings, a white Hazard belly, a white mane, bat-wing ears, white "
        "elbow blades and claws")
build = make("blackgrowmon", "adult", black=True)
