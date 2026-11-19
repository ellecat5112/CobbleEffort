"""Togemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Togemon changed by the X-Antibody: an angry cactus in a straw sombrero with a zigzag band and a yellow fringed
poncho, with big red boxing gloves. 15 blocks.

Front is -z, y is up. Adult stage. Built by _togemon.make.
"""
from __future__ import annotations

from _digi import sized
from _togemon import make

HEIGHT = 32
SCALE, HITBOX = sized(15, HEIGHT, 3.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "an angry walking cactus in a straw sombrero and yellow poncho with red boxing gloves"
build = make("togemonxantibody", True)
