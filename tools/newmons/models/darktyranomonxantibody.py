"""Dark Tyranomon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a crouching black tyrannosaur with glowing red stripes, green crystal back spines and glowing green flames at its claws and tail. 15 blocks tall.

Front is -z, y is up. 40 units tall; Adult stage.
"""
from __future__ import annotations

from _darktyranomon import make
from _digi import sized

HEIGHT = 40
SCALE, HITBOX = sized(15, HEIGHT, 2.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a crouching black tyrannosaur with glowing red stripes, green crystal back spines and glowing green flames at its claws and tail"

build = make("darktyranomonxantibody", x=True)
