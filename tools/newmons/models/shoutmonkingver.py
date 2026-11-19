"""Shoutmon (King Ver.) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
Shoutmon as king: wreathed in a ring of golden flame with a fireball blazing in its fist. 1 block. Built by _shoutmon.small.

Front is -z, y is up. 30 units tall; Child stage.
"""
from __future__ import annotations

from _digi import sized
from _shoutmon import mech, small  # noqa: F401

HEIGHT = 30
SCALE, HITBOX = sized(1, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "Shoutmon as king: wreathed in a ring of golden flame with a fireball blazing in its fist"
build = small('shoutmonkingver', 'king')
