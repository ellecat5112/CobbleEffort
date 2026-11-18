"""Gabumon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gabumon awakened by the X-Antibody: a big round yellow beast under a shaggy lavender striped pelt, a
long golden horn, a blue-and-red emblem on its belly and huge white claws. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall. Built by _gabumon.make(look="x").
"""
from __future__ import annotations

from _digi import sized
from _gabumon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a big round yellow beast under a lavender striped pelt with a long golden horn and huge white claws"
build = make("gabumonxantibody", "x")
