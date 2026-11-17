"""Belphemon: Rage Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Demon Lord of Sloth awake and raging: a hulking dark muscled demon with ram horns,
violet bat wings, chains and claws blazing with green fire. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by belphemon.make("rage").
"""
from __future__ import annotations

from _digi import sized
from belphemon import BASE, SHINY, make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ('the Demon Lord of Sloth awake and raging: a hulking dark muscled demon with ram horns, violet bat wings, '
        'chains and claws blazing with green fire')
build = make("belphemonragemode", "rage")
