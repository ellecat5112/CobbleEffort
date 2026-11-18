"""Omegamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Royal Knight born of War Greymon and Metal Garurumon: a towering knight in white plate trimmed blue and gold, a horned helm with a red visor, a cape white without and red within, the golden War Greymon head and Grey Sword on its left arm and the blue Metal Garurumon head and Garuru Cannon on its right. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _omegamon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _omegamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the Royal Knight born of War Greymon and Metal Garurumon: a towering knight in white plate trimmed blue and gold, a horned helm with a red visor, a cape white without and red within, the golden War Greymon head and Grey Sword on its left arm and the blue Metal Garurumon head and Garuru Cannon on its right"
build = make("omegamon", look="base")
