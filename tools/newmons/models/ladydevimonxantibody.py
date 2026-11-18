"""Lady Devimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Lady Devimon awakened by the X-Antibody: a black leather-clad figure with long white hair, a grinning horned shadow familiar above her head, a mechanical camera-eye arm with golden claws and a tattered grey cape. 25 blocks tall. Built by _ladydevimon.make(x=True), fully clothed as drawn.

Front is -z, y is up. 64 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _ladydevimon import make

HEIGHT = 64
SCALE, HITBOX = sized(25, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a black leather-clad figure with long white hair, a grinning horned shadow familiar above her head, a mechanical camera-eye arm with golden claws and a tattered grey cape"
build = make("ladydevimonxantibody", x=True)
