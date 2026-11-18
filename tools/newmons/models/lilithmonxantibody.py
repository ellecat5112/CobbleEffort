"""Lilithmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): Lilithmon awakened by the X-Antibody: a sorceress-queen in crimson-and-violet robes with a horned crown, long black hair, a golden claw and great tattered wings traced with glowing green rings. 35 blocks tall. Built by _lilithmon.make(x=True), fully robed as drawn.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _lilithmon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 4}
LOOK = "a sorceress-queen in crimson-and-violet robes with a horned crown, long black hair, a golden claw and great tattered wings traced with glowing green rings"
build = make("lilithmonxantibody", x=True)
