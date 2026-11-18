"""Imperialdramon: Fighter Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard
after the official art on wikimon.net): the emperor dragon standing as a warrior: black armour trimmed with gold, a
red chest gem, a white helm with a blue face, gold talons, red wings and the Positron Laser on its right arm. 35
blocks tall.

Front is -z, y is up. Ultimate stage. Built by _imperial.make(mode="fighter", black=False).
"""
from __future__ import annotations

from _digi import sized
from _imperial import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an upright black-armoured dragon warrior with a white helm, a red chest gem, red wings and an arm cannon"
build = make("imperialdramonfightermode", mode="fighter", black=False)
