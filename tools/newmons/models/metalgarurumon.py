"""Metal Garurumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Garurumon rebuilt as a war machine: a wolf of blue-grey steel plates with a gold muzzle, a yellow armoured back, swept wing-blades trailing yellow light, a tail blade, red missile pods and huge pink-red claws. 35 blocks long.

Front is -z, y is up. 36 units tall; Ultimate stage. Built by _metalgarurumon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _metalgarurumon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "Garurumon rebuilt as a war machine: a wolf of blue-grey steel plates with a gold muzzle, a yellow armoured back, swept wing-blades trailing yellow light, a tail blade, red missile pods and huge pink-red claws"
build = make("metalgarurumon", look="base")
