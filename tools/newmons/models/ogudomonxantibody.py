"""Ogudomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Ogudomon changed by the X-Antibody into a crystalline horror of crimson-black thorns, its legs splitting into fractal barbs, wreathed in pink light. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage (Demon Lord size). Built by _ogudomon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _ogudomon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "floater"
K = 3
LOOK = "Ogudomon changed by the X-Antibody into a crystalline horror of crimson-black thorns, its legs splitting into fractal barbs, wreathed in pink light"
build = make("ogudomonxantibody", x=True)
