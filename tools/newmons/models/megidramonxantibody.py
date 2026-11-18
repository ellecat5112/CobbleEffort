"""Megidramon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the evil dragon in darker crimson armour bristling with black spikes, wings of pure fire, a molten honeycomb-scaled tail and fire in its claws. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by _megidramon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _megidramon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 5.0)
KIND = "floater"
K = 3
LOOK = "the evil dragon in darker crimson armour bristling with black spikes, wings of pure fire, a molten honeycomb-scaled tail and fire in its claws"
build = make("megidramonxantibody", look="x")
