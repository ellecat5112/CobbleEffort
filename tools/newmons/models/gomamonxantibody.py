"""Gomamon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gomamon awakened by the X-Antibody: a shaggy red mohawk, a red chest ruff, longer ears, violet stripes and
black claws. Child stage, 1 block long.

Front is -z, y is up. 20 units tall. Built by _gomamon.make(x=True).
"""
from __future__ import annotations

from _digi import sized
from _gomamon import make

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = "a white seal-pup with a shaggy red mohawk and red chest ruff, violet stripes and black claws"
build = make("gomamonxantibody", x=True)
