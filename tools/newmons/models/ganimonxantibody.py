"""Ganimon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Ganimon awakened by the X-Antibody: a broad dark-blue crab with a spiked shell, a red-eyed shark-toothed
maw, red-striped legs and a huge curved claw. Child stage, 1 block long.

Front is -z, y is up. 22 units tall. Built by _ganimon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _ganimon import make

HEIGHT = 22
SCALE, HITBOX = sized(1.0, HEIGHT, 2.6)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 8}
LOOK = "a broad dark-blue crab with a spiked shell, a red-eyed shark-toothed maw, red-striped legs and a huge claw"
build = make("ganimonxantibody", x=True)
