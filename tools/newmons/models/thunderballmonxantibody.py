"""Thunderballmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the
official art on wikimon.net): Thunderballmon changed by the X-Antibody: a blue ball with a red X scar across its face, a
mechanical arm holding up a glowing light bulb, a leather glove and tangled red and teal cables. 15 blocks.

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
LOOK = "a blue ball with a red X scar, a lightning crest, a mechanical arm holding a glowing bulb and tangled cables"
build = make("thunderballmonxantibody", True)
