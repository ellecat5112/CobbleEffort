"""Ulforce V-dramon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Royal Knight of speed: a slim blue armoured dragon-man with a gold V on its chest and brow, silver-white plating, pink-lined wings and V-bracelet shields, a cyan blade jutting from one. 35 blocks.

Front is -z, y is up. Ultimate stage. Built by _ulforce.make.
"""
from __future__ import annotations

from _digi import sized
from _ulforce import make

HEIGHT = 65
SCALE, HITBOX = sized(35, HEIGHT, 6.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the Royal Knight of speed: a slim blue armoured dragon-man with a gold V on its chest and brow, silver-white plating, pink-lined wings and V-bracelet shields, a cyan blade jutting from one"
build = make("ulforcevdramon", "base")
