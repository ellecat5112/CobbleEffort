"""Dark Knightmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built at the detail standard after the official art on
wikimon.net): a lurid violet-and-gold knight with neon seams, a skull face, a crimson cape, a glowing green spear and a huge white scythe-blade. 35 blocks tall.

Front is -z, y is up. 66 units tall; Ultimate stage.
"""
from __future__ import annotations

from _darkknightmon import make
from _digi import sized

HEIGHT = 66
SCALE, HITBOX = sized(35, HEIGHT, 2.4)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a lurid violet-and-gold knight with neon seams, a skull face, a crimson cape, a glowing green spear and a huge white scythe-blade"

build = make("darkknightmonxantibody", x=True)
