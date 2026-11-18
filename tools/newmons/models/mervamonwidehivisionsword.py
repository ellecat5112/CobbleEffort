"""Mervamon Wide Hi-Vision Sword (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Mervamon with Olympia grown into a towering broad red blade as tall as she is, held upright beside her, the serpent Ouroboros on her left arm. 35 blocks tall.

Front is -z, y is up. 72 units tall (the sword); Ultimate stage. Built covered (an armoured tunic). Built by
_mervamon.make(wide=True).
"""
from __future__ import annotations

from _digi import sized
from _mervamon import make

HEIGHT = 72
SCALE, HITBOX = sized(35, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "Mervamon with Olympia grown into a towering broad red blade as tall as she is, held upright beside her, the serpent Ouroboros on her left arm"
build = make("mervamonwidehivisionsword", wide=True)
