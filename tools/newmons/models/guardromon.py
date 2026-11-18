"""Guardromon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net):
the walking boiler robot: a round riveted copper hull with a slit visor and one blue-green eye, pipes, big bolted arms
with clamp hands, a periscope arm with a pointing glove and stubby piston legs. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall. Built by _guardromon.make(gold=False).
"""
from __future__ import annotations

from _digi import sized
from _guardromon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a round riveted copper boiler robot with a slit visor, bolted clamp arms and piston legs"
build = make("guardromon", gold=False)
