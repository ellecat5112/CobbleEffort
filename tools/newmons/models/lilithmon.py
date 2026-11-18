"""Lilithmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the Demon Lord of Lust drawn as a dark sorceress-queen: a tall figure in a long gold-trimmed purple kimono-robe, long black hair with golden hairpins, a golden clawed gauntlet and black bat wings with golden spear-ribs. 35 blocks tall. Built by _lilithmon.make(x=False), fully robed as drawn.

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
LOOK = "a tall figure in a long gold-trimmed purple kimono-robe, long black hair with golden hairpins, a golden clawed gauntlet and black bat wings with golden spear-ribs"
build = make("lilithmon", x=False)
