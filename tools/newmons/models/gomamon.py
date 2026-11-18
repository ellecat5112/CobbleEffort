"""Gomamon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a
cheerful white seal-pup with violet stripes, big green eyes, a spiky orange mohawk, little fangs, flippered forepaws
with black claws and a striped tail fin. Child stage, 1 block long.

Front is -z, y is up. 20 units tall. Built by _gomamon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _gomamon import make

HEIGHT = 20
SCALE, HITBOX = sized(1.0, HEIGHT, 2.0)
KIND = "quadruped"
K = 4
ANIM = {"leg_amp": 6}
LOOK = "a cheerful white seal-pup with violet stripes, green eyes and a spiky orange mohawk"
build = make("gomamon", x=False)
