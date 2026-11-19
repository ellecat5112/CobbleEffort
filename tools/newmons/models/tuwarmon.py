"""Tuwarmon (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art
on wikimon.net): a gold-armoured war machine with a white breastplate bearing a star, a tall pointed gold cone head with
a red crest and a little gold figure perched on its shoulder, two great white rolled-scroll wings, a long gold pickaxe
staff, a gold lance-blade on its right arm, black legs bound with steel rings and curved gold axe blades for feet.
15 blocks (the same design Deadly Tuwarmon grows from).

Front is -z, y is up. Adult stage. Built by _tuwar.make.
"""
from __future__ import annotations

from _digi import sized
from _tuwar import make

HEIGHT = 66
SCALE, HITBOX = sized(15, HEIGHT, 3.2)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 8}
LOOK = "a gold-armoured war machine with a pointed gold cone head, white scroll wings, a gold pickaxe staff and axe-blade feet"
build = make("tuwarmon")
