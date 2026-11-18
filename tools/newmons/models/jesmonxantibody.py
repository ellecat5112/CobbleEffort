"""JESmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): JESmon awakened by the X-Antibody. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _jesmon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _jesmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = " red-and-gold spiked armour, thorny limbs, a great red blade and wings of jagged gold crystal shards:a red-and-gold spiked knight with thorny limbs, a great red blade and wings of gold crystal shards"
build = make("jesmonxantibody", look="x")
