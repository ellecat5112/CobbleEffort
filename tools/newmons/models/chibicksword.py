"""Chibick Sword (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
manga art on wikimon.net): the long serrated bone-white blade Chibickmon turns into, studded with knobs along its spine,
with a guard and a grip. Child stage (a weapon Digimon).

Front is -z, y is up. 44 units tall.
"""
from __future__ import annotations

from chibickmon import make
from _digi import sized

HEIGHT = 44
SCALE, HITBOX = sized(1.0, HEIGHT, 0.4)
KIND = "floater"
K = 3
LOOK = "a long serrated bone-white blade studded with knobs along its spine, with a guard and a grip"

build = make("chibicksword", sword=True)
