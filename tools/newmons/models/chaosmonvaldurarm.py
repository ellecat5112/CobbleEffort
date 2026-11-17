"""Chaosmon: Valdur Arm (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): Chaosmon's golden god form: a halo of rainbow light, great pale feathered wings and a blazing lion gauntlet. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage.
"""
from __future__ import annotations

from _chaosmon import make
from _digi import sized

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Chaosmon's golden god form: a halo of rainbow light, great pale feathered wings and a blazing lion gauntlet"

build = make("chaosmonvaldurarm", valdur=True)
