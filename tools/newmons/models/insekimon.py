"""Insekimon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the
meteorite golem: Icemon's chunked build in pale green meteoric stone, with a big blocky head, round yellow eyes, a wide
grin and chunky stone arms and legs. 25 blocks tall. Built by _rockmon.make.

Front is -z, y is up. 26 units tall; Perfect stage.
"""
from __future__ import annotations

from _digi import sized
from _rockmon import make

HEIGHT = 26
SCALE, HITBOX = sized(25, HEIGHT, 1.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a golem of pale green meteorite chunks with a big blocky head, round yellow eyes, a wide grin and chunky arms"
build = make("insekimon", {"stone": (200, 230, 210), "stone_dark": (120, 160, 140), "stone_light": (240, 252, 244)},
             {"stone": (220, 190, 140), "stone_dark": (150, 110, 70), "stone_light": (250, 236, 200)})
