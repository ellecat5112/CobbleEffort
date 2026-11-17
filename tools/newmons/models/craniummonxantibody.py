"""Craniummon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): the Royal Knight awakened by the X-Antibody: magenta-and-violet armour bristling with spikes, teal glowing seams, red ribbons and a long lance. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _craniummon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "the Royal Knight awakened by the X-Antibody: magenta-and-violet armour bristling with spikes, teal glowing seams, red ribbons and a long lance"

build = make("craniummonxantibody", x=True)
