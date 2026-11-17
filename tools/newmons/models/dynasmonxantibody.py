"""Dynasmon (X-Antibody) (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): Dynasmon awakened by the X-Antibody, in dark navy armour edged with teal light and copper, with spikier gauntlets, pink gems and jagged dark wings.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from _digi import sized
from _dynasmon import make

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 3.8)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a dark navy armoured wyvern knight edged with teal light and copper, with spiky gauntlets, pink gems and jagged dark wings"
build = make("dynasmonxantibody", x=True)
