"""Shine Greymon: Ruin Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a black-armoured dragon-man streaked red with glowing red eyes, vast smoky feathered wings and a dark vortex in its claw.
35 blocks. Built by _shinegreymon.make(look="ruin").

Front is -z, y is up. 70 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _shinegreymon import make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a black-armoured dragon-man streaked red with glowing red eyes, vast smoky feathered wings and a dark vortex in its claw"
build = make("shinegreymonruinmode", look="ruin")
