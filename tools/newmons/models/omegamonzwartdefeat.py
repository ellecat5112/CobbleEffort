"""Omegamon Zwart Defeat (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): the black Omegamon broken in defeat: tattered black cape, scorched black plate bristling with broken spikes and a red-lit blade. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage. Built by _omegamon.make(look="zwartdefeat").
"""
from __future__ import annotations

from _digi import sized
from _omegamon import make

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "the black Omegamon broken in defeat: tattered black cape, scorched black plate bristling with broken spikes and a red-lit blade"
build = make("omegamonzwartdefeat", look="zwartdefeat")
