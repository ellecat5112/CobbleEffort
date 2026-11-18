"""JESmon GX (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): JESmon in its GX form. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _jesmon.make(look="gx").
"""
from __future__ import annotations

from _digi import sized
from _jesmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = " a slender red-and-gold knight with a long lance and wide wings of cyan-and-gold light shards:a slender red-and-gold knight with a long lance and wide wings of cyan-and-gold light shards"
build = make("jesmongx", look="gx")
