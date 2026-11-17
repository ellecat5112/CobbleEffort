"""Black Tailmon Uver. (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Black Tailmon out on the town: a green hooded cap with a cat badge pulled low over
sleepy eyes, a hooded green top, a red backpack, big violet glove-paws and a violet-ringed tail. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _tailmon.make(black=True, uver=True).
"""
from __future__ import annotations

from _digi import sized
from _tailmon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "Black Tailmon in a green hooded cap and top with a red backpack, sleepy eyes and big violet glove-paws"
build = make("blacktailmonuver", black=True, uver=True)
