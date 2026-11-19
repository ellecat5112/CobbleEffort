"""Toy Agumon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Agumon built from brightly coloured toy bricks: studded blocks stacked into a
little dinosaur with a round green eye, grey brick hands with studded fingers and a puff of flame. 1 block.

Front is -z, y is up. Child stage. Built by _toyagumon.make.
"""
from __future__ import annotations

from _digi import sized
from _toyagumon import make

HEIGHT = 23
SCALE, HITBOX = sized(1.0, HEIGHT, 1.4)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 10}
LOOK = "Agumon built from brightly coloured toy bricks, with a round green eye, studded brick hands and a puff of flame"
build = make("toyagumon", False)
