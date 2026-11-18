"""Metal Mamemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the little cyborg in a sleek blue-grey shell with an orange face plate, a glass dome of crackling energy on its cannon arm, coloured cables and trailing orange fins. 25 blocks tall.

Front is -z, y is up. 20 units tall; Perfect stage. Built by _metalmamemon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _metalmamemon import make

HEIGHT = 20
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the little cyborg in a sleek blue-grey shell with an orange face plate, a glass dome of crackling energy on its cannon arm, coloured cables and trailing orange fins"
build = make("metalmamemonxantibody", x=True)
