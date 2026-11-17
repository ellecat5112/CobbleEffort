"""Chaos Greymon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
render on wikimon.net): a War Greymon-type dragon-man in grey-white Chrome Digizoid armour with a yellow breastplate, a
silver mane, long claws and great grey wings. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _wargreymon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = ("a War Greymon-type dragon-man in grey-white armour with a yellow breastplate, a silver mane, long claws and "
        "great grey wings")

build = make("chaosgreymon", "chaos")
