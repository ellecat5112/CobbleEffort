"""Belphemon: Sleep Mode (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): the Demon Lord of Sloth asleep: a huge ball of dark shaggy fur with ram horns, closed
eyes, fang-plates, little violet wings, chains and a gold alarm clock. 35 blocks tall.

Front is -z, y is up. 62 units tall; Ultimate stage. Built by belphemon.make("sleep").
"""
from __future__ import annotations

from _digi import sized
from belphemon import BASE, SHINY, make

HEIGHT = 62
SCALE, HITBOX = sized(35, HEIGHT, 3.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = ('the Demon Lord of Sloth asleep: a huge ball of dark shaggy fur with ram horns, closed eyes, fang-plates, '
        'little violet wings, chains and a gold alarm clock')
build = make("belphemonsleepmode", "sleep")
