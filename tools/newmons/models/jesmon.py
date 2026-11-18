"""JESmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the newest Royal Knight. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _jesmon.make(look="base").
"""
from __future__ import annotations

from _digi import sized
from _jesmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = " a white-armoured knight with a ribbed breastplate, a horned crested helm, a tattered red cape, a long red sword etched with script and four blazing golden flame-blades fanned behind:a white-armoured knight with a horned helm, a red cape, a long red sword and four blazing flame-blades behind"
build = make("jesmon", look="base")
