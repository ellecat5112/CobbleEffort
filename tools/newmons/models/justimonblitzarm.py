"""Justimon: Blitz Arm (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the masked hero with his Blitz Arm: a lean cyborg in a blue-and-white bodysuit with a
silver horned helm, a long red scarf and a thick armoured arm with a short blade. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _justimon.make(arm="blitz", x=False).
"""
from __future__ import annotations

from _digi import sized
from _justimon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a masked blue-and-white cyborg hero with a silver horned helm, a long red scarf and a thick bladed arm"
build = make("justimonblitzarm", arm="blitz", x=False)
