"""Skull Mammon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a bigger undead mammoth with a golden spiked chain-arm trunk, great curved silver tusks and a long dark mane.
35 blocks. Built by _skullmammon.make(x=True).

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
LOOK = "a bigger undead mammoth with a golden spiked chain-arm trunk, great curved silver tusks and a long dark mane"
build = make("skullmammonxantibody", x=True)
