"""Metal Garurumon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the war-machine wolf in gunmetal black plates with a gold muzzle, wing-blades trailing yellow light, red missile pods and white claws. 35 blocks long.

Front is -z, y is up. 36 units tall; Ultimate stage. Built by _metalgarurumon.make(look="black").
"""
from __future__ import annotations

from _digi import sized
from _metalgarurumon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "the war-machine wolf in gunmetal black plates with a gold muzzle, wing-blades trailing yellow light, red missile pods and white claws"
build = make("metalgarurumonblack", look="black")
