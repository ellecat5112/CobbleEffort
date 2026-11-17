"""Belphemon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Demon Lord of Sloth awakened by the X-Antibody: gold armour over a black body,
magenta crystal spikes, pink bat wings, chains and ram horns. 35 blocks tall.

Front is -z, y is up. 70 units tall; Ultimate stage. Built by belphemon.make("x").
"""
from __future__ import annotations

from _digi import sized
from belphemon import BASE, SHINY, make

HEIGHT = 70
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ('the Demon Lord of Sloth awakened by the X-Antibody: gold armour over a black body, magenta crystal '
        'spikes, pink bat wings, chains and ram horns')
build = make("belphemonxantibody", "x")
