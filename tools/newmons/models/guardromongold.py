"""Guardromon (Gold) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on
wikimon.net): Guardromon in polished gold: the round riveted hull, slit visor, bolted clamp arms, periscope glove and
piston legs all gleaming gold. Adult stage, 15 blocks tall.

Front is -z, y is up. 40 units tall. Built by _guardromon.make(gold=True).
"""
from __future__ import annotations

from _digi import sized
from _guardromon import make

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a round riveted golden boiler robot with a slit visor, bolted clamp arms and piston legs"
build = make("guardromongold", gold=True)
