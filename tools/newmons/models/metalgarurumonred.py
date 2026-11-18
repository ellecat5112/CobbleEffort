"""Metal Garurumon (Red) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the war-machine wolf in crimson plates, gold trim, wing-blades trailing yellow light and golden claws, after its pixel sprite. 35 blocks long.

Front is -z, y is up. 36 units tall; Ultimate stage. Built by _metalgarurumon.make(look="red").
"""
from __future__ import annotations

from _digi import sized
from _metalgarurumon import make

HEIGHT = 36
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "the war-machine wolf in crimson plates, gold trim, wing-blades trailing yellow light and golden claws, after its pixel sprite"
build = make("metalgarurumonred", look="red")
