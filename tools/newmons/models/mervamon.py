"""Mervamon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the Olympos war goddess in a white serpent-skull helm over long green braids, a red-and-black armoured tunic, a ragged red cape, her left arm the bone-white serpent Ouroboros and the red zigzag sword Olympia in her right hand. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built covered (an armoured tunic). Built by
_mervamon.make(wide=False).
"""
from __future__ import annotations

from _digi import sized
from _mervamon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the Olympos war goddess in a white serpent-skull helm over long green braids, a red-and-black armoured tunic, a ragged red cape, her left arm the bone-white serpent Ouroboros and the red zigzag sword Olympia in her right hand"
build = make("mervamon", wide=False)
