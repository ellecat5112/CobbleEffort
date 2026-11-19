"""Tailmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a small white cat standing upright, with big yellow glove-paws striped in red and tipped with black
claws, violet ear tufts, round blue eyes and a long violet-ringed tail. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _tailmon.make(black=False).
"""
from __future__ import annotations

from _digi import sized
from _tailmon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a small white cat with big yellow red-striped glove-paws and black claws, violet ear tufts and a violet-ringed tail"
_C = {"glove": (246, 222, 70), "glove_dark": (190, 150, 30), "stripe": (210, 50, 40), "claw": (40, 36, 44),
      "eye": (70, 150, 230)}
build = make("tailmon", black=False, colours=_C, shiny_colours=_C, slit=False)
