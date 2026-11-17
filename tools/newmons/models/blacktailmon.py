"""Black Tailmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): Tailmon's dark twin: a small charcoal cat standing upright, with big violet padded glove-paws and
pink claws, violet ear tufts, slit yellow eyes and a long violet-ringed tail. 15 blocks tall.

Front is -z, y is up. 30 units tall; Adult stage. Built by _tailmon.make(black=True).
"""
from __future__ import annotations

from _digi import sized
from _tailmon import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 1.6)
KIND = "biped"
K = 4
ANIM = {"leg_amp": 16}
LOOK = "a small charcoal cat with big violet glove-paws and pink claws, violet ear tufts and a violet-ringed tail"
build = make("blacktailmon", black=True)
