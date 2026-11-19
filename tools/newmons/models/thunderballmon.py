"""Thunderballmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): a navy ball with a golden lightning-bolt crest, big eyes and a wide mouth, floating
white-gloved fists, red boots and a ring of crackling lime lightning. 15 blocks.

Front is -z, y is up. Adult stage. Built by _thunderball.make.
"""
from __future__ import annotations

from _digi import sized
from _thunderball import make

HEIGHT = 30
SCALE, HITBOX = sized(15, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 12}
LOOK = "a navy ball with a golden lightning-bolt crest, big eyes, white-gloved fists and a ring of lime lightning"
build = make("thunderballmon", False)
