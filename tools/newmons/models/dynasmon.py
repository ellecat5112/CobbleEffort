"""Dynasmon (a Digimon of the CobbleEffort: Digital crossover; hand-built after the official art on wikimon.net): the wyvern Royal Knight, broad in pale lavender-white armour with gold spikes and bosses, a wyvern-skull helm, huge clawed gauntlets with red palm gems, great tattered violet wings and golden cone-spike feet.
35 blocks tall.

Front is -z, y is up. 68 units tall; Ultimate stage.
"""
from _digi import sized
from _dynasmon import make

HEIGHT = 68
SCALE, HITBOX = sized(35, HEIGHT, 3.6)
KIND = "biped"
K = 3
ANIM = {"leg_amp": 10}
LOOK = "a broad lavender-white armoured wyvern knight with gold spikes, huge clawed gauntlets, tattered violet wings and golden cone-spike feet"
build = make("dynasmon")
