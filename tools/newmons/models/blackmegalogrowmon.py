"""Black Megalo Growmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Megalo Growmon's dark twin: a charcoal-grey cyborg dinosaur with red markings, steel
chest armour with twin glowing cannons, a steel helm, a white mane, elbow blades and mechanical wing struts.
25 blocks tall.

Front is -z, y is up. 52 units tall; Perfect stage. Built by _guilmon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _guilmon import make

HEIGHT = 52
SCALE, HITBOX = sized(25, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a charcoal-grey cyborg dinosaur with red markings, steel chest armour with twin cannons, a steel helm, a "
        "white mane and mechanical wing struts")
build = make("blackmegalogrowmon", "perfect", black=True)
