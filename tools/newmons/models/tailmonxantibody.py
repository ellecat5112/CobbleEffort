"""Tailmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Tailmon changed by the X-Antibody: huge golden paws with red paw pads and long black
claws, a heavy gold collar ring, round blue eyes and a long violet-ringed tail. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _tailmon.make(black=False, xab=True).
"""
from __future__ import annotations

from _digi import sized
from _tailmon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 2.2)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a small white cat with huge golden red-padded paws and black claws, a gold collar ring and a violet-ringed tail"
_C = {"glove": (246, 200, 50), "glove_dark": (190, 130, 20), "xpad": (220, 80, 70), "claw": (40, 36, 44),
      "eye": (70, 150, 230), "gold": (240, 196, 60)}
build = make("tailmonxantibody", black=False, colours=_C, shiny_colours=_C, slit=False, xab=True)
