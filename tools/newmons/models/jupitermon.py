"""Jupitermon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): the king of the Olympos Twelve. 35 blocks tall.

Front is -z, y is up. 64 units tall; Ultimate stage. Built by _jupitermon.make(wrath=False).
"""
from __future__ import annotations

from _digi import sized
from _jupitermon import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 6}
LOOK = " a god in ornate golden armour with a crested helm, a red halo, one white feathered wing, two golden thunder hammers and a crackling ring of lightning:a god in ornate golden armour with a crested helm, a red halo, a white wing, two golden hammers and a ring of lightning"
build = make("jupitermon", wrath=False)
