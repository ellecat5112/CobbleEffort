"""Omega Shoutmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official
art on wikimon.net): a slender black-and-gold dragon-knight with a great V crest of golden horns, a red visor, spiked gold pauldrons, a long golden lance-blade and spirals of fire coiling round it. 25 blocks tall.

Front is -z, y is up. 72 units tall (the horns); Perfect stage. Built by _omegashoutmon.make(x=False).
"""
from __future__ import annotations

from _digi import sized
from _omegashoutmon import make

HEIGHT = 72
SCALE, HITBOX = sized(25, HEIGHT, 4.0)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a slender black-and-gold dragon-knight with a great V crest of golden horns, a red visor, spiked gold pauldrons, a long golden lance-blade and spirals of fire coiling round it"
build = make("omegashoutmon", x=False)
