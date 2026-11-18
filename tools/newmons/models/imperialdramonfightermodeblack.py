"""Imperialdramon: Fighter Mode (Black) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail
standard after the official art on wikimon.net): the black emperor dragon as a warrior: darker armour, a silver helm,
red eyes, tattered crimson wings and the Positron Laser. 35 blocks tall.

Front is -z, y is up. Ultimate stage. Built by _imperial.make(mode="fighter", black=True).
"""
from __future__ import annotations

from _digi import sized
from _imperial import make

HEIGHT = 64
SCALE, HITBOX = sized(35, HEIGHT, 4.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "an upright dark dragon warrior with a silver helm, tattered crimson wings and an arm cannon"
build = make("imperialdramonfightermodeblack", mode="fighter", black=True)
