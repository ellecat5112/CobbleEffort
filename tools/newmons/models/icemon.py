"""Icemon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): a little
golem of ice blocks: a big blocky head of pale-blue ice chunks with round ears, round yellow eyes and a wide grin, and
chunky ice-block arms and legs. Child stage, 1 block tall. Built by _rockmon.make.

Front is -z, y is up. 26 units tall.
"""
from __future__ import annotations

from _digi import sized
from _rockmon import make

HEIGHT = 26
SCALE, HITBOX = sized(1.0, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "a little golem of pale-blue ice blocks with a big blocky head, round yellow eyes, a wide grin and chunky arms"
build = make("icemon", {"stone": (200, 226, 246), "stone_dark": (130, 160, 200), "stone_light": (245, 252, 255)},
             {"stone": (170, 230, 210), "stone_dark": (90, 170, 150), "stone_light": (230, 255, 245)})
