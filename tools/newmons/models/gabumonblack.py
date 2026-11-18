"""Gabumon (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Gabumon's dark twin: grey hide under a dark brown pelt striped in cream, a ridged horn, amber eyes and
dark claws. Child stage, 1 block tall.

Front is -z, y is up. 30 units tall. Built by _gabumon.make(look="black").
"""
from __future__ import annotations

from _digi import sized
from _gabumon import make

HEIGHT = 30
SCALE, HITBOX = sized(1.0, HEIGHT, 1.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 14}
LOOK = "a stocky grey reptile under a dark brown cream-striped wolf pelt with a ridged horn and amber eyes"
build = make("gabumonblack", "black")
