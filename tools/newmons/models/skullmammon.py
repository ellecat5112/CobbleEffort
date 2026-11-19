"""Skull Mammon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): an undead mammoth skeleton of silver bones with a red-glowing core, violet crystal spikes on its skull and a golden mechanical trunk.
35 blocks. Built by _skullmammon.make(x=False).

Front is -z, y is up. 50 units tall; Ultimate stage.
"""
from __future__ import annotations

from _digi import sized
from _skullmammon import make

HEIGHT = 50
SCALE, HITBOX = sized(35, HEIGHT, 8.0)
KIND = "quadruped"
K = 3
ANIM = {"leg_amp": 5}
LOOK = "an undead mammoth skeleton of silver bones with a red-glowing core, violet crystal spikes on its skull and a golden mechanical trunk"
build = make("skullmammon", x=False)
